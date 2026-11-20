# Propose a candidate and ablation

## Reusable prompt

Propose the smallest change that could fix a named rank error.

Inputs

- Failing trace: <query and missed reference>
- Allowed settings or code paths: <list>
- Frozen inputs and score rule: <list>
- Baseline score and budget: <values>
- Known counterexample: <query or failure mode>

State a causal hypothesis about the trace. Predict which term or rule can change the rank. Specify one change, one paired control, and one counterexample case. If a change needs two parts, define an ablation for each part. Keep the query cases, index, result count, grader, metric, and cost budget fixed.

Return candidate settings, predicted rank changes, two risk checks, and a discard condition. Mark observations separately from predictions.

## Filled example

For D01, predict that the added word jam and title hits can promote K11 and K12. Test alias-only, title-only, and both. Keep two slots per query. Check D04 for the seal alias and D03 for a critical exact match. Discard any candidate with a new critical miss or one that fails to exceed the incumbent recall under the contract.

## Check

Confirm that the ablation keeps tight aliases when title weight returns to zero. A comparison that changes both settings cannot isolate either contribution.
