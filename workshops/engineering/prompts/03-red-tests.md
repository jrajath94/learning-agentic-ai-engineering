# Record the regression before the repair

Paste one prompt in the implementation worktree at the pinned base.
Provide the approved task note and the list of files you can edit.
Check the failing assertion yourself before any implementation change.

## Filled example

Add tests/test_retries.py only.
Invoke the public CLI for fixtures/nightly.jsonl.
Assert the report for nightly-a and nightly-b, including both token totals.
Repeat the call with the input lines in reverse order.
Do not use output from the implementation to set expected values.
Run python3 -B -m unittest discover -s tests -v.
Report the exit code, failure names, and expected and observed values.
Stop before you edit trace_rollup/aggregate.py.

## Reuse

Change only {REGRESSION_TESTS}.
Assert {EXPECTED_PUBLIC_OUTPUT} for {SYNTHETIC_REPRODUCTION}.
Run {TEST_COMMAND} on {BASE}.
Report the oracle source, observed response, and failing assertion.
If the test passes or the test setup fails, stop and explain why.
