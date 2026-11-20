# Execute a fixed budget and checkpoint

## Reusable prompt

Execute a frozen development plan and preserve evidence for every attempted candidate.

Inputs

- Authorized commands and paths: <commands and paths>
- Baseline and candidate plan: <path>
- Run directory and budget: <directory, count and timeout if applicable>
- Metrics and guardrails: <contract>
- Checkpoint format: <artifact>

Run the baseline once per input digest. Before each candidate, check that the previous checkpoint and input digest agree. Run the next declared candidate. Save the result, errors, configuration, guard states, and incumbent after the decision. Publish the completed checkpoint before you advance. Resume at the next unsaved candidate. Pause if data, policy, or code differs. Use only development inputs until selection stops.

Return a ledger with attempt, configuration, hypothesis, metrics, guard states, decision, and incumbent. Return the number of attempts charged and the reason for stop or pause.

## Filled example

Run `python3 -B run.py dev --out session-01 --stop-after 2`. Preserve the checkpoint with the titles incumbent. Resume with `python3 -B run.py dev --out session-01`. Stop at four saved candidates with combined as incumbent. Preserve the wide discard although it beats the baseline.

## Check

Compare the final resumed checkpoint to a fresh run under the same digest. The first two ledger rows must appear once.
