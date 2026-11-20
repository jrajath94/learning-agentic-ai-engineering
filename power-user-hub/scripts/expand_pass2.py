#!/usr/bin/env python3
"""Merge pass-2 claims and write the new pages. Idempotent on claim ids."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAV = (
    '<a href="index.html">Home</a><a href="grok.html">Grok</a><a href="claude.html">Claude</a>'
    '<a href="gemini.html">Gemini</a><a href="codex.html">Codex</a><a href="muse.html">Muse</a>'
    '<a href="cross-cutting.html">Stack</a><a href="profiles.html">Profiles</a>'
    '<a href="principles.html">Principles</a><a href="prompts.html">Prompts</a>'
    '<a href="repos.html">Repos</a><a href="library.html">Library</a>'
    '<a href="method.html">Method</a><a href="tokens.html">Tokens</a>'
    '<a href="talks.html">Talks</a><a href="directory.html">Directory</a>'
    '<a href="sources.html">Ledger</a><a href="gaps.html">Gaps</a>'
)
OLD_NAV = (
    '<a href="index.html">Home</a><a href="grok.html">Grok</a><a href="claude.html">Claude</a>'
    '<a href="gemini.html">Gemini</a><a href="codex.html">Codex</a><a href="muse.html">Muse</a>'
    '<a href="cross-cutting.html">Stack</a><a href="profiles.html">Profiles</a>'
    '<a href="principles.html">Principles</a><a href="prompts.html">Prompts</a>'
    '<a href="repos.html">Repos</a><a href="library.html">Library</a>'
    '<a href="sources.html">Ledger</a><a href="gaps.html">Gaps</a>'
)
FONT = (
    '<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,450;6..72,560'
    '&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;1,400'
    '&family=JetBrains+Mono:wght@450;600&display=swap" rel="stylesheet">'
)
MARK = (
    '<a class="mark" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true">'
    '<rect x="1.5" y="1.5" width="29" height="29" fill="none" stroke="#e0b15b" stroke-width="1.4"/>'
    '<circle cx="16" cy="16" r="3.2" fill="#e0b15b"/></svg> Power User Hub</a>'
)

CLUSTER_MAP = {
    "instruction-files": "claude",
    "orchestration": "claude",
    "verification": "practice",
    "mcp": "mcp",
    "security-failures": "practice",
    "team-workflow": "claude",
    "model-routing": "claude",
    "context": "claude",
    "skills": "repos",
    "hooks": "claude",
    "memory": "claude",
    "install": "repos",
    "workflow": "repos",
    "privacy": "repos",
    "telemetry": "repos",
    "catalog": "repos",
    "claude-md": "claude",
    "vibe-coding": "practice",
    "claude-code-product": "claude",
    "agent-harness": "claude",
    "skills-workflows": "repos",
    "evals": "practice",
    "operator-stack": "practice",
    "identity-disambiguation": "people",
}


def clean(text: str) -> str:
    text = text.replace("\u2014", ":").replace("\u2013", "-")
    text = text.replace(" : ", ": ")
    return text


def page(title: str, kicker: str, h1: str, lede: str, body: str, desc: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{clean(title)}</title>
<meta name="description" content="{clean(desc)}">
{FONT}
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="top-row">
    {MARK}
    <p class="asof">Checked 20 Nov 2026</p>
    <form class="finder" role="search" action="search.html"><label class="sr" for="q">Search</label><input id="q" name="q" type="search" placeholder="Search the hub  (/)"></form>
  </div>
  <nav class="nav" aria-label="Sections">
    {NAV}
  </nav>
</header>
<main id="main">
  <p class="kicker">{clean(kicker)}</p>
  <h1>{clean(h1)}</h1>
  <p class="lede">{clean(lede)}</p>
{body}
</main>
<footer class="foot"><div class="foot-in"><p><a href="method.html">Method</a> · <a href="sources.html">Ledger</a> · <a href="gaps.html">Gaps</a></p></div></footer>
<script src="js/claims.js"></script>
<script src="js/catalog.js"></script>
<script src="js/site.js"></script>
<script type="module" src="js/visuals.js"></script>
</body>
</html>
"""


def visual(flow_cap: str, mermaid: str, map_cap: str, markmap: str) -> str:
    return f"""
<section class="section" id="page-map">
  <h2>See the shape first</h2>
  <div class="visual-grid">
    <figure class="diagram">
      <figcaption>{clean(flow_cap)}</figcaption>
      <pre class="mermaid">{mermaid}</pre>
    </figure>
    <figure class="diagram">
      <figcaption>{clean(map_cap)}</figcaption>
      <svg class="markmap-svg" aria-label="{clean(map_cap)}"></svg>
      <script type="text/markmap">{markmap}</script>
    </figure>
  </div>
</section>
"""


def load_new() -> list[dict]:
    items = []
    for name in ["transcripts.json", "reddit.json", "github.json", "blogs.json"]:
        path = Path("/tmp/research2/claims") / name
        batch = json.loads(path.read_text(encoding="utf-8"))
        for raw in batch:
            item = {k: clean(str(v)) if isinstance(v, str) else v for k, v in raw.items()}
            item["cluster"] = CLUSTER_MAP.get(item.get("cluster", ""), item.get("cluster", "practice"))
            if name == "reddit.json":
                item["notes"] = (item.get("notes") or "") + " Text taken from an Arctic Shift archive of r/ClaudeAI selftexts. reddit.com returned 403 to this environment's link checker on 2026-11-20. The post id was matched to the archive file."
                item["confidence"] = "medium"
            items.append(item)
    items.append({
        "cluster": "tokens",
        "claim": "In a YouTube page text for an interview titled around Claude Code's head, the speaker who describes releasing Claude Code says they run about five agents at a time on a computer and, most nights, hundreds and sometimes thousands in parallel, at the edge of a max plan, with API billing as the overflow.",
        "url": "https://www.youtube.com/watch?v=Z6IT4gjrcPE",
        "source_title": "Claude Code Head Boris Cherny: token maxing interview page text",
        "author": "Speaker on the Boris Cherny interview page (labels absent)",
        "date": "fetched 2026-11-20",
        "confidence": "medium",
        "independence": "primary",
        "notes": "yt-dlp auto-captions were blocked (YouTube bot check, no cookies). This sentence is from the page text saved by the research fetcher, not a timestamped caption file. The five-at-a-time line matches Boris Cherny's 2 Jan 2026 post, which is why the speaker is likely him. Not labelled in the file.",
    })
    items.append({
        "cluster": "tokens",
        "claim": "The same page text says the amount of code written per engineer at Anthropic had grown something like 250 percent since Claude Code, with code quality and reliability described as held stable. No speaker label is in the extract.",
        "url": "https://www.youtube.com/watch?v=Z6IT4gjrcPE",
        "source_title": "Claude Code Head Boris Cherny: token maxing interview page text",
        "author": "Speaker on the Boris Cherny interview page (labels absent)",
        "date": "fetched 2026-11-20",
        "confidence": "medium",
        "independence": "primary",
        "notes": "Same caption limitation as the parallel-sessions line. The phrase 'the last number that we reported' is in the extract. Treat as a reported figure, not a paper.",
    })
    items.append({
        "cluster": "tokens",
        "claim": "No source opened in this pass states that Anthropic or OpenAI employees use 5,000 to 10,000 tokens per day. The documented quantities are a May 2025 external spend of about $6 per active user per day, free internal use at that date, thousands of dollars a day for a few automated workloads, and later descriptions of hundreds of parallel sessions.",
        "url": "https://latentspace.podhood.com/953b54c2-6d60-4e9c-b1d7-f7c767a0a1b0",
        "source_title": "Claude Code: Anthropic's CLI Agent transcript mirror",
        "author": "Cat Wu and Boris Cherny, via transcript mirror",
        "date": "2025-05-07",
        "confidence": "high",
        "independence": "primary",
        "notes": "Negative finding for this corpus, not a proof that no one has ever said 5-10k. yt-dlp could not pull captions. The $6 line is at about 14:48 in the mirror. The thousands-of-dollars line is Boris at about 13:18.",
    })
    return items


def merge(existing: list[dict], new_items: list[dict]) -> list[dict]:
    seen = set()
    for row in existing:
        seen.add((row["url"], re.sub(r"\s+", " ", row["claim"].lower())[:90]))
    start = max(int(row["id"][1:]) for row in existing) + 1
    out = list(existing)
    for item in new_items:
        key = (item["url"], re.sub(r"\s+", " ", item["claim"].lower())[:90])
        if key in seen:
            continue
        seen.add(key)
        row = {
            "id": f"C{start}",
            "cluster": item.get("cluster") or "practice",
            "claim": item["claim"],
            "url": item["url"],
            "source_title": item.get("source_title") or item["url"],
            "author": item.get("author") or "unknown",
            "date": item.get("date") or "2026-11-20",
            "confidence": item.get("confidence") or "medium",
            "independence": item.get("independence") or "primary",
            "notes": item.get("notes") or "",
        }
        out.append(row)
        start += 1
    return out


def write_ledger(rows: list[dict]) -> None:
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    (data / "sources.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (data / "sources.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "js" / "claims.js").write_text("window.HUB_CLAIMS = " + json.dumps(rows) + ";\n", encoding="utf-8")
    pass2 = [row for row in rows if int(row["id"][1:]) >= 53]
    (data / "pass2-claims.json").write_text(json.dumps(pass2, indent=2) + "\n", encoding="utf-8")


def resources(rows: list[dict]) -> list[dict]:
    best = {}
    for row in rows:
        url = row["url"]
        if url not in best:
            kind = "article"
            if "reddit.com" in url:
                kind = "reddit"
            elif "github.com" in url:
                kind = "repo"
            elif "youtube.com" in url or "latent.space" in url or "podhood" in url:
                kind = "talk"
            elif "anthropic.com" in url or "openai.com" in url or "x.ai" in url or "antigravity" in url or "meta.ai" in url:
                kind = "official"
            best[url] = {
                "title": row["source_title"],
                "url": url,
                "author": row["author"],
                "date": row["date"],
                "cluster": row["cluster"],
                "kind": kind,
                "claims": 1,
            }
        else:
            best[url]["claims"] += 1
    return sorted(best.values(), key=lambda r: (-r["claims"], r["title"]))


def build_pages(rows: list[dict]) -> None:
    n = len(rows)
    method_body = visual(
        "Russian doll: stop when a new source repeats a claim you already have.",
        """flowchart TD
  Q[Layer 0: what do power users do?] --> C[Layer 1: five tools plus tokens]
  C --> S[Layer 2: features, workflows, cost, failure]
  S --> P[Layer 3: repo, config, quote, timestamp]
  P --> Sat{New claim?}
  Sat -->|yes| P
  Sat -->|no| Stop[Record saturation]""",
        "Where pass 2 looked.",
        """# Pass 2
## Transcripts
### Latent Space Boris and Cat
### Latent Space Thariq
## Lab study
### Anthropic Aug 2025
## Code
### GitHub READMEs and hooks
## Reddit
### r/ClaudeAI archive only
## Not reached
### YouTube captions
### Most subreddits
### X threads
""",
    ) + """
<section class="section" id="layers">
  <h2>The doll, in the open</h2>
  <ol class="steps">
    <li><strong>Layer 0.</strong> What do power users do with frontier tools that a chat box does not, and which of those moves are written down?</li>
    <li><strong>Layer 1.</strong> Grok, Claude, Gemini, Codex, Muse, plus token use, MCP, and skills.</li>
    <li><strong>Layer 2.</strong> For each: features, workflows, configs, prompts, failures, and cost.</li>
    <li><strong>Layer 3.</strong> The artifact: a repo file, a config line, a quote, or a timestamp. Echoes of one announcement stay one origin.</li>
  </ol>
  <p>Pass 1 stopped at official product pages: 52 claims. Pass 2 opened interview transcripts, one Anthropic study, GitHub files, an Arctic Shift slice of r/ClaudeAI, and a handful of practitioner posts. The ledger is now """ + str(n) + """ claims. Saturation inside r/ClaudeAI was real: later posts repeated CLAUDE.md, hooks, small MCP lists, and 'do not trust the model's own report.' Other subreddits did not return posts. YouTube captions did not download. That is recorded on the <a href="gaps.html">gap report</a>, not papered over.</p>
</section>
<section class="section" id="what-opened">
  <h2>What was opened</h2>
  <ul class="clean">
    <li>Latent Space mirror transcript, Boris Cherny and Cat Wu, 7 May 2025, with timestamps. <a href="talks.html">Talks</a>.</li>
    <li>Latent Space page for Thariq Shihipar, fetched with timestamps in the page text.</li>
    <li>Anthropic, 'How AI is transforming work at Anthropic,' August 2025 survey and Claude Code transcript study.</li>
    <li>GitHub READMEs and two extra repos named in the field notes: awesome-claude-code, awesome-mcp-servers, openai/codex, anthropics/claude-code, mattpocock/skills, superpowers, a hooks showcase, and a CLAUDE.md explorer.</li>
    <li>Arctic Shift search of r/ClaudeAI after 20 Nov 2025. 382 posts saved, 58 claims kept, later posts dropped as repeats. Direct reddit.com JSON returned 403.</li>
    <li>Practitioner pages: Simon Willison on Karpathy, Armin Ronacher, Kent Beck, Hamel Husain, Jesse Vincent's Superpowers post, Greg Isenberg's 17 Mar 2026 guide, Latent Space wiki pages for Boris and Cat.</li>
  </ul>
</section>
<section class="section" id="stopped">
  <h2>Where new sources stopped adding claims</h2>
  <ul class="clean">
    <li>r/ClaudeAI archive: after instruction files, hooks, MCP size, compaction, cheaper subagents, and replay-or-screenshot, more posts restated those five.</li>
    <li>Blogs: human review, CLAUDE.md or AGENTS.md, search over a heavy index, and evals showed up on more than one fetched page. Further hits on the same authors were not opened.</li>
    <li>GitHub: install lines and skill philosophy repeated the pass 1 repos. New claims were the extra hook and CLAUDE.md files, not a new theory.</li>
    <li>YouTube: yt-dlp was blocked, so caption mining stopped. One page-text extract was kept and labelled medium confidence.</li>
  </ul>
</section>
"""
    (ROOT / "method.html").write_text(page(
        "Method: Power User Hub",
        "Russian doll",
        "How this pass decided it had enough, and where it did not.",
        "Layer 0 is the question. Each inner layer is a narrower artifact. A source that only repeats a claim already in the ledger is an echo or a saturation note, not a new row.",
        method_body,
        "Research method and saturation notes for the power user hub.",
    ), encoding="utf-8")

    tokens_body = visual(
        "Documented quantities. The 5 to 10 thousand tokens a day figure is not among them.",
        """flowchart TD
  A[5 to 10 thousand tokens a day] --> B[Not in the opened sources]
  C[May 2025 external] --> D["About 6 dollars a day per active user"]
  E[May 2025 internal] --> F[Free at Anthropic]
  G[May 2025 edge] --> H[Thousands of dollars a day for a few people]
  I[Later interview page] --> J[Five local, hundreds at night]
  K[Aug 2025 study] --> L[Share of work and PRs, not a token total]""",
        "Token evidence map.",
        """# Token evidence
## Not found
### 5 to 10 thousand tokens a day
## May 2025 Latent Space
### Free internally
### About 6 dollars external
### Thousands of dollars for a few
### 1000 lints, 1000 Claudes
## Later interview text
### Five at a time
### Hundreds most nights
## Aug 2025 study
### 59 percent of work
### 50 percent productivity
### 67 percent more merged PRs
""",
    ) + """
<section class="section" id="finding">
  <h2>The 5 to 10 thousand figure</h2>
  <p>It is not in the sources this pass opened. A coding agent that reads a repo and runs tests spends that many tokens in a single tool result. Treating 5 to 10 thousand tokens as a frontier-lab day would be low by orders of magnitude next to the numbers that are written down.</p>
  <p>What is written down, with the speaker and the time:</p>
  <ul class="clean">
    <li>7 May 2025, about 13:50. Boris Cherny: Claude Code is free internally. Transcript mirror of Latent Space.</li>
    <li>Same episode, about 14:48. Cat Wu: external active users were around $6 per day, a bit higher across a month than a $20 Cursor subscription. She also said the tool is aimed at being snappy and thorough, not at minimizing tokens.</li>
    <li>Same episode, about 13:18. Boris: some people at Anthropic had been racking up thousands of dollars a day with automation. Most people were not. He had just described starting one Claude per lint violation, up to about 1,000.</li>
    <li>Same episode, about 1:04. Cat Wu: there was no separate subscription yet. Pay as you go kept the upfront commitment at zero. So the $6 figure is from the API-priced period, not from a later bundled plan.</li>
    <li>28 Sep 2026 Latent Space page, about 00:52. Thariq Shihipar: before Claude Code, people were not used to spending more than $20 a month. Opus 4 was expensive. Opus 4.5 was, in his words, both great and cheap. The host's line about 15 Claude Code accounts is the host's line.</li>
    <li>YouTube page text for the Boris interview, no caption file: the speaker says about five at a time on a computer, and most nights hundreds, sometimes thousands, in parallel, at the edge of a max plan, with the API as overflow. Speaker labels are missing. Medium confidence. yt-dlp could not save captions.</li>
    <li>August 2025 Anthropic study: 132 engineers and researchers surveyed, 53 interviewed, 200,000 Claude Code transcripts from February and August 2025. Self-report: Claude in 59 percent of work and a 50 percent productivity gain, up from 28 percent and 20 percent a year earlier. They also report a 67 percent increase in merged pull requests per engineer per day after adopting Claude Code. No token total per person is in that page.</li>
  </ul>
  <p>The internal-free line and the thousands-of-dollars line sit a minute apart. The page does not say whether those dollars were an internal transfer price or a real invoice. Both sentences are quoted. The tension is left open.</p>
</section>
<section class="section" id="how">
  <h2>How a large token bill actually gets spent</h2>
  <p>These are the mechanisms named by the people above, not a guessed stack.</p>
  <ol class="steps">
    <li><strong>Parallel sessions, separate work.</strong> Five on one computer in the later interview text. The 2 Jan 2026 post already said five local checkouts plus five to ten on the web. The May 2025 episode adds the extreme form: one agent per lint, and some people running that wide enough to look like thousands of dollars a day.</li>
    <li><strong>Overnight fan-out.</strong> The interview page text says most nights, not every night, hundreds in parallel. That is a scheduled burst, not a longer chat.</li>
    <li><strong>Compaction instead of a bigger window.</strong> Boris, about 8:58 in the May episode: after truncation and rewriting old tool calls, compaction that worked was asking Claude to summarize the previous messages. Cat Wu, about 55:53: compacting several times weakens the original intent. Long runs spend tokens twice, once to work and once to forget carefully.</li>
    <li><strong>Verification, which the August study says is still mostly human.</strong> More than half of respondents could fully delegate only 0 to 20 percent of their work. They debug and reread because they did not write the code. That reread is part of the cost, and it is also why a token total is not a productivity total.</li>
    <li><strong>Effort routed by task.</strong> Thariq, about 00:25: high or max effort for code review and security, low or medium for UI. High effort is more tokens on purpose.</li>
  </ol>
</section>
<section class="section" id="solo">
  <h2>A cost sketch for one subscriber</h2>
  <p>This sketch uses only published prices and the reader's own subscription list. It is not a bill from any lab.</p>
  <table>
    <thead><tr><th>Input</th><th>What it is</th></tr></thead>
    <tbody>
      <tr><td>Reader's seats</td><td>Codex on the order of $100 a month, Claude Code on the order of $20, plus Google AI Pro, Meta Muse Code, and Grok Bot. Those dollar figures are the reader's report of what they pay, not a price page fetched for this pass, except Muse token rates.</td></tr>
      <tr><td>Muse Spark standard</td><td>$1.25 per million input tokens and $4.25 per million output tokens. Contributor mode is cheaper because it allows training on your content. Subscriptions default to Contributor mode.</td></tr>
      <tr><td>5 to 10 thousand output tokens a day</td><td>About 0.15 to 0.30 million tokens a month. At $4.25 per million output, that is well under $2 a month. That is a light chat, not the workflows above.</td></tr>
      <tr><td>May 2025 external average</td><td>About $6 a day, on the order of $180 across 30 days, while the product was pay as you go. A $20 subscription did not exist yet for Claude Code, by Cat Wu's account in that episode.</td></tr>
    </tbody>
  </table>
  <div class="callout hyp">
    <strong class="tag">Synthesis, not a measurement</strong>
    <p>Stay inside one subscription until the product's own usage screen says you are at the cap. The reproducible loop is still: one bug, one failing test, one diff you read. Add a second checkout only when the first session is waiting on a long command. Add an overnight fan-out only for tasks that do not share files, the lint-sized shape Boris described, and only after you have watched one of them fail a test. If the cap arrives, the documented overflow is the API, which is how the May 2025 $6 average was produced. Do not buy a second account because a host joked about fifteen.</p>
  </div>
</section>
"""
    (ROOT / "tokens.html").write_text(page(
        "Token use: Power User Hub",
        "Frontier labs",
        "Nobody in the opened record says 5 to 10 thousand tokens a day.",
        "The figure is too small for the workflows these same people describe. What the transcripts and the August 2025 study do record is spend, parallel sessions, and a share of the workday.",
        tokens_body,
        "What is documented about token and dollar use at Anthropic, and a solo cost sketch.",
    ), encoding="utf-8")

    talks_body = visual(
        "Two Latent Space episodes that name workflows, not vibes.",
        """flowchart LR
  A[May 2025 Boris and Cat] --> B[Unix utility, free inside, 6 dollars outside]
  C[Sep 2026 Thariq] --> D[Effort by task, 20 then 200 dollars]""",
        "Talks opened.",
        """# Talks
## 7 May 2025
### Boris Cherny
### Cat Wu
### Swyx and Alessio
## 28 Sep 2026
### Thariq Shihipar
## Not captioned
### YouTube auto-subs blocked
""",
    ) + """
<section class="section" id="ls-may">
  <h2>Latent Space, 7 May 2025: Boris Cherny and Cat Wu</h2>
  <p>Source: a transcript mirror with timestamps, <a href="https://latentspace.podhood.com/953b54c2-6d60-4e9c-b1d7-f7c767a0a1b0">latentspace.podhood.com</a>. It is a mirror, not the YouTube caption track. yt-dlp could not download captions. Quotes below were checked against that file.</p>
  <ul class="clean">
    <li>0:17 area. Claude Code is Claude in the terminal: commands and files, agentically. Boris.</li>
    <li>About 8:58. Compaction that worked: ask Claude to summarize previous messages. Earlier tries were truncation and rewriting old tool calls.</li>
    <li>About 12:32. Raw access, no large UI. Example: 1,000 lint violations, 1,000 Claudes.</li>
    <li>13:18. Some Anthropic people racking up thousands of dollars a day. Most people do not.</li>
    <li>13:50. Free internally.</li>
    <li>14:48. Cat Wu: about $6 per day per active external user.</li>
    <li>About 47 to 48 minutes. Early RAG with Voyage underperformed agentic search with ordinary code search. Boris says the comparison was mostly internal vibes, plus some internal benchmarks.</li>
    <li>About 55:53. Cat Wu: repeated compaction weakens the original user intent.</li>
    <li>About 1:00. Default model then was Sonnet. Users could override, including Haiku.</li>
    <li>About 1:05. Boris: about 2x for him, and he thinks about 10x for some Anthropic engineers. Cat's separate metrics, earlier in the episode, were cycle time and features that would not exist otherwise.</li>
  </ul>
  <p>Cat Wu's role on the Latent Space wiki, fetched the same day, is product, not the model. The wiki is a secondary synthesis dated as of 20 Sep 2026 and says human review of the wiki was still pending. Prefer the transcript for quotes.</p>
</section>
<section class="section" id="thariq">
  <h2>Latent Space, 28 Sep 2026: Thariq Shihipar</h2>
  <p>Page: <a href="https://latent.space/p/thariq/">latent.space/p/thariq</a>. Timestamps are in the fetched page text.</p>
  <ul class="clean">
    <li>00:21. High effort changes security evals a lot. For software engineering it mostly adds verification and edge cases.</li>
    <li>00:25. His rough split: high or max for code review and security, low or medium for UI.</li>
    <li>00:52. People were not used to more than $20 a month. Opus 4 was expensive. Opus 4.5 was both strong and cheaper, in his wording. The host mentions a $200 plan and 15 accounts. That is the host, not a staffing recommendation.</li>
  </ul>
</section>
<section class="section" id="not">
  <h2>Talks named and not opened</h2>
  <p>Dwarkesh, Lenny's, Lex Fridman, No Priors, Changelog, Cognitive Revolution, and the AI Engineer stages were not transcribed here. Pragmatic Engineer pages that are paywalled were not used past what a public extract already supported in pass 1. The gap list says so.</p>
</section>
"""
    (ROOT / "talks.html").write_text(page(
        "Talks: Power User Hub",
        "Transcripts",
        "Two episodes with timestamps. The rest of the podcast list was not opened.",
        "Pass 2 did not pretend a caption file existed when YouTube blocked the download. These notes follow pages that were actually fetched.",
        talks_body,
        "Timestamped notes from Latent Space episodes with Boris Cherny, Cat Wu, and Thariq Shihipar.",
    ), encoding="utf-8")

    reddit_rows = [r for r in rows if "reddit.com" in r["url"]]
    items = "\n".join(
        f'<li><a href="{r["url"]}">{r["source_title"]}</a>: {r["claim"]}</li>'
        for r in reddit_rows[:12]
    )
    reddit_body = visual(
        "What repeated in r/ClaudeAI after the archive search, and what was dropped.",
        """flowchart TD
  A[Arctic Shift search] --> B[382 selftexts]
  B --> C[58 claims]
  C --> D[Later posts repeated the same five moves]
  E[reddit.com JSON] --> F[403 blocked]""",
        "Reddit coverage.",
        """# Reddit
## Opened
### r/ClaudeAI via Arctic Shift
## Repeated and then dropped
### CLAUDE.md
### Hooks
### Small MCP lists
### Compaction
### Do not trust the report
## Not opened
### Other subs timed out or 403
""",
    ) + f"""
<section class="section" id="sample">
  <h2>Twelve of the archive claims</h2>
  <p>Every row in the ledger whose URL is reddit.com was matched to a post id in the saved archive. The link checker got 403 from reddit.com itself. Read these as archive-backed, not as a live scrape of the front page.</p>
  <ul class="clean">
    {items}
  </ul>
  <p><a href="sources.html">The ledger</a> has the rest. Filter the directory to kind reddit.</p>
</section>
"""
    (ROOT / "reddit-field.html").write_text(page(
        "Reddit field notes: Power User Hub",
        "r/ClaudeAI archive",
        "The subreddit that returned posts, and the five moves it kept repeating.",
        "Direct Reddit JSON was blocked. An Arctic Shift search of r/ClaudeAI after 20 Nov 2025 supplied the selftexts. Other named subs did not return posts.",
        reddit_body,
        "Archive-backed Reddit claims about Claude Code workflows.",
    ), encoding="utf-8")

    cat_body = visual(
        "Cat Wu, from the May 2025 episode and the Latent Space wiki.",
        """flowchart TD
  A[Uses the tool and sends feedback] --> B[Becomes PM]
  B --> C[Permissions, latency, metrics]
  C --> D[Non-engineers landing PRs]""",
        "What she is on record for.",
        """# Cat Wu
## May 2025
### About 6 dollars a day external
### Latency over token thrift
### Permissions with Robert
### Cycle time
## Wiki
### Head of Product by May 2026 conference listing
### Secondary page
""",
    ) + """
<section class="section" id="record">
  <h2>What a primary page supports</h2>
  <p>In the 7 May 2025 transcript she is in the room as the product person. She states the $6 external figure, argues for a snappy thorough tool, and describes permission controls. The transcript also has her on compaction weakening intent in long chats. The Latent Space wiki adds a later title, Head of Product, Claude Code, tied to a May 2026 conference listing. That wiki page says review was still pending, so the title is secondary.</p>
  <p>She is not given a personal token total. She does not publish a CLAUDE.md in the pages opened here. The useful move she does describe is incremental automation: one test, then ten, then look at the failures, which the wiki summarizes from the interview. Prefer the timestamped transcript when the two differ.</p>
  <p><a href="talks.html#ls-may">Talk notes</a> · <a href="https://latent.space/wiki/cat-wu/">Wiki</a></p>
</section>
"""
    (ROOT / "cat-wu.html").write_text(page(
        "Cat Wu: Power User Hub",
        "Profile",
        "Cat Wu, on product limits, cost, and who gets to merge.",
        "A short profile from the May 2025 Latent Space transcript and the Latent Space wiki. No private workflow was invented.",
        cat_body,
        "Source-backed profile of Cat Wu.",
    ), encoding="utf-8")

    res = resources(rows)
    (ROOT / "data" / "directory.json").write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    dir_body = visual(
        "One card per URL. Echoes share a URL and stack on the same card.",
        """flowchart LR
  A[Claim rows] --> B[Group by URL]
  B --> C[Filter by kind and cluster]""",
        "Directory shelves.",
        """# Directory
## official
## talk
## repo
## reddit
## article
""",
    ) + """
<section class="section" id="browse">
  <h2>Browse</h2>
  <div class="filters">
    <label>Kind <select id="kind"><option value="">All</option><option>official</option><option>talk</option><option>repo</option><option>reddit</option><option>article</option></select></label>
    <label>Cluster <select id="dcluster"><option value="">All</option></select></label>
    <input id="dirfilter" type="search" placeholder="Filter title or author">
    <span id="dcount" class="muted"></span>
  </div>
  <div id="directory" class="stack"></div>
</section>
<script>
window.DIR = """ + json.dumps(res) + """;
</script>
"""
    html = page(
        "Directory: Power User Hub",
        "Niche shelf",
        "Every URL in the ledger, once.",
        "Filter by kind and cluster. Reddit cards point at reddit.com even though that host blocked the link checker. The post ids were checked against the Arctic Shift file.",
        dir_body,
        "Filterable directory of sources used in the power user hub.",
    )
    # directory page needs extra script before site.js. The template already closes body.
    # Inject a small runner before site.js by replacing the script tag once.
    html = html.replace(
        '<script src="js/claims.js"></script>',
        """<script>
document.addEventListener('DOMContentLoaded', function () {
  var rows = window.DIR || [];
  var cluster = document.getElementById('dcluster');
  var kinds = {};
  rows.forEach(function (r) { kinds[r.cluster] = 1; });
  Object.keys(kinds).sort().forEach(function (name) {
    var opt = document.createElement('option');
    opt.value = name; opt.textContent = name; cluster.appendChild(opt);
  });
  function paint() {
    var k = document.getElementById('kind').value;
    var c = cluster.value;
    var q = (document.getElementById('dirfilter').value || '').toLowerCase();
    var shown = rows.filter(function (r) {
      if (k && r.kind !== k) return false;
      if (c && r.cluster !== c) return false;
      var blob = (r.title + ' ' + r.author + ' ' + r.url).toLowerCase();
      if (q && blob.indexOf(q) === -1) return false;
      return true;
    });
    document.getElementById('dcount').textContent = shown.length + ' sources';
    document.getElementById('directory').innerHTML = shown.map(function (r) {
      return '<article class="card"><p class="kicker">' + r.kind + ' · ' + r.cluster + ' · ' + r.claims + ' claims</p><h3><a href="' + r.url + '">' + r.title + '</a></h3><p>' + r.author + ' · ' + r.date + '</p></article>';
    }).join('');
  }
  document.getElementById('kind').addEventListener('change', paint);
  cluster.addEventListener('change', paint);
  document.getElementById('dirfilter').addEventListener('input', paint);
  paint();
});
</script>
<script src="js/claims.js"></script>""",
    )
    (ROOT / "directory.html").write_text(html, encoding="utf-8")


def patch_existing(n: int) -> None:
    for path in ROOT.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        if OLD_NAV in text and "method.html" not in text.split("nav", 1)[-1][:800]:
            text = text.replace(OLD_NAV, NAV)
        text = text.replace(
            "52 rows. The same data",
            f"{n} rows. The same data",
        )
        path.write_text(text, encoding="utf-8")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if "method.html" not in index.split("<main", 1)[-1][:2500]:
        index = index.replace(
            '<section class="section" id="dashboard">',
            '''<section class="section" id="pass2">
  <h2>Pass 2 is the inner dolls</h2>
  <p>Official docs were pass 1. Pass 2 opens transcripts, a lab study, GitHub files, and an r/ClaudeAI archive. Start at the <a href="method.html">method</a>, the <a href="tokens.html">token finding</a>, or the <a href="directory.html">directory</a>.</p>
</section>
<section class="section" id="dashboard">''',
        )
        (ROOT / "index.html").write_text(index, encoding="utf-8")
    profiles = (ROOT / "profiles.html").read_text(encoding="utf-8")
    if "cat-wu.html" not in profiles:
        profiles = profiles.replace(
            '<section class="section" id="missing">',
            '''<section class="section" id="cat">
  <h2>Added in pass 2</h2>
  <p><a href="cat-wu.html">Cat Wu</a> now has a page from the May 2025 transcript. <a href="talks.html">Talk notes</a> cover that episode and Thariq Shihipar. Mayank Shah, Codie Sanchez, and Greg Isenberg are still thin: see the gap report.</p>
</section>
<section class="section" id="missing">''',
        )
        (ROOT / "profiles.html").write_text(profiles, encoding="utf-8")
    gaps = (ROOT / "gaps.html").read_text(encoding="utf-8")
    if 'id="g18"' not in gaps:
        gaps = gaps.replace(
            '<section class="section" id="review">',
            '''<section class="section" id="g18">
  <h2>G18. Pass 2 holes</h2>
  <ul class="clean">
    <li>yt-dlp could not download YouTube auto-captions: the site asked for a sign-in. One interview's page text was kept and marked medium confidence because it has no speaker labels.</li>
    <li>reddit.com JSON returned 403. Only an Arctic Shift slice of r/ClaudeAI produced posts. r/ClaudeCode, r/cursor, r/LocalLLaMA, and the other named subs did not.</li>
    <li>X threads were not pulled in bulk. The 2 Jan 2026 Boris mirror from pass 1 is still the X-adjacent item.</li>
    <li>Dwarkesh, Lenny, Lex, No Priors, Changelog, and Cognitive Revolution were not transcribed.</li>
    <li>Codie Sanchez still has no first-party essay in the opened set. Mayank Shah is still three possible people. Greg Isenberg's opened page is a 17 Mar 2026 beginner guide, not a lab workflow.</li>
    <li>A Dealroom line about billions of tokens was seen in search and not fetched, so it is not a claim.</li>
  </ul>
</section>
<section class="section" id="review">''',
        )
        (ROOT / "gaps.html").write_text(gaps, encoding="utf-8")
    catalog = (ROOT / "js" / "catalog.js").read_text(encoding="utf-8")
    if "method.html" not in catalog:
        catalog = catalog.replace(
            "];",
            """  {href:"method.html", cluster:"method", title:"Research method", text:"Russian doll layers and where new sources stopped adding claims."},
  {href:"tokens.html", cluster:"tokens", title:"Token use", text:"5 to 10 thousand tokens a day was not found. Six dollars a day, free internal use, parallel sessions."},
  {href:"talks.html", cluster:"talks", title:"Talks", text:"Latent Space with Boris Cherny, Cat Wu, and Thariq Shihipar, with timestamps."},
  {href:"directory.html", cluster:"library", title:"Source directory", text:"One card per URL, filterable by kind and cluster."},
  {href:"reddit-field.html", cluster:"reddit", title:"Reddit field notes", text:"Arctic Shift slice of r/ClaudeAI. Other subs did not return."},
  {href:"cat-wu.html", cluster:"people", title:"Cat Wu", text:"Product lead notes from the May 2025 transcript and a secondary wiki."},
];""",
        )
        (ROOT / "js" / "catalog.js").write_text(catalog, encoding="utf-8")


def main() -> None:
    existing = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    # If re-run, drop previous pass2 ids so we do not duplicate.
    existing = [row for row in existing if int(row["id"][1:]) < 53]
    rows = merge(existing, load_new())
    for row in rows:
        for key in ("claim", "notes", "source_title", "author"):
            row[key] = clean(row[key])
    write_ledger(rows)
    build_pages(rows)
    patch_existing(len(rows))
    print(f"ledger {len(rows)} claims")


if __name__ == "__main__":
    main()
