"""Check the generated offline guide. Run with Python 3."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CSS_REFERENCE = re.compile(r"""url\(\s*['"]?([^)'"]+)['"]?\s*\)|@import\s+['"]([^'"]+)['"]""", re.I)
RUNTIME_NETWORK = re.compile(r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\s*\(")


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = Counter()
        self.refs = []
        self.labels = []
        self.inline_css = []
        self.inline_script = []
        self.collect = None
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "a" and attrs.get("name") and attrs["name"] != attrs.get("id"):
            self.ids[attrs["name"]] += 1
        if tag == "label" and attrs.get("for"):
            self.labels.append(attrs["for"])
        if tag == "base":
            self.refs.append(("base", "base elements change relative links"))
        for name in ("href", "src", "poster", "srcset", "data", "action", "formaction", "xlink:href"):
            value = attrs.get(name)
            if not value:
                continue
            if name == "srcset":
                for item in value.split(","):
                    if item.strip():
                        self.refs.append(("asset", item.strip().split()[0]))
            elif name in {"href", "xlink:href"}:
                self.refs.append(("link" if tag == "a" else "asset", value))
            elif name != "data" or tag == "object":
                self.refs.append(("asset", value))
        if attrs.get("style"):
            self.inline_css.append(attrs["style"])
        if tag == "style":
            self.collect = self.inline_css
        elif tag == "script" and "src" not in attrs:
            self.collect = self.inline_script
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refs.append(("base", "refresh elements can change the offline page"))

    def handle_endtag(self, tag):
        if tag in {"style", "script"}:
            self.collect = None

    def handle_data(self, data):
        if self.collect is not None:
            self.collect.append(data)


def main():
    errors = []
    pages = {path: Page(path) for path in sorted(ROOT.glob("*.html"))}
    if ROOT / "index.html" not in pages:
        errors.append("index.html: missing generated entry page")
    checked = Counter()

    def flag(source, message):
        errors.append(f"{source.relative_to(ROOT)}: {message}")

    def check_ref(source, kind, value):
        checked[kind] += 1
        if kind == "base":
            flag(source, value)
            return
        try:
            parts = urlsplit(value.strip())
        except ValueError:
            flag(source, f"invalid reference {value!r}")
            return
        if parts.scheme or parts.netloc:
            if kind == "asset" and parts.scheme != "data":
                flag(source, f"remote or absolute asset {value!r}")
            elif kind == "link" and parts.scheme not in {"http", "https", "mailto", "tel", ""}:
                flag(source, f"unsafe or absolute link {value!r}")
            return
        if parts.path.startswith("/"):
            flag(source, f"root-relative reference {value!r}")
            return
        target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
        if not target.is_relative_to(ROOT):
            flag(source, f"reference escapes guide root {value!r}")
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            flag(source, f"missing target {value!r}")
        elif parts.fragment and target.suffix == ".html":
            page = pages.get(target) or Page(target)
            if unquote(parts.fragment) not in page.ids:
                flag(source, f"missing anchor {value!r}")

    def check_css(source, css):
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for url, imported in CSS_REFERENCE.findall(css):
            check_ref(source, "asset", url.strip() or imported.strip())

    def check_script(source, script):
        if RUNTIME_NETWORK.search(script):
            flag(source, "script uses a network API")

    for path, page in pages.items():
        for name, count in page.ids.items():
            if count > 1:
                flag(path, f"duplicate id or named anchor {name!r} ({count})")
        for name in page.labels:
            if name not in page.ids:
                flag(path, f"label refers to missing id {name!r}")
        for kind, value in page.refs:
            check_ref(path, kind, value)
        check_css(path, "\n".join(page.inline_css))
        check_script(path, "\n".join(page.inline_script))

    assets = ROOT / "assets"
    for path in sorted(assets.rglob("*.css")):
        check_css(path, path.read_text(encoding="utf-8"))
    for path in sorted(assets.rglob("*.js")):
        if path.name != "search-index.js":
            check_script(path, path.read_text(encoding="utf-8"))

    index_path = assets / "search-index.js"
    if pages and not index_path.is_file():
        flag(index_path, "missing search index")
    elif index_path.is_file():
        script = index_path.read_text(encoding="utf-8")
        assignment = re.search(r"window\.GUIDE_INDEX\s*=\s*", script)
        try:
            if not assignment:
                raise ValueError("expected window.GUIDE_INDEX assignment")
            records, _ = json.JSONDecoder().raw_decode(script[assignment.end():])
            if not isinstance(records, list) or not records:
                raise ValueError("expected a nonempty JSON array")
            hrefs = Counter()
            for record in records:
                if not isinstance(record, dict) or not all(
                    isinstance(record.get(key), str)
                    for key in ("title", "section", "href", "text", "group")
                ):
                    raise ValueError("each record needs title, section, href, text, and group strings")
                href = record["href"]
                if not re.fullmatch(r"[\w-]+\.html(?:#[\w-]+)?", href):
                    flag(index_path, f"invalid search target {href!r}")
                else:
                    check_ref(ROOT / "index.html", "search target", href)
                hrefs[href] += 1
            for href, count in hrefs.items():
                if count > 1:
                    flag(index_path, f"duplicate search target {href!r} ({count})")
        except ValueError as error:
            flag(index_path, str(error))

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(pages)} generated pages and {sum(checked.values())} references.")
    print("Local targets, anchors, search records, and declared assets passed.")


if __name__ == "__main__":
    main()
