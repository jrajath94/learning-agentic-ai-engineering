# Write acceptance criteria

## Purpose

Add an optional discount in cents to the invoice service.

## Inputs

Subtotal 300 cents, discount 100, tax 8.25 percent. Existing one-argument calls must work. Tax rounds up at half a cent. Reject negatives, fractions, and Booleans.

## Constraints

Preserve the API. Deduct discount before tax. Cap taxable cents at zero. Use exact integer arithmetic.

## Output

Checks: 200 taxable cents returns 217 total cents; equal discount returns zero; omitted discount matches old call; invalid values fail.

## Verification

Calculate tax as 16.5 cents, rounded to 17. Check large values without floats.

## Stop

Stop if discount range or error type is unspecified.
