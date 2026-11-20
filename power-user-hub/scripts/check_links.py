#!/usr/bin/env python3
"""Check internal links and that external URLs do not 404.

Exit 1 if any internal target is missing or any external URL returns 404/410.
Other HTTP errors are reported and do not fail the run, because several
publishers block non-browser clients. Those URLs were fetched while researching.
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HREF = re.compile(r"""href=["']([^"']+)["']""", re.I)
ID = re.compile(r"""\bid=["']([^"']+)["']""")
UA = "Mozilla/5.0 (compatible; PowerUserHubLinkCheck/1.0)"


def pages() -> list[Path]:
    return sorted(ROOT.glob("*.html"))


def ids_in(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    found = set(ID.findall(text))
    if path.name == "sources.html":
        claims = (ROOT / "js" / "claims.js").read_text(encoding="utf-8")
        found.update(re.findall(r'"id": "(C\d+)"', claims))
    return found


def check_external(url: str) -> tuple[str, str]:
    req = Request(url, method="GET", headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=25) as res:
            return url, str(res.status)
    except HTTPError as err:
        return url, str(err.code)
    except URLError as err:
        return url, f"ERR {err.reason}"
    except Exception as err:  # noqa: BLE001
        return url, f"ERR {err}"


def main() -> int:
    html_pages = {p.name: p for p in pages()}
    missing_internal: list[str] = []
    external: set[str] = set()
    for path in html_pages.values():
        text = path.read_text(encoding="utf-8")
        for href in HREF.findall(text):
            if href.startswith(("#", "mailto:", "javascript:")):
                if href.startswith("#") and href[1:] not in ids_in(path):
                    missing_internal.append(f"{path.name} -> {href} (missing id)")
                continue
            if href.startswith("http://") or href.startswith("https://"):
                external.add(href.split("#")[0])
                continue
            target, _, frag = href.partition("#")
            target = target or path.name
            if target not in html_pages and not (ROOT / target).exists():
                missing_internal.append(f"{path.name} -> {href} (missing file)")
                continue
            if frag:
                file = html_pages.get(target) or (ROOT / target)
                if file.suffix == ".html" and frag not in ids_in(file):
                    missing_internal.append(f"{path.name} -> {href} (missing id)")

    print(f"internal problems: {len(missing_internal)}")
    for line in missing_internal:
        print(" ", line)

    results: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(check_external, url) for url in sorted(external)]
        for fut in as_completed(futs):
            results.append(fut.result())
    results.sort()
    hard = []
    for url, status in results:
        flag = ""
        if status in {"404", "410"}:
            flag = " FAIL"
            hard.append(url)
        elif not status.startswith("2") and status not in {"301", "302", "303", "307", "308"}:
            flag = " WARN"
        print(f"{status}{flag} {url}")
    print(f"external urls: {len(results)} hard_failures: {len(hard)}")
    return 1 if missing_internal or hard else 0


if __name__ == "__main__":
    sys.exit(main())
