# Calibrate a review before a larger batch

Attach the task contract, final diff, baseline result and current test output. Start a fresh review context. The author explanation can provide navigation, but findings must come from the diff and evidence.

Read one changed function and its callers. Derive the behavior for one ordinary input, one boundary input and one malformed input. Predict the result before executing a test. Compare the prediction with the actual result.

For each finding, give the file and function, trigger input, observed or deduced behavior, expected behavior from the contract, and a minimal reproduction. Mark a deduction as unexecuted until a command confirms it. Omit a proposed issue if you cannot identify its trigger or consequence.

Return a review with three sections. Include confirmed defects, unresolved questions and checked behavior. A passing test is evidence for its stated case. Explain a missing case when it matters to the contract.

After I inspect this one review, apply the same standard to the remaining changed functions. Keep one owner per edited file. Re-run relevant checks after the final repair. A review before the final repair cannot approve the new revision.

## Filled example

A function aggregates agent trace events. Two rows repeat the same event ID after a client retry. The contract counts logical events once. Use a fixture with an original event, its identical replay and a distinct event. Inspect whether the implementation deduplicates before it aggregates tokens. Then change the replay content and check whether the conflict is rejected. A set of IDs can suppress a conflicting event without exposing the inconsistency. State the expected conflict rule before approval.
