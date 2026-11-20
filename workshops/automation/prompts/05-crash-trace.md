# Diagnose an ambiguous retry

## Filled prompt

The process returned code 73 and no receipt for `2026-W45`. Read `results/replay.json`. Explain the before-commit and after-commit histories. Identify which history code 73 represents in this fixture. Give the database query and expected counts before issuing a retry. Use run keys. Do not delete SQLite rows.

## Reference response

Before commit, the run row and snapshot event remain. The draft count is zero and its evidence count is zero. Code 73 means the injected stop occurred after the draft commit. Query the rows by the same `run_key`.

```sql
SELECT state FROM runs WHERE run_key = ?;
SELECT COUNT(*) FROM drafts WHERE run_key = ?;
SELECT COUNT(*) FROM evidence WHERE run_key = ?;
```

The recorded result is `draft_staged`, one draft and three evidence rows. Rerun with the same input file and week. Expect `reused` and the same draft key.

## Reusable prompt

Diagnose `{{ambiguous_failure}}` in `{{workflow}}` with `{{trace}}`. List plausible persisted histories. Name the evidence that selects one history. Give read-only checks for `{{operation_key}}`. Predict the outcome of a retry with the same key. Identify which failure requires correction before retry.
