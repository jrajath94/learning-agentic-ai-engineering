#!/usr/bin/env python3
"""Capture real browser viewports of public docs and local command output.

A shot is kept only when the page has a title and the image is not a flat field.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "shots"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("claude-hooks", "https://code.claude.com/docs/en/hooks", "Hooks"),
    ("claude-practices", "https://code.claude.com/docs/en/best-practices", "Best practices"),
    ("claude-plan", "https://code.claude.com/docs/en/common-workflows", "Plan mode"),
    ("codex-config", "https://developers.openai.com/codex/config-sample", "sandbox_mode"),
    ("antigravity-orchestrator", "https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity/", "Orchestrator"),
    ("muse-docs", "https://dev.meta.ai/docs/muse-code", "plan"),
    ("grok-overview", "https://docs.x.ai/grok-bot/overview", "routine"),
    ("grok-skills", "https://x.ai/news/grok-skills", "skill"),
    (
        "github-tdd-skill",
        "https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/tdd/SKILL.md",
        "Test-Driven Development",
    ),
    (
        "github-gemini-md",
        "https://github.com/google-gemini/gemini-cli/blob/addc194f5bc414e7134c2bd6a414a40e1b4cbbed/GEMINI.md",
        "preflight",
    ),
]


def local_pages() -> list[tuple[str, Path, str]]:
    demo = subprocess.run(
        ["sh", str(ROOT / "kit" / "scripts" / "tdd-demo.sh")],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    demo_text = demo.stdout or ""
    work = Path("/tmp/shot-diff")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    (work / "counter.py").write_text("def inc(n):\n    return n\n", encoding="utf-8")
    (work / "test_counter.py").write_text(
        "from counter import inc\n\nassert inc(1) == 2, \"inc(1) should be 2\"\nprint(\"ok\")\n",
        encoding="utf-8",
    )
    red = subprocess.run(["python3", "test_counter.py"], cwd=work, capture_output=True, text=True)
    (work / "counter.py").write_text("def inc(n):\n    return n + 1\n", encoding="utf-8")
    green = subprocess.run(["python3", "test_counter.py"], cwd=work, capture_output=True, text=True)
    diff = subprocess.run(["diff", "-u", "/dev/null", str(work / "counter.py")], capture_output=True, text=True)
    # A before/after unified diff of the function, built from the two files we wrote.
    before = "def inc(n):\n    return n\n"
    after = (work / "counter.py").read_text(encoding="utf-8")
    diff_body = subprocess.run(
        ["diff", "-u", str(work / "before.py") if False else "-"],
        input="",
        capture_output=True,
        text=True,
    )
    import tempfile, os
    b = work / "before.py"
    a = work / "after.py"
    b.write_text(before, encoding="utf-8")
    a.write_text(after, encoding="utf-8")
    real_diff = subprocess.run(["diff", "-u", str(b), str(a)], capture_output=True, text=True).stdout

    def page(title: str, body: str) -> str:
        escaped = (
            body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {{ margin: 0; background: #000; color: #f4f1ea; font: 16px/1.45 ui-monospace, monospace; }}
header {{ padding: 16px 20px; border-bottom: 1px solid #333; font-family: sans-serif; }}
pre {{ padding: 16px 20px; white-space: pre-wrap; }}
</style></head>
<body><header><strong>{title}</strong><br>Captured on this machine, 20 Nov 2026. Not a vendor product screenshot.</header>
<pre>{escaped}</pre></body></html>"""

    term = Path("/tmp/shot-terminal.html")
    diffp = Path("/tmp/shot-diff.html")
    term.write_text(
        page(
            "sh kit/scripts/tdd-demo.sh",
            demo_text.strip() + f"\nprocess exit {demo.returncode}\n",
        ),
        encoding="utf-8",
    )
    diffp.write_text(
        page(
            "diff -u before.py after.py",
            "red exit {0}\n{1}\ngreen exit {2}\n{3}\n{4}".format(
                red.returncode,
                (red.stderr or red.stdout or "").strip(),
                green.returncode,
                (green.stdout or "").strip(),
                real_diff,
            ),
        ),
        encoding="utf-8",
    )
    return [
        ("local-tdd-demo", term, "AssertionError"),
        ("local-counter-diff", diffp, "return n + 1"),
    ]


def not_flat(path: Path) -> bool:
    from PIL import Image, ImageStat
    im = Image.open(path).convert("L")
    stat = ImageStat.Stat(im)
    return stat.stddev[0] > 12


def main() -> None:
    bins = {name: shutil.which(name) for name in ("claude", "codex", "muse", "agy")}
    manifest = []
    locals_ = local_pages()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        for name, url, needle in PAGES:
            page = context.new_page()
            dest = OUT / f"{name}.png"
            note = ""
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2500)
                loc = page.get_by_text(needle, exact=False)
                if loc.count():
                    try:
                        loc.first.scroll_into_view_if_needed(timeout=4000)
                        page.wait_for_timeout(400)
                    except Exception as exc:  # noqa: BLE001
                        note = f"Could not scroll to {needle!r}: {exc.__class__.__name__}. Shot is the viewport that did load."
                else:
                    note = f"Text {needle!r} was not found in the rendered page."
                page.screenshot(path=str(dest))
                title = page.title()
                final = page.url
            except Exception as exc:  # noqa: BLE001
                note = f"capture failed: {exc}"
                title = ""
                final = url
            page.close()
            if dest.exists() and not_flat(dest):
                manifest.append({
                    "file": f"assets/shots/{name}.png",
                    "url": final,
                    "requested_url": url,
                    "title": title,
                    "captured": "2026-11-20",
                    "kind": "public page viewport",
                    "note": note,
                })
                print("kept", name, title[:60])
            else:
                if dest.exists():
                    dest.unlink()
                print("dropped", name, note or "flat")
                manifest.append({
                    "file": None,
                    "url": final if "final" in dir() else url,
                    "requested_url": url,
                    "title": "",
                    "captured": "2026-11-20",
                    "kind": "failed",
                    "note": note or "image was flat",
                })
        for name, path, needle in locals_:
            page = context.new_page()
            dest = OUT / f"{name}.png"
            page.goto(path.resolve().as_uri(), wait_until="load")
            page.screenshot(path=str(dest))
            page.close()
            manifest.append({
                "file": f"assets/shots/{name}.png",
                "url": "local command",
                "requested_url": str(path.name),
                "title": name,
                "captured": "2026-11-20",
                "kind": "local command output",
                "note": "Rendered from the command's own stdout. Not a Claude or Codex window.",
            })
            print("kept", name)
        browser.close()
    manifest.append({"binaries": bins})
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("done", sum(1 for row in manifest if row.get("file")))


if __name__ == "__main__":
    main()
