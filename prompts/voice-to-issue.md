# Voice to Issue (Cora form)

Purpose: turn a dictated rough idea into a filed issue.
Inputs: voice transcript, repo, board lanes.

PIPELINE PROMPT:
Take this rough idea: <TRANSCRIPT>
Stage 1, ground: research the codebase. What exists near this
idea? Name files and current behavior.
Stage 2, research: search the web and open source for best
practice on this problem. Cite sources.
Stage 3, plan: present a plan for my review. Ask what a good
product manager would ask, with two options per open point.
Stage 4, file: on my approval, create the issue with five
parts: problem statement, solution vision, requirements,
technical requirements, implementation steps. File it in the
<LANE> lane.

EVAL RULE: run this command on ten sample ideas. Where the
output fails the five part form, rewrite this prompt until
the pass holds ten of ten.
VERIFY: the issue stands alone. A developer can build from
the issue with no chat history.
