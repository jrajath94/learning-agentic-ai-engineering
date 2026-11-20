#!/usr/bin/env python3
"""Fail if the site contains em dashes or a list of AI-slop phrases."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".png", ".jpg", ".webp", ".gif"}
SLOP = [
    "delve",
    "delves",
    "delving",
    "tapestry",
    "game-changer",
    "game changer",
    "unlock the power",
    "in today's fast-paced",
    "in today’s fast-paced",
    "it's worth noting",
    "it is worth noting",
    "seamless",
    "cutting-edge",
    "cutting edge",
    "elevate your",
    "holistic",
    "deep dive",
    "dive deep",
    "supercharge",
    "next-level",
    "paradigm shift",
    "synergy",
    "plethora",
    "myriad",
    "nestled",
    "vibrant tapestry",
    "unlock your",
    "in order to truly",
    "at the end of the day",
    "robust solution",
    "leverage the",
    "landscape of",
    "it's not just",
    "it’s not just",
    "whether you're",
    "whether you’re",
    "dive into",
]

hits = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() in SKIP:
        continue
    rel = str(path.relative_to(ROOT))
    if rel == "scripts/check_prose.py":
        continue
    # Vendored libraries and a copied upstream file. The excerpt keeps the
    # publisher's wording, including words this checker rejects in our prose.
    if rel.startswith("assets/vendor/") or rel.endswith(".upstream-excerpt"):
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    if "\u2014" in text:
        hits.append(f"{path.relative_to(ROOT)}: em dash U+2014")
    if "\u2013" in text:
        hits.append(f"{path.relative_to(ROOT)}: en dash U+2013")
    low = text.lower()
    for phrase in SLOP:
        if phrase in low:
            hits.append(f"{path.relative_to(ROOT)}: slop phrase '{phrase}'")

if hits:
    print("\n".join(hits))
    sys.exit(1)
print("prose check passed")
