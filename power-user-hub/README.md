# Power User Hub

Source-grounded notes on what power users actually do with Grok, Claude, Gemini, Codex, and Meta Muse, checked against public pages on **20 November 2026**.

There is no books-page template in this repository (the repo was a one-line README before this hub). Every page uses the same layout: `css/site.css`, the sticky nav, and `js/site.js`. The theme is pitch black (`#000`), with Newsreader for headings (a free text serif in the Tiempos family of shapes), Plus Jakarta Sans for body and UI, and JetBrains Mono for code. Paragraphs are justified. Diagrams render in the browser from Mermaid and Markmap on a CDN. If the CDN is blocked, the diagram source stays in the page.

The site is static HTML, CSS, and JavaScript. Nothing needs to be built or installed to read it.

## Open it

From this folder:

```bash
python3 -m http.server 8765
```

Then open [http://127.0.0.1:8765/](http://127.0.0.1:8765/).

You can also open `index.html` directly in a browser. Search, the ledger table, and on-page filters are inlined scripts, so they work without a server. Fonts are loaded from Google Fonts when you are online and fall back to Palatino and system sans-serif when you are not.

## What is inside

| Page | Role |
| --- | --- |
| `index.html` | Landing page and version dashboard |
| `grok.html`, `claude.html`, `gemini.html`, `codex.html`, `muse.html` | One deep page per tool cluster |
| `cross-cutting.html` | One-person stack, loops, MCP, vibe coding |
| `principles.html` | Harness model and verification |
| `profiles.html` | Named people, plus names this pass would not profile |
| `prompts.html` | Attributed prompts only |
| `repos.html` | Install notes for the skill repos |
| `library.html` | The URLs the pages rely on |
| `sources.html` | Claim ledger |
| `gaps.html` | Unverified items and the adversarial review |
| `data/sources.json`, `data/sources.csv` | The same ledger as files |

## Regenerating the ledger

Edit the list in `scripts/build_ledger.py`, then:

```bash
python3 scripts/build_ledger.py
```

Check links:

```bash
python3 scripts/check_links.py
python3 scripts/check_prose.py
```

The link checker fails on missing internal targets and on external 404s. Publishers that block a script's user agent are reported and do not fail the run. The prose checker fails on em dashes, en dashes, and a list of stock AI phrases.
