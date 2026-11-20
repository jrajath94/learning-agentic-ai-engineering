#!/usr/bin/env python3
"""V5 visuals for deep pages: flow SVG + mermaid + markmap. Fonts and local
mermaid script already present via the niche shell."""
import os, re, html, glob

src = open(os.path.expanduser("~/workspace/learning-agentic-site/build_v3.py")).read().splitlines()
prefix = "\n".join(src[:200])
g = {}
exec(prefix, g)
make_svg, markmap_html = g["make_svg"], g["markmap_html"]
OUT = g["OUT"]

VIS = {
"deep.html": dict(nodes=["Pick one system","Run its checklist","Log the learning","Next system"],
 mermaid="flowchart LR\n A[Deep index] --> B[One deep page]\n B --> C[Checklist on a live task]\n C --> D[Learning logged]\n D --> B",
 mark=[("Builders",[("Reed, Hashimoto, Ronacher"),("Yan code level")]),("Fleets",[("Cherny, Gas Town"),("Tan roster")]),("Systems",[("OpenAI harness"),("Anthropic swarm"),("Mods and evals")])]),
"deep-reed.html": dict(nodes=["Idea talk","spec.md","prompt_plan.md","todo.md state"],
 mermaid="flowchart LR\n A[Idea] --> B[One question at a time]\n B --> C[spec.md]\n C --> D[prompt_plan.md]\n D --> E[One prompt per step]\n E --> F[todo.md check]\n F -->|stuck| G[repomix pack to fresh chat]\n G --> E",
 mark=[("Files",[("spec.md"),("prompt_plan.md"),("todo.md"),("output.txt pack")]),("Modes",[("Pair mode"),("Agent mode"),("Brownfield mise tasks")]),("Rules",[("No orphan code"),("One prompt at a time")])]),
"deep-hashimoto.html": dict(nodes=["Reproduce own work","End of day starts","Morning filter","Harness fix per error"],
 mermaid="flowchart TD\n A[Last 30 min of day] --> B[Surveys, probes, triage]\n B --> C[Reports by morning]\n C --> D{Slam dunk?}\n D -->|yes| E[Background run, alerts off]\n D -->|no| F[Drop]\n E --> G[Error becomes rule or tool]\n G --> A",
 mark=[("Six steps",[("Agent not chat"),("Reproduce work"),("End of day"),("Slam dunks"),("Harness"),("One agent running")]),("Ghostty file",[("Commands"),("Scoped rules"),("Map"),("Prohibitions")]),("Time",[("30 min starts"),("Morning filter")])]),
"deep-ball.html": dict(nodes=["Ship","Scheduled wake","Proof artifact","Revert or keep"],
 mermaid="flowchart LR\n A[Ship change] --> B[Agent wakes on schedule]\n B --> C[Check deploy, errors, behavior]\n C --> D{Proof holds?}\n D -->|yes| E[Keep]\n D -->|no| F[Revert with report]",
 mark=[("Access",[("Deploys and CI"),("Logs and metrics"),("Feature flags")]),("Machines",[("Orbs, throwaway"),("Runners, stateful")]),("Tests",[("Proof demand"),("Instruction eval, 5 to 10 fresh")])]),
"deep-gastown.html": dict(nodes=["Mayor takes goal","Convoy and beads","Polecats run hooks","Refinery merges"],
 mermaid="flowchart TD\n A[Human goal] --> B[Mayor]\n B --> C[Convoy of beads]\n C --> D[Polecats on hooks]\n D --> E[Witness watch]\n E --> F[Refinery gates]\n F --> G[Merge to main]\n B --> H[Deacon patrol]\n H --> E",
 mark=[("Roles",[("Mayor"),("Witness"),("Deacon and Dogs"),("Refinery")]),("Data",[("Beads ledger"),("Hooks in worktrees"),("Formulas in TOML")]),("Lite form",[("Ledger file"),("One merge at a time"),("Patrol scan")])]),
"deep-litt.html": dict(nodes=["Primary work, human","Secondary work, agent","Explainer page","Quiz gate"],
 mermaid="flowchart LR\n A[Change lands] --> B[Explain diff page]\n B --> C[Background, intuition, code]\n C --> D[Five question quiz]\n D -->|pass| E[Ship]\n D -->|fail| F[Fix explainer, retest]\n F --> D",
 mark=[("Surgeon split",[("Guide and spike"),("Spec fixes"),("Docs")]),("Explainer",[("Background"),("Intuition"),("Code"),("Quiz")]),("Gate",[("Read before diff"),("Pass before ship")])]),
"deep-ronacher.html": dict(nodes=["Fast friendly tools","One log file","Segmented state","Parallel agents"],
 mermaid="flowchart LR\n A[make dev] --> B[Services plus pidfile]\n B --> C[One log file]\n C --> D[Agent reads log]\n D --> E[Sign in link, errors, proof]\n E --> F[Fix in loop]",
 mark=[("Setup",[("Yolo alias in Docker"),("Near zero MCP"),("psql for data")]),("Stack",[("Go backends"),("Python with care"),("Tailwind and Vite")]),("Style",[("Dumb code wins"),("Long clear names"),("Plain SQL")])]),
"deep-yan.html": dict(nodes=["feeds.txt","Split in three","Sub agents process","Merge to one file"],
 mermaid="flowchart TD\n A[Main agent reads feeds.txt] --> B[Chunk 1]\n A --> C[Chunk 2]\n A --> D[Chunk 3]\n B --> E[Part files]\n C --> E\n D --> E\n E --> F[main-summary.md]",
 mark=[("Tools",[("FastMCP per feed"),("Errors as strings"),("10 second timeout")]),("Files",[("Main instructions"),("Sub instructions"),("Two templates")]),("Run",[("124 items"),("42 categories")])]),
"deep-cherny.html": dict(nodes=["Plan mode","Fleet in worktrees","Verify subagent","Rule file update"],
 mermaid="flowchart TD\n A[Plan mode] --> B[Plan holds]\n B --> C[Auto accept build]\n C --> D[Verify: tests, browser]\n D -->|fail| A\n D -->|pass| E[Simplify pass]\n E --> F[Lesson to CLAUDE.md]",
 mark=[("Fleet",[("5 terminal plus 5 to 10 web"),("Worktrees za zb zc"),("Phone starts")]),("Files",[("Shared CLAUDE.md"),("Commands in git"),("Permissions shared")]),("Doctrines",[("Verification first"),("Ablation each 6 months"),("Hard tasks, exit rules")])]),
"deep-openai-harness.html": dict(nodes=["Map rule file","Docs of record","Self review loop","Doc care agent"],
 mermaid="flowchart LR\n A[Prompt] --> B[Agent opens PR]\n B --> C[Self review]\n C --> D[Named agent reviews]\n D -->|notes| C\n D -->|all pass| E[Merge]\n F[Doc care scan] --> G[Fix PRs for stale docs]",
 mark=[("Docs",[("Design index"),("Architecture and layers"),("Quality grades"),("Plans as files")]),("Layer law",[("Types to UI, one way"),("Providers for cross cuts")]),("Entropy",[("Golden principles"),("Drift scan PRs")])]),
"deep-anthropic.html": dict(nodes=["Lead plans","Sub agents search","Judge scores","Lock file claims"],
 mermaid="flowchart TD\n A[Lead agent] --> B[Sub agent 1]\n A --> C[Sub agent 2]\n A --> D[Sub agent 3]\n B --> E[Compressed returns]\n C --> E\n D --> E\n E --> F[Lead synthesis]\n F --> G[Judge: 5 criteria]",
 mark=[("Swarm",[("8 principles"),("90.2 percent eval gain"),("Near 15x tokens")]),("Best practice",[("Short rule file"),("Check ladder"),("Five unattended answers")]),("Compiler",[("16 agents"),("Lock files"),("GCC oracle bisect")])]),
"deep-repos.html": dict(nodes=["Stub entry skill","Discipline skill","Two stage review","Measured claims"],
 mermaid="flowchart LR\n A[User invokes stub] --> B[Discipline skill runs]\n B --> C[Work at agreed seams]\n C --> D[Review: spec fit]\n D --> E[Review: quality]\n E --> F[Commit]",
 mark=[("Pocock",[("27 skills, two classes"),("Grill pair"),("Diagnosing loop")]),("Superpowers",[("Mandatory loop"),("2 to 5 minute tasks"),("TDD deletes early code")]),("Caveman",[("Voice rules"),("Input compression"),("Vendor figures, test self")])]),
"deep-podcasts.html": dict(nodes=["Plan with research","Work from plan","Assess by personas","Compound learnings"],
 mermaid="flowchart LR\n A[Plan: 3 research passes] --> B[Spec flow walk]\n B --> C[Work: clear session, plan in]\n C --> D[Assess: personas, P1 to P3]\n D --> E[Triage by human]\n E --> F[Compound: learnings files]\n F --> A",
 mark=[("Compound",[("Plan, work, assess, compound"),("Learnings with front matter")]),("Cora",[("Voice to issue"),("Five part issue"),("Prompt evals")]),("Capsule",[("Figma map to PRD"),("Sibling repo build")])]),
"deep-tan.html": dict(nodes=["Goal named","Process dump by voice","Bot restates","Routine trigger"],
 mermaid="flowchart LR\n A[Name the goal] --> B[Brain dump the process]\n B --> C[Bot restates both]\n C -->|wrong| B\n C -->|right| D[Routine runs]\n D --> E[Runtime verification]\n E --> F[Blind eval check]",
 mark=[("Roster",[("1 chief of staff"),("3 managers"),("11 execution")]),("Safety",[("Runtime verification"),("Blind evals"),("Anti jobs named")]),("Flags",[("Self reported counts"),("Sanchez score at pipeline value")])]),
"deep-mods-evals.html": dict(nodes=["Watcher with trigger","Fork and verdict","Error read by hand","Judge after labels"],
 mermaid="flowchart TD\n A[Turn edits files or 8 plus calls] --> B[Supervisor forks]\n B --> C[Verdict: concerns plus next step]\n C --> D{Human acts}\n E[20 to 50 traces read] --> F[Failure modes named]\n F --> G[Binary labels]\n G --> H[Judge prompt validated]",
 mark=[("Mods",[("Middleware in the harness"),("Six built in"),("Not sandboxed")]),("Supervisor",[("99 of 111 turns fired"),("5 to 6k tokens per check")]),("Hamel",[("Error analysis first"),("Binary, no scales"),("Guardrail vs evaluator")])]),
}

count = 0
for fname, v in VIS.items():
    path = os.path.join(OUT, fname)
    t = open(path).read()
    if "assets/img/" in t:
        print("skip", fname); continue
    slug = fname.replace(".html", "")
    tm = re.search(r"<h1>(.*?)</h1>", t, re.S)
    title = re.sub(r"<[^>]+>", "", tm.group(1)).strip() if tm else slug
    img_rel = make_svg(slug, v["nodes"], title)
    figure = (f'\n<figure class="visual"><img src="{img_rel}" alt="Flow diagram: {html.escape(", ".join(v["nodes"]))}">'
              f'<figcaption>Figure 1. {html.escape(title)} as a flow. Each box names one stage on this page. Arrows show work order.</figcaption></figure>\n')
    t2, n = re.subn(r'(<p class="lede">.*?</p>)', r"\1" + figure, t, count=1, flags=re.S)
    if n == 0:
        t2, n = re.subn(r'(<h1>.*?</h1>)', r"\1" + figure, t, count=1, flags=re.S)
    t = t2
    section = f"""
<h2>Visual map of this page</h2>
<p>Two views of one page: a Mermaid flow for work order, rendered by the local Mermaid library in this folder, and a markmap for concept groups.</p>
<div class="mermaid">
{v["mermaid"]}
</div>
<details class="mermaid-src"><summary>Mermaid source, for offline read</summary><pre>{html.escape(v["mermaid"])}</pre></details>
<div class="readguide"><p>How to read the flow diagram. Step 1: start at the first box. Step 2: follow each arrow to the next stage. Step 3: at a branch box, read both paths before a choice. Step 4: a loop arrow means work returns for one more pass vs a test.</p></div>
<h3>Markmap: concepts on this page</h3>
{markmap_html(title, v["mark"])}
"""
    t = t.replace("</main>", section + "</main>")
    open(path, "w").write(t)
    count += 1
print("v5 visuals applied", count)
