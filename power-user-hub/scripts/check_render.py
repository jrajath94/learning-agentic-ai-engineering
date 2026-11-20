#!/usr/bin/env python3
"""Open every hub page in headless Chromium with the network off.

Fails if a Mermaid block has no SVG, the SVG is tiny, or the SVG text
contains "Syntax error". Fails if a markmap SVG has no paths.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    pages = sorted(ROOT.glob("*.html"))
    failures: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context()
        context.set_offline(True)
        for path in pages:
            page = context.new_page()
            page.goto(path.resolve().as_uri(), wait_until="load")
            try:
                page.wait_for_function(
                    "() => document.documentElement.dataset.diagrams === 'ready'",
                    timeout=20000,
                )
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path.name}: diagrams did not finish ({exc})")
                page.close()
                continue
            mermaids = page.locator("pre.mermaid, div.mermaid")
            count = mermaids.count()
            for index in range(count):
                block = mermaids.nth(index)
                svg = block.locator("svg")
                if svg.count() == 0:
                    failures.append(f"{path.name}: mermaid {index} has no svg")
                    continue
                text = svg.first.evaluate("node => node.textContent || ''")
                if "Syntax error" in text:
                    failures.append(f"{path.name}: mermaid {index} syntax error")
                    continue
                box = svg.first.bounding_box()
                if not box or box["height"] < 40 or box["width"] < 40:
                    failures.append(f"{path.name}: mermaid {index} svg is empty")
            maps = page.locator("svg.markmap-svg")
            for index in range(maps.count()):
                paths = maps.nth(index).locator("path, circle")
                if paths.count() == 0:
                    failures.append(f"{path.name}: markmap {index} has no marks")
            page.close()
        browser.close()
    if failures:
        print("\n".join(failures))
        return 1
    print(f"render check passed: {len(pages)} pages, network off")
    return 0


if __name__ == "__main__":
    sys.exit(main())
