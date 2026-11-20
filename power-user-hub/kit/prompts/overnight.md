# Overnight, only with a score

Provenance: original synthesis from Andrej Karpathy, No Priors, 20 Mar 2026. He said if you cannot evaluate, you cannot run the loop, and pushing it too far is net harmful.

```text
Metric: {{COMMAND}}
Direction: {{higher_or_lower}}
Trials: {{N}}
Allowed: {{PATHS}}
Forbidden: {{SECRET_PATHS}}

Do not ask questions.
Each trial changes one thing, reruns the metric, and writes a row to RESULTS.md with before, after, and kept or reverted.
Stop after {{N}} trials or two non-improvements.
If the metric command fails, stop and write the stderr. Do not invent a number.
```
