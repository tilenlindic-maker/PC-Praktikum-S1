"""MkDocs hook converting Obsidian links to GitHub Pages links.

Does not modify source files. Supports wiki links, aliases, embedded images,
ordinary Markdown links (including unescaped spaces), and attachments.
"""
from pathlib import Path
from urllib.parse import quote, unquote
import posixpath
import re

ROOT = None
FILES = []
IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}


def on_pre_build(config):
    global ROOT, FILES
    ROOT = Path(config['docs_dir']).resolve()
    FILES = sorted(p.relative_to(ROOT) for p in ROOT.rglob('*') if p.is_file())


def on_page_markdown(markdown, page, config, files):
    current = Path(page.file.src_path)

    def resolve(target):
        """Find a file by Obsidian basename, relative path, or legacy vault path."""
        target = unquote(target).replace('\\ ', ' ').strip().replace('\\', '/')
        if not target:
            return None
        raw = target.lstrip('./')
        if raw.startswith('S1_files/'):
            raw = raw[len('S1_files/'):]
        # Obsidian aliases handled before calling resolve().
        name = Path(raw).name.casefold()
        suffix = Path(raw).suffix.lower()
        possibilities = [raw]
        if not suffix:
            possibilities.append(raw + '.md')

        # Try exact paths first, then relative to current Markdown file.
        for value in possibilities:
            for candidate in (Path(value), current.parent / value):
                if candidate in FILES:
                    return candidate
        # Obsidian convention: link target can refer to any vault file by name.
        names = {Path(v).name.casefold() for v in possibilities}
        matches = [p for p in FILES if p.name.casefold() in names]
        if not matches:
            return None
        # Prefer same folder; then shortest path; warn on ambiguity.
        matches.sort(key=lambda p: (p.parent != current.parent, len(p.parts), str(p)))
        if len(matches) > 1:
            print(f'WARNING: Ambiguous link in {current}: {target} -> {matches}')
        return matches[0]

    def published_path(path):
        if path.suffix.lower() == '.md':
            if path.name == 'index.md':
                return path.parent.as_posix().strip('/') + '/' if path.parent.parts else ''
            return path.with_suffix('').as_posix().strip('/') + '/'
        return path.as_posix()

    # MkDocs use_directory_urls=True (its default):
    # /Guide/index.html sits at /Guide/, not at /Guide.md.
    current_dir = published_path(current)
    if not current_dir.endswith('/'):
        current_dir += '/'

    def make_url(target, label=None):
        target = target.strip()
        if target.startswith(('http://', 'https://', 'mailto:', 'tel:', '//')):
            return target
        if target.startswith('#'):
            return target
        if target.startswith('/'):
            return target  # keep intentional site-absolute links
        file_part, hashmark, fragment = target.partition('#')
        dest = resolve(file_part)
        if dest is None:
            print(f'WARNING: Missing target in {current}: {target}')
            return None
        path = published_path(dest)
        # Compute a URL relative to the *published* page, not source .md.
        relative = posixpath.relpath(path.rstrip('/'), current_dir.rstrip('/'))
        relative = quote(relative, safe='/-_.~')
        if dest.suffix.lower() == '.md':
            relative += '/'
        if hashmark:
            slug = re.sub(r'[^\w\- ]', '', fragment.casefold()).strip().replace(' ', '-')
            relative += '#' + quote(slug, safe='-_.~')
        return relative

    def convert(fragment):
        # Wiki syntax: [[Page]], [[Page|label]], ![[image.png]], [[Page#Heading]].
        def wiki(m):
            embedded, spec = m.groups()
            target, sep, alias = spec.partition('|')
            url = make_url(target)
            if url is None:
                return m.group(0)
            name = (alias if sep else Path(target.split('#')[0]).stem) or target
            if embedded and Path(target.split('#')[0]).suffix.lower() in IMAGE_EXT:
                return f'![{name}]({url})'
            return f'[{name}]({url})'

        fragment = re.sub(r'(!?)\[\[([^\]\n]+)\]\]', wiki, fragment)

        # Markdown links, including Obsidian's nonstandard [name](File With Spaces).
        # Skip links starting ! only for the name of the replacement, not resolution.
        def markdown_link(m):
            mark, label, raw_target = m.groups()
            target = raw_target.strip()
            # Do not touch already valid absolute URLs.
            if target.startswith(('http:', 'https:', 'mailto:', 'tel:', '//', '#', '/', '../', './')):
                return m.group(0)
            target = target.removeprefix('<').removesuffix('>')
            target = target.replace('\\ ', ' ')
            # Handles [AvogadroGuide|Some label](AvogadroGuide|Some label).
            if '|' in target:
                target, alias = target.split('|', 1)
                label = alias
            elif '|' in label:
                label = label.split('|', 1)[1]
            url = make_url(target)
            if url is None:
                return m.group(0)
            return f'{mark}[{label}]({url})'
        fragment = re.sub(
            r'(!?)\[([^\]\n]+)\]\(([^)\n]+)\)',
            markdown_link,
            fragment,
        )
        return fragment

    return convert(markdown)
