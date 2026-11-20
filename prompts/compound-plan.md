# Compound Plan (Klaassen form)

Purpose: plan with research sub agents, then compound learnings.
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
for a human call before work starts.
