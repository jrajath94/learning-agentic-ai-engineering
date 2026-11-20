# Review a change for defects

## Purpose

Review a patch against behavior, risk, and evidence.

## Inputs

Diff, specification, tests, runtime context.

## Constraints

Do not rewrite for style unless style hides a defect. Cite line or behavior.

## Output

Findings by severity, evidence, impact, and fix. State checks not run.

## Verification

Confirm each finding from the diff and a reproducible case.

## Stop

Stop after reviewing changed paths and relevant callers.
