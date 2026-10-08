"""MkDocs hook: translate common Obsidian links without editing the vault."""
from pathlib import Path
from urllib.parse import quote, unquote
import os
import re

PAGES = {}
ASSETS = {}


def on_pre_build(config):
    global PAGES, ASSETS
    root = Path(config['docs_dir'])
    PAGES = {}
    ASSETS = {}
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        mapping = PAGES if path.suffix.lower() == '.md' else ASSETS
        mapping.setdefault(path.stem.casefold(), []).append(path)
        mapping.setdefault(path.name.casefold(), []).append(path)


def on_page_markdown(markdown, page, config, files):
    root = Path(config['docs_dir'])
    current = root / page.file.src_path

    def url_for(target, image=False):
        target = unquote(target.strip())
        if not target or target.startswith(('/', '#')) or '://' in target or target.startswith('mailto:'):
            return None
        # Obsidian uses # for section headings and | for aliases.
        path_part, sep, fragment = target.partition('#')
        if not path_part:
            return '#' + quote(fragment, safe='-_.~')
        key = Path(path_part).name.casefold()
        lookup = ASSETS if image else PAGES
        candidates = lookup.get(key, [])
        if not candidates and not image:
            candidates = PAGES.get((Path(path_part).stem + '.md').casefold(), [])
        if not candidates:
            return None
        # Prefer a file located beside the current page if names are duplicated.
        dest = next((p for p in candidates if p.parent == current.parent), candidates[0])
        relative = Path(os.path.relpath(dest, current.parent)).as_posix()
        result = quote(relative, safe='/-_.~')
        if sep:
            # Common Obsidian heading anchors, roughly matching MkDocs slug generation.
            anchor = re.sub(r'[^\w -]', '', fragment.lower()).strip().replace(' ', '-')
            result += '#' + quote(anchor, safe='-_.~')
        return result

    def replace_wikilink(match):
        embedded = bool(match.group(1))
        raw = match.group(2)
        target, _, label = raw.partition('|')
        suffix = Path(target.split('#', 1)[0]).suffix.lower()
        is_image = embedded and suffix in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
        dest = url_for(target, image=is_image)
        if not dest:
            print(f'WARNING: Unresolved Obsidian reference in {page.file.src_path}: {raw}')
            return match.group(0)
        title = label or Path(target.split('#', 1)[0]).stem or target
        if is_image:
            return f'![{title}]({dest})'
        return f'[{title}]({dest})'

    # Handle ![[image.png]], [[page]], [[page#heading|caption]], etc.
    markdown = re.sub(r'(!?)\[\[([^\]\n]+)\]\]', replace_wikilink, markdown)

    # Also convert old-style bare Markdown links: [Page](Page Name)
    # Already working URLs, anchors, and explicit .md links are left alone.
def replace_markdown_link(match):
    prefix, title, target = match.groups()

    # Leave external URLs and anchors unchanged.
    if target.startswith(
        ('http:', 'https:', 'mailto:', '#', '/', '../', './')
    ):
        return match.group(0)

    # Remove Markdown escape characters before spaces.
    target = target.replace('\\ ', ' ')
    title = title.replace('\\ ', ' ')

    # Handle Obsidian aliases.
    if '|' in target:
        target, alias = target.split('|', 1)
        title = alias

    # Find the target among Markdown pages or attachments.
    suffix = Path(target.split('#', 1)[0]).suffix.lower()

    markdown = re.sub(r'(?<!\!)((?:!)?)\[([^\]\n]+)\]\(([^)\n]+)\)', replace_markdown_link, markdown)
    return markdown
