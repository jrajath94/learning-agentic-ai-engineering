# Hand off work for recovery

## Purpose

Give the next person enough state to continue safely.

## Inputs

Task state, revision, commands, outputs, open risks.

## Constraints

Do not claim unrun checks. Preserve paths and stop conditions.

## Output

Handoff with status, evidence, next action, and recovery rule.

## Verification

Confirm paths exist and the restart condition matches saved state.

## Stop

Stop at a human review or unresolved failure.
