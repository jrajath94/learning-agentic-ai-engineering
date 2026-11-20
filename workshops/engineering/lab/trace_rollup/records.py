from dataclasses import dataclass
import json


class TraceError(ValueError):
    """The export cannot produce a valid report."""


@dataclass(frozen=True)
class Result:
    line: int
    run_id: str
    case_id: str
    status: str
    input_tokens: int
    output_tokens: int


def read_records(lines):
    for line, text in enumerate(lines, start=1):
        if not text.strip():
            continue
        try:
            item = json.loads(text)
        except json.JSONDecodeError as error:
            raise TraceError(f"line {line}: invalid JSON") from error

        if not isinstance(item, dict):
            raise TraceError(f"line {line}: expected an object")
        run_id = item.get("run_id")
        case_id = item.get("case_id")
        for field, value in (("run_id", run_id), ("case_id", case_id)):
            if not isinstance(value, str) or not value.strip():
                raise TraceError(f"line {line}: invalid {field}")

        status = item.get("status")
        if status not in ("pass", "fail"):
            raise TraceError(f"line {line}: invalid status")
        input_tokens = item.get("input_tokens")
        output_tokens = item.get("output_tokens")
        for field, value in (
            ("input_tokens", input_tokens),
            ("output_tokens", output_tokens),
        ):
            if type(value) is not int or value < 0:
                raise TraceError(f"line {line}: invalid {field}")

        yield Result(line, run_id, case_id, status, input_tokens, output_tokens)
