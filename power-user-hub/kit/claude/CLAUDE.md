# Project facts Claude cannot see in the code

Provenance: original synthesis. The rule "only write what the repo does not already show" is from Anthropic's best-practices page, fetched 2026-11-20: https://code.claude.com/docs/en/best-practices

Keep this file short. Procedures belong in `skills/`, not here.

- Tests: `{{TEST_COMMAND}}`
- Do not edit: `{{GENERATED_DIR}}`
- A change is done only when `{{TEST_COMMAND}}` exits 0 and a person has read the diff.
- Customer data, account numbers, and production credentials are out of scope. Refuse paths under `{{SECRET_DIR}}`.
