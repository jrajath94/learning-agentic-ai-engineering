# Grill Session (Pocock grilling form)

Purpose: sharpen a plan by interview before any build.
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
named in the plan, before the build starts.
