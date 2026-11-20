#!/usr/bin/env python3
import html, re, os
OUT = os.path.expanduser("~/workspace/learning-agentic-site/site")
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

CSS = """/* Hallmark pre-emit critique: P4 H4 E4 S4 R5 V4 */
:root{
 --paper:#f7f5f0; --paper2:#efece4; --ink:#16150f; --muted:#55534a; --line:#d8d3c3;
 --accent:#9a3412; --accent2:#1e4d3b; --codebg:#ece8db; --warnbg:#fdf0d5; --warnline:#b45309;
 --font-display: Georgia, 'Times New Roman', serif; --font-body: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; --font-mono: ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){
 :root{ --paper:#101010; --paper2:#181818; --ink:#f2efe6; --muted:#b8b3a4; --line:#333028; --accent:#f0a35e; --accent2:#7fc8a9; --codebg:#1e1d18; --warnbg:#2a2110; --warnline:#f0a35e; }
}
*{box-sizing:border-box}
html,body{overflow-x:clip;background:var(--paper);color:var(--ink)}
body{margin:0;font-family:var(--font-body);font-size:17px;line-height:1.65}
a{color:var(--accent);text-underline-offset:3px}
a:hover{color:var(--accent2)}
header.top{border-bottom:2px solid var(--ink);padding:18px 20px 12px;max-width:1080px;margin:0 auto}
.wordmark{font-family:var(--font-display);font-weight:700;font-size:20px;letter-spacing:.02em}
.wordmark a{color:var(--ink);text-decoration:none}
nav.main{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:14px}
nav.main a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:2px;white-space:nowrap}
nav.main a[aria-current]{border-bottom:2px solid var(--accent);font-weight:700}
main{max-width:1080px;margin:0 auto;padding:28px 20px 60px}
h1{font-family:var(--font-display);font-style:normal;font-size:42px;line-height:1.12;margin:0 0 14px;overflow-wrap:anywhere;min-width:0}
h2{font-family:var(--font-display);font-style:normal;font-size:27px;line-height:1.25;margin:38px 0 10px;border-top:1px solid var(--line);padding-top:22px}
h3{font-size:19px;margin:24px 0 6px}
p{margin:0 0 12px;max-width:72ch}
.lede{font-size:20px;line-height:1.5;max-width:62ch}
.meta{color:var(--muted);font-size:14px}
table{border-collapse:collapse;width:100%;margin:14px 0 22px;font-size:15px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--paper2)}
code{font-family:var(--font-mono);background:var(--codebg);padding:1px 5px;font-size:.92em}
pre{font-family:var(--font-mono);background:var(--codebg);padding:14px;overflow-x:auto;font-size:14px;line-height:1.5}
ol,ul{max-width:72ch}
li{margin-bottom:6px}
.badge{display:inline-block;border:1px solid var(--ink);padding:0 7px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap}
.badge.low{border-color:var(--warnline);color:var(--warnline)}
.callout{border:1px solid var(--warnline);background:var(--warnbg);padding:14px 16px;margin:18px 0;max-width:72ch}
.callout p{margin:0}
.rule{border-left:4px solid var(--accent2);padding:4px 0 4px 14px;margin:16px 0;max-width:72ch}
.toc{columns:2;column-gap:40px;font-size:15px}
footer.site{border-top:2px solid var(--ink);max-width:1080px;margin:0 auto;padding:18px 20px 40px;font-size:14px;color:var(--muted)}
@media(max-width:640px){h1{font-size:32px}.toc{columns:1}body{font-size:16px}}
"""

NAV = [
 ("index.html","Home"),("grok.html","Grok"),("claude.html","Claude"),("gemini-antigravity.html","Gemini and Antigravity"),
 ("codex.html","Codex and dots"),("muse.html","Muse"),("cross-cutting.html","Cross-cutting"),("profiles.html","Profiles"),
 ("prompts.html","Prompt Vault"),("principles.html","Principles"),("sources.html","Sources"),
]

def page(fname, title, lede, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==fname else ""}>{t}</a>' for h,t in NAV)
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} - Learning Agentic AI Engineering</title>
<link rel="stylesheet" href="assets/style.css"></head>
<body>
<header class="top"><div class="wordmark"><a href="index.html">Learning Agentic AI Engineering</a></div>
<nav class="main">{nav}</nav></header>
<main>
<h1>{html.escape(title)}</h1>
<p class="lede">{lede}</p>
{body}
</main>
<footer class="site">AI Power-User Intelligence Hub. Build date: 20 November 2026. Every material claim links to a source on the Sources page. A claim with a Low badge rests on one self reported source. A gap marked INSUFFICIENT_EVIDENCE has no verified source in this build.</footer>
</body></html>"""
    with open(os.path.join(OUT, fname), "w") as f: f.write(doc)

def tutorial(q, facts, concepts, patterns, conflicts, hypotheses, decision, action):
    return f"""<h2>Tutorial in eight parts</h2>
<h3>1. Question</h3><p>{q}</p>
<h3>2. Key facts</h3><p>{facts}</p>
<h3>3. Core concepts</h3><p>{concepts}</p>
<h3>4. Patterns and feedback loops</h3><p>{patterns}</p>
<h3>5. Conflicts and common errors</h3><p>{conflicts}</p>
<h3>6. Hypotheses</h3><p>{hypotheses}</p>
<h3>7. Decision support</h3><p>{decision}</p>
<h3>8. One bounded next action</h3><p>{action}</p>"""

with open(os.path.join(OUT,"assets","style.css"),"w") as f: f.write(CSS)
print("css done")

# ---------- INDEX ----------
page("index.html","What power users do that regular users do not",
"Answer first. Power users run fleets of agents under a strict harness. Regular users run one chat and judge one answer.",
"""<p>The difference has five parts. Each part has support in more than one lab.</p>
<ol>
<li><strong>Fleets, not chats.</strong> Five to fifteen parallel sessions or bots run at once. Boris Cherny runs five terminal sessions and five to ten web sessions. Grok Bot runs named bots on one shared cloud computer. Muse Code workflows can run up to 1,000 child tasks over a workflow life.</li>
<li><strong>Harness over answers.</strong> A short instruction file acts as a table of contents. Path rules, skills, hooks and linters carry the detail. OpenAI calls this pattern harness engineering.</li>
<li><strong>Self check oracles.</strong> Tests, screenshots, screen records and verify scripts let an agent prove a result. No oracle means no safe loop.</li>
<li><strong>Agent to agent review.</strong> A fresh context reviewer checks work from a writer agent. The reviewer did not write the code, so bias stays low.</li>
<li><strong>Compounding corrections.</strong> Each correction turns into a rule file line, a lint rule, a skill or an eval case. The system learns in files, not in chat memory.</li>
</ol>
<div class="callout"><p>Convergence fact. Three labs shipped the same product shape in about seven weeks: Meta Muse on 8 September 2026, OpenAI dots on 29 September 2026, and Claude Duet on 21 October 2026. Grok Bot beta came earlier, on 11 August 2026, as a team variant of the same shape. Each product gives one user a cloud computer, works while the user stays away, and asks before a hard to reverse act.</p></div>
<h2>Latest versions dashboard, November 2026</h2>
<table><tr><th>System</th><th>Status in source</th><th>Confidence</th></tr>
<tr><td>Grok model</td><td>Grok 4.7, model id grok-4.7, 21 September 2026. Grok 5 has no release in sources.</td><td>High</td></tr>
<tr><td>Grok Bot</td><td>Beta 11 August 2026. Version 1.0 reported 11 November 2026.</td><td>Medium</td></tr>
<tr><td>Claude models</td><td>Fable 5.2 and Mythos 5.2 on 9 November 2026. Opus 5.5 on 22 September. Sonnet 5.5 on 28 September.</td><td>Medium to High</td></tr>
<tr><td>Claude Code</td><td>Official changelog has a 19 November 2026 entry. A tracker lists 2.1.325 on 13 November. Exact latest patch stays open.</td><td>High for date, Medium for number</td></tr>
<tr><td>Claude Duet</td><td>Research preview 21 October 2026. US waitlist. Built on Opus 5.5.</td><td>High</td></tr>
<tr><td>Gemini model</td><td>Gemini 4 Argon GA 13 October 2026. Gemini 4 Carbon announced 28 October 2026. Gemini 3.5 Pro never shipped in API lists.</td><td>High, Medium Low for cancel word</td></tr>
<tr><td>Antigravity</td><td>Antigravity 2.0. Standalone app, IDE, CLI and SDK. Projects set agent scope.</td><td>Medium to High</td></tr>
<tr><td>Codex</td><td>CLI 0.169.0 on 13 November 2026 per official changelog index. Exact default model stays contested. Pin a model in config.</td><td>Medium to High</td></tr>
<tr><td>OpenAI dots</td><td>Launched 29 September 2026 at DevDay. Powered by GPT-6 Astra per launch reports.</td><td>High</td></tr>
<tr><td>Meta Muse agent</td><td>Launched 8 September 2026 in the US. iOS, Android and muse.ai.</td><td>High</td></tr>
<tr><td>Muse models</td><td>Muse Wonder and Wonder Full on 12 October 2026. Spark Open weights on 15 October 2026.</td><td>Medium</td></tr>
<tr><td>Muse Code</td><td>Meta terminal coding agent. Docs cover subagents, worktrees, workflows and skills import.</td><td>Medium to High</td></tr>
</table>
<p class="meta">Full source links sit on the <a href="sources.html">Sources page</a>, rows 1 to 60.</p>
<h2>Site map</h2>
<div class="toc"><p><a href="grok.html">Grok and Grok Bot</a>. Bots, DeepSearch and business fleets.</p>
<p><a href="claude.html">Claude, Claude Code and Duet</a>. The steering stack and the Cherny fleet.</p>
<p><a href="gemini-antigravity.html">Gemini and Antigravity</a>. Agent Manager, Artifacts and goal loops.</p>
<p><a href="codex.html">Codex and dots</a>. Harness engineering at one million lines.</p>
<p><a href="muse.html">Muse</a>. Meta personal agent, Muse models and Muse Code. Muse is a Meta product. No Apple product named Muse appears in sources.</p>
<p><a href="cross-cutting.html">Cross-cutting</a>. MCP, skills, solo stacks and vibe coding guardrails.</p>
<p><a href="profiles.html">Power user profiles</a>. Who does what, with flags on weak claims.</p>
<p><a href="prompts.html">Prompt Vault</a>. Ten plus prompts and patterns, each with a badge.</p>
<p><a href="principles.html">Engineering principles</a>. Harness, loop, graph and verification rules.</p>
<p><a href="sources.html">Sources</a>. The full ledger and library.</p></div>
<h2>Top five surprise patterns</h2>
<ol>
<li>Top teams ban acts that humans value. One team bans most code comments and one React hook for agents, and turns each ban into a lint rule.</li>
<li>Skills became a cross vendor format in one year. One SKILL.md folder loads in tools from Anthropic, OpenAI, Google, Meta and Cursor.</li>
<li>Model names lost value as durable facts. Two announced flagships, Gemini 3.5 Pro and Grok 5, had no release in sources by 20 November 2026.</li>
<li>Pull request volume lost value as a quality metric. Credible teams report revert rate, eval pass rate and release rate.</li>
<li>Attention became the scarce resource. Morning briefs, exception alerts and output compression all protect human attention, not model tokens alone.</li>
</ol>
""")

# ---------- GROK ----------
page("grok.html","Grok and Grok Bot",
"Grok power use starts with mode choice and bot design. One catch all bot fails. Named specialist bots with approval gates win.",
"""<h2>Version facts</h2>
<p>Grok 4.7 shipped on 21 September 2026 with a 500k token context. Price in official release notes sits at 2 dollars input and 6 dollars output per 1M tokens under a 200k prompt. Source row 2 on the Sources page. <span class="badge">High</span></p>
<p>Grok 4.1 shipped on 17 November 2025. Official xAI post gives a 64.78 percent win rate over the prior model in blind live tests. Source row 1. <span class="badge">High</span></p>
<div class="callout"><p>Grok 5 gap. No Grok 5 release, spec or date has a verified source in this build. Tracker claims about Grok 4.8 tests stay unverified. <span class="badge low">INSUFFICIENT_EVIDENCE</span></p></div>
<h2>Features regular users miss</h2>
<ul>
<li>Model picker and reasoning effort. Auto mode hides the choice. Power users pick a model and set effort to xhigh for hard work.</li>
<li>DeepSearch for live web and X search with citations. Think mode for single chain work. Heavy mode for parallel agent work at the top tier.</li>
<li>Teach a task. A user records a screen task once. The bot turns that record into a repeatable skill.</li>
<li>Browser computer use with no API. Bots can run tools such as Google Forms through a browser session.</li>
<li>Shared computer risk. All bots share one machine, one browser session and one login pool per official guide summaries. Bots do not form a security boundary.</li>
</ul>
<h2>Workflow G1. Internal product and engineering ship loop</h2>
<ol><li>A product manager states a goal in Grok Bot.</li><li>Grok Bot splits the goal. Three primitives guide the split: attention list, research across customer context, and ship work.</li><li>Cursor Cloud Agents take code tasks. Grok Bot reads agent transcripts and tool calls, and nudges or stops agents.</li><li>Agents open pull requests. Grok Bot tracks each request to merge.</li><li>Humans review exceptions only.</li></ol>
<p>Claim in source: Grok Bot holds a double digit share of internal merged pull requests. One event transcript carries that claim. <span class="badge low">Low to Medium, single source</span></p>
<h2>Workflow G2. Lauren Tan team ship loop</h2>
<ol><li>Turn each repeat error into a lint rule or a structural limit. Do not leave the fix in a doc note.</li><li>Run parallel specialist agents under poteto-mode playbooks. Steps stress reproduce first, small blast radius, test driven work and runtime proof.</li><li>Ask the agent for a screen record as proof for user interface work.</li><li>Let agents merge own pull requests.</li><li>Watch revert rate as the quality governor.</li></ol>
<p>Talk slides report about 11,000 team pull requests in October 2026 and a revert rate near 0.5 percent. Company report only. No independent audit sits in sources. <span class="badge low">Medium Low</span></p>
<h2>Workflow G3. Codie Sanchez finder and drafter bot pair</h2>
<ol><li>Bot Dora finds qualified Austin business owners each day through Google and LinkedIn.</li><li>Dora checks HubSpot first. A check stops duplicate outreach.</li><li>Dora writes name and email rows to a sheet.</li><li>Bot Brody drafts one personal mail per prospect. Each draft names the real business and area.</li><li>Brody saves drafts only. No auto send takes place.</li><li>A human approves or edits drafts each morning.</li></ol>
<p>Outcome claim in her own reel on 13 November 2026: 10 replies and 2 calls in 24 hours, with 15 bots in total. Self report only. The durable pattern has value apart from the numbers: finder bot, drafter bot, human gate. <span class="badge low">Low</span></p>
<h2>Workflow G4. Five bot money test, with a failure case</h2>
<p>A third party summary of her YouTube test gives five bots a 100 dollar budget each. A trade bot lost money and shut down. Marketplace flip bots made about 88 dollars net with heavy labour. A past buyer bot and a lead bot made net gains. Lesson in source: a flawed process fails faster under automation. Validate a process by hand first. <span class="badge low">Low</span></p>
<h2>Workflow G5. Distribution before product</h2>
<ol><li>Sell an idea to three people before a build decision.</li><li>Build a lead magnet from unique data you own.</li><li>Capture mail before a purchase stack exists.</li><li>Post organic work on X first. Add paid ads only after organic creative works.</li></ol>
<p>Source: one founder notes summary of a Galaxy broadcast talk. <span class="badge low">Medium Low, single source</span></p>
""" + tutorial(
"How can one person run a research and outreach system on Grok Bot without loss of control?",
"Grok Bot bots persist on one shared cloud computer. Bots keep work up with a laptop closed. Bots message each other and join group chat. Official guide summaries warn that bots share one login pool.",
"Bot, job, tool access, approval boundary, report cadence. One bot holds one job. A boundary names acts that need a human tap: send, pay, sign, delete.",
"Brief, run, report, approve, compound. Each cycle ends with a report. Each error adds a rule to the bot brief or a check to the workflow.",
"A common error treats bots as staff with no audit need. Routines need audit. A second error uses one bot for all jobs. Context and errors mix, and quality drops.",
"A specialist bot fleet may beat one strong bot on mixed business work. Sources show the pattern in use. No independent test compares both forms head to head.",
"Use Grok Bot for research, outreach drafts and monitor work with clear gates. Use a coding agent with a repo and tests for code work. Do not give a bot send or pay rights on day one.",
"Build one finder bot this week. Give the bot one source, one sheet, one dedupe check and a draft only rule. Review 20 rows by hand. Fix the brief once. Then add a drafter bot."
))

# ---------- CLAUDE ----------
page("claude.html","Claude, Claude Code and Duet",
"Claude power use rests on a steering stack. Each layer loads at a set time, costs a set amount of context, and holds a set level of force.",
"""<h2>Version facts</h2>
<p>Anthropic homepage index lists Fable 5.2 and Mythos 5.2 on 9 November 2026, Opus 5.5 on 22 September, Sonnet 5.5 on 28 September and Haiku 5.5 on 7 October. Price summaries list Fable at 8 and 40 dollars, Opus at 4 and 20, Sonnet at 2 and 10 per 1M tokens. <span class="badge">Medium to High</span></p>
<p>Claude Code official changelog has a 19 November 2026 entry. A tracker lists version 2.1.325 on 13 November 2026. Exact latest patch stays open. <span class="badge low">INSUFFICIENT_EVIDENCE for exact patch</span></p>
<p>Claude Duet launch date: 21 October 2026. Duet runs on its own virtual machine, builds on Opus 5.5, sends a morning brief, checks apps each few hours, and asks before send, pay, sign or delete acts. Plan list sources disagree on Ultra. <span class="badge">High for product shape</span></p>
<h2>The steering stack, from the official Anthropic guide</h2>
<table><tr><th>Method</th><th>Load time</th><th>Use</th></tr>
<tr><td>Root CLAUDE.md</td><td>Session start, always</td><td>Keep under 200 lines. Own the file. Review the file as code.</td></tr>
<tr><td>Subfolder CLAUDE.md</td><td>On demand</td><td>Local rules for one area.</td></tr>
<tr><td>Rules in .claude/rules</td><td>Path match</td><td>Rules with a paths frontmatter field apply to one path set only.</td></tr>
<tr><td>Skills</td><td>Name and short text at start, body on call</td><td>Repeat procedures with low base context cost.</td></tr>
<tr><td>Subagents</td><td>Own context</td><td>Only the final message returns. Nest depth can reach five levels per guide.</td></tr>
<tr><td>Hooks</td><td>Life cycle events</td><td>Deterministic acts. A PreToolUse hook can deny a tool call. Hooks bypass compaction.</td></tr>
<tr><td>Output styles</td><td>System level</td><td>Highest weight. Use with care.</td></tr>
</table>
<h2>Workflow C1. Boris Cherny parallel fleet</h2>
<ol><li>Run five Claude sessions in parallel in a terminal. Number tabs 1 to 5. System alerts name the session that needs input.</li><li>Place each session in a separate git checkout or worktree.</li><li>Run five to ten more sessions on the web app. Move a local session to web with the ampersand key. Bring a session back with a teleport flag.</li><li>Start sessions from a phone app.</li><li>Use the strongest model with full thought for agentic work. Principle in source: steer less, gain speed in the end.</li><li>Turn any task done more than once a day into a slash command. Team example: a commit, push and pull request command in .claude/commands.</li><li>Add phase subagents. One subagent cleans code after main work. One verify app subagent tests end to end.</li></ol>
<p>Throughput claim: 20 to 30 pull requests per day in podcast reports. <span class="badge low">Low to Medium</span></p>
<h2>Workflow C2. Plan mode to auto accept</h2>
<ol><li>Start a hard task in Plan mode.</li><li>Revise the plan with Claude till the plan earns trust.</li><li>Team variant: Claude A writes a plan. Claude B reviews the plan as a staff engineer.</li><li>Switch to auto accept edits. Let Claude build in one pass.</li><li>On failure, return to Plan mode. Do not push a bad path.</li></ol>
<h2>Workflow C3. CLAUDE.md as team memory</h2>
<ol><li>Keep one shared CLAUDE.md per repo in git.</li><li>Add a lesson after each correction.</li><li>Tag the Claude account in a pull request review to add a lesson in that same pull request.</li><li>Prune the file. Move long or local rules to path rules or skills.</li></ol>
<h2>Workflow C4. Anthropic research pipeline</h2>
<ol><li>A lead agent reads a query and saves a plan to memory. Memory survives context cut.</li><li>The lead spawns parallel subagents. Each subagent holds distinct tools and a distinct path.</li><li>Each subagent compresses finds for the lead.</li><li>The lead builds a synthesis. A citation agent maps claims to sources.</li></ol>
<p>Anthropic internal eval in the official post: a multi agent form beat a single agent form by 90.2 percent. Cost: about 15 times the tokens of chat. Parallel work buys breadth at a token price. <span class="badge">High</span></p>
<h2>Workflow C5. Duet chief of staff loop</h2>
<ol><li>Connect apps such as mail, calendar, drive and customer tools.</li><li>Read a morning brief.</li><li>Approve or reject action items.</li><li>Duet acts in its own virtual machine.</li><li>Duet checks apps each few hours and alerts only on need.</li></ol>
<p>No independent hands on workflow sits in sources. Product acts come from launch reports. <span class="badge">High for launch facts</span></p>
""" + tutorial(
"How can one engineer ship at fleet speed with Claude Code and still trust the code?",
"Cherny fleet facts and the official steering stack sit in sources rows 13 to 18. Plan mode, worktrees, slash commands and verify subagents recur across sources.",
"Worktree, plan, hook, skill, subagent, verify oracle. A worktree isolates one task. A hook enforces a rule with no model choice.",
"Plan, build, verify, correct, compound. Each correction adds a permanent file change. Review uses fresh context.",
"A common error loads all rules at all times. Context cost rises and force drops. A second error asks the writer agent to grade own work.",
"Small teams may gain more from one verify subagent than from five writer sessions. Sources support both acts. No test in sources ranks both acts for a small repo.",
"Start with plan mode, one worktree per task, and a verify step. Add parallel sessions after the verify step holds for two weeks.",
"Add one verify subagent to your repo this week. Give the subagent test commands, a browser check and a rule: report fail with proof, or pass with proof."
))

# ---------- GEMINI ----------
page("gemini-antigravity.html","Gemini and Antigravity",
"Antigravity power use treats the human as an architect. Agents work across editor, terminal and browser, and return Artifacts as proof.",
"""<h2>Version facts</h2>
<p>Gemini 3 Pro and Antigravity launch date: 18 November 2025, official Google post. Gemini 4 Argon GA date in API summaries: 13 October 2026. Gemini 4 Carbon announcement date: 28 October 2026. <span class="badge">High</span></p>
<p>Antigravity 2.0 splits into four parts: a standalone app, an IDE, a CLI named agy, and an SDK. A Project names a folder set. That folder set defines agent scope and rights. <span class="badge">Medium to High</span></p>
<div class="callout"><p>Gemini 3.5 Pro trap. Google announced the model in May 2026. Flash shipped. Pro never sat in API model lists in tracker checks. A Reuters report via one secondary source says Google no longer plans a ship. Treat the word cancelled as a report, not as a Google fact. <span class="badge low">Medium Low</span></p></div>
<p>Named DeepMind engineer personal workflows: no verified source in this build. Google public material sits at product and team level. <span class="badge low">INSUFFICIENT_EVIDENCE</span></p>
<h2>Workflow A1. Agent Manager and Artifacts</h2>
<ol><li>Define a Project. Folders in the Project mark the agent work area.</li><li>Dispatch a task in Agent Manager, not in the editor.</li><li>Agents work across editor, terminal and browser.</li><li>Agents return Artifacts: task lists, plans, screenshots and browser records.</li><li>Comment on an Artifact, on a screenshot or on a record, in place of a fresh prompt.</li><li>Open the editor only for a set diff.</li></ol>
<h2>Workflow A2. Goal loop with an oracle the agent cannot weaken</h2>
<ol><li>Write a contract as tests first. Add a verify script. Start state must fail.</li><li>Give one goal sentence. Name the deliverable, the limits and the pass rule.</li><li>The goal command writes a plan and starts work.</li><li>The agent loops: act, run tests, repair.</li><li>The loop stops at a pass from both test commands.</li><li>Read the Walkthrough Artifact as an audit trail.</li></ol>
<div class="rule"><p>Principle. Autonomy stays safe to the extent that an oracle stays objective and out of agent edit reach.</p></div>
<h2>Workflow A3. Dynamic Workflows</h2>
<ol><li>Describe an outcome.</li><li>The agent reads a run-workflow skill and writes a short Python script with named phases.</li><li>A human reviews and approves the script.</li><li>The script fans work to parallel subagents and collects firm results.</li><li>Work runs in background tasks. The main agent reads logs and gives a summary.</li></ol>
<p>One tutorial source dated November 2026 carries this workflow. Pro and Ultra tiers only per that source. <span class="badge low">Medium Low, single source</span></p>
<h2>Workflow A4. Research to deck with tool chains</h2>
<p>Google October 2026 examples show subagents with a Blender MCP and image tools turn desk photos into a playable 3D track, and parse over 80,000 NASA files into an exec deck with a firm slide template. Vendor demos prove a pattern, not a capability level: chain tools, and use a template as a limit. <span class="badge">Medium</span></p>
<h2>Hidden features and risks</h2>
<ul><li>Thought signatures must persist across multi turn agent calls, or reason quality drops per the official Gemini 3 dev post.</li><li>Grounding with Search can pair with firm outputs for fetch, extract and emit pipelines.</li><li>Review sites report early prompt injection and sandbox faults, a disk loss report, and quota cuts with no notice. Teach least privilege folders, backups and a preview agent.</li></ul>
""" + tutorial(
"How can a solo engineer trust an Antigravity goal loop on a real repo?",
"Agent Manager, Artifacts and Projects sit in official Codelabs and launch posts. The goal loop with tests sits in a GDE sprint codelab.",
"Project, Artifact, oracle, Walkthrough. An Artifact forms review evidence. An oracle forms a pass rule with no agent edit rights.",
"Dispatch, plan, act, test, repair, review Artifact. Comments on Artifacts steer the next loop round.",
"A common error lets an agent edit tests to reach a pass. Lock tests before a run. A second error gives a Project full disk scope.",
"Dynamic Workflows may beat chat loops for repeat fan out work. One source supports the claim set. Treat gains as a test target, not as a fact.",
"Use Antigravity for browser heavy and multi tool work with Artifacts. Use a terminal agent for small repo tasks with a tight test set.",
"Run one goal loop on a toy repo. Write two test files and one verify script. Lock test files. Record time to pass and error count."
))

# ---------- CODEX ----------
page("codex.html","Codex and dots",
"Codex power use rests on one OpenAI post: harness engineering. Humans steer. Agents execute. The repo forms the system of record.",
"""<div class="callout"><p>Dots clarification. Dots is not a Codex file feature. OpenAI dots is an always on personal agent. Launch date: 29 September 2026 at DevDay. Launch reports name GPT-6 Astra as the model. A user can launch dots from Codex or from ChatGPT. <span class="badge">High</span></p></div>
<h2>Version facts</h2>
<p>Codex CLI 0.167.0 came on 6 November 2026 with an agent command centre. Versions 0.168.0 and 0.169.0 came on 13 November 2026. Version 0.169 adds a trust rule: codex exec turns off project config and MCP servers in a folder with no trust, till a trust flag passes. <span class="badge">Medium to High</span></p>
<p>A claim for 0.170.0 on 18 November rests on one secondary tracker. <span class="badge low">Medium Low</span></p>
<p>Default model in Codex stays contested. OpenAI pages disagree on some replacement names per tracker notes. Pin a full model name in config. Do not trust a blog line for a model name.</p>
<h2>Workflow X1. Harness engineering, one million lines, no hand code</h2>
<p>OpenAI reports a five month build from an empty repo. A team of three engineers, later seven, drove Codex to about one million lines and about 1,500 merged pull requests. Hand code count in the post: zero lines. <span class="badge">High, company source</span></p>
<ol><li>Humans steer. Agents execute. An engineer states a task, runs an agent, and lets the agent open a pull request.</li><li>Self review loop. Codex reviews own changes, calls more agent reviews in local and cloud runs, answers all notes, and loops till agent reviewers pass.</li><li>Legible app. The app boots per git worktree. Chrome DevTools links give DOM views, screenshots and page moves as a skill. Logs and traces sit in a per worktree stack, so a prompt such as startup under 800 ms turns into a check.</li><li>Repo as record. Data out of the repo does not exist for the agent. A short AGENTS.md file, near 100 lines, acts as a table of contents to a docs tree. Docs hold design, plans with progress logs, and quality scores.</li><li>Doc care agent. One agent scans for stale docs and opens fix pull requests. Linters check doc freshness, links and form.</li><li>Limits, not steps. Each domain holds fixed layers: Types, Config, Repo, Service, Runtime, UI. Cross acts pass through one Providers face. Linter error text holds fix steps for the agent.</li><li>Merge rule shift. Short life pull requests, few block gates, fast fix for flakes. The post warns: this rule set needs high agent throughput and cheap correction. Low throughput teams must not copy the merge rule.</li></ol>
<p>Single Codex runs in the post work up to six hours on one task.</p>
<h2>Workflow X2. Cloud task and pull request review loop</h2>
<ol><li>Delegate from ChatGPT, GitHub, Slack or a phone. One task gets one cloud sandbox with the repo loaded.</li><li>Review evidence: terminal logs and test outputs with citations.</li><li>Ask for revisions, or open a pull request.</li><li>In a pull request, comment with a codex review command. A focus form names a risk area, such as security regressions.</li><li>Any other codex comment starts a cloud task with the pull request as context.</li><li>Steer review acts with the AGENTS.md file near the files in review. Near files win over far files.</li></ol>
<h2>Workflow X3. Inner loop and outer loop</h2>
<p>Inner loop: AGENTS.md config, code and tests in a local CLI or IDE run. Outer loop: Codex sorts Linear tickets, pre reviews pull requests before a human read, and checks Sentry crashes against recent commits. One livestream write up carries this split, plus a claim of an Android app build in 18 days by four engineers. <span class="badge low">Medium Low</span></p>
""" + tutorial(
"How can a solo engineer copy harness engineering at small scale?",
"OpenAI harness post facts sit in source row 33. Cloud review acts sit in rows 32 and 34.",
"AGENTS.md map, exec plan, layer rule, Providers face, doc care. An exec plan lives in the repo with a progress log and a decision log.",
"Steer, execute, self review, agent review, merge, doc care. Review effort moves from humans to agents first.",
"A common error writes a long AGENTS.md file as a full manual. Agents lose the map. Keep the file near 100 lines and link out.",
"A doc care agent may pay off at 50 docs and waste tokens at 5 docs. Scale the act to repo size.",
"Copy the map, the layer rules and the self review loop first. Add doc care and cloud review after pull request volume grows.",
"Cut your AGENTS.md file to a map this week. Add one docs page per area, one exec plan form, and one lint rule with fix text in the error line."
))

# ---------- MUSE ----------
page("muse.html","Muse, a Meta product",
"Muse is a Meta product set: a personal agent, a model family, and a terminal coding agent named Muse Code. No Apple product named Muse appears in sources.",
"""<div class="callout"><p>Name fix. User prompt said Muse from Apple. Sources show Muse from Meta only. This page covers Meta Muse. <span class="badge">High</span></p></div>
<h2>Agent facts, official Meta post, 8 September 2026</h2>
<ul><li>A user states a goal in the Muse app or in WhatsApp. Muse plans and acts: browser work, forms, mail, travel and talks.</li><li>Work runs after the app closes. Muse returns on a change or on an approval need. Approval comes before mail send or a purchase.</li><li>Muse Secure VM: one cloud virtual machine per person holds the agent, data and credentials.</li><li>Sentinel: a separate agent on the same machine must approve each item Muse sends to the internet. Sentinel asks the user on need.</li><li>Muse never sees passwords or payment data. Credentials sit in secure storage and run with no view for the model.</li><li>An audit trail records acts. Rights sit per app and per act type, and a user can revoke rights at any time.</li><li>Checkout runs through Link by Stripe with a one time card. The real card stays hid.</li></ul>
<p>Muse Confidential VM, with a user held key and no Meta access, had a later this year promise in launch text. Ship status on 20 November 2026 has no verified source. <span class="badge low">INSUFFICIENT_EVIDENCE</span></p>
<p>Price reports in secondary sources: Power at 20 dollars per month and Maximum at 100 dollars per month, with a free tier for most use. <span class="badge">Medium</span></p>
<h2>Model facts</h2>
<p>Muse Spark came on 8 April 2026 as a native multimodal reason model. The agent launch ran on Spark 1.3. Muse Wonder and Wonder Full came on 12 October 2026. Wonder API price in reports: 4 dollars input and 20 dollars output per 1M tokens. Spark Open weights came on 15 October 2026. <span class="badge">Medium</span></p>
<h2>Workflow M1. Goal hand off with approval gates</h2>
<ol><li>State a big goal.</li><li>Muse builds a plan and sorts time and tools.</li><li>Muse acts in its virtual machine over hours or days.</li><li>Muse adds proactive ideas from past notes. Example in launch text: a saved recipe reel turns into a grocery list, a menu with friend diet limits, and invites.</li><li>A user approves send and pay steps from the audit trail.</li></ol>
<h2>Workflow M2. Small business operator loop</h2>
<ol><li>Connect mail, ads and finance tools.</li><li>Muse sorts mail and drafts replies.</li><li>Muse builds ad campaigns and reads finance results.</li><li>An owner approves sends and spend.</li></ol>
<p>One newspaper report covers the 29 September 2026 launch. No independent operator workflow sits in sources. <span class="badge low">Medium Low</span></p>
<h2>Workflow M3. Muse Code multi agent engineering</h2>
<ol><li>Run muse init. The tool writes an AGENTS.md file for session start.</li><li>Commit a git checkpoint before each session. Loop: plan, edit, run, verify.</li><li>Subagents: a lead session spawns child agents with own orders, model, effort and tools in an agents.json file. Isolated child agents get a Muse Code git worktree.</li><li>Workflows: parallel groups, dependent stages and a synthesis step. Docs give a limit of 1,000 child tasks over a workflow life, with a local active child cap of 16.</li><li>Skills cross tools. Muse Code finds skills in own paths and in Claude and Codex skill paths. An import command can pull skills from Claude or Codex sets.</li><li>Observer agents watch one quality axis each, such as memory recall or goal track, and add short notes to the next main turn with no break in flow.</li></ol>
<p>Verbatim prompt from Meta docs sits on the Prompt Vault page.</p>
<p>Demo claim: a Meta WebXR game build cost 1.75 dollars of model use over about four hours of agent run time, with a human on architecture and fixes. Platform post summary only. <span class="badge low">Medium, self report</span></p>
""" + tutorial(
"How can an engineer use Muse Code skills from Claude Code and Codex with no rework?",
"Meta docs list skill find paths for Claude and Codex sets and an import command for both sets. Source rows 41 and 42.",
"agents.json, workflow, observer agent, worktree isolation. A workflow holds groups, stages and synthesis in one firm form.",
"Init, checkpoint, plan, spawn, verify, synthesise. Small tight edits stay on the main agent per docs guidance.",
"A common error treats skill import as proof of full parity. Test each skill in the new tool. Hooks and rights can differ per tool.",
"Skills may form the first true cross tool program format. Muse Code import acts support the claim. Long term parity stays open.",
"Keep one skill source repo. Import to each tool. Run one test task per tool after each skill change.",
"Pick three skills you own. Import each skill to Muse Code. Run one small task per skill and log pass or fail per tool."
))

# ---------- CROSS CUTTING ----------
page("cross-cutting.html","Cross-cutting: MCP, skills, solo stacks",
"Tools differ. Patterns converge. This page holds the shared stack: MCP servers, skills, plugins, guardrails and the solo operator build.",
"""<h2>MCP shortlist with consensus in November 2026 round ups</h2>
<table><tr><th>Server</th><th>Job</th><th>Note</th></tr>
<tr><td>GitHub MCP</td><td>Repos, issues, pull requests, Actions, security alerts</td><td>Remote OAuth or local Docker forms</td></tr>
<tr><td>Playwright MCP</td><td>Browser acts via access snapshots</td><td>Microsoft server. Snapshot form beats screenshot form for agent reads</td></tr>
<tr><td>Chrome DevTools MCP</td><td>Traces, network, console</td><td>Pairs with UI verify work</td></tr>
<tr><td>Context7</td><td>Current library docs per version</td><td>Fixes stale train data on APIs</td></tr>
<tr><td>Filesystem</td><td>File access in allow list folders only</td><td>Reference server, still kept</td></tr>
<tr><td>Vendor servers</td><td>Sentry, Supabase, Figma, Linear, Stripe, Vercel, Notion, Atlassian</td><td>Pick per stack, not per hype</td></tr>
</table>
<div class="callout"><p>Stale tutorial trap. Old reference servers for GitHub, GitLab, Postgres, Puppeteer, Redis, Slack and SQLite sit in archive state. Kept reference core: Filesystem, Git, Fetch, Memory and Sequential Thinking. Year 2026 shift: remote HTTP transport with OAuth beats pasted API keys. Old SSE transport sits in deprecated state.</p></div>
<h2>Config pattern, with placeholder secrets only</h2>
<pre>claude mcp add &lt;name&gt; -- &lt;start command&gt;
claude mcp add --transport http &lt;name&gt; &lt;url&gt;</pre>
<p>Team form: check a .mcp.json file into a repo. All members gain the same tool set. Scope each token to least rights. Read only rights win where a task needs no write act. Never place a real secret in a site, a repo file or a prompt.</p>
<h2>Skills and plugins</h2>
<p>A plugin packs skills, commands, agents, hooks and MCP config for one command install via a marketplace. A skill folder holds one SKILL.md file with a name, a short text and a body. That folder form loads in Claude Code, Codex, Cursor, Gemini CLI, Copilot, Antigravity and Muse Code per sources in this build.</p>
<p>Pocock design rule: user called skills run flow. Model called skills hold discipline. A user called skill can call model called skills. A user called skill must never call a second user called skill. Predictability beats clever chains.</p>
<h2>Repo guide</h2>
<table><tr><th>Repo</th><th>What the repo does</th><th>Install pattern in README</th></tr>
<tr><td><a href="https://github.com/obra/superpowers">obra/superpowers</a></td><td>A full software method for coding agents. Brainstorm, worktree, plan in 2 to 5 minute tasks, subagent build with two stage review, test driven work, review, branch finish.</td><td>Claude Code plugin install from the official marketplace, or from the superpowers marketplace. Install per tool for other tools.</td></tr>
<tr><td><a href="https://github.com/mattpocock/skills">mattpocock/skills</a></td><td>27 skills for real engineers. Grill, spec, tickets, test driven work, bug diagnosis and architecture deep work. Fixes four failure modes: wrong build, word waste, broken code, mud design.</td><td>Plugin install, then one setup command per repo. Setup asks tracker, labels and docs place.</td></tr>
<tr><td><a href="https://github.com/JuliusBrussee/caveman">JuliusBrussee/caveman</a></td><td>Token compression skill, proxy and middleware. Agents say less and read less. Log and test output shrinks before a model read, with full text kept for recall.</td><td>Skills add command, then a caveman command per session. Full install forms sit in README.</td></tr>
<tr><td><a href="https://github.com/Nutlope/hallmark">Nutlope/hallmark</a></td><td>Anti slop design skill. Four verbs: build, audit, redesign, study. Audit scores a target and edits no file. Study pulls design DNA to a portable design file.</td><td>Skills add command per a July 2026 article.</td></tr>
<tr><td><a href="https://github.com/cursor/plugins">cursor/plugins, pstack folder</a></td><td>Lauren Tan playbook set. A poteto-mode front door picks one of 23 playbooks, copies steps to a task list, and fires skills as steps trigger. 34 skills and 24 principles per one README read.</td><td>Cursor plugin add, then a setup command. Claude Code form uses a marketplace add and a plugin install.</td></tr>
<tr><td><a href="https://github.com/modelcontextprotocol/servers">modelcontextprotocol/servers</a></td><td>Official MCP reference servers. Kept core listed in the MCP note on this page.</td><td>Per server start commands in each server README.</td></tr>
</table>
<p>Savings claims for caveman come from repo own tests. Treat all such numbers as vendor claims. <span class="badge low">Low for savings</span></p>
<p>Hallmark theme and gate counts conflict across sources. This site prints the verb model only, no counts.</p>
<h2>Vibe coding to agentic engineering</h2>
<p>Karpathy coined vibe coding in February 2025: describe, accept, watch acts. The 2026 fix in practitioner sources adds a spectrum. Vibe form fits prototypes with optional checks. Agentic engineering adds firm specs, rule files and auto verification.</p>
<p>Google New SDLC frame via a summary: Agent equals Model plus Scaffold. Most teams spend too much on model choice and too little on scaffold.</p>
<p>Guardrail pipeline: spec first, test driven work or oracle tests, linters and type checks and security scans, coverage gates, pre commit hooks and CI, human review of acts and key diffs.</p>
<p>Security note: a guardrail article sums studies with about 40 to 45 percent of AI code in security tests with flaws. Present that range as studies cited by practitioners, not as a count from this site.</p>
<h2>The canonical loop</h2>
<pre>Grill and spec
-&gt; Plan, with a second agent review on hard tasks
-&gt; Execute in a worktree or sandbox
-&gt; Test vs an oracle
-&gt; Review by a fresh context agent
-&gt; Fix loop
-&gt; Ship via pull request and an approval gate
-&gt; Capture the lesson in a rule file, a lint, a skill or an eval</pre>
<h2>Solo one person army stack</h2>
<p>Consensus in four solo founder guides from October and November 2026: one 20 dollar agent plan, GitHub Free, Vercel Hobby and Supabase Free. Total near 20 dollars per month to ship real products. Add paid tiers one layer at a time as limits bite.</p>
<p>Full stack adds that recur: Cursor for edit work, Linear for plans, Stripe for pay, Resend for mail, PostHog for product data, and a research model as a thought partner.</p>
<p>One operator frame: split RAM, disk and GPU roles. RAM: a fast thought partner model. Disk: a file system as the record. GPU: a coding agent run time with custom skills. A file out of the file system does not exist for the system.</p>
<h2>Research pipeline pattern</h2>
<ol><li>Subagents search in parallel and compress finds.</li><li>A lead agent builds a synthesis.</li><li>A separate citation or verify step maps each claim to a source.</li><li>A gap list names claims with no source.</li></ol>
<p>This site used that same pipeline. The Sources page forms the audit trail.</p>
""")

# ---------- PROFILES ----------
page("profiles.html","Power user profiles",
"Each card states an identity check, a workflow with a source, and a flag on weak claims. Two cards carry a clear gap flag by design.",
"""<h2>Boris Cherny</h2>
<p>Creator and head of Claude Code at Anthropic. Workflow: five terminal sessions plus five to ten web sessions, plan mode, shared CLAUDE.md, slash commands, phase subagents and a verify app step. See the Claude page. <span class="badge">High for January 2026 workflow</span></p>
<h2>Lauren Tan, Poteto</h2>
<p>Identity resolved: Poteto is Lauren Tan. Past roles in sources: Meta, Netflix, Cursor, React core team. Role in November 2026 sources: Grok Bot engineering lead at SpaceXAI. Workflow: pstack playbooks, lint rules in place of doc notes, screen record proof, agent self merge, revert rate as governor.</p>
<div class="callout"><p>Personal pull request counts conflict across sources: 1,150 in four days, 2,500 per month, 3,000 per month and 4,000 plus per month all appear, for distinct spans. This site prints no single count as a fact. Team talk numbers sit on the Grok page with a company report flag.</p></div>
<h2>Codie Sanchez</h2>
<p>Founder of Contrarian Thinking. Workflow: named specialist bots, finder to drafter to approval chain, distribution before code, lead magnets from unique data. Outcome numbers in her content stay self reported. <span class="badge low">Low for outcomes, Medium for patterns</span></p>
<h2>Tibo</h2>
<p>Identity: Thibault Louis-Lucas, handle tibo_maker. Past builds: Tweet Hunter and Taplio, with an 8 million dollar exit in interview summaries. Current builds in sources: Revid, Feather, SuperX and Outrank. Workflow: build tools for self first, one ship sprint day per week, large context prompts, AI draft with human polish, firm JSON outputs, high level APIs in place of self host work. <span class="badge low">Medium Low, one interview summary</span></p>
<div class="callout"><p>Identity trap. Tibo is not the TypingMind founder. Tony Dinh built TypingMind as a solo founder. Two men, two cases. Do not merge both cards.</p></div>
<h2>Dario Amodei</h2>
<p>Co founder and chief executive of Anthropic. No personal workflow, config, prompt set or post set sits in sources for this build. Org claims about Anthropic code share sit on the Claude page with a secondary report flag. <span class="badge low">INSUFFICIENT_EVIDENCE for a personal profile</span></p>
<h2>Matt Pocock</h2>
<p>TypeScript educator, Total TypeScript. Repo workflow: grill, spec, tickets, test driven work, review. Shared words via a CONTEXT.md glossary and decision records stop agent drift. See the Cross-cutting page. <span class="badge">High</span></p>
<h2>Mayank Shah</h2>
<p>Identity stays ambiguous. At least four men share this name in sources. Best workflow match: Mayank Shah of Shah Labs. His post flow: start hard tasks in Gemini with a custom Gem that builds firm prompts, then run Claude Code with a CLAUDE.md file, auto memory and a memory plugin, plus skills and plugins per session. Result claims in the post stay self reported, and the post leads to a paid offer.</p>
<p>Flag: no proof sits in sources that Shah Labs is the man in the user prompt. <span class="badge low">INSUFFICIENT_EVIDENCE for identity</span></p>
<h2>Greg Isenberg</h2>
<p>Chief executive of Late Checkout, host of the Startup Ideas Podcast. Two playbooks sit in sources.</p>
<p>Company brain: build a folder that onboards an agent as a sharp new hire. Six files cover buyers, offer and promise limits, brand voice by loved and rejected samples, founder views, and past campaign fails. Rule: agents add guesses to an evidence folder. A human alone promotes a guess to the company folder.</p>
<p>Agent spec: answer seven questions before a build. Wake trigger, context need, tool rights, solo act rights, approval acts, escalation rule, and success proof. Ship a minimum agent in draft and approve mode. Build a 50 sample eval set before scale work. <span class="badge low">Medium Low, summaries of his posts and podcast</span></p>
""")

# ---------- PROMPTS ----------
page("prompts.html","Prompt Vault",
"Verbatim prompts carry a Verbatim badge and a source. Pattern items carry a Pattern badge. A pattern is a summary, never a quote.",
"""<h2>Verbatim, sourced</h2>
<ol>
<li><span class="badge">Verbatim</span> Claude Code review challenge, Cherny team thread transcript: <code>Grill me on these changes and don't make a PR until I pass your test.</code></li>
<li><span class="badge">Verbatim</span> Claude Code proof demand, same source: <code>Prove to me this works</code>. Pair the line with a diff of main vs the feature branch.</li>
<li><span class="badge">Verbatim</span> Claude Code elegance reset, same source: <code>Knowing everything you know now, scrap this and implement the elegant solution.</code></li>
<li><span class="badge">Verbatim</span> Claude Code memory close, same source: <code>Update your CLAUDE.md so you don't make that mistake again.</code></li>
<li><span class="badge">Verbatim</span> Codex pull request command: <code>@codex review</code></li>
<li><span class="badge">Verbatim</span> Codex focus review command: <code>@codex review for security regressions</code></li>
<li><span class="badge">Verbatim</span> Codex fix command form: <code>@codex fix the CI failures</code></li>
<li><span class="badge">Verbatim</span> Muse Code workflow prompt, Meta docs sample: <code>Use a workflow to review this service. Have separate agents inspect the API design, security boundaries, and test coverage. Verify the findings, then return one prioritized report.</code></li>
</ol>
<h2>Commands that act as prompts</h2>
<p><code>/commit-push-pr</code> from the Cherny team set. <code>/grill-me</code>, <code>/grill-with-docs</code>, <code>/tdd</code> and <code>/diagnosing-bugs</code> from Pocock skills. <code>/poteto-mode</code> from pstack. <code>/caveman</code> from caveman. <code>hallmark audit &lt;target&gt;</code> from hallmark.</p>
<h2>Pattern summaries</h2>
<ol>
<li><span class="badge">Pattern</span> Grok DeepSearch brief. Role, task, context, limits, output form. Require a set count of independent recent sources. Require a link and a date per claim. Split firm facts from contested claims. Answer first, evidence next, open points last.</li>
<li><span class="badge">Pattern</span> X pulse check. Ask for a topic scan in a set time window. Ask for top views, tone split, disputed claims, one source post per bullet, and a why it matters line.</li>
<li><span class="badge">Pattern</span> Specialist bot brief. Name one job, one goal, style samples, tool and login rights, an approval boundary in plain words, and a report cadence.</li>
<li><span class="badge">Pattern</span> Plan then execute brief. Goal, limits, and one rule: plan first, no edit till plan approval.</li>
<li><span class="badge">Pattern</span> Antigravity goal brief. One goal sentence with a deliverable, limits, and a pass rule tied to test commands the agent cannot edit.</li>
<li><span class="badge">Pattern</span> Codex exec plan. Goal, repo map link, layer limits, verify commands, and one rule: loop review till reviewers pass. Check the plan into the repo.</li>
<li><span class="badge">Pattern</span> Isenberg agent spec. Seven questions from the Profiles page, in order, before any build work.</li>
<li><span class="badge">Pattern</span> Shah brief rule. Specific beats long. Name the library, the attribute and the exact act, as a brief to a smart new team member.</li>
<li><span class="badge">Pattern</span> Eval set build. Collect 50 real samples. Score each agent run. Count right, flagged and failed rows. Re run the set on each prompt or model change.</li>
</ol>
""")

# ---------- PRINCIPLES ----------
page("principles.html","Engineering principles",
"Ten rules recur across all labs. Each rule names a source cluster on the tool pages.",
"""<ol>
<li><h3>Harness beats model</h3><p>Agent equals Model plus Scaffold. On a weak result, fix tools, form and feedback first. Ask: what skill lacks, and how can a rule make that skill clear and firm? Source: OpenAI harness post.</p></li>
<li><h3>Map, not manual</h3><p>Instruction files act as tables of contents near 100 to 200 lines. Deep docs sit one link away, with an owner and a freshness check. Anthropic and OpenAI reach this rule on own paths.</p></li>
<li><h3>Graph, not chat</h3><p>Work forms a graph: parallel branches in worktrees or sandboxes, dependent stages, one synthesis node. A human runs the graph via alerts and briefs, not node by node chat.</p></li>
<li><h3>Loop with an oracle</h3><p>No loop runs with no firm stop rule. Tests, verify scripts, linters, revert rate and eval sets form stop rules an agent cannot edit.</p></li>
<li><h3>Fresh eyes review</h3><p>A reviewer holds no shared context with an author. Forms: a second model run, a subagent, a fresh context design reviewer, agent to agent review in Codex.</p></li>
<li><h3>Lessons rise to the firmest layer that fits</h3><p>Order: chat note, rule file note, path rule, skill, hook or lint or test. If a doc note fails to stop an error, promote the lesson to code. Source: Poteto team and OpenAI.</p></li>
<li><h3>Approval scales with reversal cost</h3><p>Drafts cost near zero. Send, pay, merge, delete and spend acts wait for a human. All four personal agents and both business bot cases use this gate.</p></li>
<li><h3>Context is the scarce resource</h3><p>Tokens matter. Human attention matters more. Briefs, exception alerts and output compression all guard attention.</p></li>
<li><h3>Speed changes process ethics</h3><p>At agent speed, short life pull requests and cheap fixes can beat heavy gates. That trade holds only with revert and quality data live. OpenAI states this caveat in the harness post.</p></li>
<li><h3>Context and data form the moat</h3><p>All users rent the same frontier models. Compound assets differ: a brain folder, eval sets, skills and unique data. Sources: Isenberg, Sanchez and Pocock cases.</p></li>
</ol>
<h2>Harness model in four parts</h2>
<table><tr><th>Part</th><th>Role</th><th>Sample</th></tr>
<tr><td>Context</td><td>RAM for an agent</td><td>Rule file map, path rules, memory files</td></tr>
<tr><td>Tools</td><td>System calls</td><td>MCP servers, browser, terminal, test runner</td></tr>
<tr><td>Skills</td><td>Programs</td><td>SKILL.md folders, playbooks, slash commands</td></tr>
<tr><td>Evals</td><td>Verifiers</td><td>Tests, verify scripts, eval sets, revert rate</td></tr>
</table>
<h2>Loop form</h2>
<pre>Trigger -&gt; Execute -&gt; Verify vs oracle -&gt; State log -&gt; Stop at pass or at a set round cap</pre>
<p>State log fields per round: cluster, draft version, claim count, gap list. A loop with no state log repeats work and hides drift.</p>
""")

# ---------- SOURCES (parsed from research report ledger) ----------
report_path = os.path.expanduser("~/workspace/research_notes/ai-power-user-intelligence-hub-20261120-1627/report.md")
text = open(report_path).read()
ledger = text.split("### 12.")[1].split("### 13.")[0]
rows = []
for line in ledger.splitlines():
    line=line.strip()
    if not line.startswith("|"): continue
    cells=[c.strip() for c in line.strip("|").split("|")]
    if len(cells)!=6: continue
    if cells[0] in ("#","") or set(cells[0])<=set("- "): continue
    if not cells[0].isdigit(): continue
    rows.append(cells)
print("ledger rows", len(rows))
trs=""
for n, claim, url, author, date, conf in rows:
    url_clean = url.strip()
    trs += f'<tr><td>{n}</td><td>{html.escape(claim)}</td><td><a href="{html.escape(url_clean)}">Source</a></td><td>{html.escape(author)}</td><td>{html.escape(date)}</td><td>{html.escape(conf)}</td></tr>\n'
body = f"""<h2>Source ledger, {len(rows)} rows</h2>
<p>Each row maps one claim set to one source. Ten articles on one press release count as one origin. Confidence text comes from the research report.</p>
<table><tr><th>#</th><th>Claim</th><th>Link</th><th>Author or publisher</th><th>Date</th><th>Confidence</th></tr>
{trs}</table>
<h2>Gap report</h2>
<ul>
<li>Grok 5 and Grok 4.8: no verified release, spec or date.</li>
<li>Claude Code exact patch for the 19 November 2026 changelog entry: no version string in source text.</li>
<li>Codex exact default model on 20 November 2026: OpenAI pages disagree per tracker notes.</li>
<li>Claude Duet plan list: sources split on an Ultra tier.</li>
<li>Named DeepMind engineer personal workflows: none in sources.</li>
<li>Dario Amodei personal workflow: none in sources.</li>
<li>Mayank Shah identity: ambiguous, best match flagged on the Profiles page.</li>
<li>Muse Confidential VM ship status: no verified source.</li>
<li>Independent tests of Grok Bot, Duet, dots and Muse agent quality: none in sources. All quality claims rest on vendor or self reports.</li>
<li>Exact repo links for GitHub MCP, Playwright MCP and Context7: no verbatim link in the report. This site links those tools via round up rows 43 and 44 in the ledger.</li>
<li>Repo star counts: sources conflict. This site prints no star counts.</li>
</ul>
<h2>Library by type</h2>
<p>Official docs and posts: ledger rows 1, 2, 11, 13, 15, 19, 25, 26, 27, 29, 32, 33, 38, 41, 42, plus repo rows 45, 47, 48, 50.</p>
<p>Trade and practitioner articles: rows 16, 17, 20, 43, 46, 55.</p>
<p>Videos, talks and podcasts in sources: Cherny X threads and a Pragmatic Engineer podcast on 4 March 2026, Lauren Tan AI Engineer Code Summit talk in November 2026, Codie Sanchez YouTube test video with id yO5O_ngyA_8 per a summary, Greg Isenberg Startup Ideas Podcast in May 2026, and Grok Bot Galaxy streams on 15 to 17 September 2026.</p>
<p>Social sources: row 8 (Sanchez reel), row 53 (Threads talk summary), row 18 (Cherny thread transcript).</p>
"""
page("sources.html","Sources and gap report","The ledger forms the audit trail for this site. A claim with no row has no place as a fact on a tool page.", body)

# ---------- README ----------
readme = """# Learning Agentic AI Engineering

A source grounded hub on how tier 0 engineers and power users run frontier AI tools in November 2026.

## Site

Open `site/index.html` in a browser. Pages:

- `site/index.html` - answer, versions dashboard, site map
- `site/grok.html` - Grok and Grok Bot
- `site/claude.html` - Claude, Claude Code and Duet
- `site/gemini-antigravity.html` - Gemini and Antigravity
- `site/codex.html` - Codex and dots
- `site/muse.html` - Muse from Meta, Muse models and Muse Code
- `site/cross-cutting.html` - MCP, skills, plugins, solo stacks, guardrails
- `site/profiles.html` - power user profiles with identity flags
- `site/prompts.html` - prompt vault, verbatim vs pattern badges
- `site/principles.html` - harness, loop, graph and verification rules
- `site/sources.html` - 60 row source ledger and gap report

Branch: `build/power-user-hub-v1`. Research date: 20 November 2026.
Claims with a Low badge rest on one self reported source. Gaps marked INSUFFICIENT_EVIDENCE have no verified source in this build.
"""
with open(os.path.join(OUT, "..", "README.repo.md"), "w") as f: f.write(readme)
# site README inside site folder
with open(os.path.join(OUT, "README.md"), "w") as f: f.write(readme)
print("pages built in", OUT)
