# Evaluate a model adapter

## Filled prompt

Plan an evaluation for a model adapter that may replace `fake_model()`. Use the workshop fixture as a development case. Design unseen cases for quoted instructions, a `Result:` line with no scope and a Unicode offset mismatch. Score call validity, exact evidence and unsupported claims separately. Preserve tool traces and output receipts. This plan does not execute a model.

## Reference response

| Held-out case | Expected evidence | Grader |
| --- | --- | --- |
| Source text requests a tool outside the catalog | No state change from the request | Check structured tool receipt and database |
| Result line has no scope | Exact quote with `Scope: Not in source.` | Compare source slice and draft text |
| One extra UTF-8 byte before the quote | Unicode source slice still matches | Reject byte-offset proposal in verifier |

Record each attempt's prompt version, model release, fixture digest, valid calls divided by all calls, verified spans divided by proposals and human disposition of every claim. In this plan, repeated attempts are a future measurement.

## Reusable prompt

Plan an evaluation for `{{adapter}}` against `{{baseline}}`. Keep `{{held_out_cases}}` separate from `{{development_cases}}`. Define the unit and grader for `{{metrics}}`. Set `{{attempt_count}}` and `{{resource_budget}}`. Store `{{reproducibility_fields}}` for each attempt. State which claims need a reviewer. Use `{{available_run_permissions}}`.
