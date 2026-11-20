# Derive independent checks

Paste one prompt in a fresh session with the base and contract.
Give access to the review worktree only.
Keep the implementation transcript out of this session.

## Filled example

Use CONTRACT.md and the original CLI.
Write tests/test_review.py for a conflicting status and for each token field conflict.
Keep a gap in the input to check physical line numbers.
Include a repeat before a conflict to check that the first line stays fixed.
Check distinct values that differ in spaces.
Check an invalid token on a repeated key.
Use the existing CLI test helper.
Return your expected exit code, stdout, and stderr for each invalid case.

## Reuse

From {CONTRACT} on {BASE}, derive counterexamples for {CHANGE_BEHAVIOR}.
Own {REVIEW_TEST_PATH}.
Check {REPEAT_CASE}, {CONFLICT_CASE}, and {INVALID_CASE} through {PUBLIC_CALLER}.
For each, record input, expected effect, and source of the expectation.
Keep implementation files unchanged.
