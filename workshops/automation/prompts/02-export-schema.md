# Specify an export validator

## Filled prompt

Review `fixtures/posts.jsonl` and `fixtures/conflict.jsonl`. Write rules for an offline JSONL validator. Accept the fields `source_id`, `date`, `title` and `body`. Use the ISO week `2026-W45`. Keep source offsets in decoded Unicode code points. Give a rule for repeated IDs with different data. Classify lines 6 and 7 from the first fixture and lines 1 through 4 from the second fixture. Give expected issue codes. Preserve the accepted source body exactly.

## Reference response

| Fixture and line | Action | Code |
| --- | --- | --- |
| posts line 6 | Skip the prior Sunday | `outside_week` |
| posts line 7 | Skip the record that lacks a body | `invalid_fields` |
| conflict lines 1 and 2 | Set aside both versions of SRC-201 | `conflicting_source_id` |
| conflict line 3 | Keep SRC-202 | No issue |
| conflict line 4 | Reject the second title member | `duplicate_json_member` |

Decode UTF-8 before parse. Use a half-open Monday-to-Monday date range. Limit size before parse and reject malformed types. Save the accepted body with its line endings and code points intact.

## Reusable prompt

Specify a validator for `{{export_format}}` with `{{required_fields}}`. Use `{{encoding}}`, `{{period_rule}}`, `{{size_limits}}`, `{{id_rule}}` and `{{offset_unit}}`. Classify `{{fixture_rows}}` by action and stable issue code. Define a rule for multiple rows with the same ID. List the fields and transformations that affect evidence offsets.
