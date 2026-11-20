# Implement a bounded change

## Purpose

Fix invoice tax rounding and add the optional discount.

## Inputs

service.py and test_service.py. 200 cents at 8.25 percent must return 217.

## Constraints

Keep one-argument calls valid. Use cents as integers. Reject bool despite bool being an int subtype.

## Output

Update the function and tests for discount before tax, zero taxable amount, and exact half-cent rounding.

## Verification

Run the service tests. Confirm the 10²⁰-plus case and inspect the diff.

## Stop

Stop if a required test fails or the change needs another module.
