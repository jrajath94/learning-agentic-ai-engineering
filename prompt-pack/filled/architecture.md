# Choose a small design

## Purpose

Plan the invoice discount change.

## Inputs

The service is one function. Existing calls pass only subtotal. Eight tests cover rounding, big values, and invalid inputs.

## Constraints

Do not add a dependency, class, or new public type.

## Output

Keep one function. Add optional discount_cents=0. Validate both integer inputs, cap taxable amount, then compute tax with integer arithmetic.

## Verification

Trace omitted discount, equal discount, and 10²⁰-plus subtotal through the proposed steps.

## Stop

Stop if the required exception contract is absent.
