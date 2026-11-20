# Verify the combined revision

Paste one prompt at the integration worktree.
Give permission to inspect and run tests.
Do local merges yourself unless you explicitly delegate them.

## Filled example

Identify the base, repaired implementation commit, and review commit.
Inspect each branch diff against the same base.
Confirm that the implementation branch owns aggregate.py and test_retries.py.
Confirm that the review branch owns test_review.py.
After both branches merge into main, record the combined commit and parent IDs.
Run git diff --check BASE HEAD and the full test suite.
Run nightly, conflict, invalid, and legacy fixtures on the combined commit.
Keep the revision local.

## Reuse

At {INTEGRATION_PATH}, inspect {BASE}, {IMPLEMENTATION}, and {REVIEW}.
Compare changed paths with {BRANCH_OWNERSHIP}.
Record the combined revision and its expected parents.
Require {CHECK_COMMANDS}, {EXPECTED_RESULTS}, and a clean worktree.
Stop on an unexpected parent, conflict, or failing check.
