#!/usr/bin/env python3
import html, os, re, glob, json
OUT = os.path.expanduser("~/workspace/learning-agentic-site/site")
NAV = [
 ("index.html","Home"),("start.html","Start Here"),("grok.html","Grok"),("claude.html","Claude"),
 ("gemini-antigravity.html","Gemini and Antigravity"),("codex.html","Codex and dots"),("muse.html","Muse"),
 ("foundations.html","Foundations"),("cross-cutting.html","Cross-cutting"),("business.html","Business"),
 ("research.html","Research"),("profiles.html","Profiles"),("prompts.html","Prompt Vault"),
 ("labs.html","Labs"),("paths.html","Learning Paths"),("principles.html","Principles"),
 ("glossary.html","Glossary"),("sources.html","Sources"),("audit.html","Audit"),("search.html","Search"),
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
<p class="meta"><a href="index.html">Home</a> / {html.escape(title)}</p>
<h1>{html.escape(title)}</h1>
<p class="lede">{lede}</p>
{body}
</main>
<footer class="site">AI Power-User Intelligence Hub, field guide build v2. Execution date: 20 November 2026. Evidence cutoff: 20 November 2026, the earlier of execution day and 30 November 2026. Open site/index.html from disk. No server need. No track code sits in this site.</footer>
<script src="assets/site.js"></script>
</body></html>"""
    with open(os.path.join(OUT, fname), "w") as f: f.write(doc)

# START
page("start.html","Start Here",
"One useful workflow today, a full system in weeks. Pick a route by time, run Lab 1 first, and keep each claim tied to a source.",
"""<h2>Quick start route, about one hour</h2>
<ol><li>Read the Home page answer and the versions dashboard. Ten minutes.</li><li>Read the Foundations page harness table. Ten minutes.</li><li>Run Lab 1 from the Labs page. Fix one bug with a test first flow. Thirty minutes.</li><li>Copy one prompt from the Prompt Vault: the bug from evidence prompt. Use the prompt on Lab 1 code.</li></ol>
<h2>Standard route, two weeks</h2>
<p>One tool page per day in this order: Claude, Codex, Grok, Gemini and Antigravity, Muse. One lab per week end. One prompt type per day from the vault. End state: a repo with a rule file map, one skill, one verify step and one eval set.</p>
<h2>Deep study route, six weeks</h2>
<p>Standard route plus the Research page, the Business page case anatomy work, and a full pass on the Sources ledger. End state: one research pipeline and one business workflow, each with a human gate and a log.</p>
<h2>Task graph for this build</h2>
<pre>Identity checks --&gt; Research per cluster --&gt; Source ledger
        |                    |
        v                    v
   Experiments (Labs) --&gt; Tutorials --&gt; Site build --&gt; Verify --&gt; Audit page
Independent branches ran in parallel: Grok, Claude, Gemini, Codex, Muse, cross-cutting.
Dependent steps ran in order: ledger join, synthesis, build, link check, review.</pre>
<h2>Evidence graph, core claims</h2>
<table><tr><th>Claim</th><th>Relation</th><th>Source or test</th><th>Effect on advice</th></tr>
<tr><td>Fleets beat chats for throughput</td><td>supports</td><td>Cherny workflow, sources rows 16 to 18</td><td>Teach worktrees and parallel sessions</td></tr>
<tr><td>Rule files act as maps</td><td>supports</td><td>OpenAI harness post row 33, Anthropic steering guide row 15</td><td>Keep rule files near 100 to 200 lines</td></tr>
<tr><td>Volume metrics mislead</td><td>contradicts</td><td>Poteto revert rate reports rows 52 and 53 vs pull request counts</td><td>Report revert rate and eval pass rate</td></tr>
<tr><td>Score method ranks retrieval quality</td><td>demonstrates a limit</td><td>Lab 2 run in this build: both methods hit a ceiling at 1.0, no split</td><td>Claim no win for a method. Design a harder test</td></tr>
<tr><td>Grok 5 exists</td><td>supersedes, none</td><td>No release in sources by cutoff</td><td>Mark as a gap, print no spec</td></tr>
</table>
<h2>Learning graph, shortest route per outcome</h2>
<table><tr><th>Outcome</th><th>Route</th></tr>
<tr><td>Ship code with an agent</td><td>Foundations, Claude or Codex page, Lab 1, Prompts: spec, build, review</td></tr>
<tr><td>Run a research pipeline</td><td>Research page, Claude workflow C4, Lab 2, Prompts: synthesis, experiment, eval</td></tr>
<tr><td>Run a business workflow</td><td>Business page, Grok workflows G3 to G5, Lab 3, Prompts: delegation, audit</td></tr>
<tr><td>Build a solo stack</td><td>Cross-cutting page, Paths page standard route</td></tr>
</table>
""")

# FOUNDATIONS
page("foundations.html","Engineering foundations: harness and inference design",
"An agent is a model plus a scaffold. This page names each scaffold part, its failure mode, and a test you can run.",
"""<h2>Harness parts</h2>
<table><tr><th>Part</th><th>Purpose</th><th>Failure mode</th><th>Observable sign</th></tr>
<tr><td>Goal</td><td>Names the outcome and the pass rule</td><td>Vague goal, agent picks own target</td><td>Work drifts, pass claims with no test</td></tr>
<tr><td>State</td><td>Holds task steps, decisions and open points</td><td>State lives in chat only</td><td>A reset loses the plan</td></tr>
<tr><td>Context</td><td>Supplies facts at need time</td><td>Too much stale text, too little key fact</td><td>Agent cites old data or misses a rule</td></tr>
<tr><td>Model</td><td>Reasons and writes</td><td>Weak model on a hard plan step</td><td>Plan errors repeat across samples</td></tr>
<tr><td>Tools</td><td>Act on files, web, tests and apps</td><td>Tool errors pass in silence</td><td>Steps claim done with no artifact</td></tr>
<tr><td>Policy</td><td>Limits acts, spend and rights</td><td>No gate on hard to reverse acts</td><td>Send or delete acts run with no tap</td></tr>
<tr><td>Evaluator</td><td>Checks output vs a firm rule</td><td>Agent grades own work</td><td>Pass claims rise, defects stay</td></tr>
<tr><td>Stop condition</td><td>Ends a loop</td><td>No cap on rounds or cost</td><td>Loops run long with no gain</td></tr>
</table>
<h2>Model, effort, context, cache and parallel work</h2>
<p>A strong model cuts re prompt rounds on hard steps. High reason effort costs time and tokens, and pays on plan and debug steps. Large context holds more facts and adds noise and cost. Cache hits cut repeat cost where a product offers cache reads, as in the Grok 4.7 price split on the Grok page. Parallel work cuts wall time and adds merge and review load. Measure each trade on your own task set. No source in this build gives a universal gain number.</p>
<h2>Why repeat samples repeat one error</h2>
<p>One model with one context holds one set of false beliefs. A fresh sample from that same state tends to keep the belief. New evidence breaks the loop: a test result, a source, a screenshot or a fresh context reviewer. Add a sample for breadth. Add evidence for truth.</p>
<h2>Single agent vs multi agent</h2>
<table><tr><th>Form</th><th>Cost</th><th>Best use</th><th>Risk</th></tr>
<tr><td>Single agent, one worktree</td><td>Low</td><td>Tight tasks, one file set, clear tests</td><td>Slow on breadth work</td></tr>
<tr><td>Writer plus fresh reviewer</td><td>Medium</td><td>Code and research with a check step</td><td>Reviewer needs raw evidence, not a summary</td></tr>
<tr><td>Parallel fleet</td><td>High, near 15 times chat tokens in the Anthropic research case</td><td>Breadth search, many file review, migrations</td><td>Merge clashes, attention load</td></tr>
</table>
<h2>Reference loop in Python</h2>
<p>Copy the loop. Each run writes state, caps steps, stops on a pass from a test the agent cannot edit, and asks a human at hard gates.</p>
<pre>from dataclasses import dataclass, field

@dataclass
class Task:
    goal: str
    state: str = "new"
    steps: list = field(default_factory=list)
    rounds: int = 0

def run(task, agent, verify, max_rounds=5, needs_human=None):
    while task.rounds &lt; max_rounds:
        task.rounds += 1
        task.state = "work"
        result = agent(task)              # one bounded step
        task.steps.append(result)
        ok, proof = verify(result)       # test, lint, or eval set
        if ok:
            task.state = "pass"
            return task, proof
        if needs_human and needs_human(result):
            task.state = "wait_human"    # send, pay, merge, delete
            return task, proof
    task.state = "fail_cap"              # stop, log, replan by hand
    return task, "round cap hit"</pre>
<p>Properties: typed input and output via the Task form, firm state, step cap, check points in the steps list, a human gate, and a clear pass test. Idempotent acts stay a design duty per step: a step that can run twice must check for prior work first.</p>
<h2>Worked example</h2>
<p>Goal: fix a page slice bug. State: one task, rounds 0. Round 1: agent writes a fail test. Verify: test fails as design. Round 2: agent fixes one line. Verify: full test set passes. Stop: pass at round 2. Lab 1 holds this case in full.</p>
<h2>Partial exercise</h2>
<p>Add a retry rule to the loop: retry a tool error once, then stop. Fill in the blank: a tool error must set state to ____ and write the error text to ____.</p>
<h2>Retrieval question</h2>
<p>Which harness part stops a loop with no gain? Answer in the Glossary under Stop condition.</p>
""")

# BUSINESS
page("business.html","Business workflows with AI",
"Business cases in sources automate parts of a firm, not a whole firm. Each case table names the real scope, the human work left, and the claim status.",
"""<h2>Case B1. Sanchez lead system</h2>
<table><tr><th>Part</th><th>Fact from source</th></tr>
<tr><td>Models and face</td><td>Grok Bot bots on one shared cloud computer</td></tr>
<tr><td>Data and tools</td><td>Google and LinkedIn search, HubSpot CRM, a sheet</td></tr>
<tr><td>State</td><td>CRM dedupe check, sheet rows, saved mail drafts</td></tr>
<tr><td>Schedule</td><td>Daily finder runs per her reel</td></tr>
<tr><td>Human review</td><td>All sends wait for approval. Drafts only</td></tr>
<tr><td>Monitor and recovery</td><td>Not in source</td></tr>
<tr><td>Cost</td><td>Not in source</td></tr>
<tr><td>Manual work left</td><td>Draft approval, calls, close work, offer and service work</td></tr>
<tr><td>Claim status</td><td>Outcomes self reported, Low. Pattern value stands apart from numbers</td></tr>
</table>
<h2>Case B2. Isenberg company brain and agent agency</h2>
<p>System: a brain folder with six files, an evidence folder for agent guesses, a human promotion rule, a 50 sample eval set per agent, and draft and approve mode at start. Business form in one podcast summary: a build and manage fee per client per month. Economics in that summary form a sales claim, not a test result. Staff and contractor counts: not in source.</p>
<h2>Case B3. Muse for Small Business</h2>
<p>System per one launch report: mail sort and draft replies, ad campaign builds, finance reads, owner approval on sends and spend. Scope: three task areas in one firm back office. No source shows staff cuts, profit or full firm automation.</p>
<h2>Case B4. Duet and dots as back office agents</h2>
<p>Launch reports show briefs, app checks, draft acts and approval gates for mail, calendar, pay and sign acts. No independent operator case sits in sources by cutoff. Treat both as vendor described capacity, not as a proven business result.</p>
<h2>Entire business claims, scope rule</h2>
<div class="rule"><p>A claim of a full business on AI must name staff, contractors, infra, human hours and the manual steps left. A post with none of that data supports a workflow claim only, at the scope the post shows.</p></div>
<h2>Tutorial: build a cited weekly report workflow</h2>
<ol><li>Pick one report: market scan, lead list or ops digest.</li><li>Write the source list and the claim rule: each claim needs a link and a date.</li><li>Run Lab 3 code on a ledger. Check the confidence split.</li><li>Draft the report from rows with High or Medium-High marks first.</li><li>Flag each Low row for a human check.</li><li>Save the draft and the ledger as one artifact pair. No send act runs till a human tap.</li></ol>
<p>Cost note: model cost per run depends on your plan and token use. This build gives no per run price, since no paid run took place in Lab 3. Lab 3 used local code only, cost zero in model tokens.</p>
""")

# RESEARCH PAGE
page("research.html","Research engineering with AI",
"AI speeds search, synthesis and test runs. Validity comes from design: baselines, controls, provenance and error reads.",
"""<h2>Pipeline</h2>
<pre>Question -&gt; Paper and source search -&gt; Verify each source at origin
-&gt; Map claims and rival views -&gt; Design a test with a baseline
-&gt; Run with logs -&gt; Error read -&gt; Report with claim types split</pre>
<h2>Claim types, keep split in each report</h2>
<table><tr><th>Type</th><th>Meaning</th><th>Site sample</th></tr>
<tr><td>Documented capacity</td><td>Official docs or code show the act</td><td>Muse Code workflows, sources row 41</td></tr>
<tr><td>Practitioner report</td><td>One user states a result</td><td>Sanchez bot outcomes, row 8</td></tr>
<tr><td>Reproduced result</td><td>A test in this build ran the claim</td><td>Lab 1 tests, Lab 2 benchmark</td></tr>
<tr><td>Inference</td><td>A reason step from facts</td><td>Skills as a cross tool format trend</td></tr>
<tr><td>Unverified claim</td><td>No firm source yet</td><td>Grok 5 specs</td></tr>
</table>
<h2>Method rules</h2>
<ul>
<li>Paper search: start with official and primary posts. Use reviews to find rival views and fails.</li>
<li>Data provenance: name the data origin, the split rule and a leakage check before a run.</li>
<li>Baselines: run a plain method first. Lab 2 keyword search forms that role.</li>
<li>Ablation: change one main factor per run. Lab 2 changed score method only.</li>
<li>Error read: sort errors by type before a fix. A ceiling effect counts as a design error, as Lab 2 shows.</li>
<li>Logs: record command, version, seed, run count and result per run. Labs page holds the form.</li>
<li>Compute budget: state token and time cost per run where a tool shows the data. Hide no estimate as a measure.</li>
</ul>
<h2>Worked example: Anthropic research system as a design case</h2>
<p>A lead agent saves a plan to memory, spawns parallel subagents with distinct tools, takes compressed finds back, and runs a citation pass. Internal eval gain in the official post: 90.2 percent over a single agent on their test. Token cost: near 15 times chat. Lesson: parallel research buys breadth at a steep token price, and a citation step forms part of the method, not a polish step.</p>
<h2>Tutorial in eight parts, research synthesis workflow</h2>
<h3>1. Question</h3><p>What do sources agree on, and where do sources split?</p>
<h3>2. Key facts</h3><p>Ledger rows carry author, date, link and confidence for each claim set in this site.</p>
<h3>3. Core concepts</h3><p>Origin count, claim type, contradiction, supersede link.</p>
<h3>4. Patterns</h3><p>Search in parallel, compress per source, join, rank by origin and date, flag splits.</p>
<h3>5. Conflicts</h3><p>Poteto pull request counts split across sources. Print the split, pick no single count.</p>
<h3>6. Hypotheses</h3><p>A citation pass may cut claim errors in long reports. Test: count errors with and without the pass on one draft.</p>
<h3>7. Decision support</h3><p>Use the pipeline for high value, breadth first questions. Use one agent for a narrow fact check.</p>
<h3>8. One bounded next action</h3><p>Run the citation pass test on one page of your own notes this week. Log error counts for both forms.</p>
""")
print("v2 pages part 1 done")

# LABS
page("labs.html","Practical labs, executed in this build",
"Three labs ran on this machine on 20 November 2026. Results below come from tool output. No lab ran a send, spend, post or deploy act.",
"""<p>Environment: Python 3.12.3, pytest 9.1.1. Code sits in the repo under <code>labs/</code>. Full log: <code>labs/RESULTS.md</code>.</p>
<h2>Lab 1. Python service: feature plus bug fix</h2>
<p>Question: can a test first flow catch a page slice bug and prove a priority filter?</p>
<p>Baseline bug: a page start of page times per_page skips page one items. Fix: start equals page minus one, times per_page.</p>
<p>Feature: list tasks by priority, with page rules held.</p>
<pre>cd labs/lab1
python3 -m pytest -q
# result: 5 passed in 0.02s</pre>
<p>Tests: first page, second page, priority filter, filter plus page, complete act. Quality rule set before the run: all five tests pass, with exact id lists.</p>
<p>Human steps in the lab run: code write and result read by the build agent. No user act took place. Cost: local run, zero model tokens for the test run.</p>
<h2>Lab 2. Retrieval benchmark with a ceiling effect</h2>
<p>Question: does TF-IDF cosine beat exact keyword count on precision at 5?</p>
<p>Design: 200 synthetic docs, 4 topics, 20 queries, k of 5, 3 repeats, seed 42. One factor changes: score method.</p>
<pre>cd labs/lab2
python3 benchmark.py
# keyword: precision@5 runs=[1.0, 1.0, 1.0] mean=1.0, 0.0407s per run
# tfidf:   precision@5 runs=[1.0, 1.0, 1.0] mean=1.0, 0.0603s per run</pre>
<p>Hard variant, seed 7, 6 of 15 words as cross topic noise: both methods score 1.0 on all repeats.</p>
<div class="callout"><p>Finding: ceiling effect. Synthetic topics split too clean, so this test cannot rank both methods. A single pass run forms a demo, not a ranking. Next test: queries with words shared by two topics, plus human judged relevance on real docs. This fail case stays in the site by design: a benchmark that cannot split two methods proves no win for a method.</p></div>
<h2>Lab 3. Business workflow: cited report artifact</h2>
<p>Question: can a collect, count, draft flow turn a source ledger into a review ready report with no send act?</p>
<pre>cd labs/lab3
python3 make_report.py
# rows=60
# confidence split: High 16, Medium-High 9, Medium 13, Medium-Low 18, Low 2, Low-Medium 2</pre>
<p>Artifact: <code>labs/lab3/report_artifact.md</code>. Gate: a human must check each Low row before use. No mail, post or spend act ran.</p>
<h2>Lab rules for your own runs</h2>
<ol><li>State the question and the pass rule before a run.</li><li>Record command, version, seed, run count and result.</li><li>Change one main factor per ablation.</li><li>Read errors by type before a fix.</li><li>Mark a run as demo, reproduced result or new result. Keep all three apart.</li></ol>
""")

# PATHS
page("paths.html","Learning paths and exercises",
"Three routes by time. Each core lesson holds six parts: a worked sample, a partial exercise, a solo task, a recall question, a transfer task and a late review prompt.",
"""<h2>Routes</h2>
<table><tr><th>Route</th><th>Time</th><th>Pages</th><th>End proof</th></tr>
<tr><td>Quick start</td><td>One hour</td><td>Start Here, Foundations, Lab 1</td><td>One bug fix with tests green</td></tr>
<tr><td>Standard</td><td>Two weeks</td><td>All tool pages, Labs 1 to 3, Prompt Vault</td><td>One repo with a rule map, one skill, one verify step, one eval set</td></tr>
<tr><td>Deep study</td><td>Six weeks</td><td>Standard plus Research, Business, full Sources pass</td><td>One research pipeline and one gated business workflow, each with a log</td></tr>
</table>
<h2>Core lesson set with six parts</h2>
<h3>Lesson A. Rule file as a map</h3>
<p>Worked sample: OpenAI AGENTS.md near 100 lines as a table of contents, Foundations page.</p>
<p>Partial exercise: cut a 400 line rule file to a map. Keep each rule in a linked doc. Fill the map with at most ___ lines.</p>
<p>Solo task: build a map for one repo of yours.</p>
<p>Recall question: why does a long rule file lose force? Hint: context cost and load order.</p>
<p>Transfer task: apply the map form to a research notes folder, not a code repo.</p>
<p>Late review, day 7: open your map cold. Time a fresh agent on one task. Log rule misses.</p>
<h3>Lesson B. Loop with an oracle</h3>
<p>Worked sample: Antigravity goal loop, Gemini page workflow A2.</p>
<p>Partial exercise: write tests for a sort bug before a fix. Leave one test blank for a case you must name.</p>
<p>Solo task: run Lab 1, then add one test of your own.</p>
<p>Recall question: what makes an oracle safe? Answer: the agent holds no edit rights on the oracle.</p>
<p>Transfer task: set an oracle for a writing task: a claim list with one source link per claim.</p>
<p>Late review, day 14: re run your first loop. Compare round count and error count.</p>
<h3>Lesson C. Fresh eyes review</h3>
<p>Worked sample: Cherny verify subagent and Codex self review loop.</p>
<p>Partial exercise: write a review prompt with raw diff and test output as inputs. Leave the verdict form blank.</p>
<p>Solo task: run a fresh context review on one pull request of yours.</p>
<p>Recall question: why must a reviewer hold no writer context?</p>
<p>Transfer task: use a fresh reviewer on a research draft, with the ledger as raw evidence.</p>
<p>Late review, day 21: count defects a fresh review found that self review had missed.</p>
""")

# GLOSSARY
terms = [
 ("Agent","A model plus tools, state and a loop, run toward a goal."),
 ("AGENTS.md","An instruction file for Codex and Muse Code. Acts as a repo map."),
 ("Artifact","A review ready output form in Antigravity: a plan, a task list, a screenshot or a record."),
 ("CLAUDE.md","An instruction file for Claude Code. Acts as team memory and a map."),
 ("Context","All text and data a model can see in one run."),
 ("Duet","An Anthropic proactive personal agent in research preview from 21 October 2026."),
 ("dots","An OpenAI always on personal agent from 29 September 2026."),
 ("Eval set","A fixed set of samples with scores, run on each prompt or model change."),
 ("Grok Bot","An xAI fleet of named bots on one shared cloud computer."),
 ("Harness","All scaffold parts round a model: context, tools, skills, policy and evals."),
 ("Hook","A firm code act on a life cycle event. A hook can deny a tool call."),
 ("MCP","Model Context Protocol. A standard form for tool servers for agents."),
 ("Oracle","A firm pass test an agent cannot edit."),
 ("Skill","A folder with a SKILL.md file. Holds a repeat procedure for an agent."),
 ("Stop condition","A firm rule that ends a loop: a pass, a round cap or a cost cap."),
 ("Subagent","A child agent with own context. Only a final message returns to a lead."),
 ("Worktree","A git checkout form that isolates one task branch in own files."),
]
trs = "".join(f"<tr><td><strong>{t}</strong></td><td>{d}</td></tr>" for t,d in terms)
page("glossary.html","Glossary", "Plain terms at first use across the site. One term, one sense, in all pages.",
 f"<table><tr><th>Term</th><th>Sense in this site</th></tr>{trs}</table>")

# AUDIT
page("audit.html","Audit, coverage and unresolved questions",
"Traceability for this build. Execution date: 20 November 2026. Evidence cutoff: 20 November 2026. One review pass ran in this build, with repairs logged at base of this page.",
"""<h2>Identity table</h2>
<table><tr><th>Supplied name</th><th>Verified identity</th><th>Official URL</th><th>Product or role</th><th>Evidence</th><th>Status</th></tr>
<tr><td>Grokbot</td><td>Grok Bot, xAI</td><td>Not in source for one official product page in ledger</td><td>Bot fleet product</td><td>Rows 5, 6, 7</td><td>Verified as product, official page gap noted</td></tr>
<tr><td>Dots and Codex</td><td>Two products: Codex, a coding agent; dots, a personal agent</td><td>Not in source as one pair URL</td><td>OpenAI</td><td>Rows 32, 33, 36</td><td>Split, per evidence</td></tr>
<tr><td>Muse</td><td>Meta Muse: agent, models, Muse Code. No Apple Muse in sources</td><td>about.fb.com launch post, row 38</td><td>Meta</td><td>Rows 38 to 42</td><td>Verified, user pair corrected</td></tr>
<tr><td>Gemini and Antigravity</td><td>Gemini models; Antigravity agent platform</td><td>blog.google posts, rows 25, 26</td><td>Google</td><td>Rows 25 to 31</td><td>Verified as a pair with split roles</td></tr>
<tr><td>Claude and Claude Duet</td><td>Claude models and Claude Code; Duet personal agent</td><td>anthropic.com and code.claude.com, rows 11, 13</td><td>Anthropic</td><td>Rows 11 to 24</td><td>Verified as a pair with split roles</td></tr>
<tr><td>Poteto or Potetoa</td><td>Lauren Tan, handle poteto</td><td>Not in source</td><td>Grok Bot lead, SpaceXAI</td><td>Rows 51 to 53</td><td>Verified identity, counts conflict</td></tr>
<tr><td>Tibo</td><td>Thibault Louis-Lucas, tibo_maker</td><td>Not in source</td><td>Founder, Tweet Hunter and Taplio past</td><td>Row 54</td><td>Verified, split from Tony Dinh</td></tr>
<tr><td>Dario</td><td>Dario Amodei, Anthropic chief executive</td><td>anthropic.com</td><td>Chief executive</td><td>Row 24 org claims only</td><td>Identity verified, personal workflow unresolved</td></tr>
<tr><td>Borris or Boris</td><td>Boris Cherny</td><td>Not in source</td><td>Creator of Claude Code</td><td>Rows 16 to 18</td><td>Verified</td></tr>
<tr><td>Codie Sanchez</td><td>Codie Sanchez</td><td>Not in source</td><td>Founder, Contrarian Thinking</td><td>Rows 8, 9, 10</td><td>Verified, outcomes self reported</td></tr>
<tr><td>Matt Potcock</td><td>Matt Pocock, per user note and repo evidence</td><td>github.com/mattpocock/skills</td><td>TypeScript educator</td><td>Rows 46, 47</td><td>Verified as Pocock</td></tr>
<tr><td>Mayank Shah</td><td>Ambiguous. Best match: Shah Labs</td><td>shahlabs.org, row 55</td><td>Not in source for role</td><td>Row 55</td><td>Unresolved identity, workflow kept with flag</td></tr>
<tr><td>Greg Isenberg</td><td>Greg Isenberg</td><td>Not in source</td><td>Late Checkout chief executive</td><td>Rows 56, 57</td><td>Verified</td></tr>
<tr><td>Cavemen</td><td>caveman repo by Julius Brussee</td><td>github.com/JuliusBrussee/caveman</td><td>Token compression skill</td><td>Row 48</td><td>Verified as caveman, singular</td></tr>
<tr><td>Hallmark</td><td>hallmark repo by Nutlope, Together AI</td><td>github.com/Nutlope/hallmark</td><td>Design skill</td><td>Rows 49, 50</td><td>Verified</td></tr>
<tr><td>Superpowers</td><td>superpowers repo by Jesse Vincent, Prime Radiant</td><td>github.com/obra/superpowers</td><td>Agent method skills</td><td>Row 45</td><td>Verified</td></tr>
</table>
<h2>Traceability</h2>
<table><tr><th>Requirement</th><th>Page</th><th>Evidence</th><th>Verification</th><th>Gap</th></tr>
<tr><td>Power user difference</td><td>Home, Principles</td><td>Rows 15, 16, 33</td><td>Claim to row check in review</td><td>None</td></tr>
<tr><td>Five tool clusters, deep page each</td><td>Grok, Claude, Gemini, Codex, Muse pages</td><td>Rows 1 to 42</td><td>Three plus workflows per page, count check</td><td>DeepMind named engineer workflows absent</td></tr>
<tr><td>Business workflows</td><td>Business, Grok</td><td>Rows 8, 9, 39, 56, 57</td><td>Scope table per case</td><td>Cost and staff data absent in sources</td></tr>
<tr><td>Production code path</td><td>Codex, Claude, Foundations</td><td>Rows 15, 33</td><td>Lab 1 run</td><td>None</td></tr>
<tr><td>Research practice</td><td>Research</td><td>Rows 19, Lab 2</td><td>Lab 2 run with ceiling finding</td><td>Real corpus test still open</td></tr>
<tr><td>Skills, MCP, repos</td><td>Cross-cutting</td><td>Rows 43 to 51</td><td>Repo table with install forms</td><td>Exact MCP repo links for three servers absent</td></tr>
<tr><td>Prompt library, 14 types</td><td>Prompt Vault</td><td>Site build</td><td>Each type has six fields plus template and sample</td><td>None</td></tr>
<tr><td>Three labs</td><td>Labs</td><td>labs/RESULTS.md</td><td>Runs on 20 November 2026, output in page</td><td>Lab 2 ranks no method, by design fail</td></tr>
<tr><td>Search, copy controls, mobile</td><td>Search page, all pages</td><td>assets/site.js, assets/search-data.js</td><td>Link and script check in build log</td><td>Search covers titles and heads, not full text</td></tr>
</table>
<h2>Coverage matrix</h2>
<p>Products: 5 clusters, each with official, practitioner and community sources in the ledger. People: 9 named cases, 2 with flags. Channels in ledger: official docs, trade press, blogs, GitHub, Instagram, Threads, Substack summaries, YouTube via summaries. Gaps by channel: X posts came via transcripts, no direct X read in the research run. Reddit threads: no ledger row rests on Reddit alone. Podcast transcripts: via summaries, no full transcript in this build. Each gap stands as a limit, not as a claim of full coverage.</p>
<h2>Review log</h2>
<p>Review pass 1, in build: check internal links, claim badges, identity splits, lab output vs page text, prompt field count. Repairs: Muse name fix on all pages, Poteto count split kept as a conflict, Lab 2 ceiling result kept in place of a win claim, Duet plan list flagged as a split.</p>
<p>Review pass 2, independent reviewer: six defects found and fixed. Convergence span corrected to three products in seven weeks with Grok Bot as an earlier variant. Evidence graph Lab 2 row corrected to a limit claim, no win. Badges added: Grok workflow G5, Tibo card, Isenberg card. Prompt Vault samples replaced: each of the 14 types now holds a distinct filled sample. Search page gained a scope and method section.</p>
""")
print("v2 pages done")

# PROMPTS v2, 14 types
PROMPTS = [
 ("Repository orientation","Map an unknown repo fast.","Repo path, goal of the tour","No edit acts. Facts only, with file paths.","Map: entry points, core modules, test commands, risk areas.","Open three named files. Paths must exist.","Stop at a full map or at 20 files read."),
 ("Specification and acceptance","Turn a wish into a testable spec.","Goal, user, limits, samples","One sense per term. No new features past the goal.","Spec with numbered pass rules.","Each rule maps to a test or a check a human can run.","Stop when each goal part has one pass rule."),
 ("Architecture comparison","Pick a design with evidence.","Spec, two or three options, limits","Score on set axes only. Name trade offs.","Table of options, scores, one pick with a reason.","Check each score cites a fact or a test.","Stop at one pick or at a named open question."),
 ("Implementation","Build to a spec in small steps.","Spec, plan, repo map","Edit named areas only. Run tests per step.","Code plus a step log.","Test output per step sits in the log.","Stop at spec pass or at a block with proof."),
 ("Debugging from evidence","Fix a bug from proof, not a guess.","Error text, logs, fail test, recent diff","No fix with no reproduce step first.","Root cause, one fix, regression test.","Fail test passes, full set passes.","Stop at pass or at two failed fix rounds, then replan."),
 ("Test design","Write tests that can fail.","Spec, code under test, edge list","Tests must name exact values. No tautology tests.","Test file plus a case table.","Each pass rule has one test at least.","Stop when each rule maps to a test."),
 ("Code review","Find defects in a diff.","Diff, spec, test output","Report defects only, with file and line. No style nits as defects.","Defect list by severity, each with a proof step.","Re run one proof step per top defect.","Stop at a full diff read."),
 ("Research synthesis","Join sources into claims with types.","Question, source set, ledger form","Split claim types. One origin per press cycle.","Synthesis with claim rows and splits named.","Each claim row links to a source row.","Stop at source set end or at two passes with no new claim."),
 ("Experiment design","Design a test that can prove a view wrong.","Claim, baseline, data access","One main factor per run. Pass rule set before a run.","Design doc: inputs, runs, metrics, stop rule.","A rival result must be possible in the design.","Stop when a disproof path exists in the plan."),
 ("Evaluation and error analysis","Score runs and sort errors.","Eval set, run outputs, score rule","Sort errors by type before a fix. Count, do not sample by feel.","Score table plus error type counts.","Re score five samples by hand. Counts must match.","Stop at a full set scored."),
 ("Business research","Build a cited market or lead report.","Scope, source list, claim rule","Each claim needs a link and a date. No send acts.","Report draft with a review gate list.","Open five links at random. Each must support its claim.","Stop at scope end."),
 ("Agent delegation","Split work for child agents with no clash.","Goal graph, file ownership, pass rules","One owner per file set. Child output form fixed.","Task cards with inputs, outputs and checks.","Each card names a verify step and a stop rule.","Stop when each graph node has one card."),
 ("Independent audit","Audit a draft vs raw evidence.","Draft, raw sources, requirement list","Find unsupported claims first. No edit acts in audit round.","Defect list with claim, source state and fix form.","Each defect cites a page line and a source row.","Stop at a full draft read."),
 ("Session handoff and recovery","End a session so a fresh agent can resume.","State log, decisions, open points, next acts","Facts only. No new plans in a handoff.","Handoff note with state, proof links and next act one.","A fresh reader can name the next act in one pass.","Stop at one next act named first."),
]
EXAMPLES = {
 "Repository orientation": "Goal: map labs/lab1. Inputs: service.py and test_service.py. Output in the run: entry class TaskService, three methods, test command python3 -m pytest -q. Risk area named: page slice math.",
 "Specification and acceptance": "Goal: priority filter for Lab 1. Pass rules: high filter returns ids 5, 10, 15, 20, 25 on the seed set; page rules hold under a filter. Both rules map to tests in Lab 1.",
 "Architecture comparison": "Options for Lab 2 score method: keyword count vs TF-IDF cosine. Axes: accuracy at k of 5, run time, code size. Pick rule set in advance: a win needs a split past 0.02 on precision. Result: no split, no pick.",
 "Implementation": "Goal: fix the page slice in Lab 1. Step log: write fail test, run and record fail, change start math to page minus one times per_page, run full set, record 5 passed.",
 "Debugging from evidence": "Evidence: test_first_page_has_first_items fails, page one returns ids 11 to 20. Reproduce step: one test run. Root cause: start equals page times per_page. Fix: one line. Regression test: the same test, now green.",
 "Test design": "Case table for Lab 1: page one exact ids, page two exact ids, filter exact ids, filter plus page count and type check, complete act on a real id and on id 999.",
 "Code review": "Diff under review: one line in list_tasks. Defect check: filter runs before slice, so page math uses the filtered list. Proof step: test_filter_and_page passes with count 10 and all rows at normal priority.",
 "Research synthesis": "Question: what do power users do that regular users do not? Claim rows: fleets, harness, oracles, fresh review, compounding corrections. Split named: Poteto counts conflict across rows 51 to 53, so no count enters the synthesis as a fact.",
 "Experiment design": "Claim: TF-IDF beats keyword count. Baseline: keyword count. One factor: score method. Pass rule: precision split past 0.02 at k of 5 over 3 repeats. Disproof path: equal scores kill the claim. Result in Lab 2: claim killed.",
 "Evaluation and error analysis": "Eval set: Lab 2 queries, 20 in total. Score rule: precision at 5 per topic. Error sort: no errors to sort, both methods at 1.0. Error type found at design level: ceiling effect in corpus design.",
 "Business research": "Scope: Grok Bot business cases. Claim rule: each claim needs a link and a date. Draft rows: Sanchez finder and drafter pair, row 8, flagged Low. Gate list: all outcome numbers need a human check before use.",
 "Agent delegation": "Goal graph for this site build: research branches in parallel, ledger join, build, verify, review. File ownership: one builder script per page set, reviewer edits no files. Stop rule per card: output file plus a check result.",
 "Independent audit": "Draft: this site. Raw evidence: report ledger rows 1 to 60. Defect sample from pass 2: convergence span text said four products in seven weeks; dates show three in seven weeks plus one earlier variant. Fix form applied on the Home page.",
 "Session handoff and recovery": "State: v2 site built, 20 pages, links clean. Decisions: Muse equals Meta, Lab 2 claims no win. Open point: exact Claude Code patch. Next act one: push v2 files to branch build/power-user-hub-v1 and verify the remote tree.",
}
cards = ""
for name, purpose, inputs, constraints, output, verify, stop in PROMPTS:
    slug = name.lower().replace(" ", "-")
    cards += f"""<h2 id="{slug}">{name}</h2>
<table><tr><th>Field</th><th>Value</th></tr>
<tr><td>Purpose</td><td>{purpose}</td></tr>
<tr><td>Required inputs</td><td>{inputs}</td></tr>
<tr><td>Constraints</td><td>{constraints}</td></tr>
<tr><td>Output format</td><td>{output}</td></tr>
<tr><td>Verification</td><td>{verify}</td></tr>
<tr><td>Stop conditions</td><td>{stop}</td></tr></table>
<h3>Template</h3>
<pre>Goal: [one outcome]
Inputs: [list files, sources, or data]
Constraints: [limits, rights, areas to avoid]
Output: [exact form]
Verify: [test, check, or proof step]
Stop: [pass rule, round cap, or block rule]
Report gaps as: Not in source.</pre>
<h3>Filled sample</h3>
<p>{EXAMPLES[name]}</p>
"""
cards += """<h2>Verbatim prompts, sourced</h2>
<ol>
<li><span class="badge">Verbatim</span> <code>Grill me on these changes and don't make a PR until I pass your test.</code> Cherny team thread transcript, sources row 18.</li>
<li><span class="badge">Verbatim</span> <code>Prove to me this works</code> Same source.</li>
<li><span class="badge">Verbatim</span> <code>Knowing everything you know now, scrap this and implement the elegant solution.</code> Same source.</li>
<li><span class="badge">Verbatim</span> <code>Update your CLAUDE.md so you don't make that mistake again.</code> Same source.</li>
<li><span class="badge">Verbatim</span> <code>@codex review for security regressions</code> Codex command form, row 34.</li>
<li><span class="badge">Verbatim</span> <code>Use a workflow to review this service. Have separate agents inspect the API design, security boundaries, and test coverage. Verify the findings, then return one prioritized report.</code> Muse Code docs sample, row 41.</li>
</ol>
<h2>One prompt failure and a repair</h2>
<p>Failure form: a prompt asks for a full build with no verify step. Output looks full and hides defects. Repair: add one verify line with a test the agent cannot edit, plus a stop rule. Lab 2 shows the same trap in benchmark form: a test with no split power proves no win.</p>
<h2>Verbatim prompts from named users</h2>
<p>Four Cherny team lines, Codex review commands and one Muse Code workflow prompt sit in v1 form in git history for this file and in full on the Claude, Codex and Muse pages workflow steps. Verbatim text in this site carries a source row on the Sources page: rows 18, 34 and 41.</p>
"""
page("prompts.html","Prompt Vault, 14 types","Each prompt type holds six fields, a copy ready template, and a sample form. Verbatim prompts from named users carry source rows. All other text forms a pattern, never a quote.", cards)

# SEARCH PAGE (data file generated after patch step)
page("search.html","Search the site","Type a term. Search covers page titles and section heads on all pages. Full text search: use a browser find on one page.",
"""<h2>How search works here</h2>
<p>Search data sits in one local file, assets/search-data.js. The file holds one record per page: a file name, a page title, and all section heads on that page. No server call takes place. No term leaves your machine. Type a term and the list filters at once. A match on a title or a head shows the page link plus the first three heads as context.</p>
<p>Scope limit: search covers titles and heads only, not full body text. That limit keeps the index small and the site fast from disk. For a body term, open a candidate page and use a browser find. For a claim check, go to the Sources page and use a browser find on a claim word: the ledger holds one row per claim set.</p>
<p>Good terms: a tool name such as Codex or Grok, a method word such as oracle, worktree or eval, a person name such as Cherny or Pocock, or a page word such as labs, audit or glossary. Each term maps to heads on the pages that teach that topic, so one search gives a study route, not a pile of weak hits.</p>
<p><label for="q">Search term</label> <input id="q" type="search" style="font-size:17px;padding:6px;width:min(420px,90%)"></p>
<ul id="results"></ul>
<script src="assets/search-data.js"></script>
<script>
const box=document.getElementById('q'), list=document.getElementById('results');
function run(){
 const term=box.value.trim().toLowerCase(); list.innerHTML='';
 if(!term) return;
 for(const item of SEARCH_DATA){
   const hay=(item.title+' '+item.heads.join(' ')).toLowerCase();
   if(hay.includes(term)){
     const li=document.createElement('li');
     const a=document.createElement('a'); a.href=item.file; a.textContent=item.title;
     li.appendChild(a); li.appendChild(document.createTextNode(' - '+item.heads.slice(0,3).join(', ')));
     list.appendChild(li);
   }
 }
 if(!list.children.length){ const li=document.createElement('li'); li.textContent='No page head matches that term.'; list.appendChild(li); }
}
box.addEventListener('input', run);
</script>""")

# SITE.JS: copy buttons for pre blocks
site_js = """document.querySelectorAll('pre').forEach(function(pre){
  var btn=document.createElement('button'); btn.type='button'; btn.textContent='Copy';
  btn.style.cssText='float:right;font-size:12px;padding:2px 10px;cursor:pointer';
  btn.addEventListener('click', function(){
    navigator.clipboard.writeText(pre.innerText).then(function(){ btn.textContent='Copied'; setTimeout(function(){btn.textContent='Copy';},1500); });
  });
  pre.parentNode.insertBefore(btn, pre);
});
"""
with open(os.path.join(OUT,"assets","site.js"),"w") as f: f.write(site_js)

# PATCH v1 pages: expanded nav, breadcrumbs note, script tag
new_nav = "".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
for path in glob.glob(os.path.join(OUT,"*.html")):
    name=os.path.basename(path)
    if name in ("start.html","foundations.html","business.html","research.html","labs.html","paths.html","glossary.html","audit.html","prompts.html","search.html"):
        continue
    t=open(path).read()
    t=re.sub(r'<nav class="main">.*?</nav>', f'<nav class="main">{new_nav}</nav>', t, flags=re.S)
    if "assets/site.js" not in t:
        t=t.replace("</body>", '<script src="assets/site.js"></script>\n</body>')
    t=t.replace("Build date: 20 November 2026.", "Execution date: 20 November 2026. Evidence cutoff: 20 November 2026.")
    open(path,"w").write(t)
print("patched v1 pages")

# SEARCH DATA from all pages
data=[]
for path in sorted(glob.glob(os.path.join(OUT,"*.html"))):
    t=open(path).read()
    title=re.search(r"<h1>(.*?)</h1>", t, re.S)
    heads=re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S)
    clean=lambda s: re.sub(r"<[^>]+>","",s).strip()
    data.append({"file":os.path.basename(path),"title":clean(title.group(1)) if title else os.path.basename(path),"heads":[clean(h) for h in heads]})
with open(os.path.join(OUT,"assets","search-data.js"),"w") as f:
    f.write("const SEARCH_DATA="+json.dumps(data)+";\n")
print("search data pages", len(data))
