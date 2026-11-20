# Hand off work for recovery

## Purpose

Hand off a support report workflow after a write-timeout.

## Inputs

The workflow writes draft.md, then the process times out before returning. state.json records stage and fingerprint.

## Constraints

Do not rerun blindly or send the report. Confirm input fingerprint and draft content first.

## Output

Status: write may have completed. Inspect checkpoint, verify exact draft, then resume to review. If missing or mismatched, retain failure and ask for repair.

## Verification

Use a restart with the same output path. Confirm unchanged draft and zero extra writes on intact output.

## Stop

Stop before any external delivery or if fingerprint changed.
