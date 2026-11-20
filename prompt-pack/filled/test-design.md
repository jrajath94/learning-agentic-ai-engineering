# Design tests from rules

## Purpose

Test invoice discount and rounding.

## Inputs

Discount comes before tax. Tax rounds up at half-cent. Taxable base cannot go below zero.

## Constraints

Test public behavior. Do not call private helpers or compute expected values with the same formula.

## Output

Cases: omitted discount; 300 less 100 gives 217; discount equals subtotal gives 0; half-cent rounds up; huge amount exact; reject -1, 1.5, True.

## Verification

Manually derive 200 cents × 825 / 10000 = 16.5 cents, then 17.

## Stop

Stop if a rule has no expected output.
