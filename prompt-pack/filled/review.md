# Review a change for defects

## Purpose

Review a patch that adds invoice discounts.

## Inputs

Spec: exact cents, optional discount, deduction before tax, nonnegative base. Diff and test output are attached.

## Constraints

Treat tests as evidence, not proof. Do not infer unseen files.

## Output

Check compatibility, validation including bool, rounding, large values, and test independence. Report only actionable findings.

## Verification

Recompute the 200-cent case and inspect whether tests catch float truncation.

## Stop

Stop if the diff or acceptance rules are missing.
