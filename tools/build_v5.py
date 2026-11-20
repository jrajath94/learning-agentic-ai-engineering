#!/usr/bin/env python3
"""V5 deep dives: replication grade pages from round 3 report + prompt files."""
import os, re

BASE = os.path.expanduser("~/workspace/learning-agentic-site")
OUT = os.path.join(BASE, "site")
PROMPTS_DIR = os.path.join(BASE, "prompts")
os.makedirs(PROMPTS_DIR, exist_ok=True)

shell = open(os.path.join(OUT, "niche.html")).read()
head = shell.split("<main>")[0]
head = re.sub(r"<title>.*?</title>", "<title>PLACEHOLDER</title>", head)
foot = "</main>" + shell.split("</main>", 1)[1]

def deep(fname, title, lede, body):
    h = head.replace("PLACEHOLDER", title + " | Learning Agentic AI Engineering")
    main = f"""<main>
<p class="meta">Home / Deep Dives / {title}</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>
{body}
</main>
"""
    open(os.path.join(OUT, fname), "w").write(h + main + foot)
    print("deep page", fname)

def steps(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def pre(text):
    return "<pre>" + text.replace("&","&amp;").replace("<","&lt;") + "</pre>"

def apply_block(text):
    return f'<h2>Apply this to your work</h2><div class="rule"><p>{text}</p></div>'

def check_block(items):
    return "<h2>Replication checklist</h2>" + steps(items)

# ---------------- 1. REED ----------------
deep("deep-reed.html", "Deep Dive: Harper Reed Spec Pipeline",
"The full build system from one blog post: talk an idea into a spec, turn the spec into a prompt plan, run the plan one prompt at a time, and keep state in a todo file. Source: Harper Reed, My LLM Codegen Workflow, 16 February 2025, read in full. Confidence: High.",
"""<h2>The system in one view</h2>
<p>Three files carry the whole method. spec.md holds what to build. prompt_plan.md holds one self contained prompt per build step. todo.md holds state across sessions, and the codegen tool checks items off as it works. Planning takes near 15 minutes. Build time goes to execution, not to re-explaining.</p>
<h2>Phase 1: idea honing</h2>
<p>Tool: a strong chat model. Method: the model asks one question at a time. You answer in short form. The talk ends when the idea holds no open branch: user, scope, data, edge cases, and what done means.</p>
""" + pre("""Opening prompt pattern (from the post, structure verbatim):
Ask me one question at a time about <IDEA> until the idea is fully
specified. Then compile the answers into a developer-ready spec
and save it as spec.md.""") + """
<p>Why one question at a time works: a batch of ten questions gets skim answers. One question forces a decision per turn. The spec at the end is a compile step, not a summary: the model restates every decision in build terms.</p>
<h2>Phase 2: the prompt plan</h2>
<p>Tool: a reasoning model. Input: spec.md. Output rules from the post: markdown file, each step is one self contained prompt in a code block, steps broken down twice to reach the right size, and no step may leave orphaned code that nothing integrates. Then one more prompt creates todo.md as a full checklist.</p>
""" + pre("""Plan prompt pattern (structure from the post):
Read <SPEC>. Produce prompt_plan.md. Each step is a single prompt
in a code block. Each prompt must stand alone: it names the files,
the behavior, and the test for that step. Break each step down
twice. No step may leave code that no later step integrates.

Then: Can you make a todo.md that I can use as a checklist?
Be thorough.""") + """
<h2>Phase 3: execution, two modes</h2>
""" + steps([
 "Pair mode: paste one prompt from prompt_plan.md into the coding chat. You own boilerplate and tooling choices. Review the diff. Check the todo item.",
 "Agent mode: paste the prompt into an agent runner. The agent runs tests and debugs inside the step. You review at step end.",
 "Stuck protocol: pack the whole repo with repomix and hand the pack to a fresh chat with the failing step and the error text. Fresh context plus full code beats a long stuck thread.",
]) + """
<h2>Brownfield mode: the mise task system</h2>
<p>For work on an existing repo, Reed plans per task, not per project. A global mise config holds seven tasks. Each task packs the repo with repomix into output.txt, then pipes the pack through the llm CLI with a named prompt template.</p>
""" + pre("""The seven task names, verbatim from the post:
LLM:clean_bundles
LLM:copy_buffer_bundle
LLM:generate_code_review
LLM:generate_github_issues
LLM:generate_issue_prompts
LLM:generate_missing_tests
LLM:generate_readme

Pipeline pattern under the tasks:
cat output.txt | llm -t code-review-gen -m claude-3.5-sonnet > code-review.md
cat output.txt | llm -t readme-gen > README.md

Local override rule: a repo .mise.toml may replace a task,
but the task must still produce output.txt.""") + """
<p>The loop in use: run generate_missing_tests, read missing-tests.md, copy the bundle, paste the bundle plus the first issue into the coding tool, run tests, repeat. Each pass is small, state lives in files, and any session can resume from todo.md alone.</p>
<h2>Prompt magic: the persona frame</h2>
<p>His three workhorse prompts (code review, issue generation, missing tests) share one frame: a senior developer persona, the packed repo as input, and an explicit do not hallucinate rule. The frame matters less than the input discipline: the model sees the whole repo, not a fragment, so its review names real files.</p>
""" + apply_block("Your study builds and paper builds fit this pipeline with no change. Idea talk becomes a scope talk: one question at a time on sources, depth, and output form. spec.md becomes the build brief you already demand in one pass. prompt_plan.md becomes one prompt per chapter or per paper section, each with its own acceptance check. todo.md becomes the atomic coverage list. Your current pain, restating scope mid build, is the exact failure this system removes: the spec file holds scope, so no session re-litigates it.") +
check_block([
 "Write the idea talk prompt into your chat tool today.",
 "Run one idea through all three phases on a small tool you want.",
 "Save spec.md, prompt_plan.md and todo.md in the repo root.",
 "Add one mise style task or one shell script per repeat job: review, tests, readme.",
 "Rule: if a step leaves orphan code, the plan is wrong. Fix the plan, not the code.",
]) + """
<p>Prompt file: <a href="../prompts/spec-pipeline.md">prompts/spec-pipeline.md</a> in the repo root of this branch.</p>
<p>Missing from the source: the literal body of each mise task. The post gives names and the pipeline pattern only. The prompt file in this repo rebuilds each task body from that pattern and marks the rebuild as a template.</p>""")

# ---------------- 2. HASHIMOTO ----------------
deep("deep-hashimoto.html", "Deep Dive: Hashimoto System and the Ghostty AGENTS.md",
"Six adoption steps, a daily agent routine with exact times, and the real production AGENTS.md from the Ghostty repo, read in full. Sources: Mitchell Hashimoto, My AI Adoption Journey, 5 February 2026, and github.com/ghostty-org/ghostty AGENTS.md. Confidence: High.",
"""<h2>Step 1: drop the chatbot</h2>
<p>Use an agent that can read files, run programs, and make HTTP requests. Chat alone caps the gain. His proof case: Gemini reproduced the Zed command palette in SwiftUI, and a light edit of that output ships in Ghostty for macOS.</p>
<h2>Step 2: reproduce your own work</h2>
<p>Do each manual commit twice: once by hand, once with the agent, with no sight of the manual version. Fight the agent to equal quality. Four lessons fall out: split work into clear tasks, split vague work into a plan session and an execution session, give the agent a way to verify its own work, and learn when an agent is the wrong tool.</p>
<h2>Step 3: End of Day Agents, the daily routine</h2>
""" + steps([
 "Block the last 30 minutes of the work day. No code in this block. Only agent starts.",
 "Start deep research surveys: one agent per library or option, each returns pros, cons, activity, license, and sentiment.",
 "Start parallel probes on vague ideas. The goal is light, not a ship. Most probes die. The map of the space is the product.",
 "Start issue and PR triage with the gh CLI, agents in parallel. Hard rule: agents never respond in public. Reports only.",
 "Stop. Agents finish in under 30 minutes in his report. No all night loops.",
]) + """
<h2>Step 4: the morning slam dunk filter</h2>
<p>Start the day on the triage reports. Keep only near certain wins. Run them one at a time in the background during deep work. Turn agent desktop notifications off. Check the agent at natural breaks only. The filter is the skill: a warm start beats a cold start, and a wrong warm start costs more than none.</p>
<h2>Step 5: harness engineering</h2>
<p>His rule, in his words: anytime an agent makes a mistake, engineer a fix so the agent never makes that mistake again. Two forms. Form one: a line in AGENTS.md that names the wrong command or the right API. Form two: a programmed tool, such as a screenshot script or a filtered test runner, plus an AGENTS.md line that points the agent at the tool.</p>
<h2>Step 6: always one agent running</h2>
<p>His current state: one agent running for 10 to 20 percent of a work day, deep mode runs of 30 plus minutes. One agent, not a fleet. The counter case to Cherny and Yegge in this guide: depth over count, with a harness that compounds.</p>
<h2>The Ghostty AGENTS.md, full structure</h2>
<p>The file runs near 40 lines. Every line maps to a past agent error, per Hashimoto. Structure, complete:</p>
""" + pre("""Title: Agent Development Guide

1. Commands
   Build: zig build (macOS: add -Demit-macos-app=false to skip
   the app bundle and speed compilation)
   Test: zig build test
   Rule: prefer targeted tests with -Dtest-filter, full suite is slow
   Format Zig: zig fmt .
   Format Swift: swiftlint lint --strict --fix
   Format rest: prettier -w .

2. libghostty-vt (a sub library with its own build)
   Build: zig build -Demit-lib-vt
   Build WASM: zig build -Demit-lib-vt -Dtarget=wasm32-freestanding
     -Doptimize=ReleaseSmall
   Test: zig build test-lib-vt -Dtest-filter=<filter>
   Rule: prefer this test when the change sits in a lib file
   Portability rule: all C enums in include/ghostty/vt/ end with
   a _MAX_VALUE = GHOSTTY_ENUM_MAX_VALUE sentinel

3. Directory Structure
   Shared Zig core: src/
   macOS app: macos/
   GTK app: src/apprt/gtk

4. Issue and PR Guidelines
   Never create an issue. Never create a PR.""") + """
<p>Read the shape, not the content. Commands first, with the fast variant named. One scoped sub build. One portability rule from a real past break. A three line map. Two hard prohibitions. Nothing else earns a line. The repo also ships vetted agent prompts in .agents/commands, such as a GitHub issue diagnosis command that explains the problem and suggests a plan, with read only access.</p>
""" + apply_block("Your AGENTS.md files for study repos can copy this shape at once: exact build and test commands with the fast targeted variant, one scoped rule per sub project, a three line map, and hard prohibitions that match your standing orders, such as no pushes without a pass and no edits to live masters before a pilot gate. Your end of day slot also maps to your life coach rhythm: a 30 minute agent start block before the night review, with triage reports on papers, roles, and study queues waiting at the morning battle plan.") +
check_block([
 "Write your repo AGENTS.md in the Ghostty shape: commands, scoped rules, map, prohibitions. Cap at 50 lines.",
 "Start the 30 minute end of day block for one week. Three starts per day, no more.",
 "Morning rule: filter to slam dunks only. Run one at a time. Notifications off.",
 "Each agent error this week becomes one AGENTS.md line or one checker tool. Log both forms.",
]) + """
<p>Prompt file: <a href="../prompts/end-of-day-agents.md">prompts/end-of-day-agents.md</a>.</p>""")

# ---------------- 3. BALL ----------------
deep("deep-ball.html", "Deep Dive: Thorsten Ball and Amp Automations",
"A timestamped talk transcript, read in full: self waking agents, proof demands, 15 AGENTS.md files, Orbs and Runners, and a no PR process. Source: Amp Time Capsule 6, Thorsten Ball, October 2026. Confidence: High.",
"""<h2>Prompt the what, not the how</h2>
<p>At 00:02:50 in the transcript: modern agents need the goal and the constraints, not the method. No mention tags, no manual context assembly. The agent plus the codebase plus the process forms the working triad.</p>
<h2>Going horizontal: full SDLC access</h2>
<p>At 00:04:55: the agent sees deploys, CI, production logs, monitoring and metrics, and feature flags. A coding only agent guesses at impact. An agent with the full loop sees the result of its own change and reacts. This one access decision explains most of the gap between demo agents and his daily use.</p>
<h2>Automations: the agent wakes itself</h2>
""" + steps([
 "Ship a change.",
 "Tell the agent: in two hours, check again. The agent schedules its own wake up.",
 "At wake: the agent checks deploy state, error rates, and user visible behavior.",
 "His worked case: the wake report said the commit is live, inference errors did not rise, and a user visible regression exists. Result: a revert, started by the agent report.",
 "Daily maintenance checks run on the same pattern. Snooze rules keep the sidebar clean: a thread sleeps until the next message matters.",
]) + """
<h2>The proof demand</h2>
<p>At 00:14:01: he reviews load bearing code only. For the rest, one prompt rules, verbatim in the transcript at 00:15:00: Give me irrefutable proof that this works now. The agent, in a throwaway machine, installs what it needs and returns screenshots, videos, or a test matrix. Proof is an artifact, not a claim.</p>
<h2>Codebase legibility kit</h2>
""" + steps([
 "Dev server start and stop as agent runnable commands, with seed data.",
 "A REPL the agent can drive.",
 "15 AGENTS.md files across the Amp repo, scoped per area.",
 "Separate skills for the dev server, for cloud production access, for the data warehouse, and for the app framework.",
 "Threads as searchable context: a later agent reads an earlier thread as a source.",
]) + """
<h2>Orbs and Runners</h2>
<p>An Orb is one throwaway remote machine per thread, scale to zero, no local dev state. A Runner is the opposite: a stateful shared machine, such as a macOS build runner. Orbs can spawn threads on a Runner. Agents pass files and messages both ways. The split maps to a simple rule: stateless work goes to Orbs, stateful work goes to Runners.</p>
<h2>Process: no PRs, plugins for ops</h2>
<p>His team pushes to main with no PR layer. Designers ship code. No Figma step. Bug reports from Slack start an agent with a diagnostic bundle attached. TypeScript plugins cover bug reports, user mail, system health, feature flags, and credits. Ops work is agent work with a plugin shape.</p>
<h2>Eval your own instructions</h2>
<p>At 00:29:04: after any AGENTS.md change, spawn 5 to 10 fresh Orbs and test if the new instruction holds in practice. An instruction that fresh agents ignore is not an instruction. This is the missing test step in most rule files.</p>
""" + apply_block("Your builds already run long agent jobs. Add the wake pattern: each long job ends with a scheduled self check that reads its own output against the acceptance list and reports proof or a defect, in place of a status claim. Your study repos gain the legibility kit at once: one command to build, one to check, seed data for sample pages, and a per area rule file. And run his instruction eval on your own standing rules: spawn fresh sessions, give a task that tempts the old error, and count how often the rule holds.") +
check_block([
 "Add one scheduled wake check to your longest running agent job.",
 "Write the proof demand into your review prompts verbatim.",
 "List your legibility gaps: no seed data, no REPL, no scoped rule file. Fix one per week.",
 "After your next rule file change, test it with 5 fresh sessions before you trust it.",
]) + """
<p>Prompt file: <a href="../prompts/proof-demand.md">prompts/proof-demand.md</a>.</p>""")

# ---------------- 4. GAS TOWN ----------------
deep("deep-gastown.html", "Deep Dive: Gas Town, the 20 to 30 Agent Town",
"Every role, command, and data structure from the public repo README, read in full, plus a solo lite form. Source: github.com/steveyegge/gastown, Steve Yegge. Confidence: High for repo facts, Medium for failure modes, since the launch post stands unopened in full.",
"""<h2>What Gas Town is</h2>
<p>A workspace manager for 20 to 30 agents. Work persists in git backed hooks and a Beads ledger, so agent sessions can die and the town keeps the state. The human talks to one coordinator. The coordinator runs the town.</p>
<h2>Roles, exact jobs</h2>
""" + pre("""Mayor        Primary coordinator. Full workspace context.
             Start: gt mayor attach
Town         The workspace root, ~/gt/
Rigs         One container per project, wraps a git repo
Crew         A human personal workspace in a rig
Polecats     Worker agents. Fixed identity, throwaway sessions
Hooks        Git worktree storage pinned to an agent
Convoys      Work units that bundle beads for one goal
Beads        Git backed issues. ID form: prefix + 5 chars,
             gt-abc12, hq-x7k2m
Molecules    Workflow templates in motion
Formulas     TOML files that create molecules
Witness      Per rig life cycle manager: watch polecats,
             spot stuck work, recover, clean up. No build work
Deacon       Cross rig supervisor on patrol: gt patrol
Dogs         Infra workers the Deacon sends. Boot is the
             triage Dog. Heartbeat each 3 minutes:
             daemon to Boot to Deacon to Witness and Refinery
Refinery     Per rig merge queue. On gt done: batch merge
             requests, run gates, bisect merge to main.
             Polecats never push to main
Escalation   gt escalate -s HIGH "..." routes Deacon to
             Mayor to Overseer. Levels: CRITICAL P0,
             HIGH P1, MEDIUM P2""") + """
<h2>The MEOW flow</h2>
""" + steps([
 "Tell the Mayor the goal.",
 "The Mayor analyzes and creates a convoy.",
 "The Mayor spawns agents and slings beads onto hooks.",
 "Agents run under the propulsion rule: if work sits on your hook, you run it. No idle wait for a push.",
 "The Witness watches each rig. The Deacon patrols across rigs.",
 "The Refinery merges in order, with gates.",
 "The Mayor summarizes for the human.",
]) + """
<h2>Commands, verbatim from the README</h2>
""" + pre("""brew install gastown
gt install ~/gt --shell --git
gt up                       boots Dolt, daemon, Deacon, Mayor,
                            per rig Witness and Refinery
gt doctor --fix
gt rig add myproject <repo-url> [--prefix mp]
gt mayor attach
gt convoy create "Feature X" gt-abc12 gt-def34 --notify --human
gt sling gt-abc12 myproject
gt convoy list
gt agents
gt prime                    context recovery for an agent
gt feed [--problems]        town view: GUPP Violation, Stalled,
                            Zombie, Working, Idle
gt dashboard [--port 3000]
gt seance                   talk to a predecessor session""") + """
<h2>Formulas: workflows as TOML</h2>
<p>Formulas live in internal/formula/formulas. The release formula runs bump version, run tests, build, create tag, publish, each step with needs edges. Commands: bd formula list, bd cook release --var version=1.2.0 to test, bd mol pour release to run with checkpoint recovery. Two wisp forms exist: root only wisps create steps at run time, poured wisps fix steps in advance with checkpoints.</p>
<h2>Prerequisites and the honest cost</h2>
<p>Needs: Git 2.20 plus, Go for source builds, Beads bd 0.57 plus, sqlite3, tmux for full mode. Runtimes: Claude Code by default, with presets for Gemini, Codex, Cursor, Amp, Copilot and more. His own warning stands in round 2 notes: most users are not ready. Run 3 to 5 parallel agents well first. The town pattern pays at 10 plus sustained agents and costs real money at all times.</p>
<h2>Gas Town Lite, the solo form</h2>
""" + steps([
 "One coordinator chat acts as Mayor. It holds the goal list and the state file.",
 "Workers are plain parallel sessions, one worktree each. No town software.",
 "A beads file in plain markdown holds tasks with IDs: two letter prefix plus a number.",
 "A merge order rule replaces the Refinery: one merge at a time, gates run per merge.",
 "A patrol habit replaces the Deacon: the coordinator scans for stalled workers at each check in and restarts or kills by rule.",
 "Escalation rule: a worker stops and reports on a gate fail. It never pushes past a red gate.",
]) + apply_block("Your parallel build lanes already run Mayor style work through coordinators. The lite form adds the three parts your lanes miss at times: a persistent task ledger with IDs that survives session death, a merge queue rule of one at a time with gates, and a patrol scan that names stalled workers in plain states. Your watermark sweep and repo pushes fit the ledger form at once: each repo one bead, each push one gate check by blob hash.") +
check_block([
 "Do not install Gas Town until one project holds 10 plus sustained parallel agents for a week.",
 "Adopt the ledger, the merge rule, and the patrol scan in lite form now.",
 "Write your escalation levels in one line each: P0 stop all, P1 coordinator decides, P2 log and continue.",
]) + """
<p>Prompt file: <a href="../prompts/gas-town-lite.md">prompts/gas-town-lite.md</a>.</p>""")

# ---------------- 5. LITT ----------------
deep("deep-litt.html", "Deep Dive: Litt, Surgeon Model and Explain Diff",
"The delegation taxonomy from Code like a Surgeon, plus the full explain diff skill structure from his public gist, read in full. Sources: geoffreylitt.com, 24 October 2025, and gist.github.com/geoffreylitt. Confidence: High.",
"""<h2>The surgeon model</h2>
<p>The name comes from the chief programmer team in old software practice: one surgeon holds the core work, a team takes the rest. Litt maps the split to agents. The human keeps primary work: design, core logic, fast feedback edits. The agent takes secondary work, in four named forms:</p>
""" + steps([
 "A guide to the code areas a big task will touch, written before the task starts.",
 "A spike: a rough attempt at a big change, built to review and often to throw away.",
 "Fixes with a clear spec: type errors, named bugs, bounded repairs.",
 "Documentation of finished work.",
]) + """
<p>Secondary work runs async, in the background, at times overnight. His example: an agent told to have a research report ready by 7 in the morning. Primary work stays tight loop, with tab complete level feedback. The autonomy slider is the whole model: loose for secondary, tight for primary.</p>
<h2>The explain diff skill, full structure</h2>
<p>The gist holds two variants, HTML and Notion, with one content spec. Opening line of the skill: Please make me a rich, interactive explanation of the specified code change. Four sections, in fixed order:</p>
""" + pre("""Section 1: Background
  The system around the change. A deep background for a
  beginner first, skippable. Then a narrow background on the
  exact area the change touches. Explore wide before writing.

Section 2: Intuition
  The essence before the detail. Concrete examples with toy
  data. Figures and diagrams in number.

Section 3: Code
  A walk through the change, grouped by idea, in an order a
  reader can follow. Never in file order.

Section 4: Quiz
  Five questions, medium difficulty, real understanding,
  no gotchas. HTML form: pick an answer, get right or wrong
  feedback at once. Notion form: answers in toggle blocks,
  each with a note on why it is right or wrong.""") + """
<h2>Format rules from the gist</h2>
""" + steps([
 "One self contained HTML file, CSS and JS inside, one long page, section headers, a table of contents. No tabs for top level structure.",
 "File lives in a global place outside the repo. Name starts with the date: YYYY-MM-DD-.",
 "Prose model named in the skill: the clarity and flow of Martin Kleppmann.",
 "Diagrams: reuse a few diagram families. Simplified UI diagrams and system flow diagrams with example data. No ASCII diagrams. HTML designs in place of text art.",
 "Code blocks in pre tags. Any custom div that holds code gets white space pre-wrap, with a scan for that rule before save.",
 "Callouts for key concepts, definitions, and edge cases.",
]) + """
<h2>The usage rule</h2>
<p>From his later talk, via a secondary account: read the explainer before the raw diff, and pass the five question quiz before the code ships. The quiz is the gate. A reviewer who fails the quiz has not reviewed, no matter how long the diff stayed open.</p>
""" + apply_block("This skill fits your review load at once. Your agent lanes ship diffs and pages faster than you can read them, and your standing rule is that a worker claim never counts without a check. Run explain diff on each lane output: one explainer page per change set, five questions, and your pass is the ship gate. The form also matches your study law: background, intuition, code, quiz is your Russian doll order in one page, and the quiz gives you the retrieval practice your learning system demands.") +
check_block([
 "Copy the skill structure into a command in your main coding tool this week.",
 "Run it on the next agent diff you must review. Take the quiz before you open the raw diff.",
 "Rule: quiz fail means the change waits, and the explainer gets a fix first.",
]) + """
<p>Prompt file: <a href="../prompts/explain-diff.md">prompts/explain-diff.md</a>, a full template built on the gist structure.</p>""")
print("part 1 pages done")

# ---------------- 6. RONACHER ----------------
deep("deep-ronacher.html", "Deep Dive: Ronacher Setup Rules",
"Every recommendation from Agentic Coding Recommendations with its reason, the yolo alias, the Makefile log pattern, and the tool design rules. Source: Armin Ronacher, lucumr.pocoo.org, 12 June 2025, read in full. Confidence: High.",
"""<h2>Base setup</h2>
""" + steps([
 "Claude Code on the 100 dollar Max plan, Sonnet as his model pick at post time, for speed and cost balance.",
 "Alias, verbatim in effect: claude-yolo runs claude --dangerously-skip-permissions. Risk control sits in the environment: dev work lives in Docker, so a wild agent hits a container, not the host.",
 "Token discipline: no screenshots and no browser runs for routine work. Both burn context for little signal in his setup.",
 "MCP: near zero. Use it only when a plain tool proves too unreliable. His one standing exception: Playwright MCP. Database work goes through psql. Custom tools are plain scripts.",
]) + """
<h2>Stack picks with reasons</h2>
""" + steps([
 "Go for new backends: a context system agents handle well, test caching for speed, structural interfaces, low ecosystem churn, and code that tolerates sloppy generation.",
 "Python with care: pytest fixture magic confuses agents, async event loop errors cost turns, and slow interpreter start taxes each loop step.",
 "Frontend: Tailwind, React with TanStack Query and Router, Vite. One trap named: the TanStack file router dollar param file names break under shell interpolation and confuse agents.",
 "Dependencies: upgrade slower than feels right. Prefer code generation over a new dependency. Prefer stable ecosystems: Go, Flask.",
]) + """
<h2>Tool design rules</h2>
<p>Anything can be a tool. A good tool for an agent meets four tests from the post: fast, since crashes pass but hangs kill a loop; friendly, with error text that teaches the fix; chaos proof, built for an LLM chaos monkey, with no user error and no undefined behavior as a design stance; and observable, so a failure shows its cause.</p>
<h2>The Makefile log pattern, step by step</h2>
""" + steps([
 "Critical tools live in a Makefile. One target starts the dev stack: make dev.",
 "A process manager starts services and writes a pidfile. A second start attempt fails loud with a services already running note, in place of a silent double start.",
 "All service output prints to the terminal and lands in one log file the agent can read: make tail-log shows it.",
 "Debug sign in mail lands in the log. A CLAUDE.md line tells the agent: read the log for the confirmation link. Result: the agent can complete a full sign in flow alone in the browser.",
 "Speed rule for agent built tools: milliseconds, not minutes. For one slow app he built a watcher daemon: drop a Python module in a watched folder, the daemon runs it and writes output to the log.",
]) + """
<h2>Code style for agent readers</h2>
<p>The dumbest code that works wins. Functions with clear, long names beat classes. No inheritance tricks. Plain SQL. Permission checks local and visible in the function that acts. Refactor when a pattern repeats at scale, such as utility classes across 50 files, and not before.</p>
<h2>Parallel sessions</h2>
<p>One agent is slow. Parallel agents are the win, and shared state is the cost. Segment the state: a second checkout per agent, separate databases, separate Redis. Name the segments before the agents start.</p>
""" + apply_block("Your VM work hits his traps by name: slow Python starts in agent loops, fixture magic in test suites, and log output that agents cannot read. Copy the Makefile pattern into your active repos: one start target, one tail log target, one log file, and a rule line that points the agent at the log for sign in links and error text. His state segment rule also fixes a pain in your parallel lanes: one checkout, one data store, one log per lane, named in the task card before work starts.") +
check_block([
 "Add make dev and make tail-log to one active repo. One log file, agent readable.",
 "Add the log pointer line to that repo rule file.",
 "Write your segment map before your next parallel run: checkout, data, log per agent.",
 "Audit one tool against the four tests: fast, friendly, chaos proof, observable.",
]) + """
<p>Prompt file: <a href="../prompts/harness-loop.md">prompts/harness-loop.md</a> holds the loop form that pairs with this setup.</p>""")

# ---------------- 7. YAN ----------------
deep("deep-yan.html", "Deep Dive: Yan News Agents, Code Level",
"A full multi agent build with code: one main agent, three tmux sub agents, FastMCP tools per feed, and a merge step. Source: Eugene Yan, Building News Agents, May 2025, read in full with code. Confidence: High.",
"""<h2>Architecture</h2>
""" + pre("""Main Agent (main tmux pane)
  reads feeds.txt
  splits feeds into 3 chunks
  spawns Sub Agent 1, 2, 3 (one tmux pane each)
  each sub agent: process chunk, write summaries, report done
Main Agent merges all summaries into main-summary.md

Stack: Amazon Q CLI as the agent frame, MCP tools for feeds,
tmux for spawn and display.""") + """
<h2>Feed tool pattern</h2>
<p>Each feed gets one tool: fetch, parse, format. Fetch uses an async HTTP client with a 10 second timeout and a user agent header. Errors return as strings, never as raised exceptions, so the agent reads the failure and acts. Parse turns RSS XML into title, link, description, and date dicts.</p>
""" + pre("""Python pattern, rebuilt from the code shown in the post:

mcp = FastMCP("news-mcp")

@mcp.tool()
async def get_hackernews_stories(
    feed_url: str = DEFAULT_HN_RSS_URL, count: int = 30
) -> str:
    xml = await fetch(feed_url)          # httpx, 10s timeout
    items = parse_rss(xml)               # title, link, desc, date
    picked = items[:count]
    return "\\n---\\n".join(format_item(i) for i in picked)

Tool names as listed in the session:
news_mcp___get_wired_stories
news_mcp___get_techcrunch_stories
news_mcp___get_wallstreetjournal_stories
news_mcp___get_hackernews_stories
news_mcp___get_ainews_latest""") + """
<h2>Instruction files</h2>
<p>Two context files steer the system. The main agent file names the role (primary coordinating agent), the input (feeds.txt), the sub agent instruction file to hand out, and the output form (the main summary template). The sub agent file names its role (specialized processing agent), the work rule (finish one feed in full before the next), the output folder (summaries/, made in advance), the return form (the sub summary template), and the category set: AI and ML, technology, business, and more.</p>
<h2>Task assignment, verbatim form</h2>
""" + pre("""You are Agent [NUMBER]. Read the instructions at
/context/sub-agent.md and execute it.
Here are the feeds to process: [FEEDS]""") + """
<h2>Run commands, verbatim</h2>
""" + pre("""git clone https://github.com/eugeneyan/news-agents.git
uv sync
q chat --trust-all-tools
/context add --global context/agents.md
Prompt: Q, read context/main-agent.md and spin up
sub agents to execute it.""") + """
<h2>Feeds and one real output</h2>
<p>feeds.txt holds six feeds: Hacker News, WSJ Tech, WSJ Markets, TechCrunch, AI News, Wired. The sample run in the post: 124 items, 6 sources, 42 categories, AI and ML at 31 items, 25 percent. Small numbers, full loop: split, parallel process, merge, one file out.</p>
""" + apply_block("This is the exact shape for your event radar and wife search digests, with feeds swapped for your source lanes. One main agent holds the dedupe and ranking rules, sub agents take source chunks in parallel, each returns in one template, and the main agent merges into one brief. Your lanes already run this way by hand through crons. The gain here is the file discipline: one instruction file per role, one template per return, and errors as text the agent can read, so a failed lane reports in the merge in place of a silent gap.") +
check_block([
 "Clone the repo and run the demo once, end to end, before you adapt it.",
 "Write your two instruction files before you write any tool code.",
 "Rule for your tools: errors return as strings. No raised exceptions across the agent boundary.",
 "Pre make the output folder. Agents fail on missing folders in silence.",
]) + """
<p>Prompt file: <a href="../prompts/doc-swarm.md">prompts/doc-swarm.md</a> holds the swarm form for document work.</p>""")

# ---------------- 8. CHERNY ----------------
deep("deep-cherny.html", "Deep Dive: Cherny, Threads, Lenny, and the YC Talk",
"Three primary records joined: his January 2026 workflow thread in full, the Lenny episode transcript, and the YC Startup School talk transcript. Sources: X thread transcription on GitHub, podscripts Lenny transcript, TortoiseWolfe YC transcript. Confidence: High for thread 1 and both transcripts, Medium for thread 2 compilations.",
"""<h2>Thread 1: the 13 practices, in order</h2>
""" + steps([
 "Run 5 Claudes in parallel in the terminal. Tabs numbered 1 to 5. System notifications on tab events.",
 "Run 5 to 10 more on the web app. Hand a session from local to web and back. Start sessions from the phone app in the morning.",
 "Use the top model with thinking for all work. Steering a strong model less beats a cheap model with heavy steering, in total time.",
 "Keep one shared team CLAUDE.md in git. The whole team edits it many times per week. Each error Claude makes earns a line.",
 "In review, tag the Claude account on a team mate PR to add the lesson to CLAUDE.md inside that PR, via the GitHub Action. His name for the pattern: compounding engineering.",
 "Start most sessions in plan mode. Shape the plan until it reads right. Switch to auto accept edits. A good plan one shots the build.",
 "Slash commands for each daily inner loop job, in git, in .claude/commands/. His commit push PR command runs dozens of times per day. Commands pre compute state with inline shell, such as git status.",
 "Two named subagents: code-simplifier, which cleans code after a build, and verify-app, which holds long instructions for end to end tests of the product itself.",
 "A PostToolUse hook formats code after each edit. The hook takes the last 10 percent, so CI format errors near vanish.",
 "No skip permissions mode. Use a permissions file with safe commands pre allowed, shared with the team in .claude/settings.json.",
 "Tools by config file: Slack MCP in .mcp.json, shared. BigQuery via the bq CLI. Sentry for logs.",
 "Long runs, three forms: ask Claude to verify its work with a background agent at the end, or set an agent Stop hook, or use a loop plugin. Sandbox flags stop permission stalls.",
 "Verification is the top practice, in his own stress. Give Claude a way to verify and quality rises two to three times. His team tests each web change in a real browser via the Chrome extension: open, test the UI, fix, repeat. The check varies by domain: a shell command, a test suite, a browser, a phone simulator.",
]) + """
<h2>Thread 2: team tips, from compilations</h2>
""" + steps([
 "Run 3 to 5 git worktrees in parallel. His own form: multiple checkouts with short aliases, plus one analysis worktree for logs and data queries.",
 "Plan mode with a twist: a second Claude reviews the plan as a staff engineer. On a bad run, return to plan mode and replan, never push through.",
 "End each correction with the line: Update your CLAUDE.md so you don't make that mistake again. Edit the file with no mercy. One engineer keeps a notes folder per project, updated after each PR, with CLAUDE.md as the pointer.",
 "A job done more than once a day becomes a skill or a command. One named command runs at session end to find and kill duplicate code. One command pulls seven days of Slack, Drive, tasks, and GitHub into one context dump.",
 "Bugs: paste the Slack bug thread into Claude with the word fix. Let Claude run the whole repair.",
 "Setup notes: a fast terminal, colored named tabs, voice dictation at three times typing speed.",
]) + """
<h2>Lenny episode: principles and numbers</h2>
<p>From the full transcript: 100 percent of his code from Claude since November 2025, 10 to 40 PRs per day across the episode, near 5 agents live as he spoke, and Claude reviews 100 percent of Anthropic PRs with a human after. Team principles in order: better than doing a thing is having Claude do it; underfund projects on purpose, since constraint forces agent first work; speed as a norm, today beats tomorrow; tokens free at the start, cost cuts only after a win scales. His three user tips close the episode: use the most capable model at max effort, since a weak model burns more tokens to the same end; plan mode is one injected sentence that bars code until the plan holds, and near 80 percent of his tasks start there; and try all surfaces, his own split is one third terminal, one third desktop, one third phone.</p>
<h2>YC talk: the ablation method and hard tasks</h2>
""" + steps([
 "On each new model, delete first. His team cut 80 percent of the system prompt for Opus 5, since the prompt existed to fix acts the new model no longer shows.",
 "Method: delete the whole prompt, use the product, add a line back only when the model repeats one error. Each line is re-read each turn, so each line must earn its place.",
 "User form of the rule: each six months, delete your CLAUDE.md, your skills, and your hooks. Watch the bare model. Add back only what earns a return.",
 "Give tasks a grade too hard, with guardrails and exit criteria in the prompt, then leave the model to work. His words at 20:15: verification is the single most important thing people get wrong.",
 "Proof runs: a Bun rewrite from Zig to Rust ran as one prompt plus a dynamic workflow for 11 days. An Electron to Swift rewrite ran 14 to 15 days with a pixel compare check: run both apps, screenshot, compare, repeat until match.",
 "Dynamic workflows: say use a workflow. Agents fan out, a verify set checks, agents fan out again. His name: an algebra for agents.",
 "Loops run local on a cron. Routines run in the cloud with the laptop shut. His own product teams run 20 to 30 maintenance routines per day on Anthropic apps: dead code, test gaps, duplicate abstractions, each a one sentence prompt.",
]) + """
<h2>Two items that do not exist</h2>
<p>The round 3 sweep searched both thread transcriptions for a weekly tips ritual and for capacity planning. Neither item appears. Any guide that lists them under his name cites a source that does not hold them.</p>
""" + apply_block("Your fleet shape is close to his: parallel lanes, shared rule files, review gates. Three upgrades stand out for your work. One: the verify subagent as a named role in each lane, with browser or test proof per change, in place of a text claim. Two: the six month ablation on your own rule files, since your SOUL and AGENTS files grow by accretion and each line taxes each turn. Three: routines for your maintenance load: dead code in study repos, test gaps in labs, duplicate abstractions across your build scripts, each a one sentence cloud routine with a PR as output.") +
check_block([
 "Name your verify agent in each active lane. Write its instructions in a file, not in chat.",
 "Set a date for your first rule file ablation. Back up first. Delete half. Run a week. Add back only earned lines.",
 "Convert one repeat maintenance job into a routine with a PR output and a gate.",
 "End each correction you give an agent with the CLAUDE.md line, verbatim habit.",
]) + """
<p>Prompt files: <a href="../prompts/fleet-day.md">prompts/fleet-day.md</a> and <a href="../prompts/fleet-review.md">prompts/fleet-review.md</a>.</p>""")

# ---------------- 9. OPENAI HARNESS ----------------
deep("deep-openai-harness.html", "Deep Dive: OpenAI Harness Engineering",
"The full system from the OpenAI post, read in full: a map style AGENTS.md, a docs system of record, layer law, a doc care agent, and the self review loop. Source: openai.com/index/harness-engineering. Confidence: High.",
"""<h2>The experiment in numbers</h2>
<p>An internal product built with zero hand written code: near 1 million lines in five months, near 1,500 PRs, a team that grew from 3 to 7 engineers, an average of 3.5 PRs per engineer per day, and a build time near one tenth of the manual path. The first commit and the first AGENTS.md came from the agent itself. Their line: humans steer, agents execute.</p>
<h2>The self review loop, step by step</h2>
""" + steps([
 "The engineer writes a prompt. The agent opens a PR.",
 "The agent reviews its own change on the local checkout.",
 "The agent calls named agent reviews, local and cloud, one per concern.",
 "The agent answers human and agent notes, and loops until all agent reviewers pass.",
 "The post names the shape a Ralph Wiggum loop: the same agent works its own review queue until the queue is empty.",
 "Single runs pass six hours with no human touch, often across sleep hours.",
]) + """
<h2>Legibility and observability kit</h2>
""" + steps([
 "The app boots per worktree, one instance per change, so an agent can drive its own build.",
 "Browser control sits in the agent runtime: DOM snapshots, screenshots, navigation.",
 "Each worktree gets a throwaway observability stack: logs, metrics, traces, torn down at task end.",
 "Agents query logs with LogQL and metrics with PromQL. Sample goals from the post: service start under 800ms, and no span in four key user journeys past two seconds.",
]) + """
<h2>AGENTS.md as a map</h2>
<p>One big instruction file failed four ways: context is scarce, long text stops guiding, the file rots, and no check can verify it. The fix: AGENTS.md at near 100 lines as a table of contents. The knowledge lives in a structured docs tree as the system of record: design docs with an index and a verification state per doc, an architecture doc with domains and layer order, a quality doc that grades each domain and layer, and plans as first class files with progress and decision logs in git. Freshness is a mechanical check: linters and CI verify doc structure, cross links, and currency.</p>
<h2>The doc care agent</h2>
<p>A recurring agent scans for docs that no longer match code behavior and opens fix PRs. Docs rot is treated as a bug class with an owner, and the owner is an agent.</p>
<h2>Layer law</h2>
""" + pre("""Per business domain, dependencies flow one way only:
Types -> Config -> Repo -> Service -> Runtime -> UI

Cross cutting concerns (auth, connectors, telemetry,
feature flags) enter through one interface: Providers.

Enforcement: custom linters plus structural tests.
Lint error text carries the fix instruction, so the error
message itself teaches the agent in context.""") + """
<h2>Entropy control</h2>
<p>Hand clean up failed: the team spent each Friday, 20 percent of the week, on slop removal. The fix has two parts. Golden principles live in the repo: prefer shared utility packages over hand rolled helpers, and no YOLO data probing, with boundary checks or typed SDKs in place of guesses. Background agent tasks scan for drift from the principles, update quality grades, and open small refactor PRs that a human can review in under a minute and often auto merge.</p>
<h2>End to end autonomy, from one prompt</h2>
<p>Their list: validate state, reproduce the bug, record a video of the failure, build the fix, validate by driving the app, record a second video, open the PR, answer feedback, fix build breaks, escalate only on a judgment call, merge.</p>
""" + apply_block("Your repos carry the same rot risk at larger scale: dozens of study and library repos, each with rules, indexes, and plans. Copy three parts at once. One: cut each repo rule file to a map near 100 lines, with the deep rules in a docs tree that holds a verification state per doc. Two: a doc care routine that scans for stale index and plan files and opens fix PRs. Three: lint errors that teach: your STE checker and watermark checker already return fix text, so wire that text into agent context as the remediation step, in place of a pass or fail line alone.") +
check_block([
 "Measure your largest rule file. Cut it to a map. Move depth into a docs tree with states.",
 "Write the layer order for one service you own. Add one structural test that fails on a wrong import.",
 "Start one doc care routine on one repo. Gate: PRs only, no direct pushes.",
 "Add fix text to one lint rule you own. Read the next agent run for the change in behavior.",
]) + """
<p>Prompt file: <a href="../prompts/harness-loop.md">prompts/harness-loop.md</a>.</p>""")

# ---------------- 10. ANTHROPIC ----------------
deep("deep-anthropic.html", "Deep Dive: Anthropic Systems, Research Swarm, Best Practice, C Compiler",
"Four primary Anthropic sources read in full: the multi agent research system, the current Claude Code best practice doc, the C compiler build, and the self build report. Confidence: High, with self reported figures marked as lab claims.",
"""<h2>Multi agent research system: structure</h2>
<p>One lead agent plans and spawns parallel sub agents. Each sub agent searches in iterations and returns a compressed result. The lead compiles the final answer. On their internal research eval, the swarm beat a single top model agent by 90.2 percent. Token facts from the post: agents use near 4 times chat tokens, and multi agent systems near 15 times. Token count alone explains 80 percent of score variance on their benchmark.</p>
<h2>The 8 prompt principles</h2>
""" + steps([
 "Think like your agents: run simulations and watch where the agent mind goes wrong.",
 "Teach the lead to delegate: each sub agent gets an objective, an output form, tool and source guidance, and clear borders.",
 "Scale effort to task size: simple work gets 1 agent and 3 to 10 tool calls; comparisons get 2 to 4 sub agents at 10 to 15 calls each; hard work gets 10 plus sub agents with split duties.",
 "Tool design is critical: inspect all tools first, match tool to intent, prefer a specialist tool over a general one.",
 "Let agents improve their tools: one agent that rewrote weak MCP tool descriptions cut task time by 40 percent.",
 "Start wide, then narrow: broad search first, deep read second.",
 "Guide the thinking: extended thinking for the lead plan, interleaved thinking for sub agents.",
 "Parallel calls: the lead starts 3 to 5 sub agents at once, sub agents run 3 plus tools at once. Research time fell by up to 90 percent.",
]) + """
<h2>Eval method</h2>
<p>Start at once with near 20 real queries. One judge call per answer, one prompt, a score from 0.0 to 1.0 plus pass or fail. Rubric: fact accuracy, citation accuracy, completeness, source quality, tool efficiency. Human review still matters: their humans caught a source bias toward SEO farms over academic PDFs that the judge missed.</p>
<h2>Claude Code best practice, current doc</h2>
""" + steps([
 "Split instructions by force: prompts, CLAUDE.md, and skills guide the model; hooks, deny rules, and managed settings bind the harness. Put each rule in the layer that can hold it.",
 "CLAUDE.md stays short: exact test, typecheck, and lint commands, the single test command, warnings on code that misleads, decisions that live outside the repo, and any point corrected twice. The memory guide caps the file under 200 lines. Scope rules live in .claude/rules/ with a paths filter. Side effect flows become skills with model invocation off.",
 "The check ladder: a prompt instruction first, then a goal condition that a second model rechecks each turn, then a Stop hook that blocks the stop and feeds the error back, with a cap of 8 blocks, then a code review in a fresh sub agent. Demand evidence each time: command plus output, or a screenshot.",
 "Hooks for hard rules: a formatter after each edit, a block on edits under migrations, deny rules on secret files. Sandbox mode for unattended runs.",
 "Cost control: cheap models for sub agents by file setting, short summary demands, usage checks. Clear context between tasks. Compact with a focus note when a session must live.",
 "Unattended runs need five answers first: the done definition, the self check, the allowed scope, stop limits in turns and dollars, and the destination plus approver. Script form uses the print mode with bare, system prompt append, MCP config, settings, allowed tools, and JSON output flags.",
 "Parallel form: worktrees per task, one mechanical change split into 5 to 30 worktree units, each with its own PR.",
 "Stop doing list from the doc: aggressive context care, all caps emphasis, sub agents for context cover alone, delegation for a better answer, think hard phrasing, and keep going exhortations.",
]) + """
<h2>The C compiler build: harness over orchestration</h2>
<p>Sixteen agents built a Rust C compiler in two weeks: near 2,000 sessions, just under 20,000 dollars, 100,000 lines, a bootable Linux 6.9 on three chip families, and 99 percent pass rates on most compiler test suites. No orchestrator agent and no agent to agent talk. The harness is files:</p>
""" + steps([
 "Each agent works in a fresh container, clones a bare repo, and pushes when done.",
 "Task claim: write a text file into current_tasks/, such as current_tasks/parse_if_statement.txt. Git sync forces a second agent to pick a new task. Work, pull, merge, push, delete the lock file.",
 "Agents pick the next most clear problem and keep running notes on failed paths.",
 "Test quality carries the system: strong verifiers first, CI added when new features broke old ones.",
 "Context hygiene: few lines of live output, detail in log files, the word ERROR plus a reason on one line for grep, pre computed aggregate stats.",
 "Time blindness fix: rare progress prints, and a fast mode that runs a fixed random 1 or 10 percent sample per agent.",
 "The kernel block: all agents hit one bug in one giant task. Fix: use GCC as an oracle. Compile most files with GCC and a subset with the new compiler, swap subsets to bisect, then delta debug the file pair.",
]) + """
<h2>Self build report: the review bot</h2>
<p>Anthropic states past 80 percent of merged code comes from Claude as of May 2026, with a typical engineer merging 8 times the 2024 code volume per day, a figure the post itself flags as soft. The transferable system: an automated reviewer reads each change for bugs and security before merge. A retro check found the bot would have caught near one third of the bugs behind past incidents. Their stated bottleneck: human review. The bot exists to move that bottleneck.</p>
""" + apply_block("Your research lanes map to the swarm design with no stretch: one lead holds the question and the claim ledger, sub agents take source chunks, and the eval rubric from this page grades each brief on fact accuracy, citation accuracy, completeness, source quality, and tool efficiency. Your paper builds map to the compiler harness: a current_tasks folder with lock files gives your parallel paper lanes a claim system that survives session death, and the GCC oracle trick maps to a source oracle: one trusted text per claim set, subset swaps to bisect a wrong claim to its source.") +
check_block([
 "Write your research rubric as one judge prompt with the five criteria and a 0.0 to 1.0 scale.",
 "Add a current_tasks lock folder to your next multi lane build.",
 "Set your sub agent models by file. Cheap for search, top for synthesis.",
 "Write your five unattended answers into the task card template: done, check, scope, limits, approver.",
]) + """
<p>Prompt file: <a href="../prompts/research-swarm.md">prompts/research-swarm.md</a>.</p>""")
print("part 2 pages done")

# ---------------- 11. REPOS ----------------
deep("deep-repos.html", "Deep Dive: Skill Repos, Pocock, Superpowers, Caveman",
"The actual file systems of three public repos, from READMEs read in full and file level analyses. Confidence: Medium High for Pocock skill internals, which rest on the README plus two file level secondary analyses, High for the rest.",
"""<h2>Pocock skills: the system shape</h2>
<p>27 skills in version 1.3. Two classes. User invoked skills orchestrate: 16 of them, called by a human on purpose. Model invoked skills hold discipline: 11 of them, called by the agent or by a user invoked skill. Law of the system: a user invoked skill may call model invoked skills, and never a second user invoked skill. Folders: engineering with 20 skills and productivity with 7 ship in the plugin; misc, in progress, and deprecated stay out.</p>
<h2>The grill pair: a stub and a procedure</h2>
""" + pre("""skills/productivity/grill-me/SKILL.md (7 lines, full shape):
frontmatter: name grill-me, a one line description that calls
it a relentless interview to sharpen a plan or design,
and disable-model-invocation: true.
Body, one line in effect: call the grilling skill.

skills/productivity/grilling/SKILL.md (near 30 lines):
Treat the plan as a decision tree. Ask in numbered rounds.
Put a recommended answer under each question.
Write nothing until the user confirms.""") + """
<p>The design lesson is the split: the name a human types stays tiny, and the procedure lives in one discipline skill that many entry points can share. grill-with-docs adds one act per talk: shared terms land in a CONTEXT.md glossary, and decisions land as records in docs/adr/, so the talk compounds into repo state.</p>
<h2>Named skills, one line each</h2>
""" + steps([
 "tdd: red, green, refactor, one vertical slice at a time.",
 "diagnosing-bugs: build a feedback loop that goes red on the bug, minimise, hypothesise, instrument, fix, regression test. Each phase gates the next.",
 "to-spec: turn the current talk into a spec on the issue tracker. No interview in this skill.",
 "to-tickets and implement: implementation drives tdd at seams agreed in advance and closes with a code review before the commit.",
 "code-review: two axes, Standards and Spec, run as parallel sub agents.",
 "triage: move issues through a state machine of triage roles.",
 "Setup: one setup skill per repo asks three facts: the issue tracker, the triage labels, and the docs location.",
 "Install forms: the official plugin market, or the skills CLI with a version pin.",
]) + """
<p>One correction to round 1 of this guide: no handoff skill exists in the repo. The word names a pattern inside the grill pair, stub to procedure, not a skill. The profiles page of this site stands corrected by this page.</p>
<h2>Superpowers: the mandatory loop</h2>
""" + steps([
 "Brainstorming first, with design shown in chunks for sign off.",
 "Worktree setup: an isolated workspace and a clean test baseline.",
 "Writing plans: tasks of 2 to 5 minutes, exact file paths, complete code in the plan, and a verification step per task. The plan reads for a junior engineer with no project context, by design.",
 "Execution in one of two forms: a fresh sub agent per task with review after each task, or inline execution in one context with one final review.",
 "TDD inside execution: red, green, refactor. Code written before its test gets deleted.",
 "Code review between tasks. Critical findings block the next task.",
 "Branch finish: verify tests, then merge, PR, keep, or discard, and clean the worktree.",
 "Sub agent development carries a two stage review: spec compliance first, code quality second.",
 "Failure path: a diagnosis skill reads the session transcript and reports with line level evidence.",
]) + """
<h2>Caveman: measured, with the vendor label on</h2>
<p>The repo now holds a six part system: voice rules, input compression for logs and test output, an auto model and effort picker, a code mode that keeps and reruns agent scripts, waste fixes, and browse control. Voice rules: answer first in the form thing, action, reason, next step; one idea per sentence; meaning words stay exact (not, never, numbers, units); payload stays verbatim. Levels run from the base mode to two stronger forms. All savings figures in the README come from the vendor own runs and tests. Treat them as claims to test on your own work, never as facts. One figure worth a personal test: input compression cut input tokens by a third across six synthetic large output tasks, with all answers right.</p>
""" + apply_block("Your skill use maps to the Pocock split at once. Your standing orders act as user invoked skills: a named entry, a short body, and calls into discipline procedures such as STE lint, watermark clean, and visual audit. The grill pair gives you the shape for your own plan gate: a grill command that asks numbered rounds with a recommended answer per question, and writes nothing until you confirm. That one skill, run before each multi day build, kills the mid build scope restate cycle you flagged on the exam builds.") +
check_block([
 "Split one of your repeat procedures into a stub entry plus a discipline skill, Pocock form.",
 "Write your grill command this week. Use it before the next multi day build.",
 "Adopt the two stage review for agent built work: spec compliance, then quality.",
 "Test caveman input compression on one log heavy task. Measure on your own bill.",
]) + """
<p>Prompt file: <a href="../prompts/grill-session.md">prompts/grill-session.md</a>.</p>""")

# ---------------- 12. PODCASTS ----------------
deep("deep-podcasts.html", "Deep Dive: Podcast Systems, Compound Engineering and Voice to Issue",
"Four transcript grade systems from How I AI and AI and I: Klaassen compound engineering in full, the Cora voice to issue pipeline, the Reddit feature capsule, and the Notion spec system. Confidence: High for the first two, Medium for the last two.",
"""<h2>Compound Engineering: the four stage loop</h2>
<p>Kieran Klaassen, How I AI, full transcript. The loop: Plan, Work, Assess, Compound. Each stage feeds the next, and the compound stage writes learnings that the next plan reads. The claim under the system: the tool gets better at your codebase each cycle, since the learnings live in files the planner searches.</p>
<h2>Plan stage, in detail</h2>
""" + steps([
 "Three research sub agents run in parallel, each in a fresh context: codebase patterns, web best practice, and frameworks with the versions in use. On screen counts in the episode: 35k to 77k tokens per sub agent.",
 "A spec flow analyzer walks the plan as named user personas and hunts for missing pages and flows.",
 "Plan exits: open in an editor and read, deepen the plan with all skills loaded, send the plan to an agent review, or start work.",
 "Plan edits happen in talk. His case: a plan with many small tools became one update settings tool after one challenge round. Cheap here, costly after build.",
]) + """
<h2>Work stage</h2>
<p>Clear the session first: the plan holds the state. Start the work command with the plan pasted or pulled from the tracker. The flow asks clarifying questions where the plan runs thin, builds its own execution plan, then builds and writes tests.</p>
<h2>QA with video proof</h2>
<p>The agent drives Chrome through the flow, records video of the whole run, and pins the video to the PR. The human can order an hour of break attempts: the agent tries to break the flow, fixes finds in place, and revalidates. For flows with no system test, he signs in by hand once and tells the agent to test inside the live session.</p>
<h2>Assess stage: personas and to dos</h2>
""" + steps([
 "Reviewer personas run in parallel: his own view, security, architecture, code simplicity, agent native fit, and one named style persona.",
 "Findings merge into one story with three grades: P1 never merge, P2 fix soon, P3 nice to have.",
 "Findings land as files in a to dos folder. A status line shows the open count.",
 "No auto fix. A triage talk walks the human through each finding for an approve or reject call.",
 "Approved finds go to a resolve command: a dependency graph, parallel sub agents, one PR out.",
]) + """
<h2>The LFG command and the taxonomy</h2>
<p>One command runs the full flow end to end for near an hour: plan, work, test, review, a product video, a changelog, and the PR. His taxonomy, worth a copy: slash commands hold business logic that a human triggers on purpose, and commands can call commands. Sub agents hold work where only the result matters, and a human never calls one direct, always through a command. Skills hold just in time knowledge, and a skill description must state capabilities, since trigger text alone fires unreliably. His skill rule: agents write skills through a create skill command, humans read and review them, nobody hand writes skills.</p>
<h2>Cora: voice to issue</h2>
<p>From the AI and I full transcript: a dictated rough idea enters a fixed command pipeline. Stage 1 grounds the idea in the codebase. Stage 2 researches best practice on the web. Stage 3 presents a plan for human review. Stage 4 files a GitHub issue with five parts: problem statement, solution vision, requirements, technical requirements, implementation steps. Six or seven pipelines ran at once during the recorded call. The command itself came from a meta pipeline: a seed prompt in a chat model, run through a prompt improver, saved as the reusable command. Two rules carry the system: fix problems at the lowest value stage, since an error caught in the plan costs least; and prompt evals are tests for prompts, run a prompt ten times, and where it fails, rewrite the prompt until the pass holds.</p>
<h2>Reddit Proto and the Feature Capsule</h2>
<p>Blair Metcalf, How I AI, full timestamped transcript. Proto hides git: name a project, the app clones the repo and loads the design system scaffold. Real production data renders inside prototypes. Annotations on a prototype go to the coding tool as a file with code location, component, and request per note. The Feature Capsule path runs Figma to production: copy a frame location, the MCP walks the design token and component map, checks the map against CI and engineer feedback, and writes a PRD with goal, acceptance criteria, and frame links. Approval saves the capsule, the coding tool builds in a sibling repo, and a draft PR returns. Near 700 prototypes sit in their internal board, with full adoption across design and product.</p>
<h2>Notion: specs as source of truth</h2>
<p>Ryan Nystrom episode, from show notes and a structured write up, Medium confidence. Three systems: a standup agent that fills a fixed pre read from the last 24 hours of chat, tasks, PRs, and telemetry; a mention agent that takes a task note plus a screenshot and returns a PR with verification screenshots and a preview link in near 20 minutes; and repo spec files in plain English with code pointers and verification steps, where an edit to the spec plus a pointer to the agent ships the change. His named limit: CI speed caps agent speed, in math terms.</p>
""" + apply_block("Compound engineering is your build system with names on. Your lanes plan, build, audit, and at times lose the lesson. Add the compound stage as a hard step: each lane ends by writing learnings into a solutions folder with front matter, and each plan stage starts by searching that folder. The Cora pipeline fits your idea flow: dictate a build idea, ground it in the repo, research, review the plan, and file a task card with the five parts. Your study and paper queues become issue shaped, and any agent can pick one up cold.") +
check_block([
 "Add a solutions folder with front matter to your main build repo. End each lane with one learning file.",
 "Build your voice to issue command: ground, research, plan, file. Five parts per issue.",
 "Add reviewer personas to your audit step: security, architecture, simplicity, plus your STE and visual rules as two more.",
 "Write one prompt eval: run your most used prompt ten times, log the fails, rewrite until clean.",
]) + """
<p>Prompt files: <a href="../prompts/compound-plan.md">prompts/compound-plan.md</a> and <a href="../prompts/voice-to-issue.md">prompts/voice-to-issue.md</a>.</p>""")

# ---------------- 13. TAN ----------------
deep("deep-tan.html", "Deep Dive: Lauren Tan Fleet and the Bot Method",
"The richest X source in the sweep: a 15 bot roster, runtime verification with blind evals, and a four step bot design method from her own article. Sources: workshop analysis with artifact checks, her X article via transcription, and podcast reports. Confidence: Medium. Output numbers are her self reports.",
"""<h2>The roster</h2>
""" + pre("""1 Chief of Staff
3 Managers
11 Execution Assistants
Total: 15 named AI assistants

Her output claims, self reported:
near 1,000 PRs merged in one month
near 800 PRs in the first 12 days of one month
20 PRs auto merged overnight, clean on post merge check
600 plus PRs on one migration to an agent friendly
architecture with a 5 layer enforcement list""") + """
<h2>The core technical claim</h2>
<p>An AI that writes code is not a loop until it can run the code. Runtime verification makes autonomy safe. Her open source plugin set holds verification skills that create and maintain a check per surface, and the checks run under blind evals: workspace paths in disguise and cross model judges, so the agent under test cannot game the eval it can see. Two commands compose in her system: one builds a feature, one updates the feature map, and a maintenance command catches map drift.</p>
<h2>Benny: the bug bot pattern</h2>
<p>A named bot watches the bug channel. On a report, the bot boots a cloud desktop, reproduces the issue, and compares behavior against main. The same loop runs on alerts: a metric threshold fires, a bot reproduces on its own machine, finds the fault, and writes a fix. A second worked case ran inside one Slack thread of near 200 messages: a cloud agent with its own machine prototyped a feature and posted videos and screenshots back, the human never opened the editor, and the team reviewed artifacts in place of a diff.</p>
<h2>The bot design method, from her article</h2>
""" + steps([
 "Name the goal: what the work is for. Her warning: most people name the process, a form or a mail, in place of the goal.",
 "Brain dump the process by voice: the steps, the tools, where facts come from, and how the work gets checked.",
 "Make the bot restate the goal and the process before it starts. A wrong restate costs one message. A wrong run costs a day.",
 "Set the routine: a trigger on a mail, a message, or a schedule. With no routine, a bot works only when asked, and the fleet decays to a chat toy.",
 "Her designer bot builds new bots after a short preference talk. Design bar from the listing: coding bots get one job, clean output, verified. Other bots get one job, one voice, explicit anti jobs, and no leftover tools.",
]) + """
<h2>The Sanchez rules, with the accounting flag</h2>
<p>Codie Sanchez runs a public bot experiment with three rules: no work by her after setup, a hard spend cap, and cash or real savings only as the score. The reusable systems from the walkthroughs: a finder bot that dedupes leads into a sheet, a drafter bot that writes outreach and holds each draft for her approval, and a flipping chain with a cost check before any money moves. The flag, stated plain: the headline return counts booked calls at estimated pipeline value, not cash, which breaks her own third rule. Take the structures. Leave the score.</p>
""" + apply_block("Your agent fleet holds the Tan shape in part: named lanes with one job each. Two adds pay at once. One: runtime verification as a skill per surface, with blind evals on your audit lanes, since your auditors and builders can share context in ways that let a weak build pass. Two: the restate step as law for every lane start: the lane restates goal, process, and check in its first message, and you correct the restate in place of correcting the output a day later. Her anti jobs line also sharpens your lane cards: name what a lane must never do, in the card, next to the job.") +
check_block([
 "Add a restate block to your lane card template: goal, process, check, anti jobs.",
 "Build one verification skill for your most shipped surface. Add a blind variant.",
 "Give each standing bot a routine trigger. A bot with no trigger gets a schedule or a cut.",
]) + """
<p>Prompt file: <a href="../prompts/chief-of-staff-bot.md">prompts/chief-of-staff-bot.md</a>.</p>""")

# ---------------- 14. MODS + EVALS ----------------
deep("deep-mods-evals.html", "Deep Dive: Claude Mods, the Supervisor, and Hamel Eval Method",
"Three systems that watch the work: mods as harness middleware, a supervisor mod with measured costs, and the error analysis first eval method. Sources: Latent Space Claude Mods post read in full, Hamel Husain evals FAQ structure and method summaries. Confidence: High for mods, Medium for the eval method detail.",
"""<h2>What a mod is</h2>
<p>A mod is a Claude Code plugin made of TypeScript or JavaScript functions that run inside the tool. Mods act as middleware for the harness: they see events such as a prompt, a tool call, or a render, and they can observe the event, change the render, or handle the event in place of the default act. The post frame: as models absorb the machine side of the harness, the human side stays: when the agent interrupts you, what it shows, and which calls it brings to you. A built in skill teaches the tool to build mods, so a user asks in plain words and the tool writes the mod.</p>
<h2>The six built in mods</h2>
""" + steps([
 "agents-md: loads AGENTS.md as project instructions.",
 "diff: takes over the diff view and draws its pane.",
 "plugin-authoring: the skill the tool uses to write mods.",
 "sec-default: guards org managed settings from user mods.",
 "telemetry: sends the analytics records the tool and its mods log.",
 "you-should-know: a side agent that posts a note over the prompt when it finds a fact you may have missed. The one mod off by default.",
]) + """
<h2>You Should Know: the worked case</h2>
<p>A user asked the agent to simplify UI text. The agent trimmed copy, installed the build, and took before and after screenshots. The side agent then flagged a buried fact: the edited file plus near 45 more files held uncommitted work, so a discard of the demo edits would have cut real unfinished work. Advice: commit or stash first. The pattern is a watcher with one job: surface the material fact the main thread buried.</p>
<h2>The Next Steps Supervisor, with its own numbers</h2>
""" + steps([
 "Trigger: the mod runs only after a turn that edited files, ran commands, or made 8 plus tool calls.",
 "Act: the mod forks the talk, reads the fork, and returns a verdict: concerns such as shortcuts taken, plus a next step as a button that sends the instruction as a message.",
 "Noise cost, from the author own data: the mod fired on 99 of 111 turns.",
 "Token cost: each check forks and re reads the talk, near 5 to 6k input tokens per check on a 50k token session, more on a stale cache.",
 "Trust cost: a mod runs with your permissions. It can read and write files, see each prompt, and spend your usage. Mods are not sandboxed, in the author words. Built in mods run even in safe mode.",
 "Control: a command turns the supervisor off. The deeper control is source access: the author can rewrite his trigger terms, and you can rewrite yours.",
 "His worth test for any watcher: did it surface a fact you would have missed, make a call easier, or let you act with no distraction.",
]) + """
<h2>Thariq mods: three from Anthropic staff</h2>
<p>From the Latent Space episode notes, Medium confidence: a supervisor run as a forked sub agent, which keeps the check out of the main context and holds the prompt cache, so checks stay cheap; an assumption register that logs what the agent takes as given; and an internal model router. His stated views: prompt craft stays the core skill, a rule file may fade over time, and one file per model is a pain the vendor plans to end.</p>
<h2>Hamel eval method: error analysis first</h2>
""" + steps([
 "Read outputs by hand first: near 30 minutes on 20 to 50 traces after each large change. One domain expert acts as the quality judge of record.",
 "Open code the failures: name each failure mode as it shows, group the names, refine until the groups stop changing.",
 "Judge in binary: pass or fail with a written critique. No 1 to 5 scales.",
 "Fix the errors the read found. Only then build automation.",
 "Build the judge prompt against the human labeled set. Validate on held out data with true positive and true negative rates. Iterate the judge like a product.",
 "Keep three levels apart: fast unit checks on each change, human plus model review on samples, and A/B tests late only. Guardrails block in line. Evaluators measure off line. The two never swap jobs.",
 "Budget claim from the source: 60 to 80 percent of build time goes to error analysis and evaluation.",
]) + """
<h2>Willison sub agent rules, the short form</h2>
<p>From the one guide chapter read in full in round 3: a sub agent is a fresh copy with a fresh context and prompt, called like a tool, and the parent waits for the return. Parallel sub agents buy speed and can run cheaper models. Specialist forms: a reviewer, a test runner that hides bulk output and reports failures only, and a debugger. His warning: do not over fragment. The value is context care and token heavy work off the main thread.</p>
""" + apply_block("Your audit lanes are supervisor mods in spirit, with one gap: no trigger terms and no cost count. Copy the supervisor design with your numbers: a watcher that fires only on turns with file edits or 8 plus tool calls, returns concerns plus one next step, and logs its fire rate and token cost per week. A watcher that fires on 9 of 10 turns gets its trigger rewritten or cut, by the author own test. Pair it with the Hamel order in your eval work: hand read 20 to 50 outputs, name the failure modes, judge in binary, and only then let a judge prompt scale the read.") +
check_block([
 "Write trigger terms for your audit watcher: edits, commands, or 8 plus calls.",
 "Log fire rate and token cost for one week. Rewrite the trigger if the rate tops half of turns.",
 "Run one Hamel pass on your next lane output: 20 traces, named failure modes, binary calls.",
 "Keep one watcher job only: surface the buried material fact. No second job.",
]) + """
<p>Prompt file: <a href="../prompts/quiz-gate.md">prompts/quiz-gate.md</a> holds the review gate form that pairs with this page.</p>""")

# ---------------- DEEP INDEX ----------------
deep("deep.html", "Deep Dives Index",
"Replication grade pages built from round 3 primary extraction: full text posts, repo files, and podcast transcripts. Each page holds steps, commands, file structures, a worked walkthrough, a checklist, and an application to your work.",
"""<h2>The pages</h2>
""" + steps([
 '<a href="deep-reed.html">Reed spec pipeline</a>: spec, prompt plan, todo, and the mise task system.',
 '<a href="deep-hashimoto.html">Hashimoto system</a>: six steps, the end of day routine, and the Ghostty AGENTS.md in full structure.',
 '<a href="deep-ball.html">Ball and Amp</a>: self waking agents, the proof demand, Orbs, and instruction evals.',
 '<a href="deep-gastown.html">Gas Town</a>: all roles and commands, plus a solo lite form.',
 '<a href="deep-litt.html">Litt</a>: the surgeon model and the explain diff skill, full structure.',
 '<a href="deep-ronacher.html">Ronacher setup</a>: tool rules, the Makefile log pattern, stack picks with reasons.',
 '<a href="deep-yan.html">Yan news agents</a>: code level multi agent build with FastMCP and tmux.',
 '<a href="deep-cherny.html">Cherny</a>: the 13 practices, team tips, Lenny principles, and the YC ablation method.',
 '<a href="deep-openai-harness.html">OpenAI harness</a>: map rule file, docs system, layer law, doc care agent.',
 '<a href="deep-anthropic.html">Anthropic systems</a>: research swarm, best practice ladder, the C compiler harness.',
 '<a href="deep-repos.html">Skill repos</a>: Pocock, Superpowers, and Caveman file systems.',
 '<a href="deep-podcasts.html">Podcast systems</a>: compound engineering, voice to issue, the feature capsule, Notion specs.',
 '<a href="deep-tan.html">Lauren Tan fleet</a>: the 15 bot roster, blind evals, and the bot design method.',
 '<a href="deep-mods-evals.html">Mods and evals</a>: harness middleware, the supervisor numbers, and the Hamel method.',
]) + """
<h2>How to use this set</h2>
<p>Read one page. Run its checklist on a live task the same day. The pages cross link to prompt files in the repo prompts folder, each a full template you can paste and adapt. Depth beats coverage here: one system in your hands beats fourteen in your notes.</p>""")

# ---------------- PROMPT FILES ----------------
PF = {
"spec-pipeline.md": ("Spec Pipeline (Reed and Osmani form)",
"""Purpose: turn a rough idea into spec.md, prompt_plan.md, and todo.md.
Inputs: IDEA (one paragraph), constraints, definition of done.
Run in a strong chat model first, then a reasoning model.

STEP 1 PROMPT (idea honing):
Ask me one question at a time about the idea below until the idea
is fully specified: user, scope, data, edge cases, and what done
means. Then compile the answers into a developer-ready spec and
save it as spec.md.
IDEA: <paste>

STEP 2 PROMPT (plan):
Read spec.md. Produce prompt_plan.md. Each step is a single prompt
in a code block. Each prompt stands alone: it names the files, the
behavior, and the test for that step. Break each step down twice.
No step may leave code that no later step integrates.

STEP 3 PROMPT (state):
Can you make a todo.md that I can use as a checklist? Be thorough.
One line per plan step, in plan order.

EXECUTION RULE: paste one prompt at a time. Run its test. Check the
todo item. Never paste two steps in one message.
VERIFY: spec holds no open question; plan steps each name a test;
todo count equals plan step count.
STOP: any step that leaves orphan code means the plan is wrong.
Fix the plan, not the code."""),
"end-of-day-agents.md": ("End of Day Agents (Hashimoto form)",
"""Purpose: end the day with agents that hand you a warm start.
Inputs: today project list, open issues, one vague idea.
Time box: 30 minutes. Reports only. No public replies by agents.

PROMPT A (survey), one per option:
Survey <LIBRARY OR OPTION> for <USE>. Return: what it does,
pros, cons, recent activity, license, community sentiment,
and a fit call for our stack with one reason. Cite sources.

PROMPT B (probe), one per vague idea:
Attempt <IDEA> as a throwaway spike in a scratch folder.
Goal is light, not a ship. Return: what worked, what broke,
the shape of a real build, and a kill or keep call.

PROMPT C (triage), via the gh CLI:
Read open issues and PRs for <REPO>. Return a report only:
group by theme, flag near certain agent wins, name the human
only items, and draft no public text.

MORNING RULE: filter reports to slam dunks. Run one win at a
time in the background. Notifications off. Check at breaks.
VERIFY: each report names sources and a call. No agent posted
in public.
STOP: a probe that needs a design call stops and reports."""),
"fleet-day.md": ("Fleet Day (Cherny form)",
"""Purpose: run a parallel fleet day with plan mode and proof.
Inputs: task list, repo rule file, verify commands.

SETUP:
1. One worktree or checkout per task. Name tabs by task.
2. Each session starts in plan mode. Prompt:
   Do not write code yet. Plan <TASK>. Name files, steps,
   risks, and the check that proves each step.
3. Review each plan. Edit until the plan reads right.
4. Switch to auto accept. Let the plan one shot the build.
5. End prompt for each session:
   Prove this works. Run <VERIFY COMMAND> and show the output.
   Then run the code simplifier pass on your own diff.

RULES:
- A correction ends with: Update your CLAUDE.md so you don't
  make that mistake again.
- Bugs: paste the report thread, add the word fix, let the
  agent run the repair end to end.
- Long tasks: name a stop limit in turns and a check at end.
VERIFY: each task ends with command output or a screenshot,
never a claim.
STOP: a session that fails its check twice returns to plan mode."""),
"fleet-review.md": ("Fleet Review (reviewer personas form)",
"""Purpose: review one change set with parallel persona reviewers.
Inputs: DIFF or PR link, spec or task card.

Run five reviewers in parallel, each returns findings only:
1. Spec reviewer: does the change match the task card, line by
   line? Name each gap.
2. Security reviewer: input paths, auth checks, secret handling,
   data exposure. Name file and line.
3. Architecture reviewer: layer order, dependency direction,
   duplicate abstractions.
4. Simplicity reviewer: code that can shrink, dead branches,
   needless options.
5. Rules reviewer: project rule file, style gate, test state.

MERGE RULE: findings merge into one list, graded:
P1 never merge. P2 fix before next task. P3 log it.
No auto fix. The human triages. Approved fixes go out as
parallel tasks with the finding text attached.
VERIFY: each finding names a file, a line, and a fix.
STOP: a reviewer with no findings states the areas it read."""),
"explain-diff.md": ("Explain Diff (Litt gist structure)",
"""Purpose: one self contained HTML explainer for a code change,
with a quiz gate. Built on the structure of Geoffrey Litt
public explain-diff skill gist.

PROMPT:
Please make me a rich, interactive explanation of the specified
code change: <DIFF OR PR>.
Write with the clarity and flow of Martin Kleppmann.
Structure, in this order:
1. Background: the system around the change. A deep background
   for a beginner first, then a narrow background on the exact
   area the change touches. Explore the code wide first.
2. Intuition: the essence before the detail. Concrete examples
   with toy data. Diagrams in number, from a small set of
   diagram families. No ASCII diagrams.
3. Code: walk the change grouped by idea, in reader order,
   never in file order.
4. Quiz: five questions, medium difficulty, real understanding,
   no gotchas. Each answer gives right or wrong feedback at
   once, with a note on why.
Format: one self contained HTML file, CSS and JS inside, one
long page, section headers, table of contents, no tabs.
Code in pre tags. Save outside the repo with a name that
starts with today date in YYYY-MM-DD- form.
GATE: the human reads the explainer before the raw diff and
passes the quiz before the change ships."""),
"compound-plan.md": ("Compound Plan (Klaassen form)",
"""Purpose: plan with research sub agents, then compound learnings.
Inputs: TASK, repo, learnings folder (docs/solutions).

PLAN PROMPT:
Plan <TASK>. First, run three research passes in parallel:
Pass 1: codebase patterns for this area, with file names.
Pass 2: web best practice, with sources.
Pass 3: frameworks and libraries in use, with versions.
Then walk the draft plan as these personas: <PERSONA LIST>.
Name missing pages, flows, and edge cases.
Return one plan: steps, files, tests, and open questions.

WORK RULE: clear the session. Start work from the plan alone.
The work pass asks its open questions first, then builds.

COMPOUND PROMPT (run at task end, always):
Write the learnings from this task into docs/solutions as one
file per learning, with front matter: title, area, keywords,
date. Check the folder first: extend a near match, never
duplicate. Name: the trap, the fix, and the check that proves it.

VERIFY: the next plan on a near task cites a learning file.
STOP: a plan with an open question that changes scope stops
for a human call before work starts."""),
"voice-to-issue.md": ("Voice to Issue (Cora form)",
"""Purpose: turn a dictated rough idea into a filed issue.
Inputs: voice transcript, repo, board lanes.

PIPELINE PROMPT:
Take this rough idea: <TRANSCRIPT>
Stage 1, ground: research the codebase. What exists near this
idea? Name files and current behavior.
Stage 2, research: search the web and open source for best
practice on this problem. Cite sources.
Stage 3, plan: present a plan for my review. Ask what a good
product manager would ask, with two options per open point.
Stage 4, file: on my approval, create the issue with five
parts: problem statement, solution vision, requirements,
technical requirements, implementation steps. File it in the
<LANE> lane.

EVAL RULE: run this command on ten sample ideas. Where the
output fails the five part form, rewrite this prompt until
the pass holds ten of ten.
VERIFY: the issue stands alone. A developer can build from
the issue with no chat history."""),
"research-swarm.md": ("Research Swarm (Anthropic form)",
"""Purpose: one lead, parallel sub agents, a judged synthesis.
Inputs: QUESTION, source rules, effort class.

LEAD PROMPT:
Plan research on <QUESTION>. Split the question into
independent parts. For each part, write a sub agent brief:
objective, output form, tool and source guidance, borders.
Effort class: <simple: 1 agent, 3 to 10 calls |
comparison: 2 to 4 agents, 10 to 15 calls each |
complex: 10 plus agents, split duties>.
Start wide, then narrow. Run sub agents in parallel.

SUB AGENT RETURN FORM:
Findings in claim form. Each claim: the claim, the source,
the date, and a confidence word. End with gaps.

JUDGE PROMPT (one call per final answer):
Score this answer 0.0 to 1.0 and pass or fail on each:
fact accuracy, citation accuracy, completeness, source
quality, tool efficiency. Name the weakest criterion and
the exact fix.
VERIFY: a human spot reads 3 claims against sources.
STOP: two sub agents with the same part means the split
was wrong. Replan before more calls."""),
"harness-loop.md": ("Harness Loop (OpenAI form)",
"""Purpose: self review loop with docs as the system of record.
Inputs: TASK, repo with a map rule file and a docs tree.

LOOP PROMPT:
Take <TASK>. Open a branch. Before code, read the map file
and the docs it points to for this area.
Build the change. Then review your own diff as three
reviewers in turn: spec fit, layer order, test proof.
Answer each review note with a fix or a reason. Loop until
all three reviewers pass.
Record the run in the plan file: steps done, calls made,
open debt. If a doc no longer matches the code, fix the doc
in the same branch.

RULES:
- Dependencies flow one way: Types, Config, Repo, Service,
  Runtime, UI. Cross cutting parts enter via Providers only.
- Prefer the shared utility package over a hand rolled helper.
- No YOLO data probing: validate at the boundary or use the
  typed SDK.
VERIFY: the PR holds the change, the plan log, and any doc fix.
STOP: escalate only on a judgment call, with the options named."""),
"grill-session.md": ("Grill Session (Pocock grilling form)",
"""Purpose: sharpen a plan by interview before any build.
Inputs: PLAN draft, decision areas.

PROMPT:
Grill me on this plan: <PLAN>
Treat the plan as a decision tree. Ask in numbered rounds,
one round at a time. Under each question, put your
recommended answer and one line of reason.
Cover in order: goal and done form, scope borders, data and
sources, build order, checks and gates, risks and kills.
Write nothing until I confirm the full set of answers.
On my confirm, write the answers into the plan file and a
glossary of shared terms into CONTEXT.md.

VERIFY: each decision area holds one answer with no open
branch. The plan file changed, not only the chat.
STOP: a question I cannot answer becomes a research task,
named in the plan, before the build starts."""),
"doc-swarm.md": ("Doc Swarm (Yan form)",
"""Purpose: split a source set across sub agents, merge to one file.
Inputs: SOURCE LIST file, sub agent instruction file, templates.

MAIN PROMPT:
Read the source list. Split it into <N> near equal chunks.
For each chunk, spawn one sub agent with this message:
You are Agent <NUMBER>. Read the instructions at
<PATH/sub-agent.md> and execute it. Here are the sources
to process: <CHUNK>
Wait for all reports. Then read the part files and merge
into <OUTPUT FILE> in the merge template form.

SUB AGENT RULES (in the instruction file):
Process one source in full before the next. Write each part
to the parts folder in the part template form. Errors return
as text in the part file, never as a silent skip. End with a
completion line: sources done, sources failed, and why.
VERIFY: part count equals source count. The merge names each
failed source in a gaps section.
STOP: a chunk with half its sources failed stops the merge
for a human call."""),
"chief-of-staff-bot.md": ("Chief of Staff Bot (Tan method)",
"""Purpose: design one bot by the goal, process, restate, routine
method from Lauren Tan article on Grok Bot automation.

SETUP TALK:
1. Goal, in one line: what the work is for. Not the form,
   not the mail, not the sheet. The outcome.
2. Process brain dump, by voice: the steps, the tools,
   where facts come from, and how the work gets checked.
3. Restate: the bot repeats the goal and the process in its
   own words before any run. Correct the restate, not the run.
4. Routine: name the trigger. A mail, a message, or a schedule.
   No trigger, no bot.

BOT CARD (save as a file):
Name: <BOT NAME>
One job: <JOB>
Anti jobs: <WHAT IT MUST NEVER DO>
Inputs: <SOURCES>
Check: <HOW OUTPUT GETS VERIFIED>
Approval gate: <WHAT WAITS FOR A HUMAN>
Routine: <TRIGGER>

VERIFY: the first run output passes the named check with no
human repair.
STOP: a bot that needs daily rescue gets a redesign talk,
not more prompts."""),
"proof-demand.md": ("Proof Demand (Ball form)",
"""Purpose: replace a status claim with a proof artifact.
Inputs: the change, the claim, the surface.

PROMPT:
Give me irrefutable proof that this works now: <CLAIM>
Set up what you need in a throwaway environment. Return:
1. The exact steps you ran.
2. Screenshots, video, or a test matrix that shows the
   behavior, before and after where a change is claimed.
3. The raw command output for each check.
4. A list of what you did not test.

WAKE FORM (for deploys):
In <TIME>, check again: deploy state, error rates, and the
user visible behavior of <SURFACE>. Report proof or the
defect, with the artifact attached.

VERIFY: a human can re-run step 1 from the report alone.
STOP: proof that rests on the agent own summary text fails.
Artifacts or it did not happen."""),
"gas-town-lite.md": ("Gas Town Lite (solo form)",
"""Purpose: town discipline with no town software.
Inputs: goal list, worker sessions, one ledger file.

LEDGER FORM (one markdown file):
## <PREFIX>-<NUMBER> <TASK TITLE>
State: open | running | gated | done | killed
Worker: <SESSION NAME>
Gate: <CHECK THAT MUST PASS BEFORE MERGE>
Notes: <ONE LINE, UPDATED AT EACH CHECK IN>

COORDINATOR PROMPT (at each check in):
Read the ledger. For each running task: read the worker last
output, name its state in one word (working, stalled, zombie,
gated), and act by rule: stalled gets one nudge, zombie gets
a restart from the ledger notes, gated waits for the human.
Merges run one at a time, gate first.
Escalation: P0 stop all work. P1 coordinator decides.
P2 log and continue.

VERIFY: the ledger alone can restart any task after a full
session loss.
STOP: two workers on one file means the split was wrong.
Replan the split."""),
"quiz-gate.md": ("Quiz Gate (Litt usage rule form)",
"""Purpose: gate a merge or a ship on real understanding.
Inputs: the explainer page for the change (see explain-diff).

FLOW:
1. The reviewer reads the explainer, not the raw diff.
2. The reviewer answers the five quiz questions in writing,
   with no source open.
3. Score: 5 of 5 ships. 4 of 5: the missed area gets a
   re-read of that explainer section and a retest.
   3 or under: the explainer is wrong or thin. Fix the
   explainer first, then retest.
4. Log the score next to the change record.

AUTHOR RULE (for the explainer writer):
Questions test the change: why it exists, what breaks
without it, the data path, the edge case, and the rollback.
No gotchas. Each wrong answer in the key names the trap it
tests.
VERIFY: scores exist for the last ten changes.
STOP: a change with no explainer gets no quiz and no ship,
unless the human waives in writing in the change record."""),
}
for fname,(title,body) in PF.items():
    open(os.path.join(PROMPTS_DIR, fname),"w").write(f"# {title}\n\n{body}\n")
    print("prompt file", fname)
print("V5 build complete")
