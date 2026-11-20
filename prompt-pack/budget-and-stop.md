# Allocate a bounded agent attempt

Attach the task contract and current evidence. State the work that remains. Estimate calls by role and distinguish input, output and cached input units when the provider exposes them. Keep token quantities separate from prices and currency.

Choose the least expensive model that meets this task's quality requirement. Use a stronger model only when a concrete failed case requires it. Record the reason for escalation in the run log. Delegate only independent work with a named owner and an inspectable output.

Before each new attempt, compare its expected information gain with the remaining budget. Stop when the acceptance test passes, the budget reaches its ceiling, or two attempts repeat the same failure without a new hypothesis. A long answer does not count as new evidence.

Return a ledger with task, model, input tokens, output tokens, cached tokens when known, elapsed time, observed outcome and next decision. Mark unreported values as unknown. Never fill usage from a guessed response length.

## Filled illustrative allocation

Use one worker to reproduce the defect, one worker to implement after reproduction, and one fresh reviewer. Discovery and review may use a small model if they return source paths and executable checks. Allow a single escalation for an unresolved algorithmic invariant. The ceiling is 6 model calls. The expected result is a final diff that passes the original failing case and its boundary checks. These are proposed limits, not measurements of a provider run.
