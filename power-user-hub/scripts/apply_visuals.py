#!/usr/bin/env python3
"""Insert per-page diagrams, swap fonts, and strip dash characters. Idempotent."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FONT = (
    '<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,450;6..72,560'
    '&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;1,400'
    '&family=JetBrains+Mono:wght@450;600&display=swap" rel="stylesheet">'
)
MARK = (
    '<a class="mark" href="index.html">'
    '<svg viewBox="0 0 32 32" aria-hidden="true">'
    '<rect x="1.5" y="1.5" width="29" height="29" fill="none" stroke="#e0b15b" stroke-width="1.4"/>'
    '<circle cx="16" cy="16" r="3.2" fill="#e0b15b"/>'
    '</svg> Power User Hub</a>'
)

ARCH = '''<figure class="diagram">
  <figcaption>Five products, one ledger. Original diagram, not a vendor screenshot.</figcaption>
  <svg class="arch" viewBox="0 0 760 220" role="img" aria-label="Five tool clusters feed one claim ledger and a gap report">
    <rect width="760" height="220" fill="#000"/>
    <g font-family="Plus Jakarta Sans, sans-serif" font-size="13" fill="#f4f1ea">
      <rect x="16" y="24" width="120" height="36" rx="8" fill="#141414" stroke="#e0b15b"/>
      <text x="76" y="47" text-anchor="middle">Grok Bot</text>
      <rect x="16" y="72" width="120" height="36" rx="8" fill="#141414" stroke="#e0b15b"/>
      <text x="76" y="95" text-anchor="middle">Claude</text>
      <rect x="16" y="120" width="120" height="36" rx="8" fill="#141414" stroke="#e0b15b"/>
      <text x="76" y="143" text-anchor="middle">Antigravity</text>
      <rect x="16" y="168" width="120" height="36" rx="8" fill="#141414" stroke="#e0b15b"/>
      <text x="76" y="191" text-anchor="middle">Codex / dots</text>
      <rect x="168" y="24" width="120" height="36" rx="8" fill="#141414" stroke="#e0b15b"/>
      <text x="228" y="47" text-anchor="middle">Muse Code</text>
    </g>
    <g stroke="#e0b15b" fill="none" stroke-width="1.2">
      <path d="M136 42 H300 V110 H360"/>
      <path d="M136 90 H300"/>
      <path d="M136 138 H300 V110"/>
      <path d="M136 186 H300 V110"/>
      <path d="M288 42 H300"/>
    </g>
    <g font-family="Plus Jakarta Sans, sans-serif" font-size="14" fill="#f4f1ea">
      <rect x="360" y="78" width="160" height="64" rx="10" fill="#141414" stroke="#9dceb4"/>
      <text x="440" y="106" text-anchor="middle">Claim ledger</text>
      <text x="440" y="126" text-anchor="middle" font-size="12" fill="#b7b1a6">url, date, confidence</text>
      <rect x="580" y="78" width="150" height="64" rx="10" fill="#141414" stroke="#f0b4ae"/>
      <text x="655" y="115" text-anchor="middle">Gap report</text>
    </g>
    <path d="M520 110 H580" stroke="#9dceb4" fill="none"/>
  </svg>
  <p class="note">Teaching drawing of how this site treats sources. Not an architecture diagram from xAI, Anthropic, Google, OpenAI, or Meta.</p>
</figure>'''

def block(caption_flow, mermaid, caption_map, markmap, extra=""):
    return f'''<section class="section" id="page-map">
  <h2>See the shape first</h2>
  <div class="visual-grid">
    <figure class="diagram">
      <figcaption>{caption_flow}</figcaption>
      <pre class="mermaid">{mermaid}</pre>
    </figure>
    <figure class="diagram">
      <figcaption>{caption_map}</figcaption>
      <svg class="markmap-svg" aria-label="{caption_map}"></svg>
      <script type="text/markmap">{markmap}</script>
    </figure>
  </div>
  {extra}
</section>
'''

PAGES = {
"index.html": block(
    "How a claim moves from a product page to this hub.",
    """flowchart LR
  A[Origin page] --> B[One claim row]
  B --> C{Independent source?}
  C -->|same announcement| D[Mark as echo]
  C -->|new evidence| E[Keep as primary or secondary]
  E --> F[Page section]
  D --> F
  F --> G[Gap if the page was not read]""",
    "What the hub covers.",
    """# Power User Hub
## Products
### Grok Bot
### Claude and Duet
### Antigravity
### Codex and dots
### Muse Code
## Practice
### Skills and repos
### MCP
### Verification
## Records
### Ledger
### Gap report""",
    ARCH + '''<table>
  <caption class="muted">Product shapes as of the pages fetched on 20 Nov 2026. Dates are the dates on those pages.</caption>
  <thead><tr><th>Product</th><th>Newest string in this hub</th><th>Where the work happens</th><th>Human stop</th></tr></thead>
  <tbody>
    <tr><td>Grok Bot</td><td>App 1.2.3 on 18 Nov 2026</td><td>Cloud computer, connectors, routines</td><td>Per-tool approval</td></tr>
    <tr><td>Claude</td><td>Duet on Opus 5.5, 23 Oct 2026</td><td>Code in Claude Code, desk work in Duet</td><td>Hooks, tests, merge</td></tr>
    <tr><td>Antigravity</td><td>Neon default 18 Nov 2026, app v2.33.0</td><td>Orchestrator, swarm, SSH host</td><td>You read the diff</td></tr>
    <tr><td>Codex</td><td>CLI 0.171.0 on 20 Nov 2026</td><td>Repo. A dot may delegate here</td><td>You, plus auto-review on the dot</td></tr>
    <tr><td>Muse Code</td><td>Spark 1.2 default in docs, 1.3 on the price list</td><td>Terminal, event log, plan gate</td><td>Plan approval, and training opt-out</td></tr>
  </tbody>
</table>'''
),
"grok.html": block(
    "A Grok routine that may draft and may not send.",
    """sequenceDiagram
  participant You
  participant Bot as Grok Bot
  participant Mail as Mail connector
  You->>Bot: Save the draft pass as a skill
  Bot->>Mail: Read, if search is allowed
  Mail-->>Bot: Threads
  Bot-->>You: Drafts only
  Note over Bot,You: Send stays on Needs approval""",
    "Grok surfaces verified in this pass.",
    """# Grok
## Bot 1.2.3
### Always allow
### Auto-review
### Needs approval
### Blocked
## Skills page
### Grok 4.3 named there
### Deck and invoice examples
## Not verified
### Internal engineer diary
### A named company running on Grok"""
),
"claude.html": block(
    "Plan, test, then a person merges. The model summary is not the gate.",
    """flowchart TD
  A[Name the symptom and the test] --> B[Plan until the files are explicit]
  B --> C[Edit in one checkout]
  C --> D[Watch the test fail, then pass]
  D --> E[Second context reviews the diff]
  E --> F[Person merges]
  F --> G[Write the lesson into CLAUDE.md or a hook]""",
    "Two Claude surfaces.",
    """# Claude
## Claude Code
### Skills paged in
### Hooks enforced
### Subagents
### CLAUDE.md
## Claude Duet
### Opus 5.5
### Morning brief
### Approval before send
### Research preview
## Boris Cherny
### 2 Jan 2026 coding setup
### 23 Oct 2026 walk notes"""
),
"gemini.html": block(
    "November 2026 Antigravity: plan model, implement model, side question.",
    """sequenceDiagram
  participant You
  participant N as Neon plans
  participant H as Hydrogen edits
  participant Q as btw side question
  You->>N: Orchestrator prompt
  N->>H: Plan
  H-->>You: Diff
  You->>Q: Read-only check
  Q-->>You: Overlap or tests, no edits""",
    "Changelog primitives.",
    """# Antigravity
## Models
### Neon default 18 Nov
### Hydrogen
### Carbon
### Orchestrator
## Coordination
### slash swarm
### Dynamic Workflows
### btw read only
## Place
### SSH Linux host
### GitHub pull request pills"""
),
"codex.html": block(
    "A dot keeps the responsibility. Codex does the repo work.",
    """flowchart LR
  A[Chat] --> B[Answer in the thread]
  C[ChatGPT Work] --> D[A file or a research task]
  E[Codex CLI 0.171] --> F[Diff, tests, review]
  G[Your dot] --> H[Ongoing responsibility]
  H --> C
  H --> E
  I["~/.codex config"] --> E""",
    "Two meanings of dot.",
    """# Codex and dots
## Product: dots
### Cloud computer
### Read-only proactive research
### Delegates to Codex
### GPT-6 Astra then Terra
## CLI
### 0.171.0
### GPT-6.2 Sol default
### AGENTS.md chain
### Skills paged at about 2 percent
## Person
### Thibault Sottiaux
### AGENTS.md guide merged Oct 2025"""
),
"muse.html": block(
    "Muse's published inner loop, then a long run only if the plan holds.",
    """flowchart LR
  A["/plan waits for you"] --> B["/grill stress-tests the plan"]
  B --> C["/goal runs toward the objective"]
  C --> D[Event log]
  D --> E[Resume after a crash]
  F[Contributor mode] --> G[Training permission]
  H[Standard mode] --> I[Higher token price]""",
    "Muse facts to keep apart.",
    """# Muse Code
## Model ids
### Docs default spark 1.2
### Price list includes 1.3
## Runtime
### Background agents stay for the session
### Replay exact event log
### Sandbox on at first run
## Money and data
### Standard 1.25 and 4.25
### Contributor is the subscription default
### Contributor may train on your code"""
),
"cross-cutting.html": block(
    "The loop used across the five products. The mapping is a synthesis. The cells are sourced on this page.",
    """flowchart LR
  T[Trigger] --> E[Execute]
  E --> V[Verify]
  V --> S[State]
  S --> T
  V --> X[Stop if the check fails]""",
    "What to run in parallel, and what to sequence.",
    """# One person stack
## One harness
## One reviewer from another family
## One proactive desk
## Instruction files
### CLAUDE.md
### AGENTS.md
### Skills
## MCP 2026-07-28
## Do not stack
### Three planners at once
### Three inboxes at once
### Accept-all on a production repo"""
),
"principles.html": block(
    "Harness model. Context is addressable memory. A tool call leaves it.",
    """flowchart TB
  subgraph ram [Context as RAM]
    M[CLAUDE.md or AGENTS.md resident]
    K[Skill body paged in]
  end
  subgraph sys [Tools as syscalls]
    H[Hook or deny rule]
    P[Permission level]
  end
  ram --> sys
  sys --> V[Verifier that did not write the patch]
  V --> R[Git, glossary, or event log]""",
    "The four nouns.",
    """# Harness
## Context is RAM
### Resident instructions
### Paged skills
### Subagent summary
## Tools are syscalls
### Hooks
### Grok tool levels
### MCP bearer token
## Skills are programs
### Pocock small tools
### Superpowers mandatory sequence
### pstack router
## Evals are verifiers
### Failing test
### Fresh context
### Human merge"""
),
"profiles.html": block(
    "Who has a primary page in this hub, and who does not.",
    """flowchart TD
  A[Name in the brief] --> B{Primary page read?}
  B -->|yes| C[Profile card]
  B -->|no| D[Gap report]
  C --> E[Only the claims on that page]""",
    "People map.",
    """# People
## Profiled from a page
### Lauren Tan
### Boris Cherny
### Thibault Sottiaux
### Matt Pocock
### Jesse Vincent
### Hassan El Mghari
### Julius Brussee
## Named once in a launch post
### Duet preview users
## Not profiled
### Dario Amodei
### Codie Sanchez
### Greg Isenberg
### Mayank Shah"""
),
"prompts.html": block(
    "Every vault item has a publisher. Vendor examples are not private prompts.",
    """flowchart LR
  A[Page fetched] --> B{Verbatim prompt on it?}
  B -->|yes| C[Vault with attribution]
  B -->|no| D[Do not invent one]
  C --> E[Label vendor, docs, or author]""",
    "Where the 14 prompts came from.",
    """# Prompt vault
## xAI examples
### P01 to P04
## Anthropic docs
### P05 to P07
## Karpathy quote
### P08 specimen, not a recommendation
## Lauren Tan
### P09 to P12
## Hallmark
### P13 redesign
### P14 audit"""
),
"repos.html": block(
    "Install one router. Prove it loaded. Then stop.",
    """flowchart TD
  A[What is failing?] --> B{Requirements unclear?}
  B -->|yes| C[Pocock grill-me]
  B -->|no| D{Need a forced lifecycle?}
  D -->|yes| E[Superpowers]
  D -->|no| F{In Cursor and want a panel?}
  F -->|yes| G[pstack]
  F -->|no| H{Bill or a new page?}
  H -->|bill| I[Caveman]
  H -->|new page| J[Hallmark]""",
    "Five repos.",
    """# Repos
## mattpocock/skills
### Small and composable
## obra/superpowers
### Mandatory sequence
## JuliusBrussee/caveman
### Shorter output and tool text
## Nutlope/hallmark
### New pages only unless named
## cursor/plugins pstack
### poteto-mode router"""
),
"library.html": block(
    "A link is in this library only if a page behind it was read, or it is a labeled echo.",
    """flowchart LR
  A[Fetch origin] --> B[Library: docs]
  C[Practitioner post] --> D[Library: posts]
  E[News recap of A] --> F[Library: echoes]
  G[Unread URL] --> H[Not linked]""",
    "Shelves.",
    """# Library
## Docs and changelogs
## Repos
## Practitioner posts
## Echoes
### InfoQ
### TechCrunch
### Reuters
## Left out
### Unread Substack
### Paywalled podcasts
### Unused benchmark blogs"""
),
"sources.html": block(
    "One row per claim. Echoes stay visible and do not count as a second origin.",
    """flowchart LR
  A[Sentence on a page] --> B[id, url, author, date]
  B --> C[confidence]
  B --> D[primary or secondary or echo]
  D --> E[sources.json and this table]""",
    "Ledger fields.",
    """# Ledger
## Identity
### Id
### Cluster
## Evidence
### URL
### Author
### Date
## Judgment
### Confidence
### Independence
### Notes"""
),
"gaps.html": block(
    "Unknown stays on this page. It does not get promoted into a smooth paragraph.",
    """flowchart TD
  A[Search] --> B{Page opened?}
  B -->|no| C[Gap id]
  B -->|yes, thin| D[Profile or claim with low confidence]
  B -->|yes, launch anecdote only| E[Single-source note]
  C --> F[Next research action]""",
    "Open holes.",
    """# Gaps
## Versions
### Grok model ledger
### Claude Code semver
### Muse 1.2 versus 1.3
### Carbon plan matrix
## People
### Dario
### Codie
### Greg
### Mayank
### Tibo daily routine
## Method
### Boris thread is a mirror
### Vendor anecdotes
### Eval repos not read"""
),
"search.html": block(
    "Search hits a small index baked into the page. It does not call a server.",
    """flowchart LR
  Q[Query] --> I[HUB_INDEX in catalog.js]
  I --> F[Cluster filter]
  F --> R[Result cards]""",
    "Clusters you can filter.",
    """# Search index
## home
## grok
## claude
## gemini
## codex
## muse
## stack
## people
## ledger
## gaps"""
),
}

def clean_dashes(text: str) -> str:
    text = text.replace("\u2014", ":")
    text = text.replace("\u2013", "-")
    text = text.replace(" : ", ": ")
    return text

def main() -> None:
    for name, visual in PAGES.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet">',
            FONT,
            text,
            count=1,
        )
        text = text.replace(
            '<a class="mark" href="index.html"><span>Field notes</span> Power User Hub</a>',
            MARK,
        )
        if 'id="page-map"' not in text:
            needle = '  <section class="section"'
            idx = text.find(needle)
            if idx == -1:
                needle = "</main>"
                idx = text.find(needle)
                if idx == -1:
                    raise SystemExit(f"no insert point in {name}")
            text = text[:idx] + visual + "\n" + text[idx:]
        if "js/visuals.js" not in text:
            text = text.replace(
                '<script src="js/site.js"></script>',
                '<script src="js/site.js"></script>\n<script type="module" src="js/visuals.js"></script>',
            )
        text = clean_dashes(text)
        path.write_text(text, encoding="utf-8")
        print("updated", name)

    for path in list(ROOT.rglob("*")):
        if path.suffix.lower() not in {".py", ".md", ".json", ".csv", ".js"}:
            continue
        if path.name == "apply_visuals.py":
            continue
        text = path.read_text(encoding="utf-8")
        new = clean_dashes(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("dashes", path.relative_to(ROOT))

if __name__ == "__main__":
    main()
