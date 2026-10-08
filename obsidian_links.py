"""Publish an Obsidian vault with MkDocs, without altering the source Markdown.

Configure mkdocs.yml with:
    site_url: https://USER.github.io/REPO/
    docs_dir: S1_files
    hooks:
      - obsidian_links.py

Converts Obsidian wikilinks, aliases, image embeds and nonstandard Markdown
links to *absolute published URLs*. After building, checks all local HTML links
and assets, reporting broken targets in the GitHub Actions build log.
"""

from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import quote, unquote, urljoin, urlsplit

DOCS = None
ALL_FILES = []
BY_NAME = defaultdict(list)
SITE = None
UNRESOLVED = set()
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}
WIKI = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
MD_OPEN = re.compile(r"(?<!\[)(!?)\[([^\[\]\n]*)\]\(")
FENCE = re.compile(r"(?ms)^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?^\1\2[ \t]*(?:\n|$)")


def on_pre_build(config):
    global DOCS, ALL_FILES, BY_NAME, SITE, UNRESOLVED
    DOCS = Path(config["docs_dir"]).resolve()
    SITE = (config.get("site_url") or "").strip()
    if not SITE.startswith(("https://", "http://")):
        raise ValueError("Set site_url in mkdocs.yml to your full GitHub Pages URL")
    SITE = SITE.rstrip("/") + "/"
    ALL_FILES = sorted(p.relative_to(DOCS) for p in DOCS.rglob("*") if p.is_file())
    BY_NAME = defaultdict(list)
    for p in ALL_FILES:
        BY_NAME[p.name.casefold()].append(p)
    UNRESOLVED = set()


def find_file(target, current):
    """Resolve source filenames, vault paths, and Obsidian basename links."""
    text = unquote(target).replace(r"\ ", " ").strip().replace("\\", "/")
    text = text.replace("%20", " ").strip("<>")
    if not text:
        return None

    # Strip the old repository or vault prefix, if supplied.
    if "S1_files/" in text:
        text = text.split("S1_files/", 1)[1]
    text = text.rstrip("/")
    basename = PurePosixPath(text).name

    choices = [text]
    if not PurePosixPath(text).suffix:
        choices.append(text + ".md")
        # A published URL /Page/ can also refer to Page.md.
        choices.append(text + "/index.md")

    # First match exact paths relative to the vault root or current document.
    known = {p.as_posix().casefold(): p for p in ALL_FILES}
    for candidate in choices:
        for raw in (candidate, posixpath.normpath(posixpath.join(current.parent.as_posix(), candidate))):
            match = known.get(raw.lstrip("./").casefold())
            if match:
                return match

    # Obsidian files can be referenced by basename from anywhere in the vault.
    wanted = [basename]
    if not PurePosixPath(basename).suffix:
        wanted.append(basename + ".md")
    candidates = []
    for name in wanted:
        candidates.extend(BY_NAME.get(name.casefold(), []))
    candidates = sorted(set(candidates), key=lambda p: (p.parent != current.parent, len(p.parts), str(p)))
    if len(candidates) > 1:
        print(f"WARNING: Ambiguous file reference in {current}: {target} -> {candidates}")
    return candidates[0] if candidates else None


def published_url(file, config):
    """Return absolute URL at which MkDocs will publish this file."""
    if file.suffix.lower() == ".md":
        if config.get("use_directory_urls", True):
            dest = file.parent if file.name == "index.md" else file.with_suffix("")
            path = "" if str(dest) == "." else dest.as_posix().rstrip("/") + "/"
        else:
            dest = file.parent / "index.html" if file.name == "index.md" else file.with_suffix(".html")
            path = dest.as_posix()
    else:
        path = file.as_posix()
    return urljoin(SITE, quote(path, safe="/-_.~/"))


def slug_heading(fragment):
    # Close to the default Python-Markdown heading IDs.
    slug = re.sub(r"[^\w\- ]", "", unquote(fragment).casefold()).strip().replace(" ", "-")
    return quote(slug, safe="-_.~")


def convert_target(raw, current, config):
    target = raw.strip().replace(r"\ ", " ")
    if not target:
        return None
    if target.startswith(("https://", "http://", "mailto:", "tel:", "data:", "//")):
        return target
    if target.startswith("#"):
        return "#" + slug_heading(target[1:])
    # Do not rewrite unrelated absolute paths.
    if target.startswith("/") and not target.startswith("/S1_files/"):
        return target
    file_part, mark, anchor = target.partition("#")
    resolved = find_file(file_part, current)
    if resolved is None:
        UNRESOLVED.add((current.as_posix(), raw))
        return None
    result = published_url(resolved, config)
    if mark:
        result += "#" + slug_heading(anchor)
    return result


def convert_text(text, current, config):
    def wiki(match):
        bang, content = match.groups()
        target, has_alias, alias = content.partition("|")
        label = alias if has_alias else PurePosixPath(target.split("#")[0]).stem or target
        url = convert_target(target, current, config)
        if url is None:
            return match.group(0)
        is_image = bang and PurePosixPath(target.split("#")[0]).suffix.lower() in IMAGE_TYPES
        if is_image:
            # Obsidian image sizing, e.g. ![[figure.png|400]].
            if has_alias and alias.strip().isdigit():
                return f'<img src="{url}" width="{int(alias)}" alt="{PurePosixPath(target).name}">'
            return f"![{label}]({url})"
        return f"[{label}]({url})"

    text = WIKI.sub(wiki, text)

    # Scan existing [label](target) and ![label](target). Handle parentheses in
    # filenames, e.g. S15_MolekulareReaktionsdynamik_Skript(1) 1.pdf.
    pieces = []
    last = 0
    for found in MD_OPEN.finditer(text):
        start = found.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            ch = text[i]
            if ch == "\\" and i + 1 < len(text):
                i += 2
                continue
            if ch == "\n":
                break
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            i += 1
        if depth or found.start() < last:
            continue
        bang, label = found.group(1), found.group(2)
        raw_target = text[start:i - 1].strip()
        if raw_target.startswith("<") and raw_target.endswith(">"):
            raw_target = raw_target[1:-1]
        # Preserve optional Markdown tooltip strings.
        tooltip = ""
        title_match = re.match(r'^(.*?)\s+("[^"]*"|\x27[^\x27]*\x27)$', raw_target)
        if title_match:
            raw_target, tooltip = title_match.groups()
        if "|" in raw_target:
            raw_target, alias = raw_target.split("|", 1)
            label = alias
        elif "|" in label:
            label = label.split("|", 1)[1]
        url = convert_target(raw_target, current, config)
        if url is None:
            continue
        pieces.append(text[last:found.start()])
        pieces.append(f'{bang}[{label}]({url}{" " + tooltip if tooltip else ""})')
        last = i
    pieces.append(text[last:])
    return "".join(pieces)


def on_page_markdown(markdown, page, config, files):
    current = PurePosixPath(page.file.src_path)
    current = Path(str(current))
    # Leave fenced code examples untouched.
    parts, end = [], 0
    for match in FENCE.finditer(markdown):
        parts.append(convert_text(markdown[end:match.start()], current, config))
        parts.append(match.group(0))
        end = match.end()
    parts.append(convert_text(markdown[end:], current, config))
    return "".join(parts)


class _Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        val = attrs.get("href") if tag in {"a", "link"} else attrs.get("src")
        if val:
            self.links.append(val)


def on_post_build(config):
    """Audit published HTML, not merely MkDocs' warning messages."""
    site_dir = Path(config["site_dir"]).resolve()
    prefix = urlsplit(SITE).path
    host = urlsplit(SITE).netloc
    broken = set()
    checked = 0
    for html in site_dir.rglob("*.html"):
        parser = _Links()
        parser.feed(html.read_text(encoding="utf-8"))
        local = html.relative_to(site_dir).as_posix()
        page_url = urljoin(SITE, local.replace("index.html", ""))
        for href in parser.links:
            url = urlsplit(urljoin(page_url, href))
            if url.scheme not in ("http", "https") or url.netloc != host or not url.path.startswith(prefix):
                continue
            local_path = unquote(url.path[len(prefix):]).lstrip("/")
            if not local_path:
                local_path = "index.html"
            elif local_path.endswith("/"):
                local_path += "index.html"
            checked += 1
            if not (site_dir / local_path).is_file():
                broken.add((local, href))
    print(f"LINK AUDIT: checked {checked} same-site links; {len(broken)} broken links.")
    for source, target in sorted(broken)[:80]:
        print(f"BROKEN LINK: {source} -> {target}")
    if len(broken) > 80:
        print(f"...and {len(broken) - 80} more broken links")
    print(f"OBSIDIAN AUDIT: {len(UNRESOLVED)} unresolved source references.")
    for source, target in sorted(UNRESOLVED)[:80]:
        print(f"MISSING SOURCE: {source} -> {target}")

