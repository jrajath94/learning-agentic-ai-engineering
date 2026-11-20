from .records import TraceError


def rollup(records):
    """Return one set of terminal result totals per run."""
    runs = {}
    seen = {}
    for record in records:
        key = (record.run_id, record.case_id)
        signature = (record.status, record.input_tokens, record.output_tokens)
        previous = seen.get(key)
        if previous is not None:
            first_signature, first_line = previous
            if signature != first_signature:
                raise TraceError(
                    f"line {record.line}: terminal result conflicts with line {first_line}"
                )
            continue
        seen[key] = (signature, record.line)
        totals = runs.setdefault(
            record.run_id,
            {"passed": 0, "failed": 0, "input_tokens": 0, "output_tokens": 0},
        )
        count_field = "passed" if record.status == "pass" else "failed"
        totals[count_field] += 1
        totals["input_tokens"] += record.input_tokens
        totals["output_tokens"] += record.output_tokens
    return {"runs": runs}
