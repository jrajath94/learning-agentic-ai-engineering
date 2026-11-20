# Research Swarm (Anthropic form)

Purpose: one lead, parallel sub agents, a judged synthesis.
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
was wrong. Replan before more calls.
