# Design tests from rules

## Purpose

Turn each rule into a test that can fail for the right reason.

## Inputs

Acceptance rules, current tests, boundaries, failure history.

## Constraints

Include boundary and invalid cases. Avoid copying implementation logic.

## Output

Test matrix and a small set of highest-value examples.

## Verification

Check expected values independently and ensure each test distinguishes a plausible bug.

## Stop

Stop when every stated rule has coverage or a gap is explicit.
