#!/usr/bin/env python3
"""Insert a sequence diagram and a state diagram into every hub page."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = {
"index.html": (
"sequenceDiagram\n  participant Reader\n  participant Page\n  participant Ledger\n  Reader->>Page: open a walkthrough\n  Page->>Ledger: claim id\n  Ledger-->>Reader: URL and date",
"stateDiagram-v2\n  [*] --> Unchecked\n  Unchecked --> Kept: page opened\n  Unchecked --> Gap: page not opened\n  Kept --> [*]",
),
"claude.html": (
"sequenceDiagram\n  participant You\n  participant Test\n  participant Skill\n  You->>Test: run the red command\n  Test-->>You: assertion failure\n  You->>Skill: paste the failure\n  Skill-->>You: no production diff yet",
"stateDiagram-v2\n  [*] --> Red\n  Red --> Green: smallest change\n  Green --> Review: person reads diff\n  Review --> [*]",
),
"codex.html": (
"sequenceDiagram\n  participant You\n  participant Config\n  participant Codex\n  You->>Config: sandbox read only\n  Config->>Codex: AGENTS.md under 32 KiB\n  Codex-->>You: quotes the test command\n  You->>You: git status clean",
"stateDiagram-v2\n  [*] --> ReadOnly\n  ReadOnly --> Approval: edit requested\n  Approval --> ReadOnly: you decline\n  Approval --> Diff: you allow one directory",
),
"gemini.html": (
"sequenceDiagram\n  participant You\n  participant Neon\n  participant Hydrogen\n  You->>Neon: one task\n  Neon->>Hydrogen: implement the plan\n  You->>Hydrogen: slash btw is read only\n  Hydrogen-->>You: diff to read",
"stateDiagram-v2\n  [*] --> OneCommand\n  OneCommand --> Swarm: slices do not share files\n  OneCommand --> SideQuestion: read only\n  Swarm --> Diff\n  SideQuestion --> Diff",
),
"muse.html": (
"sequenceDiagram\n  participant You\n  participant Muse\n  You->>Muse: contributor mode off\n  You->>Muse: slash plan\n  Muse-->>You: plan quotes the test\n  You->>Muse: approve or stop",
"stateDiagram-v2\n  [*] --> TrainingOff\n  TrainingOff --> PlanGate\n  PlanGate --> Grill: plan is soft\n  PlanGate --> Goal: plan names the test\n  Goal --> [*]",
),
"grok.html": (
"sequenceDiagram\n  participant You\n  participant Bot\n  participant Mail\n  You->>Bot: read may run\n  You->>Bot: send needs approval\n  Bot->>Mail: draft only\n  Mail-->>You: you send or you do not",
"stateDiagram-v2\n  [*] --> Connected\n  Connected --> Draft\n  Draft --> Waiting: send is needs approval\n  Waiting --> Skipped: sign in died\n  Waiting --> [*]",
),
"cross-cutting.html": (
"sequenceDiagram\n  participant You\n  participant File\n  participant Tool\n  You->>File: same test command\n  File->>Tool: Claude or Codex or Gemini or Muse\n  Tool-->>You: one diff\n  You->>You: read git diff",
"stateDiagram-v2\n  [*] --> OneCommand\n  OneCommand --> OneTool\n  OneTool --> Diff\n  Diff --> [*]",
),
"principles.html": (
"sequenceDiagram\n  participant You\n  participant File\n  participant Hook\n  You->>You: same correction twice\n  You->>Hook: if a command can check it\n  You->>File: otherwise one line\n  File-->>You: next session loads it",
"stateDiagram-v2\n  [*] --> Repeated\n  Repeated --> Hook: command exists\n  Repeated --> OneLine: no command\n  Hook --> [*]\n  OneLine --> [*]",
),
"prompts.html": (
"sequenceDiagram\n  participant You\n  participant Prompt\n  participant Test\n  You->>Prompt: fill TEST_COMMAND\n  You->>Test: run the red command\n  Test-->>Prompt: paste the failure\n  Prompt-->>You: first reply has no production diff",
"stateDiagram-v2\n  [*] --> Blank\n  Blank --> Filled\n  Filled --> Red\n  Red --> Kept: reply names the command\n  Red --> Rejected: reply edits first",
),
"profiles.html": (
"sequenceDiagram\n  participant Source\n  participant You\n  participant Kit\n  Source->>You: file or command\n  You->>Kit: copy with SHA\n  Source-->>You: no file\n  You->>You: gap report",
"stateDiagram-v2\n  [*] --> Primary\n  Primary --> Kit: verbatim file\n  Primary --> Gap: no file\n  Kit --> [*]",
),
"tokens.html": (
"sequenceDiagram\n  participant Claim\n  participant Source\n  Claim->>Source: 5 to 10k tokens a day\n  Source-->>Claim: not in the opened pages\n  Source-->>Claim: dollars and sample sizes are",
"stateDiagram-v2\n  [*] --> Unsourced\n  Unsourced --> Rejected: no page\n  Unsourced --> Kept: speaker and date\n  Kept --> [*]",
),
"method.html": (
"sequenceDiagram\n  participant Search\n  participant Page\n  participant Ledger\n  Search->>Page: open the origin\n  Page->>Ledger: one row\n  Page-->>Search: not opened\n  Search->>Ledger: gap id",
"stateDiagram-v2\n  [*] --> Searching\n  Searching --> Row: page read\n  Searching --> Gap: blocked\n  Row --> [*]",
),
"sources.html": (
"sequenceDiagram\n  participant Row\n  participant URL\n  participant Reader\n  Row->>URL: origin link\n  Reader->>URL: open it\n  URL-->>Reader: primary or secondary or echo",
"stateDiagram-v2\n  [*] --> Primary\n  Primary --> Secondary: retelling\n  Primary --> Echo: news repeat\n  Secondary --> [*]",
),
"gaps.html": (
"sequenceDiagram\n  participant Search\n  participant Page\n  participant Gap\n  Search->>Page: try the URL\n  Page-->>Gap: 403 or 422 or consent wall\n  Gap-->>Search: stays unknown",
"stateDiagram-v2\n  [*] --> Tried\n  Tried --> Open: text captured\n  Tried --> Closed: could not open\n  Closed --> [*]",
),
"cat-wu.html": (
"sequenceDiagram\n  participant Mirror\n  participant Cat\n  participant Page\n  Mirror->>Cat: about 14 minutes 48\n  Cat-->>Page: about 6 dollars a day\n  Page-->>Page: May 2025, outside the window",
"stateDiagram-v2\n  [*] --> Interview\n  Interview --> Cited: timestamp named\n  Interview --> Held: no speaker label\n  Cited --> [*]",
),
"talks.html": (
"sequenceDiagram\n  participant Episode\n  participant Mirror\n  participant Page\n  Episode->>Mirror: transcript or page text\n  Mirror->>Page: timestamp\n  Page-->>Episode: captions not downloaded",
"stateDiagram-v2\n  [*] --> Listed\n  Listed --> Timestamped: text opened\n  Listed --> Gap: no captions\n  Timestamped --> [*]",
),
"podcasts.html": (
"sequenceDiagram\n  participant Show\n  participant Notes\n  participant Kit\n  Show->>Notes: official page\n  Notes->>Kit: one prompt file\n  Show-->>Notes: transcript not opened",
"stateDiagram-v2\n  [*] --> Named\n  Named --> Walkthrough: text opened\n  Named --> NotOpened: no transcript\n  Walkthrough --> [*]",
),
"podcast-pragmatic-boris.html": (
"sequenceDiagram\n  participant Boris\n  participant Plan\n  participant Checkout\n  Boris->>Plan: Shift Tab twice\n  Plan-->>Boris: plan he accepts\n  Boris->>Checkout: separate trees\n  Checkout-->>Boris: one diff to read",
"stateDiagram-v2\n  [*] --> PlanMode\n  PlanMode --> Implement: plan accepted\n  Implement --> Review\n  Review --> [*]",
),
"podcast-thariq.html": (
"sequenceDiagram\n  participant Thariq\n  participant Session\n  participant File\n  Thariq->>Session: start with no CLAUDE.md\n  Session-->>Thariq: same failure twice\n  Thariq->>File: add one line",
"stateDiagram-v2\n  [*] --> EmptyFile\n  EmptyFile --> Repeated\n  Repeated --> OneLine\n  OneLine --> [*]",
),
"podcast-karpathy.html": (
"sequenceDiagram\n  participant Karpathy\n  participant Loop\n  participant Metric\n  Karpathy->>Metric: command that scores the run\n  Metric-->>Loop: stay overnight\n  Metric-->>Karpathy: no score, stay in the loop",
"stateDiagram-v2\n  [*] --> InLoop\n  InLoop --> Overnight: metric exists\n  InLoop --> Switch: quota ends\n  Overnight --> [*]",
),
"podcast-practical-ai-352.html": (
"sequenceDiagram\n  participant Hosts\n  participant Command\n  participant Note\n  Hosts->>Command: run it\n  Command-->>Note: exit 0\n  Note-->>Hosts: only then write the line",
"stateDiagram-v2\n  [*] --> Ran\n  Ran --> Write: exit 0\n  Ran --> Skip: exit not 0\n  Write --> [*]",
),
"reddit-field.html": (
"sequenceDiagram\n  participant Archive\n  participant Post\n  participant Ledger\n  Archive->>Post: r/ClaudeAI selftext\n  Post->>Ledger: medium confidence\n  Archive-->>Ledger: other subs returned 422",
"stateDiagram-v2\n  [*] --> Archived\n  Archived --> Claim: selftext matched\n  Archived --> Gap: 422\n  Claim --> [*]",
),
"repos.html": (
"sequenceDiagram\n  participant README\n  participant You\n  participant Tree\n  README->>You: install line and SHA\n  You->>Tree: copy one skill\n  Tree-->>You: do not install three routers",
"stateDiagram-v2\n  [*] --> Readme\n  Readme --> Installed: one system\n  Readme --> Skipped: mandatory clash\n  Installed --> [*]",
),
"library.html": (
"sequenceDiagram\n  participant Cluster\n  participant URL\n  participant Reader\n  Cluster->>URL: origin first\n  URL-->>Reader: echo is not a second measure",
"stateDiagram-v2\n  [*] --> Official\n  Official --> Repo\n  Official --> Echo\n  Repo --> [*]",
),
"directory.html": (
"sequenceDiagram\n  participant Reader\n  participant Filter\n  participant Card\n  Reader->>Filter: kind or cluster\n  Filter->>Card: matching URL\n  Card-->>Reader: open the origin",
"stateDiagram-v2\n  [*] --> All\n  All --> Filtered\n  Filtered --> Opened\n  Opened --> [*]",
),
"search.html": (
"sequenceDiagram\n  participant Reader\n  participant Index\n  participant Page\n  Reader->>Index: query\n  Index->>Page: title and blurb\n  Page-->>Reader: the walkthrough",
"stateDiagram-v2\n  [*] --> Idle\n  Idle --> Hits: query\n  Hits --> Page\n  Page --> [*]",
),
}


def block(seq: str, state: str) -> str:
    return f"""
<section class="section" id="seq-state">
  <h2>Sequence and state</h2>
  <div class="visual-grid">
    <figure class="diagram">
      <figcaption>Who talks to whom. This is a map of the page, not a vendor diagram.</figcaption>
      <pre class="mermaid">{seq}</pre>
    </figure>
    <figure class="diagram">
      <figcaption>States worth naming before you run a tool.</figcaption>
      <pre class="mermaid">{state}</pre>
    </figure>
  </div>
</section>
"""


def main() -> None:
    missing = []
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if 'id="seq-state"' in text:
            print("already", path.name)
            continue
        pair = DIAGRAMS.get(path.name)
        if not pair:
            missing.append(path.name)
            continue
        if "</section>" not in text:
            missing.append(path.name + " no section")
            continue
        text = text.replace("</section>", "</section>\n" + block(*pair), 1)
        path.write_text(text, encoding="utf-8")
        print("added", path.name)
    if missing:
        raise SystemExit("missing diagrams for " + ", ".join(missing))


if __name__ == "__main__":
    main()
