# Review a pinned patch

Paste one prompt in a fresh read-only session after the candidate commit.
Give access to a detached probe directory with the review tests.
Replace the revision labels with full commit IDs from your repository.

## Filled example

Review the diff from the original rollup commit to the first retry candidate.
Read CONTRACT.md and inspect the changed aggregation logic.
Run fixtures/conflict.jsonl through the candidate CLI.
Run the independent tests in the probe.
For each finding, give the candidate revision, file, location, and one reproduction.
Include expected and observed exit code, stdout, and stderr.
Explain which consumer can receive the wrong report.
Keep the probe unchanged.

## Reuse

Review {BASE} to {CANDIDATE}. Use {REVIEW_SCOPE} and {CONTRACT}.
Begin with {DIFF_COMMAND}.
Run {INDEPENDENT_CHECKS} on {CANDIDATE_WORKTREE}.
Return {SEVERITY_RULE}, location, expected, observed, and command.
Label a finding unverified if you cannot reproduce it.
Keep all files unchanged.
