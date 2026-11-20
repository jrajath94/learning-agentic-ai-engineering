# Make the held-out decision

## Reusable prompt

Grade the locked configuration and make the declared decision.

Inputs

- Input digests: <development and held-out>
- Baseline and locked configuration: <versions>
- Paired held-out report: <path>
- Acceptance and stop rule: <contract>
- Owner of the next test set: <role>

Verify the split, required case counts, and unchanged reference labels. Apply each guard independently. Report each failure and its evidence ID. Choose accept or retain baseline by the contract. Record an inconclusive result when required evidence or a run is missing. Do not try a second candidate on the same held-out data.

Return decision, score deltas, guard verdicts, critical case IDs, limits, and next test ownership.

## Filled example

Retain the baseline. On the workshop holdout, candidate minus baseline recall is zero and precision is +1/6. The minimum recall and no-new-critical-miss guards fail. H03 loses V11. Treat H03 as a development regression candidate and assign a different ambiguous family to the next sealed holdout.

## Check

The conclusion must agree with both the exact score deltas and the critical trace. An increase in precision cannot override a failed guard.
