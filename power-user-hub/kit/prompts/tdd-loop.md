# One failing test, then the fix

Provenance: original synthesis. The loop rules are the verbatim skill at `kit/claude/skills/tdd/SKILL.md` (mattpocock/skills `abeeaf95660ba9e8b7c753eb38f441ca707a8823`).

```text
Bug: {{SYMPTOM}}
Seam to test: {{PUBLIC_FUNCTION_OR_ROUTE}}
Command: {{TEST_COMMAND}}

Write one failing test at that seam. Run {{TEST_COMMAND}}. Paste the failure.
Stop. Do not change production code in this turn.

After I reply "green", change only enough code to make that test pass.
Run {{TEST_COMMAND}} again. Paste the pass.
Do not add a second test in this turn.
```
