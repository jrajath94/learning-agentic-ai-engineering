# One metric, then leave the loop

Provenance: original synthesis from Andrej Karpathy on No Priors, 20 Mar 2026. Source transcript gist: https://gist.github.com/idvorkin-ai-tools/0de1c2615dfb58182ac149cdbec53977 (YouTube https://www.youtube.com/watch?v=kwSVtQ7dziU). The gist does not timestamp the December and auto-research passages. He said he had not typed a line of code since December, that he wants more than one Claude Code or Codex session, and that auto research only works when you can evaluate. His overnight run found weight decay and Adam beta settings he had missed. He called his program.md a rough markdown description of the loop. This file is not his program.md.

Do not use this on a task you cannot score. He said that if you cannot evaluate, you cannot auto-research it, and that pushing the loop too far is net harmful.

## Prompt

```text
Metric command: {{COMMAND_THAT_PRINTS_A_NUMBER}}
Direction: {{higher_or_lower}}
Budget: {{MAX_TRIALS}} trials, then stop.
Allowed files: {{PATHS}}
Forbidden: {{CUSTOMER_DATA_PATHS_OR_SECRETS}}

You are outside my chat. I will not answer questions.

Loop:
1. Run the metric command. Record the number.
2. Change one thing inside the allowed files.
3. Run the metric command again.
4. Keep the change only if the number moved in the stated direction and tests in {{TEST_COMMAND}} still pass.
5. Write one line to RESULTS.md: trial, change, before, after, kept or reverted.

Stop at the budget, or when two trials in a row do not improve.
Do not invent a metric. If the command fails, stop and write the error.
```

## Self-check

RESULTS.md has before and after numbers from the command, not from the model's estimate. Reverted trials are still listed. Secrets and customer paths are absent from the diff.
