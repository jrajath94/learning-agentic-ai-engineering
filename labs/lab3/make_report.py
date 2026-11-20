"""Lab 3: business workflow. Input: source ledger from the research report.
Output: a cited operations report a human can review before any use.
Steps a business bot fleet would run: collect, dedupe, count, draft, human gate.
This script runs collect to draft only. No send act takes place.
"""
import re, collections, pathlib
report = pathlib.Path.home() / "workspace/research_notes/ai-power-user-intelligence-hub-20261120-1627/report.md"
text = report.read_text()
ledger = text.split("### 12.")[1].split("### 13.")[0]
rows = []
for line in ledger.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 6 and cells[0].isdigit():
        rows.append(cells)
conf = collections.Counter(r[5].split("(")[0].strip() for r in rows)
out = ["# Cited operations report, Lab 3", "", f"Sources in ledger: {len(rows)}", ""]
out.append("## Confidence split")
for k, v in conf.most_common():
    out.append(f"- {k}: {v}")
out += ["", "## Review gate", "", "A human must check each Low row before use in a decision.", "No mail, post or spend act ran in this lab.", "", "## Sample citations"]
for r in rows[:5]:
    out.append(f"- [{r[0]}] {r[1]} - {r[2]}")
pathlib.Path("report_artifact.md").write_text("\n".join(out) + "\n")
print(f"rows={len(rows)} confidence={dict(conf)}")
print("artifact=report_artifact.md")
