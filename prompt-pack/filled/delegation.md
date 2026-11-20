# Delegate bounded subtasks

## Purpose

Delegate an audit of the support queue report.

## Inputs

Task A checks CSV counts. Task B checks citations in draft.md. Task C checks restart state and review boundary.

## Constraints

No worker edits files. Use same CSV and draft. No external delivery.

## Output

Return three short reports with row IDs or state fields, one issue each if found, and exact evidence.

## Verification

Merge only claims that cite input rows or checkpoint fields.

## Stop

Stop if source files differ across workers.
