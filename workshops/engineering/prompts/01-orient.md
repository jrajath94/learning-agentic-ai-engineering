# Map the public entry point

From a clean repository root, paste one prompt into a read-only agent session.
Give it the base revision from `git rev-parse HEAD`.
Use the same prompt as a checklist if you work alone.

## Filled example

Read AGENTS.md, CONTRACT.md, trace_rollup/__main__.py, trace_rollup/records.py, and trace_rollup/aggregate.py.
Inspect tests/test_baseline.py and fixtures/nightly.jsonl.
Run the base smoke command and the nightly CLI command.
Locate the public entry point, validation site, counter site, and output boundary.
For each claim, give a file and symbol or an observed command result.
Mark missing producer behavior as unknown.
Return a table with path, responsibility, and evidence.
Stop after the map. Keep all files unchanged.

## Reuse

Inspect {APPLICABLE_INSTRUCTIONS}, {CONTRACT}, {ENTRY_POINT}, {INPUT_BOUNDARY}, and {TESTS} on {BASE}.
Run {SMOKE_COMMAND} and {PUBLIC_SAMPLE_COMMAND}.
Map input, output, changed behavior, and caller risk.
Return path, location, observed evidence, and unknowns.
Keep the worktree unchanged.
