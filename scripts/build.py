"""Build the portable guide with the Python standard library."""
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ("index", "Start here", "AI engineering field guide", "Study", ""),
    ("workflow-kit", "Adapt a workflow", "Turn a lesson into your own workflow", "Workshops", "Use one real task, a small evidence packet and an acceptance test you can explain."),
    ("workshop-engineering", "Repository to reviewed patch", "Build a change you can review", "Workshops", "Read the code, reproduce a defect, make a bounded change and verify its final revision."),
    ("workshop-research", "Retrieval and evaluation", "Build an experiment you can trust", "Workshops", "Trace a retrieval failure through a baseline, an ablation and an error analysis."),
    ("workshop-automation", "Durable tool workflows", "Build a briefing that survives a crash", "Workshops", "Validate a tool call, ground every claim and recover from an interrupted write."),
    ("run-viewer", "Inspect recorded runs", "Read the evidence from a run", "Workshops", "Compare a candidate with its checks, then inspect the state that decides the next action."),
    ("social-practice", "From posts to practice", "Reproduce the workflow behind a post", "Workshops", "Turn a public demonstration into inputs, a state trace, a counterexample and a local check."),
    ("community", "Community practice", "Test the methods behind the posts", "Workshops", "Inspect public examples, opposing results and the conditions that make a method useful."),
    ("resource-study", "Read the implementations", "Learn from the actual implementation", "Workshops", "Follow code and source passages, predict a state change, then test your explanation."),
    ("paths", "Learning paths", "Choose your path", "Study", "Start from an outcome and leave each session with something you can inspect."),
    ("foundations", "Foundations", "How an agent makes progress", "Study", "A timeout, two possible histories, and eight decisions your program must own."),
    ("cases", "Practitioner cases", "Inside the workflows", "Study", "Follow the steps that practitioners describe, then inspect what their evidence can establish."),
    ("fieldnotes", "Practitioner field notes", "Methods from the field", "Study", "Trace a technique from its first public account to a small experiment you can try."),
    ("usage", "How labs use tokens", "What researchers spend on agents", "Evidence", "Read the units and population behind the headline. Then count the calls in one workflow."),
    ("engineering", "Production engineering", "From defect to release", "Practice", "Take a one-cent error through specification, verification, rollout and recovery."),
    ("business", "Business workflows", "From source to review queue", "Practice", "Find the software, schedules and human decisions behind an automation claim."),
    ("research", "Research workflows", "From question to experiment", "Practice", "Build a comparison that can change your mind."),
    ("labs", "Practical labs", "Run the experiments", "Practice", "Three Python labs with synthetic inputs, reference implementations and recorded results."),
    ("products", "Products and versions", "Product and version index", "Reference", "Match the product, interface, model and access tier before you try a tutorial."),
    ("tools", "Tool tutorials", "Use a tool with a test", "Reference", "Choose a small task, limit its permissions and define the result you will accept."),
    ("resources", "Resource catalog", "Skills, plugins and connectors", "Reference", "Inspect the owner, release, dependencies and permissions before you adopt a resource."),
    ("prompts", "Prompt library", "Prompts you can verify", "Reference", "Use a filled example first. Replace its inputs and acceptance criteria for your next task."),
    ("glossary", "Glossary", "Terms in context", "Reference", "Follow a term from its definition to a worked example."),
    ("graphs", "Project graphs", "Trace the dependencies", "Evidence", "See how a requirement becomes a lesson, an experiment and a checkable claim."),
    ("sources", "Source library", "Source records", "Evidence", "Look up the original evidence, its date, the relevant version and the limits of each claim."),
    ("audit", "Audit and open questions", "Evidence and verification audit", "Evidence", "Inspect what ran, which identities remain uncertain and where the evidence ends."),
]
STUDY_PAGES = ROOT / "data/study-pages.json"
if STUDY_PAGES.exists():
    PAGES.extend(tuple(row) for row in json.loads(STUDY_PAGES.read_text()))
GROUPS = list(dict.fromkeys(p[3] for p in PAGES))

def h(value):
    if isinstance(value, list):
        value = " ".join(map(str, value))
    return escape(str(value), quote=True)

def identifier(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")

class Sections(HTMLParser):
    """Index visible text under the closest explicit section or heading target."""
    def __init__(self, title):
        super().__init__(convert_charrefs=True)
        self.parts = [{"anchor":"", "title":title, "words":[]}]
        self.title_tag = None
        self.title_parts = []
        self.in_svg = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "svg":
            self.in_svg = True
        anchor = attrs.get("id")
        if anchor and tag in ("section","article","details","div","h2","h3","dt","tr"):
            self.parts.append({"anchor":anchor, "title":"", "words":[]})
        if tag in ("h2","h3","dt","summary") and not self.parts[-1]["title"]:
            self.title_tag = tag
            self.title_parts = []

    def handle_endtag(self, tag):
        if tag == "svg":
            self.in_svg = False
        if tag == self.title_tag:
            self.parts[-1]["title"] = " ".join(" ".join(self.title_parts).split())
            self.title_tag = None

    def handle_data(self, data):
        if self.in_svg:
            return
        self.parts[-1]["words"].append(data)
        if self.title_tag:
            self.title_parts.append(data)

def navigation(slug):
    result = []
    for group in GROUPS:
        items = []
        for key, label, _, section, _ in PAGES:
            if group == section:
                current = ' aria-current="page"' if key == slug else ""
                items.append(f'<a href="{key}.html"{current}>{h(label)}</a>')
        result.append(f'<div class="nav-group"><p>{h(group)}</p>{"".join(items)}</div>')
    return "".join(result)

def source_body(sources):
    rows = []
    for s in sources:
        key = h(s["id"])
        pointers = ""
        for field, label in (("evidence_pointer", "Read this part"), ("evidence", "Evidence location"), ("engagement", "Observed engagement")):
            if s.get(field):
                pointers += f'<p><strong>{label}.</strong> {h(s[field])}</p>' 
        rows.append(f'''<article id="{key}" class="source-entry"><h3>{key} · {h(s["title"])}</h3>
<p class="source-details">{h(s["author"])} · {h(s["type"])}</p>
<dl><dt>Publication</dt><dd>{h(s["date"])}</dd><dt>Version or release</dt><dd>{h(s["version"])}</dd>
<dt>Supports</dt><dd>{h(s["claims"])}</dd><dt>Limit</dt><dd>{h(s["limits"])}</dd></dl>
{pointers}<a href="{h(s["url"])}">Original source or accessible record ↗</a></article>''')
    return '<section id="source-register"><h2>Source register</h2><p>Retrieval date for this edition: November 20, 2026. An access date does not establish a release date. Duplicate records from one publication count as one origin. Search this page or filter the guide to Evidence.</p></section>'+"".join(rows)

def add_after_intro(body, anchor, addition):
    start = body.find(f'id="{anchor}"') if anchor else 0
    if start < 0:
        raise ValueError(f"Missing insertion target {anchor}")
    end = body.find("</p>", start)
    if end < 0:
        raise ValueError(f"Missing introductory paragraph {anchor}")
    return body[:end+4] + addition + body[end+4:]

def prepare_chapter(slug, body, figures):
    if slug == "social-practice":
        for name in ("social-instagram.inc", "social-tiktok.inc"):
            body += (ROOT / "fragments" / name).read_text()
    if slug == "usage":
        body += (ROOT/"fragments/meter.inc").read_text()
    if slug == "research":
        body += (ROOT/"fragments/autoresearch.inc").read_text()
    if slug == "business":
        body = (ROOT/"fragments/newsletter.inc").read_text() + body
    if slug == "index":
        body += (ROOT/"fragments/timeout.inc").read_text()
    if slug == "labs":
        body = add_after_intro(body,"benchmark",(ROOT/"fragments/score.inc").read_text())
    if slug == "paths":
        body = body.replace("engineering.html#review","engineering.html#verification")
    if slug == "audit":
        record = ROOT/"fragments/verification.inc"
        if record.exists():
            body = body.replace('<div id="verification-record"></div>',record.read_text())
    for fig in figures:
        if slug != fig["page"]:
            continue
        src = h(fig["src"])
        caption = re.sub(r'\b([EPCO]\d\d)\b', r'<a href="sources.html#\1">\1</a>', h(fig["caption"]))
        source = f'<a href="{h(fig["source"])}" download>Mermaid source</a> · ' if fig.get("source") else ""
        if fig.get("detail"):
            source += f'<a href="{h(fig["detail"])}">Explore recorded runs</a> · '
        plate = f'<figure class="learning-figure"><img src="{src}" alt="{h(fig["alt"])}" loading="lazy"><figcaption>{caption} <span class="figure-links">{source}<a href="{src}">Full-size figure</a></span></figcaption></figure>'
        body = add_after_intro(body,fig.get("anchor"),plate)
    if slug.startswith("workshop-"):
        checks = [
            ("predict", "I predicted the first failure before I ran the command."),
            ("trace", "I can explain each state change in the worked example."),
            ("rebuild", "I reconstructed the core rule and checked a changed input."),
            ("transfer", "I wrote acceptance cases for one task in my own project."),
        ]
        labels = "".join(f'<p><label><input type="checkbox" data-progress-key="{key}"> {text}</label></p>' for key, text in checks)
        body += '<section id="mastery-record"><h2>Record your practice</h2><p>Check a step only after your attempt. These marks record your own assessment.</p>' + labels + '</section>'
    return body.replace("—", ", ").replace("–", "-")

def decorate(fragment):
    # Give unanchored headings a direct link without altering existing IDs.
    ids = set(re.findall(r'\bid=["\']([^"\']+)', fragment))
    def replace(m):
        level, attrs, title = m.groups()
        if re.search(r'\bid=', attrs):
            return m.group(0)
        stem = identifier(re.sub("<[^>]+>", "", title)) or "section"
        anchor = "topic-"+stem
        n = 2
        while anchor in ids:
            anchor = f"topic-{stem}-{n}"
            n += 1
        ids.add(anchor)
        return f'<h{level}{attrs} id="{anchor}">{title}</h{level}>'
    fragment = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>",replace,fragment,flags=re.S)
    # Wide tables must scroll locally on narrow screens.
    return re.sub(r"(<table\b.*?</table>)",r'<div class="table-scroll" role="region" aria-label="Scrollable data table" tabindex="0">\1</div>',fragment,flags=re.S)

def main():
    figures = [item for name in ("visuals","plates") for item in json.loads((ROOT/"data"/(name+".json")).read_text())]
    all_sources = []
    for path in sorted((ROOT/"data").glob("*-sources.json")):
        all_sources.extend(json.loads(path.read_text()))
    ids = [s["id"] for s in all_sources]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source ID")
    index = []
    for position,(slug,label,title,group,description) in enumerate(PAGES):
        fragment = source_body(all_sources) if slug == "sources" else (ROOT/"fragments"/(slug+".html")).read_text()
        body = decorate(prepare_chapter(slug,fragment,figures))
        parser = Sections(title)
        parser.feed(body)
        for part in parser.parts:
            words = " ".join(" ".join(part["words"]).split())
            if not words:
                continue
            href = slug+".html"+("#"+part["anchor"] if part["anchor"] else "")
            section = part["title"] or (part["anchor"].replace("-"," ").capitalize() if part["anchor"] else title)
            index.append(dict(title=label, section=section, href=href,text=words,group=group))
        toc = []
        for m in re.finditer(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>',body,flags=re.S):
            caption = re.sub("<[^>]+>","",m.group(2))
            toc.append(f'<a href="#{h(m.group(1))}">{caption}</a>')
        menu = navigation(slug)
        options = "".join(f'<option value="{g}">{g}</option>' for g in GROUPS)
        next_page = PAGES[(position + 1) % len(PAGES)]
        prev_page = PAGES[position - 1]
        description_html = f'<p class="deck">{h(description)}</p>' if description else ""
        contents = f'<details class="contents"><summary>On this page</summary><div>{"".join(toc)}</div></details>' if len(toc)>1 and slug!="index" else ""
        run_assets = '<link rel="stylesheet" href="assets/run-viewer.css"><script defer src="assets/run-viewer-data.js"></script><script defer src="assets/run-viewer.js"></script>' if slug == 'run-viewer' else ''
        workshop_state = ' data-workshop-progress' if group in ("Workshops", "Source studies") else ''
        page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(label)} | AI engineering field guide</title><link rel="stylesheet" href="assets/guide.css"><link rel="stylesheet" href="assets/workshop.css">
<script defer src="assets/search-index.js"></script><script defer src="assets/guide.js"></script><script defer src="assets/visuals.js"></script><script defer src="assets/study.js"></script><script defer src="assets/workshop.js"></script>{run_assets}</head>
<body class="page-{slug}"><a class="skip" href="#main">Skip to content</a>
<header class="mast"><div class="mast-inner"><a class="wordmark" href="index.html">Engineering field guide</a>
<nav class="mast-links" aria-label="Shortcuts"><a href="labs.html">Labs</a><a href="sources.html">Sources</a><a href="#find">Search ↓</a></nav></div></header>
<div class="layout"><aside class="rail"><nav aria-label="Chapters">{menu}</nav></aside>
<div class="reading"><details id="navigation"><summary>Browse chapters</summary><nav aria-label="Mobile chapters">{menu}</nav></details>
<main id="main" tabindex="-1"{workshop_state}><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Guide</a><span>/</span>{h(group)}<span>/</span>{h(label)}</nav>
<div class="title"><h1>{h(title)}</h1>{description_html}</div>{contents}
{body}</main>
<nav class="page-turn" aria-label="Adjacent chapters"><a href="{prev_page[0]}.html">← {h(prev_page[1])}</a><a href="{next_page[0]}.html">{h(next_page[1])} →</a></nav>
<section id="find" class="find"><h2>Search the guide</h2><div class="search-fields"><label>Words or source ID<input id="guide-search" type="search" placeholder="Try checkpoint or Grok Bot" autocomplete="off"></label>
<label>Section<select id="search-group"><option value="">All sections</option>{options}</select></label></div>
<p id="search-status" role="status"></p><div id="search-results"></div><noscript>Use the chapter menu or your browser's Find command.</noscript></section>
<footer><a href="audit.html">Methods and verification</a><a href="#main">Back to top ↑</a></footer></div></div></body></html>'''
        (ROOT/(slug+".html")).write_text(page)
    (ROOT/"assets/search-index.js").write_text("window.GUIDE_INDEX = "+json.dumps(index,ensure_ascii=False,separators=(",",":"))+";\n")
    print(f"{len(PAGES)} pages, {len(all_sources)} source records, {len(index)} search records")

if __name__ == "__main__":
    main()

