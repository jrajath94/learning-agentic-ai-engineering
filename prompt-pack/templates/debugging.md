# Debug from evidence

## Purpose

Find the smallest cause that explains a failure.

## Inputs

Failing command, input, output, source revision, expected rule.

## Constraints

Do not guess from the error label. Change one cause at a time.

## Output

Reproduction, cause, minimal repair, regression check, uncertainty.

## Verification

Re-run the same input and one neighboring case.

## Stop

Stop when evidence does not isolate one cause. Ask for the missing artifact.
