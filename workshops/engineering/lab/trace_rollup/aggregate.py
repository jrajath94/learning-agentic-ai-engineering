def rollup(records):
    """Return one set of terminal result totals per run."""
    runs = {}
    for record in records:
        totals = runs.setdefault(
            record.run_id,
            {"passed": 0, "failed": 0, "input_tokens": 0, "output_tokens": 0},
        )
        count_field = "passed" if record.status == "pass" else "failed"
        totals[count_field] += 1
        totals["input_tokens"] += record.input_tokens
        totals["output_tokens"] += record.output_tokens
    return {"runs": runs}
