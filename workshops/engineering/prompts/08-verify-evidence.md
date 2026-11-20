# Audit a patch claim

Paste one prompt in a fresh session after integration.
Give the run record, commands, and allowed worktree.
Keep any real logs outside the prompt.

## Filled example

Read evidence/run.txt and test files in the combined trace rollup tree.
Find one record from the base, one from the candidate, and one from the combined revision.
Check that each report has the expected decision value.
Confirm that the conflict fixture returns exit 2 and empty stdout on the combined revision.
List any requirement with no executable check.
Report which results you reran and which you read from the record.

## Reuse

Audit {EVIDENCE_RECORD} for {REVISION}.
Match {CLAIMS} to command, input, exit code, stdout, stderr, and revision.
Rerun {ALLOWED_COMMANDS} if the worktree is available.
Record observations and evidence gaps separately.
Keep the worktree unchanged.
