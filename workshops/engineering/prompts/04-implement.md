# Repair the owning code path

Paste one prompt in the implementation worktree after the red test.
Give exact edit permissions.
Use the lab candidate file only to reproduce the planned review exercise.

## Filled example

Edit trace_rollup/aggregate.py to fulfill CONTRACT.md.
Use the pair of run ID and case ID for identity.
Compare status, input tokens, and output tokens on each repeat.
Keep the first physical line for diagnostics.
Return equal repeats without another counter increment.
Raise TraceError for conflicting tuples.
Run the retry and baseline tests and use the CLI on the conflict fixture.
Return changed files, command results, and remaining assumptions.
Keep parser, CLI and fixture files unchanged.

## Reuse

Implement {RULE} in {OWNING_PATH} on {BASE_OR_RED_REVISION}.
Preserve {LEGACY_BEHAVIOR} and {PUBLIC_INTERFACE}.
Run {REGRESSION_COMMAND} and {PUBLIC_SAMPLE_COMMAND}.
Report edits, exact checks, and cases the checks omit.
Stop if {SCOPE_BOUNDARY} must change.
