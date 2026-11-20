#!/usr/bin/env python3
"""Add harvest walkthroughs. Quotes are copied from files already checked."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAV = (
    '<a href="index.html">Home</a><a href="grok.html">Grok</a><a href="claude.html">Claude</a>'
    '<a href="gemini.html">Gemini</a><a href="codex.html">Codex</a><a href="muse.html">Muse</a>'
    '<a href="cross-cutting.html">Stack</a><a href="profiles.html">Profiles</a>'
    '<a href="principles.html">Principles</a><a href="prompts.html">Prompts</a>'
    '<a href="repos.html">Repos</a><a href="library.html">Library</a>'
    '<a href="method.html">Method</a><a href="tokens.html">Tokens</a>'
    '<a href="talks.html">Talks</a><a href="podcasts.html">Podcasts</a>'
    '<a href="social.html">Social</a><a href="shots.html">Shots</a>'
    '<a href="directory.html">Directory</a><a href="sources.html">Ledger</a>'
    '<a href="gaps.html">Gaps</a>'
)


def page(filename, title, body):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>  <link rel="stylesheet" href="assets/vendor/fonts.css">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="top-row">
    <a class="mark" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1.5" y="1.5" width="29" height="29" fill="none" stroke="#e0b15b" stroke-width="1.4"/><circle cx="16" cy="16" r="3.2" fill="#e0b15b"/></svg> Power User Hub</a>
    <p class="asof">Checked 20 Nov 2026</p>
    <form class="finder" role="search" action="search.html"><label class="sr" for="q">Search</label><input id="q" name="q" type="search" placeholder="Search the hub  (/)"></form>
  </div>
  <nav class="nav" aria-label="Sections">{NAV}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="foot-in"><p><a href="podcasts.html">All episodes</a> · <a href="gaps.html#g22">Harvest gaps</a></p></div></footer>
<script src="js/claims.js"></script>
<script src="js/catalog.js"></script>
<script src="js/site.js"></script>
<script src="assets/vendor/diagrams.js"></script>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


def diagrams(flow, seq, state, mark):
    return f"""
<section class="section" id="page-map">
  <h2>See the shape first</h2>
  <div class="visual-grid">
    <figure class="diagram">
      <figcaption>The step this episode actually states.</figcaption>
      <pre class="mermaid">{flow}</pre>
    </figure>
    <figure class="diagram">
      <figcaption>Files for this page.</figcaption>
      <svg class="markmap-svg" aria-label="Files"></svg>
      <script type="text/markmap">{mark}</script>
    </figure>
  </div>
</section>
<section class="section" id="seq-state">
  <h2>Sequence and state</h2>
  <div class="visual-grid">
    <figure class="diagram">
      <figcaption>Who talks to whom.</figcaption>
      <pre class="mermaid">{seq}</pre>
    </figure>
    <figure class="diagram">
      <figcaption>States worth naming.</figcaption>
      <pre class="mermaid">{state}</pre>
    </figure>
  </div>
</section>
"""


page(
    "podcast-boris-ablation.html",
    "Boris Cherny, delete the instructions: Power User Hub",
    """
  <p class="kicker">YC, 27 Jul 2026</p>
  <h1>Every six months, delete CLAUDE.md, the skills, and the hooks.</h1>
  <p class="lede">Source: <a href="https://www.youtube.com/watch?v=qyPCVqFUyDo">youtube.com/watch?v=qyPCVqFUQy0</a>, transcript in the harvest, captions. Boris Cherny. The captions say "Claude MD". That is the file CLAUDE.md.</p>
"""
    + diagrams(
        """flowchart TD
  A[New model] --> B[Delete CLAUDE.md skills and hooks]
  B --> C[Watch what it does]
  C --> D[Add a line only after a repeated stumble]""",
        """sequenceDiagram
  participant Boris
  participant Prompt
  Boris->>Prompt: delete the system prompt
  Prompt-->>Boris: bring lines back one by one
  Boris->>Boris: every six months delete CLAUDE.md""",
        """stateDiagram-v2
  [*] --> FullPrompt
  FullPrompt --> Ablated
  Ablated --> OneLine: a line earns its place
  OneLine --> [*]""",
        """# Ablation
## delete CLAUDE.md
## delete skills
## delete hooks
## simple mode is spoken not spelled
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What he said</h2>
  <p>At 00:04:29 the captions say they deleted 80 percent of the system prompt. At 00:04:38 he says you can pass a system prompt flag and set whatever system prompt you want. At 00:04:50 he names an undocumented environment variable in speech as "Claude Code simple equals one". Running Claude after that, he says, deletes all the system prompts, including from the tools. The spelling of that variable is the spoken form. This page does not turn it into a guessed name.</p>
  <p>At 00:06:03 he calls the method an ablation: delete the entire system prompt and bring it back line by line. At 00:06:58, for people using Claude Code rather than building it: every 6 months delete your Claude MD, delete your skills, delete your hooks, and see what the model does. At 00:07:14 he says this is what they recommend for Opus 5, because the model might not need the instructions past models needed. <a href="sources.html#C299">C299</a> <a href="sources.html#C300">C300</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p>The prompt is <a href="kit/prompts/boris-ablation.md">kit/prompts/boris-ablation.md</a>. It is a hub instruction that follows his order. It is not a file from Anthropic.</p>
</section>
<section class="section" id="fail">
  <h2>3. Failure modes</h2>
  <ul class="clean">
    <li>Typing a guessed environment variable name. Use the spoken description, or read <code>claude --help</code> on a machine that has the binary.</li>
    <li>Deleting the only copy of a hook that encodes a safety rule you still need. He is talking about instructions the new model may already follow. A deny rule for send or pay is not the same object.</li>
  </ul>
</section>
<section class="section" id="exercise">
  <h2>4. Exercise</h2>
  <p>Copy CLAUDE.md aside. Remove it for one task the model has done before. Self-check: if the task still passes the same test, the file was not earning its place. If it fails in a way you have seen twice, put one line back.</p>
</section>
""",
)

page(
    "podcast-pocock-no-init.html",
    "Matt Pocock, do not run init: Power User Hub",
    """
  <p class="kicker">Matt Pocock, 24 Feb 2026</p>
  <h1>Do not let the agent write the instruction file.</h1>
  <p class="lede">Source: <a href="https://www.youtube.com/watch?v=9tmsq-Gvx6g">youtube.com/watch?v=9tmsq-Gvx6g</a>. The captions spell the file "claw.md" and "agent.mmd". He means the init file a coding agent writes.</p>
"""
    + diagrams(
        """flowchart TD
  A[Agent offers init] --> B[Do not run it]
  B --> C[Delete an agent-written copy]
  C --> D[Keep one fact the agent cannot see]""",
        """sequenceDiagram
  participant You
  participant Agent
  You->>Agent: do not run init
  Agent-->>You: no generated instruction file
  You->>You: one line if a fact is invisible""",
        """stateDiagram-v2
  [*] --> NoFile
  NoFile --> OneFact: repeated blind spot
  OneFact --> [*]""",
        """# No init
## kit prompt
## one invisible fact
## skills for the rest
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What he said</h2>
  <p>At 00:00:10: "I am going to recommend that you never ever run this." The "this" is an init command that writes a claw.md or agents.md of codebase documentation. At 00:00:13: if you find one you think an agent created, delete it. He says the file burns tokens, distracts the agent, and goes out of date. He cites a paper whose conclusion, in the captions, is that unnecessary requirements from context files make tasks harder, and human-written context files describe only minimal requirements. <a href="sources.html#C301">C301</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/pocock-no-init.md">kit/prompts/pocock-no-init.md</a>. Pair it with the TDD skill you already have, which is a file he published, not an init dump.</p>
</section>
<section class="section" id="exercise">
  <h2>3. Exercise</h2>
  <p>If CLAUDE.md or AGENTS.md in a repo was produced by an init command, move it out of the tree and run one task. Self-check: the agent still finds the test command by reading the repo.</p>
</section>
""",
)

page(
    "podcast-pocock-hooks.html",
    "Matt Pocock, block npm with a hook: Power User Hub",
    """
  <p class="kicker">Matt Pocock, 25 Feb 2026</p>
  <h1>A PreToolUse hook exits 2 when the command starts with npm.</h1>
  <p class="lede">Source: <a href="https://www.youtube.com/watch?v=3CSi8QAoN-s">youtube.com/watch?v=3CSi8QAo8d4</a>. He describes the script on camera. This kit file is that description, not a download of his repository.</p>
"""
    + diagrams(
        """flowchart TD
  A[Bash tool call] --> B{Starts with npm?}
  B -->|yes| C[Echo use pnpm not npm]
  C --> D[Exit 2]
  B -->|no| E[Exit 0]""",
        """sequenceDiagram
  participant Claude
  participant Hook
  Claude->>Hook: bash command
  Hook-->>Claude: use pnpm not npm
  Hook-->>Claude: exit 2""",
        """stateDiagram-v2
  [*] --> Allowed
  Allowed --> Blocked: command starts with npm
  Blocked --> [*]""",
        """# Hook
## PreToolUse
## block-npm described
## settings.json
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What he said</h2>
  <p>At 00:04:02 the captions say the script checks whether the command starts with npm as a command. It echoes "use pnpm not npm", then exits with exit code two. At 00:04:15 he runs chmod plus x. At 00:04:20 the configuration is in settings.json, under hooks, Pre-tool use, matching any bash tool, running block npm.sh. <a href="sources.html#C302">C302</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/pocock-block-npm.md">kit/prompts/pocock-block-npm.md</a> records the spoken contract. Do not treat it as his settings.json. The placeholder hook already in <a href="kit/claude/settings.json">kit/claude/settings.json</a> is a different event, PostToolUse.</p>
</section>
<section class="section" id="fail">
  <h2>3. Failure modes</h2>
  <p>A repo that uses npm, not pnpm. The hook he accepted would block the real package manager. Match the script to the tool the repo already uses.</p>
</section>
""",
)

page(
    "podcast-tibo-codex.html",
    "Tibo on Codex sandbox and slash goal: Power User Hub",
    """
  <p class="kicker">Pragmatic Engineer, 9 Sep 2026</p>
  <h1>Local tools stay in the sandbox. Extra permission asks you.</h1>
  <p class="lede">Thibault Sottiaux, <a href="https://www.youtube.com/watch?v=sLSTM9znQNs">youtube.com/watch?v=sLSTM9znQNs</a>. Captions.</p>
"""
    + diagrams(
        """flowchart TD
  A[Tool call] --> B[Local sandbox]
  B --> C{Needs more permission?}
  C -->|yes| D[Ask the user]
  C -->|no| E[Run]
  F[Long task] --> G[slash goal]""",
        """sequenceDiagram
  participant Tibo
  participant Codex
  Codex->>Codex: sandbox
  Codex-->>Tibo: ask if the command leaves the sandbox
  Tibo->>Codex: slash goal for a long run""",
        """stateDiagram-v2
  [*] --> Sandbox
  Sandbox --> Asked
  Asked --> Sandbox
  Sandbox --> Goal""",
        """# Codex
## sandbox
## slash goal
## cloud kata VM
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What he said</h2>
  <p>At 00:32:33: it runs sandboxed. A command that should run with additional permissions outside the sandbox asks the user. Every tool execution happens that way, in the captions' wording. At 00:33:19 he describes a cloud choice: a managed VM, the same VM you get through the chat product, in a kata container. At 01:01:41 he names slash goal for a run that keeps going, and says it was added a few months earlier. <a href="sources.html#C304">C304</a> <a href="sources.html#C305">C305</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p>The sandbox key you can copy is still <code>sandbox_mode = "read-only"</code> in <a href="kit/codex/config.toml.sample">kit/codex/config.toml.sample</a>. Slash goal is a command, not a new config key. The newsletter quote about deletions under full access with no sandbox is <a href="sources.html#C295">C295</a>. His description here is the control that setup did not have.</p>
</section>
<section class="section" id="stack">
  <h2>3. Your stack</h2>
  <p>Keep the sample on read-only until a task names one directory. Do not turn on a mode that skips the ask, on a bank repo, because a course called the equivalent "yolo" on a different product.</p>
</section>
""",
)

page(
    "podcast-antigravity-surfaces.html",
    "Antigravity surfaces and AGY login: Power User Hub",
    """
  <p class="kicker">Google Antigravity, 12 Jun 2026 and 19 May 2026</p>
  <h1>Four surfaces. The CLI sign-in in the captions is AGY login.</h1>
  <p class="lede">Official channel transcripts: <a href="https://www.youtube.com/watch?v=04IqH38SlOI">which surface</a> and <a href="https://www.youtube.com/watch?v=6C0FjHoN3qE">2.0 beginner guide</a>.</p>
"""
    + diagrams(
        """flowchart TD
  A[Antigravity 2.0] --> B[IDE]
  A --> C[CLI]
  A --> D[SDK]
  C --> E[AGY login]
  B --> F[Settings: sandbox and network]""",
        """sequenceDiagram
  participant You
  participant CLI
  You->>CLI: AGY login
  CLI-->>You: signed in
  You->>You: whitelist or reject a command""",
        """stateDiagram-v2
  [*] --> SignedOut
  SignedOut --> SignedIn: AGY login
  SignedIn --> Sandbox
  Sandbox --> [*]""",
        """# Antigravity
## 2.0
## IDE
## CLI
## SDK
## AGY login
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What the captions say</h2>
  <p>The 12 Jun video opens by naming four products launched around Google I/O: Antigravity 2.0, the IDE, the CLI, and the SDK. At 00:07:13 the speaker types, in the captions, "AGY login", because the agent told them to. At 00:08:05 they ask for an Antigravity SDK Python script in a worker directory that takes a city name. The 19 May beginner guide, at 00:03:35, shows accept, reject, and whitelist for commands. At 00:03:56 settings include sandboxing and network permissioning. <a href="sources.html#C306">C306</a> <a href="sources.html#C307">C307</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/agy-login.md">kit/prompts/agy-login.md</a> is the sign-in line as spoken, plus the instruction not to paste the gemini-cli <code>npm</code> commands into your repo. There is still no Antigravity settings file with a commit SHA.</p>
</section>
<section class="section" id="fail">
  <h2>3. Failure modes</h2>
  <p>The captions capitalize AGY. If the binary on your machine is <code>agy</code>, use the spelling <code>agy --help</code> prints. Do not invent a second flag.</p>
</section>
""",
)

page(
    "podcast-muse-code-course.html",
    "Muse Code course: muse init and yolo: Power User Hub",
    """
  <p class="kicker">freeCodeCamp course, 26 Aug 2026</p>
  <h1>muse init writes the project file. Yolo turns the asks off.</h1>
  <p class="lede">Source: <a href="https://www.youtube.com/watch?v=b-P5ZQ1NxxE">youtube.com/watch?v=b-P5ZQ1N3dA</a>. The captions spell the file "agent.mmd" and "agents.mmd". That may be AGENTS.md misheard. This page keeps the caption spelling and does not pretend a file of that name was opened.</p>
"""
    + diagrams(
        """flowchart TD
  A[muse init] --> B[Caption file agent.mmd]
  B --> C[Project rules and commands]
  D[Tired of confirms] --> E[yolo]
  E --> F{bubblewrap installed?}
  F -->|no| G[Full permissions with no sandbox]""",
        """sequenceDiagram
  participant Instructor
  participant Muse
  Instructor->>Muse: muse init
  Muse-->>Instructor: project rules file
  Instructor->>Muse: yolo
  Muse-->>Instructor: no more asks""",
        """stateDiagram-v2
  [*] --> Asking
  Asking --> Yolo
  Yolo --> Unsafe: no bubblewrap
  Asking --> [*]""",
        """# Muse Code course
## muse init
## settings.json
## yolo
## bubblewrap
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What the captions say</h2>
  <p>At 01:49:42 the instructor says Meta chose a generic agents file, spelled "agents.mmd" in one line and "agent.mmd" in the next. At 01:49:51: <code>muse init</code> analyzes the repo and creates that file. At 01:49:58: Muse Code reads the file as project rules and common commands. At 01:55:16 settings live in settings.json, which he cats. At 02:36:44, if you are tired of confirming, "for muse we can do yolo", the equivalent of full permissions, and it will not ask. He says to be careful if bubblewrap is not installed, because that is the sandbox he does not have in that virtual environment. <a href="sources.html#C308">C308</a> <a href="sources.html#C309">C309</a>.</p>
  <p>This is Muse Code, the terminal coding agent. The 16 Sep 2026 How I AI review is a different product: a consumer agent with identity.md and WhatsApp. Do not mix the commands.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/muse-init.md">kit/prompts/muse-init.md</a> records <code>muse init</code> and the yolo warning. Contributor mode off, from the pricing page, still comes first. <a href="kit/prompts/muse-plan.md">muse-plan.md</a> is the plan gate.</p>
</section>
<section class="section" id="stack">
  <h2>3. Your stack</h2>
  <p>Do not run yolo on a bank checkout. The instructor's own caveat is the absence of bubblewrap. The plan gate is the control this hub copies. Yolo is recorded so you can recognize it and leave it off.</p>
</section>
""",
)

page(
    "podcast-lenny-grok.html",
    "Roman Ugarte on Grok Bot routines: Power User Hub",
    """
  <p class="kicker">Lenny's, 8 Sep 2026</p>
  <h1>Define the routine in a sentence. Do not fill a trigger form.</h1>
  <p class="lede">Roman Ugarte, SpaceXAI, <a href="https://www.lennysnewsletter.com/p/how-we-built-grok-bot-in-a-month">lennysnewsletter.com/p/how-we-built-grok-bot-in-a-month</a>. Transcript: the Lenny's VTT in the harvest. Speaker label SPEAKER_01.</p>
"""
    + diagrams(
        """flowchart TD
  A[Competitor form: trigger then action] --> B[People set few routines]
  C[Grok Bot] --> D[Say the automation in a sentence]
  D --> E[99 percent of automations on the platform]""",
        """sequenceDiagram
  participant Roman
  participant Bot
  Roman->>Bot: the routine in plain language
  Bot-->>Roman: the automation exists""",
        """stateDiagram-v2
  [*] --> Unscheduled
  Unscheduled --> Routine: one sentence
  Routine --> [*]""",
        """# Grok routines
## plain language
## not a plus form
## kit prompt
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What he said</h2>
  <p>At 00:29:17 he describes competitors: open a sidebar, press plus, select the trigger, select the action. He calls that clunky, and says people then do not set up many automations. At 00:29:42: Grok Bot's response was that you should define automations in natural language. At 00:29:48 he says that is how 99 percent of automations on the platform get built. The 99 percent is his figure, not an independent count. <a href="sources.html#C310">C310</a>.</p>
  <p>A separate local transcript, How I AI, 2 Sep 2026, has the host's own routine: an hourly sweep of inbox, calendar, and Slack, business hours 6am to 9pm, seven days, not overnight. The whisper file spells the product "Grockbot" in places. <a href="sources.html#C311">C311</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/grok-plain-routine.md">kit/prompts/grok-plain-routine.md</a>. Send stays Needs approval, as in <a href="kit/grok-bot/README.md">kit/grok-bot/README.md</a>. A sentence that includes "post it" is still a send. Do not put send on Always allow to make the sentence shorter.</p>
</section>
""",
)

page(
    "podcast-thariq-html.html",
    "Thariq, plan in HTML: Power User Hub",
    """
  <p class="kicker">How I AI, 18 May 2026</p>
  <h1>Brainstorm in an HTML file, then clear the context and implement that file.</h1>
  <p class="lede">Thariq Shihipar, <a href="https://www.youtube.com/watch?v=Qrpm7E80wQ0">youtube.com/watch?v=Qrpm7E80e7U</a>.</p>
"""
    + diagrams(
        """flowchart TD
  A[Brainstorm in HTML] --> B[HTML plan with excerpts]
  B --> C[Clear context]
  C --> D[Implement the HTML file]
  D --> E[HTML mock is the check]""",
        """sequenceDiagram
  participant Thariq
  participant Claude
  Thariq->>Claude: brainstorm in HTML
  Claude-->>Thariq: plan.html
  Thariq->>Claude: clear context and implement the file""",
        """stateDiagram-v2
  [*] --> HTMLPlan
  HTMLPlan --> Cleared
  Cleared --> Implemented
  Implemented --> [*]""",
        """# HTML plan
## brainstorm
## clear context
## designsystem.html
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What the captions say</h2>
  <p>At 00:09:27 he says brainstorm in HTML. At 00:10:18, after interview questions, create an HTML file as a plan. At 00:26:03 he would clear context and implement that plan. At 00:27:32 the file name in the captions is designsystem.html, passed into later projects instead of a markdown design file. <a href="sources.html#C319">C319</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/thariq-html-plan.md">kit/prompts/thariq-html-plan.md</a>. The check is still a command you run, not the model's summary of the HTML.</p>
</section>
""",
)

page(
    "podcast-cat-wu-verify.html",
    "Cat Wu, teach the agent the test: Power User Hub",
    """
  <p class="kicker">O'Reilly, 29 Apr 2026</p>
  <h1>Write the senior's correction into the instruction file, and add a verify command.</h1>
  <p class="lede">Cat Wu, <a href="https://www.youtube.com/watch?v=qnSuOFXkEH0">youtube.com/watch?v=qnSuOFXkEH0</a>. The captions say QuadMD, QuadCode, and AgentMD. Those are CLAUDE.md, Claude Code, and AGENTS.md misheard.</p>
"""
    + diagrams(
        """flowchart TD
  A[Ask the agent about the code] --> B[Senior corrects it]
  B --> C[Write the correction into the instruction file]
  C --> D[Add a verify command]
  D --> E[Small fixes before large ones]""",
        """sequenceDiagram
  participant Junior
  participant Senior
  participant File
  Junior->>Senior: is this right
  Senior-->>Junior: the nuance
  Junior->>File: one correction
  Junior->>File: verify command""",
        """stateDiagram-v2
  [*] --> Unchecked
  Unchecked --> Corrected
  Corrected --> Verifiable
  Verifiable --> [*]""",
        """# Cat Wu
## senior correction
## verify command
## paper cuts first
""",
    )
    + """
<section class="section" id="mechanism">
  <h2>1. What the captions say</h2>
  <p>At 00:00:36: if the agent is wrong and a senior tells you the nuance, update the instruction file so the next person gets it right. At 00:00:50: new people on the team fix paper cuts, which are smaller than a large change. At 00:01:49: add a verify command, and put it in the instruction file or the README, so the agent can test its work. The spoken product name in this caption file is QuadCode throughout. <a href="sources.html#C303">C303</a>.</p>
</section>
<section class="section" id="artifact">
  <h2>2. Artifact</h2>
  <p><a href="kit/prompts/cat-wu-verify.md">kit/prompts/cat-wu-verify.md</a>. The command you put in the file is one you already run. The bio on X, fetched with the harvest, says she is now at OpenAI and was previously on Claude Code. <a href="sources.html#C314">C314</a> is a different post, about Opus 5.5 as the default.</p>
</section>
""",
)

print("pages done")
