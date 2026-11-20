# Fleet Review (reviewer personas form)

Purpose: review one change set with parallel persona reviewers.
Inputs: DIFF or PR link, spec or task card.

Run five reviewers in parallel, each returns findings only:
1. Spec reviewer: does the change match the task card, line by
   line? Name each gap.
2. Security reviewer: input paths, auth checks, secret handling,
   data exposure. Name file and line.
3. Architecture reviewer: layer order, dependency direction,
   duplicate abstractions.
4. Simplicity reviewer: code that can shrink, dead branches,
   needless options.
5. Rules reviewer: project rule file, style gate, test state.

MERGE RULE: findings merge into one list, graded:
P1 never merge. P2 fix before next task. P3 log it.
No auto fix. The human triages. Approved fixes go out as
parallel tasks with the finding text attached.
VERIFY: each finding names a file, a line, and a fix.
STOP: a reviewer with no findings states the areas it read.
