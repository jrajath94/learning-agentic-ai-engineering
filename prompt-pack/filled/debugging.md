# Debug from evidence

## Purpose

Explain why the invoice returns 216 instead of 217 cents.

## Inputs

Subtotal 200 cents, tax rate 8.25 percent. Current code converts tax to int. Expected half-cent rounds up.

## Constraints

Use the supplied function and reproduce first. Do not change the rule.

## Output

Trace 200 × 8.25 / 100. Identify truncation of 16.5 to 16. Replace float conversion with exact integer rounding.

## Verification

Check 200 cents gives 217 and a non-half-cent case remains correct.

## Stop

Stop if the input or rule differs from the reported case.
