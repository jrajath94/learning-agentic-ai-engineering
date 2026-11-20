#!/usr/bin/env python3
"""V6: social sweep page, templates folder, 3 more prompt files, screen figures."""
import os, re

BASE = os.path.expanduser("~/workspace/learning-agentic-site")
OUT = os.path.join(BASE, "site")
TPL = os.path.join(BASE, "templates")
os.makedirs(TPL, exist_ok=True)
IMG = os.path.join(OUT, "assets", "img")
os.makedirs(IMG, exist_ok=True)

shell = open(os.path.join(OUT, "niche.html")).read()
head = shell.split("<main>")[0]
head = re.sub(r"<title>.*?</title>", "<title>PLACEHOLDER</title>", head)
foot = "</main>" + shell.split("</main>", 1)[1]

def page(fname, title, lede, body):
    h = head.replace("PLACEHOLDER", title + " | Learning Agentic AI Engineering")
    main = f"""<main>
<p class="meta">Home / Social Sweep / {title}</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>
{body}
</main>
"""
    open(os.path.join(OUT, fname), "w").write(h + main + foot)
    print("page", fname)

def steps(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def pre(text):
    return "<pre>" + text.replace("&","&amp;").replace("<","&lt;") + "</pre>"

# ---------- screen style figures (diagrams drawn from source descriptions) ----------
def screen_svg(fname, title, lines, caption):
    rows = ""
    y = 64
    for txt, color in lines:
        rows += f'<text x="28" y="{y}" font-family="monospace" font-size="15" fill="{color}">{txt}</text>'
        y += 26
    h = y + 18
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{h}" viewBox="0 0 860 {h}">
<rect width="860" height="{h}" fill="#0a0a0a"/>
<rect width="860" height="34" fill="#171713"/>
<circle cx="20" cy="17" r="6" fill="#3a3a32"/><circle cx="42" cy="17" r="6" fill="#3a3a32"/><circle cx="64" cy="17" r="6" fill="#e8a04c"/>
<text x="86" y="22" font-family="monospace" font-size="13" fill="#b9b2a4">{title}</text>
{rows}
</svg>'''
    open(os.path.join(IMG, fname), "w").write(svg)
    return f'<figure class="visual"><img src="assets/img/{fname}" alt="{caption}"><figcaption>{caption}</figcaption></figure>'

fleet_fig = screen_svg("screen-fleet.svg", "terminal: five named tabs, one task each",
 [("tab 1  auth-refactor      plan approved, building", "#f4f1ea"),
  ("tab 2  billing-fix        verify: tests running", "#f4f1ea"),
  ("tab 3  docs-sweep         sub agents: 3 running", "#b9b2a4"),
  ("tab 4  analysis           BigQuery pull, idle wait", "#b9b2a4"),
  ("tab 5  review-queue       2 PRs wait for quiz gate", "#e8a04c"),
  ("notify: tab 2 check failed, plan mode re-entry", "#e8a04c")],
 "Figure. Screen diagram of the Cherny fleet layout, drawn from the thread description: five numbered terminal tabs, one task per tab, system notices on tab events. A layout diagram, not a capture of his machine.")
town_fig = screen_svg("screen-town.svg", "gt feed: town states at one patrol pass",
 [("gt-abc12  checkout-rework    Working    polecat-3", "#f4f1ea"),
  ("gt-def34  test-repair        GUPP Violation, nudged", "#e8a04c"),
  ("hq-x7k2m  docs-garden        Working    polecat-7", "#f4f1ea"),
  ("gt-jkl56  merge-queue        Gated, Refinery holds", "#b9b2a4"),
  ("gt-mno78  stale-probe        Zombie, restart queued", "#e8a04c"),
  ("Deacon patrol: 5 rigs scanned, 2 acts taken", "#b9b2a4")],
 "Figure. Screen diagram of a Gas Town feed view, drawn from the README state names: Working, GUPP Violation, Stalled, Zombie, Idle. A layout diagram, not a capture of a live town.")

# insert figures into deep pages
p = os.path.join(OUT, "deep-cherny.html"); t = open(p).read()
t = t.replace("<h2>Thread 2: team tips, from compilations</h2>", fleet_fig + "\n<h2>Thread 2: team tips, from compilations</h2>", 1)
open(p, "w").write(t)
p = os.path.join(OUT, "deep-gastown.html"); t = open(p).read()
t = t.replace("<h2>Formulas: workflows as TOML</h2>", town_fig + "\n<h2>Formulas: workflows as TOML</h2>", 1)
open(p, "w").write(t)
print("screen figures inserted")

# ---------- social page ----------
page("social.html", "Social Sweep: the Viral Layer, Checked vs Primary Sources",
"Instagram, Threads, and Facebook swept on 20 November 2026 for agent workflow posts: 120 posts pulled, the top workflow items read as summaries by the platform index. Each viral pattern gets a verdict vs the primary sources in the deep pages. TikTok stands as an open gap, with the reason named.",
"""<h2>What the viral layer repeats</h2>
<p>One fact dominates the sweep: the most shared workflow content on social platforms recirculates the primary sources in this guide. A six slide carousel of Cherny tips holds 22,000 likes. A Facebook copy of the same carousel holds 890. A reel that walks his setup holds 3,500. The primary thread holds the detail; the copies hold the reach. Read the copies for what the crowd values, and the primary text for what to do.</p>
<h2>Pattern table: viral claim vs primary record</h2>
""" + pre("""Pattern (top social form)        Primary verdict
Omega setup: top model as         Real shape, creator grade.
orchestrator, cheap sub agents,   Matches Anthropic swarm design
verify loops, compact at 40 to    and Cherny fleet. The self
60 percent, self rewriting        rewriting skills part has no
skills (reel, 4.7K likes)         primary backing. Risk: a skill
                                  that edits itself breaks the
                                  audit trail. Use versioned
                                  skills with human review.

5 levels ladder: Prompt 2x,       A teaching frame, not a source
Skill 5x, Skill Chain 10x,        claim. The order matches the
Agent 20x, Agent Team 50x         guide path: prompts, skills,
(carousel, 19K likes)             agents, teams. The multipliers
                                  are marketing numbers. No
                                  primary source states them.

Loop, goal, schedule trio         Real commands, per the current
for unattended runs               best practice doc on the
(reel, 5.2K likes)                Anthropic deep page. The reel
                                  adds no limits. The doc adds
                                  the five unattended answers
                                  and stop caps. Use the doc.

Model pick by task tier           Real practice. Cherny and the
(reel, 17K likes)                 swarm post both set cheap
                                  models for sub agents and the
                                  top model for lead work.

Dynamic Workflows explainers      Real feature class. The YC
(2 reels, 8.5K and 1.4K)          talk names the trigger words
                                  and the fan out, verify, fan
                                  out shape. Social adds reach,
                                  no new mechanics.

Memory file warnings              Real risk, named in the round
(reel, 1.7K likes)                3 Reddit discipline thread:
                                  resident rule files tax each
                                  turn and rot per model era.
                                  Keep only earned lines.

5 agents, 0 staff, night          Existence grade only: one reel,
shift business (reel, low         69 likes, no system detail.
reach)                            The Tan and Sanchez deep
                                  pages hold the checked forms
                                  of this claim.""") + """
<h2>Three social only finds worth a test</h2>
""" + steps([
 "Auto compact thresholds: the Omega reel sets context compaction at 40 percent for small tasks and 60 percent for large ones. No primary source in the sweep names a number. Test both on your long lanes and keep the one that holds quality.",
 "Three ways to run agents, from a Charlie Hills carousel: the slide set teaches run modes as a choice per task. The primary form of the same idea sits in the best practice doc: session, worktree fleet, and scripted print mode, each with its own stop form.",
 "The project management feel: a Threads post by a known engineering voice (700 likes) states the tool feels less like pair work with an expert and more like project management of an expert. The Lenny transcript says the same in full: the job moved to task design, review, and steering. Social confirms the shift is felt wide, not only at labs.",
]) + """
<h2>Top posts pulled, with links</h2>
""" + steps([
 '<a href="https://www.instagram.com/p/DefCfujIPjd/">Cherny tips carousel</a>, 22K likes. The primary thread in social form.',
 '<a href="https://www.instagram.com/reel/DVwl2NOCZ5l/">Claude Skills tutorial</a>, 33K likes. Skills as the unit of reuse.',
 '<a href="https://www.instagram.com/p/DWfA-nqjXgZ/">5 levels of Claude Code carousel</a>, 19K likes. The maturity ladder frame.',
 '<a href="https://www.instagram.com/reel/Dff39V1vpj7/">Omega setup reel</a>, 4.7K likes. Orchestrator plus cheap sub agents.',
 '<a href="https://www.instagram.com/reel/DdEeXsSOF77/">Loop, goal, schedule reel</a>, 5.2K likes. The unattended trio.',
 '<a href="https://www.instagram.com/reel/DSA4y4nEf5e/">Isenberg plugin reel</a>, 8.9K likes. A top model plus three named plugins.',
 '<a href="https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm">Cherny own Threads post</a>, 5.5K likes. His setup intro in his own words.',
 '<a href="https://www.instagram.com/p/DWS197EjtKr/">Workflow cheatsheet infographic</a>, 2.9K likes. Setup, files, skills, hooks, memory in one image.',
 '<a href="https://www.instagram.com/p/DXjnpPOkRu-/">Cheat sheet after 6 months carousel</a>. Practitioner tips in slide form.',
 '<a href="https://www.instagram.com/reel/DXei0mZDa8j/">Usage limit reel</a>, 1.2K likes. Three techniques to stay under caps.',
]) + """
<h2>The TikTok gap, stated plain</h2>
<p>No TikTok lane ran in this sweep. This machine holds no TikTok connector, and the agent-reach TikTok path needs a ScrapeCreators device signup that stands open from the October setup. TikTok workflow content exists, per cross posts of the same creators on Instagram, but no TikTok post was pulled, read, or counted here. The gap closes when the signup lands or a TikTok connector connects. No TikTok claim in this guide rests on a TikTok read.</p>
<h2>How to use the viral layer</h2>
<p>Use social posts as a demand signal and a teaching frame source. The ladder frame and the trio naming teach well. For any act that spends money, merges code, or sends a message, the rule stands: the primary source or your own test decides, never a reel. Each pattern in the table names its primary home in the deep pages.</p>
<div class="rule"><p>Apply this to your work: your own saved posts hold the same split. Your 930 plus Instagram saves carry strong frames and weak mechanics in one feed. The deep pages in this guide give you the filter: a save earns a workflow slot only when a primary source or your own run backs its mechanics. Run the Omega compact test on one lane this week, since it is the one social claim with a cheap, clear test and no primary answer.</p></div>""")

# ---------- templates ----------
TPL_FILES = {
"claude-md-template.md": """# CLAUDE.md template (Ghostty shape, for a Python service)
# Rule: each line must map to a past agent error or a hard fact.
# Cap: 50 lines. Review each 6 months with an ablation pass.

## Commands
Build: <exact build command>
Test all: <exact test command>
Test one: <targeted test command with filter> (prefer this, full suite is slow)
Lint: <exact lint command>
Format: <exact format command>

## Scoped areas
<Sub area>: build with <variant command>, test with <variant command>
<One portability or platform rule from a real past break>

## Map
Core: <path/>
API: <path/>
Tests: <path/>

## Hard rules
<One prohibition per line. Example: never edit files under migrations/.>
<The log file path and the rule: read the log for sign in links and errors.>
""",
"agents-map-template.md": """# AGENTS.md as a map (OpenAI harness form)
# Cap near 100 lines. This file points. Docs hold the depth.

## Start here
Architecture and layer order: docs/architecture.md
Design docs index, with a verification state per doc: docs/design/
Quality grades per domain and layer: docs/quality.md
Active plans, with progress and decision logs: docs/plans/active/
Tech debt register: docs/plans/tech-debt.md

## Layer law
Dependencies flow one way: Types -> Config -> Repo -> Service -> Runtime -> UI
Cross cutting parts enter via Providers only.

## Golden principles
Prefer the shared utility package over a hand rolled helper.
No YOLO data probing: validate at the boundary or use the typed SDK.
<Add one principle per repeated drift find.>

## Checks an agent can run
<LogQL or log path for logs> <PromQL or metric path for metrics>
<The one command that proves a change works>
""",
"sub-agent-instructions.md": """# Sub agent instructions (Yan form)
# One file per role. The main agent hands this file to each sub agent.

Role: specialized processing agent for <SOURCE TYPE>.
Work rule: process one source in full before the next. No skips.
Input: the source chunk in your task message.
Output folder: parts/ (exists; write one part file per source).
Return form: the part template at templates/part-template.md.
Categories: <CAT SET FOR THE DOMAIN>.
Errors: write the error as text in the part file. Never skip in silence.
End: one completion line. Sources done, sources failed, and why.
""",
"part-template.md": """# Part file (one per source)
Source: <URL OR NAME>
Date: <DATE>
Claims:
- <Claim in one line> | source line or section | confidence: High/Medium/Low
- <Claim> | <locator> | <confidence>
Gaps: <What the source does not state, or Not in source>
""",
"release.formula.toml": """# Release formula (Gas Town form, TOML)
# Run: bd cook release --var version=1.2.0 (test)
# Run live: bd mol pour release --var version=1.2.0

[formula]
name = "release"
version = "1.2.0"

[[steps]]
id = "bump-version"
needs = []

[[steps]]
id = "run-tests"
needs = ["bump-version"]

[[steps]]
id = "build"
needs = ["run-tests"]

[[steps]]
id = "create-tag"
needs = ["build"]

[[steps]]
id = "publish"
needs = ["create-tag"]
""",
"learning-file-template.md": """---
title: <One line: the trap and the fix>
area: <codebase area or workflow lane>
keywords: <search terms a future plan will use>
date: <YYYY-MM-DD>
---
# Trap
<What went wrong, in two lines.>
# Fix
<The act that fixed it, in two lines.>
# Check
<The command or test that proves the fix holds.>
""",
"issue-template.md": """# Issue (Cora five part form)
## Problem statement
<What breaks or is missing, for whom, in plain terms.>
## Solution vision
<The end state in three lines.>
## Requirements
<One line per requirement.>
## Technical requirements
<Files, interfaces, data, and limits.>
## Implementation steps
<One step per line, in build order, each with its check.>
""",
"ledger-template.md": """# Task ledger (beads lite form)
# One block per task. The ledger alone must restart any task.

## <PREFIX>-<NUMBER> <TASK TITLE>
State: open | running | gated | done | killed
Worker: <session or agent name>
Gate: <the check that must pass before merge or ship>
Notes: <one line, updated at each check in>
""",
"supervisor-spec.md": """# Supervisor watcher spec (Mods form, with cost terms)
Trigger: run only after a turn that edited files, ran commands,
or made 8 or more tool calls.
Act: fork the talk. Read the fork. Return a verdict with two
parts: concerns (shortcuts, buried facts, uncommitted work at
risk) and one next step as an action the human can fire.
Cost log: record fires, turns watched, and input tokens per
check, per week.
Worth test: the watcher stays only if it surfaces a fact the
human would have missed, makes a call easier, or lets the
human act with no distraction. Two dead weeks means a rewrite
of the trigger or a cut.
Trust note: the watcher runs with full permissions and is not
sandboxed. Source access is a hard need.
Off switch: one command, tested.
""",
}
for fname, body in TPL_FILES.items():
    open(os.path.join(TPL, fname), "w").write(body)
    print("template", fname)

# ---------- 3 more prompt files ----------
PF2 = {
"ablation-reset.md": ("Ablation Reset (Cherny YC form)",
"""Purpose: strip a rule file to the lines that earn their place.
Inputs: CLAUDE.md or AGENTS.md, one week of normal work.

FLOW:
1. Back up the file with a date in the name.
2. Delete half the lines: all lines that fix acts the current
   model no longer shows, all taste lines, all repeats.
3. Work one week with the thin file. Log each repeat error
   in a scratch note: the error, the count, the cost.
4. Add back one line per error that repeats two plus times.
   Write the line as a command or a fact, never as a plea.
5. Diff old vs new. Keep the diff in the repo.

VERIFY: the new file is shorter and the repeat error count
fell or held.
STOP: a safety or permission line never enters the ablation.
Those lines stay by law, not by test."""),
"supervisor-watch.md": ("Supervisor Watch (Mods form)",
"""Purpose: a forked watcher that returns concerns and one step.
Inputs: the just finished turn, the repo state.

PROMPT (run as a fork or a fresh sub agent):
Read this session turn and the repo state. You are a watcher,
not a worker. Return:
1. Concerns: shortcuts taken, facts buried in tool output,
   uncommitted work at risk, checks claimed with no artifact.
   One line each, with the file or output that proves it.
2. One next step: the single act with the best value, stated
   as a command I can send as is.
Trigger terms: run only when the turn edited files, ran
commands, or made 8 or more tool calls.
VERIFY: each concern names its proof. A concern with no proof
gets cut from the verdict.
STOP: no fixes from the watcher. Verdicts only."""),
"capsule-prd.md": ("Capsule PRD (Reddit Proto form)",
"""Purpose: turn a design frame or a feature ask into a PRD that
an agent can build from in a clean repo.
Inputs: the frame or ask, the design token and component map,
CI and review feedback on past capsules.

PROMPT:
Build a feature capsule for <FEATURE>.
1. Walk the design map: name each token, component, and
   surface this feature touches, with the production match
   for each. Flag each part with no production match.
2. Read the CI and review feedback on the last capsules in
   this area. Fold each repeat note into a rule for this build.
3. Write the PRD: user goal, acceptance criteria in test
   form, detail notes, and links to the source frames.
4. Build in a sibling repo. Keep the production repo clean.
   Return a draft PR with screenshots of each state.
VERIFY: each acceptance item maps to one screenshot or test.
STOP: a part with no production match stops the capsule for
a human call. No invented components."""),
}
PROMPTS_DIR = os.path.join(BASE, "prompts")
for fname, (title, body) in PF2.items():
    open(os.path.join(PROMPTS_DIR, fname), "w").write(f"# {title}\n\n{body}\n")
    print("prompt file", fname)
print("V6 build complete")
