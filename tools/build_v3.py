#!/usr/bin/env python3
"""V3 visual and template pass. Pitch black book template, Jakarta and JetBrains
fonts, justified text, one original SVG figure, one Mermaid diagram and one
markmap tree per page. All diagram text comes from page content."""
import os, re, glob, html

OUT = os.path.expanduser("~/workspace/learning-agentic-site/site")
IMG = os.path.join(OUT, "assets", "img")
os.makedirs(IMG, exist_ok=True)

CSS = """/* Hallmark pre-emit critique: P4 H5 E4 S5 R5 V4. Template: book system, pitch black. */
:root{
 --paper:#050505; --paper2:#101010; --paper3:#171713;
 --ink:#f4f1ea; --muted:#c9c3b4; --faint:#9d9687;
 --line:#2c2a24; --accent:#e8a04c; --accent2:#8fd0b2;
 --codebg:#12120e; --warnbg:#221a0c; --warnline:#e8a04c;
 --font-display:"Anthropic Sans","Plus Jakarta Sans",-apple-system,"Segoe UI",Roboto,sans-serif;
 --font-body:"Anthropic Sans","Plus Jakarta Sans",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 --font-mono:"JetBrains Mono","JetBrains Sans",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{overflow-x:clip;background:var(--paper);color:var(--ink)}
body{margin:0;font-family:var(--font-body);font-size:17.5px;line-height:1.7}
p,li{text-align:justify;hyphens:auto}
a{color:var(--accent);text-underline-offset:3px}
a:hover{color:var(--accent2)}
header.top{border-bottom:2px solid var(--ink);padding:18px 20px 12px;max-width:1020px;margin:0 auto}
.wordmark{font-family:var(--font-display);font-weight:800;font-size:20px;letter-spacing:.01em}
.wordmark a{color:var(--ink);text-decoration:none}
nav.main{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:14px}
nav.main a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:2px;white-space:nowrap}
nav.main a[aria-current]{border-bottom:2px solid var(--accent);color:var(--ink);font-weight:700}
main{max-width:1020px;margin:0 auto;padding:28px 20px 60px}
h1{font-family:var(--font-display);font-style:normal;font-weight:800;font-size:44px;line-height:1.1;margin:0 0 14px;overflow-wrap:anywhere;min-width:0;letter-spacing:-.01em}
h2{font-family:var(--font-display);font-style:normal;font-weight:800;font-size:28px;line-height:1.25;margin:42px 0 10px;border-top:1px solid var(--line);padding-top:24px}
h3{font-family:var(--font-display);font-style:normal;font-weight:700;font-size:19px;margin:24px 0 6px}
p{margin:0 0 12px;max-width:74ch}
.lede{font-size:20.5px;line-height:1.55;max-width:64ch}
.meta{color:var(--faint);font-size:14px;text-align:left}
table{border-collapse:collapse;width:100%;margin:14px 0 22px;font-size:15px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--paper2);font-family:var(--font-display)}
code{font-family:var(--font-mono);background:var(--codebg);padding:1px 5px;font-size:.9em;color:var(--accent2)}
pre{font-family:var(--font-mono);background:var(--codebg);padding:14px;overflow-x:auto;font-size:13.5px;line-height:1.55;border:1px solid var(--line)}
ol,ul{max-width:74ch}
li{margin-bottom:6px}
.badge{display:inline-block;border:1px solid var(--ink);padding:0 7px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap}
.badge.low{border-color:var(--warnline);color:var(--warnline)}
.callout{border:1px solid var(--warnline);background:var(--warnbg);padding:14px 16px;margin:18px 0;max-width:74ch}
.callout p{margin:0}
.rule{border-left:4px solid var(--accent2);padding:4px 0 4px 14px;margin:16px 0;max-width:74ch}
.toc{columns:2;column-gap:40px;font-size:15px}
figure.visual{margin:22px 0 8px;max-width:74ch}
figure.visual img{width:100%;height:auto;display:block;border:1px solid var(--line);background:var(--paper2)}
figure.visual figcaption{color:var(--muted);font-size:14px;margin-top:8px;text-align:left}
.readguide{background:var(--paper2);border:1px solid var(--line);padding:12px 16px;margin:10px 0 22px;max-width:74ch;font-size:15px}
.readguide p{margin:0 0 6px;text-align:left}
.mermaid{background:var(--paper2);border:1px solid var(--line);padding:16px;overflow-x:auto;max-width:74ch}
.mermaid-src{max-width:74ch}
.markmap{max-width:74ch;font-size:15.5px}
.markmap ul{list-style:none;border-left:2px solid var(--line);margin:4px 0 4px 8px;padding-left:18px}
.markmap>ul{border-left:none;margin-left:0;padding-left:0}
.markmap li{margin:5px 0;text-align:left}
.markmap .root{font-family:var(--font-display);font-weight:800;font-size:18px;color:var(--accent)}
.markmap .branch{font-weight:700;color:var(--ink)}
.markmap .leaf{color:var(--muted)}
footer.site{border-top:2px solid var(--ink);max-width:1020px;margin:0 auto;padding:18px 20px 40px;font-size:14px;color:var(--muted)}
button{font-family:var(--font-body)}
@media(min-width:1280px){
 body{padding-left:292px}
 header.top{position:fixed;left:0;top:0;width:292px;height:100vh;overflow-y:auto;border-bottom:none;border-right:2px solid var(--ink);padding:24px 20px;background:var(--paper)}
 nav.main{flex-direction:column;gap:8px;margin-top:16px}
 nav.main a{white-space:normal}
 main,footer.site{margin:0 auto}
}
@media(max-width:640px){h1{font-size:33px}.toc{columns:1}body{font-size:16.5px}p,li{text-align:left}}
"""
with open(os.path.join(OUT, "assets", "style.css"), "w") as f: f.write(CSS)
print("css v3 written")

VIS = {
"index.html": dict(nodes=["Fleet of agents","Harness rules","Self check oracle","Compounding lessons"],
 mermaid="flowchart LR\n A[One chat] --> B[Fleet of sessions]\n B --> C[Harness: rules, skills, hooks]\n C --> D[Oracle: tests and proof]\n D --> E[Ship]\n D --> F[Lesson to rule file]\n F --> C",
 mark=[("Power user difference",["Fleets, not chats","Harness over answers","Fresh eyes review"]),("Versions dashboard",["Grok 4.7","Claude Fable 5.2","Gemini 4 Argon","Codex CLI 0.169.0"]),("Start route",["Start Here page","Lab 1 first","One prompt per day"])]),
"start.html": dict(nodes=["Pick a route","Read one tool page","Run Lab 1","Log the result"],
 mermaid="flowchart TD\n A[Quick route, one hour] --> B[Foundations]\n B --> C[Lab 1: test first fix]\n C --> D[Standard route, two weeks]\n D --> E[Deep route, six weeks]",
 mark=[("Routes",["Quick: one hour","Standard: two weeks","Deep: six weeks"]),("Graphs",["Task graph","Evidence graph","Learning graph"]),("First proof",["Lab 1 green tests","One vault prompt in use"])]),
"grok.html": dict(nodes=["Brief one bot job","Bot runs on shared computer","Draft output","Human approval gate"],
 mermaid="flowchart LR\n A[Goal brief] --> B[Specialist bot]\n B --> C[Tools: search, CRM, sheet]\n C --> D[Draft only]\n D --> E{Human gate}\n E -->|approve| F[Send or act]\n E -->|reject| B",
 mark=[("Grok models",["4.1 launch facts","4.7 current in sources","5: no release, gap"]),("Grok Bot",["Named bots, one job each","Shared computer risk","Teach a task"]),("Workflows",["G1 internal ship loop","G2 Tan team loop","G3 finder and drafter pair"])]),
"claude.html": dict(nodes=["Plan mode","Parallel worktrees","Verify subagent","CLAUDE.md lesson"],
 mermaid="flowchart LR\n A[Plan mode] --> B[Auto accept build]\n B --> C[Verify subagent]\n C -->|fail| A\n C -->|pass| D[Ship PR]\n D --> E[Lesson to CLAUDE.md]\n E --> A",
 mark=[("Steering stack",["CLAUDE.md under 200 lines","Path rules","Skills","Hooks","Subagents"]),("Fleet",["5 terminal sessions","5 to 10 web sessions","Slash commands"]),("Duet",["Own VM","Morning brief","Approval gates"])]),
"gemini-antigravity.html": dict(nodes=["Project scope","Agent Manager dispatch","Artifacts as proof","Goal loop vs oracle"],
 mermaid="flowchart TD\n A[Project folders] --> B[Dispatch in Agent Manager]\n B --> C[Agent: editor, terminal, browser]\n C --> D[Artifacts]\n D --> E[Comment on artifact]\n E --> B\n C --> F[Tests as oracle]\n F -->|pass| G[Done]",
 mark=[("Models",["Gemini 3 Pro launch","4 Argon GA","4 Carbon announced","3.5 Pro never shipped"]),("Platform",["App, IDE, CLI, SDK","Projects set scope"]),("Loops",["Agent Manager","Goal plus oracle","Dynamic Workflows"])]),
"codex.html": dict(nodes=["AGENTS.md map","Agent executes","Self review loop","Merge with telemetry"],
 mermaid="flowchart LR\n A[Human steers] --> B[Codex executes]\n B --> C[Self review]\n C --> D[Agent reviewers]\n D -->|notes| B\n D -->|pass| E[PR merge]\n E --> F[Doc care agent]",
 mark=[("Harness case",["Near 1M lines, company report","Zero hand code claim","AGENTS.md near 100 lines"]),("Surfaces",["CLI 0.169.0","Cloud tasks","PR review commands"]),("dots",["Personal agent, not a Codex feature","29 Sep 2026 launch"])]),
"muse.html": dict(nodes=["Goal in app or WhatsApp","Muse Secure VM","Sentinel approval","Audit trail"],
 mermaid="flowchart LR\n A[User goal] --> B[Muse plans]\n B --> C[Acts in Secure VM]\n C --> D{Sentinel check}\n D -->|clear| E[Send to internet]\n D -->|risk| F[User approval]\n F --> C",
 mark=[("Three Muse forms",["Personal agent","Model family","Muse Code"]),("Safety design",["Secure VM per person","Sentinel approver","One time card"]),("Code workflows",["Subagents and worktrees","Workflows to 1,000 tasks","Skills import"])]),
"foundations.html": dict(nodes=["Goal and pass rule","Context and tools","Evaluator check","Stop condition"],
 mermaid="flowchart TD\n A[Goal] --> B[State record]\n B --> C[Context load]\n C --> D[Model step]\n D --> E[Tool acts]\n E --> F{Evaluator}\n F -->|pass| G[Stop: done]\n F -->|fail, rounds left| D\n F -->|cap hit| H[Stop: replan]",
 mark=[("Harness parts",["Goal","State","Context","Model","Tools","Policy","Evaluator","Stop rule"]),("Trades",["Effort vs cost","Context size vs noise","Parallel vs merge load"]),("Repeat error rule",["New sample keeps belief","New evidence breaks loop"])]),
"cross-cutting.html": dict(nodes=["MCP tool layer","Skills layer","Guardrail pipeline","Solo stack"],
 mermaid="flowchart LR\n A[Spec first] --> B[TDD or oracle]\n B --> C[Lint, types, scans]\n C --> D[CI and hooks]\n D --> E[Human review of key diffs]\n E --> F[Ship]",
 mark=[("MCP shortlist",["GitHub","Playwright","Context7","Filesystem","Vendor servers"]),("Repos",["superpowers","pocock skills","caveman","hallmark","pstack"]),("Solo stack",["One agent plan","GitHub, Vercel, Supabase","Near 20 dollars per month"])]),
"business.html": dict(nodes=["Source list","Bot collect run","Cited draft","Human review gate"],
 mermaid="flowchart LR\n A[Scope and source list] --> B[Finder or collect bot]\n B --> C[Dedupe check]\n C --> D[Cited draft]\n D --> E{Human gate}\n E -->|approve| F[Use or send]\n E -->|fix| B",
 mark=[("Cases",["Sanchez lead system","Isenberg brain folder","Muse for Small Business","Duet and dots, vendor form"]),("Scope rule",["Name staff and manual work","No scope, no full firm claim"]),("Gate",["Drafts free","Send and spend wait"])]),
"research.html": dict(nodes=["Question","Source verify at origin","Baseline test","Error read and report"],
 mermaid="flowchart TD\n A[Question] --> B[Search primary sources]\n B --> C[Verify at origin]\n C --> D[Claim map, rival views]\n D --> E[Test with baseline]\n E --> F[Error read]\n F --> G[Report, claim types split]",
 mark=[("Claim types",["Documented capacity","Practitioner report","Reproduced result","Inference","Unverified claim"]),("Method rules",["Provenance and leakage","One factor ablation","Logs with seeds"]),("Case",["Anthropic research system","90.2 percent internal eval","Near 15x token cost"])]),
"profiles.html": dict(nodes=["Identity check","Workflow with source","Flag weak claims","Card with status"],
 mermaid="flowchart LR\n A[Supplied name] --> B[Identity check]\n B --> C{Resolved?}\n C -->|yes| D[Workflow card]\n C -->|no| E[Card with gap flag]\n D --> F[Confidence badge]",
 mark=[("Resolved",["Cherny","Tan as Poteto","Tibo, split from Dinh","Pocock","Sanchez","Isenberg"]),("Flagged",["Dario: org claims only","Mayank Shah: identity open"]),("Rule",["Counts in conflict print as splits"])]),
"prompts.html": dict(nodes=["Goal line","Inputs and limits","Output form","Verify and stop rule"],
 mermaid="flowchart LR\n A[Purpose] --> B[Required inputs]\n B --> C[Constraints]\n C --> D[Output form]\n D --> E[Verification]\n E --> F[Stop rule]",
 mark=[("14 types",["Orientation and spec","Build and debug","Review and audit","Research and eval","Business and handoff"]),("Verbatim set",["Cherny lines, row 18","Codex commands, row 34","Muse Code sample, row 41"]),("Failure fix",["No verify line hides defects","Add an oracle and a cap"])]),
"labs.html": dict(nodes=["Question and pass rule","Run with logs","Read results","State limits"],
 mermaid="flowchart TD\n A[Lab 1: service tests] --> D[Results log]\n B[Lab 2: retrieval bench] --> D\n C[Lab 3: cited report] --> D\n D --> E[Limits and next test]",
 mark=[("Lab 1",["5 tests pass","Page slice fix","Priority filter"]),("Lab 2",["Both methods 1.0","Ceiling effect","Harder test named"]),("Lab 3",["60 ledger rows","Confidence split","Draft only, no send"])]),
"paths.html": dict(nodes=["Quick route","Standard route","Deep route","End proof artifact"],
 mermaid="flowchart LR\n A[Quick, one hour] --> B[Standard, two weeks]\n B --> C[Deep, six weeks]\n C --> D[Proof: repo plus logs]",
 mark=[("Lesson parts",["Worked sample","Partial exercise","Solo task","Recall question","Transfer task","Late review"]),("Lessons",["Rule file as map","Loop with oracle","Fresh eyes review"]),("End proofs",["Green tests","Rule map plus skill","Pipeline plus gate log"])]),
"principles.html": dict(nodes=["Harness beats model","Map not manual","Loop with oracle","Approval by reversal cost"],
 mermaid="flowchart TD\n A[Harness] --> B[Graph of work]\n B --> C[Loop vs oracle]\n C --> D[Fresh eyes review]\n D --> E[Lesson to firm layer]\n E --> A",
 mark=[("Ten rules",["Harness, map, graph","Loop, fresh eyes, firm lessons","Approval, context, speed, moat"]),("Harness table",["Context as RAM","Tools as calls","Skills as programs","Evals as verifiers"])]),
"glossary.html": dict(nodes=["Term","One sense","Use in a page","Recall check"],
 mermaid="flowchart LR\n A[New term] --> B[One sense in glossary]\n B --> C[Same sense on all pages]\n C --> D[Recall question]",
 mark=[("Core terms",["Agent","Harness","Oracle","Skill"]),("File terms",["CLAUDE.md","AGENTS.md","SKILL.md"]),("Loop terms",["Stop condition","Subagent","Worktree"])]),
"sources.html": dict(nodes=["Claim on a page","Ledger row","Original source","Confidence mark"],
 mermaid="flowchart LR\n A[Page claim] --> B[Ledger row 1 to 60]\n B --> C[Original URL]\n C --> D[Confidence and gap state]",
 mark=[("Ledger",["60 rows","Author, date, link","Confidence per row"]),("Gaps",["Grok 5","Exact patches","DeepMind named workflows"]),("Library",["Official posts","Trade articles","Videos and talks"])]),
"audit.html": dict(nodes=["Requirement","Page","Evidence row","Verification and gap"],
 mermaid="flowchart LR\n A[Requirement] --> B[Website page]\n B --> C[Evidence]\n C --> D[Verification run]\n D --> E[Gap or pass]",
 mark=[("Tables",["Identity table, 16 rows","Traceability table","Coverage matrix"]),("Review",["Pass 1 in build","Pass 2 independent","Six defects fixed"]),("Open gaps",["Lab 2 real corpus test","Three MCP repo links"])]),
"search.html": dict(nodes=["Type a term","Match titles and heads","Open the page","Find in page for body text"],
 mermaid="flowchart LR\n A[Term] --> B[Local index file]\n B --> C[Page links with heads]\n C --> D[Open page]\n D --> E[Browser find for body terms]",
 mark=[("Scope",["Titles and heads","Local file, no server"]),("Good terms",["Tool names","Method words","Person names"]),("Claim check",["Sources page ledger","One row per claim set"])]),
}
print("vis entries", len(VIS))

def wrap(label, width=17):
    words, lines, cur = label.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines[:3]

def make_svg(slug, nodes, title):
    W, H = 920, 190
    box_w, gap = 200, 26
    x0 = 18
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    parts.append('<rect width="100%" height="100%" fill="#101010"/>')
    parts.append(f'<text x="18" y="30" fill="#e8a04c" font-family="Plus Jakarta Sans, sans-serif" font-size="15" font-weight="700">{html.escape(title.upper())}</text>')
    for i, node in enumerate(nodes):
        x = x0 + i * (box_w + gap)
        fill = "#171713" if i % 2 == 0 else "#1d1a12"
        stroke = "#e8a04c" if i == 0 else "#8fd0b2" if i == len(nodes)-1 else "#3a372c"
        parts.append(f'<rect x="{x}" y="58" width="{box_w}" height="96" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        lines = wrap(node)
        ty = 96 - (len(lines)-1)*11
        for ln in lines:
            parts.append(f'<text x="{x+box_w//2}" y="{ty}" fill="#f4f1ea" font-family="Plus Jakarta Sans, sans-serif" font-size="15.5" font-weight="700" text-anchor="middle">{html.escape(ln)}</text>')
            ty += 22
        if i < len(nodes)-1:
            ax = x + box_w + 3
            parts.append(f'<line x1="{ax}" y1="106" x2="{ax+gap-6}" y2="106" stroke="#e8a04c" stroke-width="2.5"/>')
            parts.append(f'<polygon points="{ax+gap-6},106 {ax+gap-14},100 {ax+gap-14},112" fill="#e8a04c"/>')
    parts.append("</svg>")
    path = os.path.join(IMG, slug + ".svg")
    with open(path, "w") as f: f.write("\n".join(parts))
    return "assets/img/" + slug + ".svg"

def markmap_html(root, mark):
    out = ['<div class="markmap"><ul><li><span class="root">' + html.escape(root) + "</span><ul>"]
    for branch, leaves in mark:
        out.append('<li><span class="branch">' + html.escape(branch) + "</span><ul>")
        for leaf in leaves:
            out.append('<li><span class="leaf">' + html.escape(leaf) + "</span></li>")
        out.append("</ul></li>")
    out.append("</ul></li></ul></div>")
    return "".join(out)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">'
MERMAID_JS = """<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:true, theme:'dark', themeVariables:{background:'#101010', primaryColor:'#171713', primaryTextColor:'#f4f1ea', lineColor:'#e8a04c', secondaryColor:'#1d1a12', tertiaryColor:'#101010'}});
</script>"""

count = 0
for path in sorted(glob.glob(os.path.join(OUT, "*.html"))):
    fname = os.path.basename(path)
    if fname not in VIS: continue
    v = VIS[fname]
    t = open(path).read()
    if "assets/img/" in t:  # idempotent
        print("skip, v3 present:", fname); continue
    slug = fname.replace(".html", "")
    title_m = re.search(r"<h1>(.*?)</h1>", t, re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else slug
    img_rel = make_svg(slug, v["nodes"], title)
    figure = (f'\n<figure class="visual"><img src="{img_rel}" alt="Flow diagram: {html.escape(", ".join(v["nodes"]))}">'
              f'<figcaption>Figure 1. {html.escape(title)} as a flow. Each box names one stage on this page. Arrows show work order.</figcaption></figure>\n')
    # insert after lede paragraph
    t2, n = re.subn(r'(<p class="lede">.*?</p>)', r"\1" + figure, t, count=1, flags=re.S)
    if n == 0:
        t2, n = re.subn(r'(<h1>.*?</h1>)', r"\1" + figure, t, count=1, flags=re.S)
    t = t2
    section = f"""
<h2>Visual map of this page</h2>
<p>Three views of one page: a Mermaid flow for work order, a markmap for concept groups, and a read guide for the flow.</p>
<div class="mermaid">
{v["mermaid"]}
</div>
<details class="mermaid-src"><summary>Mermaid source, for offline read</summary><pre>{html.escape(v["mermaid"])}</pre></details>
<div class="readguide"><p>How to read the flow diagram. Step 1: start at the left box. Step 2: follow each arrow to the next stage. Step 3: at a branch box, read both paths before a choice. Step 4: a loop arrow means work returns for one more pass vs a test.</p></div>
<h3>Markmap: concepts on this page</h3>
{markmap_html(title, v["mark"])}
"""
    t = t.replace("</main>", section + "</main>")
    # head: fonts
    t = t.replace('<link rel="stylesheet" href="assets/style.css">', '<link rel="stylesheet" href="assets/style.css">\n' + FONTS)
    # mermaid script before </body>
    t = t.replace("</body>", MERMAID_JS + "\n</body>")
    # footer text update
    t = t.replace("field guide build v2", "field guide build v3")
    open(path, "w").write(t)
    count += 1
print("v3 pages upgraded", count)
