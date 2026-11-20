# Terminal evaluation export contract

Pass a UTF-8 JSONL file path to `python3 -B -m trace_rollup`.
A blank line has no result. Keep physical line numbers for error reports.
Each nonblank line must contain a JSON object with these fields.

| Field | Rule |
| --- | --- |
| run_id | Nonblank string. Retain its value and case. |
| case_id | Nonblank string. Retain its value and case. |
| status | String `pass` or `fail`. |
| input_tokens | Integer at least zero. Boolean values are invalid. |
| output_tokens | Integer at least zero. Boolean values are invalid. |

The exporter provides one terminal result per pair of run ID and case ID.
The transport can deliver that result more than once.
The tuple of status, input tokens, and output tokens defines the result for comparison.
The report counts an equal tuple for the same pair once.
The report counts the same case ID in separate runs independently.
Two unequal tuples for one pair invalidate the file.
The error identifies the first accepted line and the conflicting line.

Fields outside the table are optional metadata.
The legacy exporter has no delivery ID or schema field.
Delivery identifiers, optional metadata, and JSON field order have no effect on totals.
A retry here means a delivery retry of one terminal result.
The export has no operation for a new evaluation attempt within the same pair.

On success, print one JSON object with a `runs` map.
Each run has `passed`, `failed`, `input_tokens`, and `output_tokens` integer fields.
Sort JSON keys and end the report with one newline.
An empty export has an empty runs map.
Exit with status 0 after success.

On an invalid row or a conflict, print an error to stderr and exit with status 2.
Leave stdout empty on error, even after valid rows.
The command does not change the file or keep state between runs.
