# Harness Loop (OpenAI form)

Purpose: self review loop with docs as the system of record.
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
STOP: escalate only on a judgment call, with the options named.
