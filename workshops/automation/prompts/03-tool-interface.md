# Design a narrow source tool

## Filled prompt

Design `get_evidence_window` for an agent that writes evidence proposals for the weekly research draft. The executor has an active snapshot. Inputs are `source_id`, `start` and `max_chars`. The maximum slice is 600 Unicode code points. Disallow extra keys. Use SRC-103 with offset 46 and length 72 as the success case. Give a repairable error for `start: true`, an extra `destination`, and an unknown source. The tool can read from the snapshot only.

## Reference response

```json
{"tool":"get_evidence_window","arguments":{"source_id":"SRC-103","start":46,"max_chars":72}}
```

Success returns offsets `[46:118]`, the verbatim query result and `next_start: 118`. The `untrusted_text` property contains the source data. `start: true` yields `invalid_start`. `destination` yields `invalid_arguments`. A well-formed ID outside this run yields `unknown_source`. Return a stable code and a correction for each error. Do not include a source body on an error.

## Reusable prompt

Design `{{tool_name}}` for `{{user_task}}`. Allow `{{permitted_reads_or_writes}}` against `{{scope}}`. Specify exact inputs, type checks, size bounds and output shape. Use `{{valid_request}}` to give a success response. Use `{{invalid_requests}}` to give codes and corrections. Describe what the executor does before it reads data or makes a write.
