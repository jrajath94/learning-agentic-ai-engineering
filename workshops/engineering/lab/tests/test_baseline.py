import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


LAB = Path(__file__).resolve().parents[1]


def run_cli(source):
    return subprocess.run(
        [sys.executable, "-B", "-m", "trace_rollup", str(source)],
        cwd=LAB,
        text=True,
        capture_output=True,
        check=False,
    )


def run_rows(source):
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / "trace.jsonl"
        fixture.write_text(source, encoding="utf-8")
        return run_cli(fixture)


class BaselineTests(unittest.TestCase):
    def test_legacy_export_without_delivery_metadata(self):
        result = run_cli(LAB / "fixtures" / "legacy.jsonl")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            json.loads(result.stdout),
            {"runs": {"legacy": {
                "passed": 1, "failed": 1,
                "input_tokens": 7, "output_tokens": 2,
            }}},
        )

    def test_invalid_row_does_not_emit_partial_report(self):
        result = run_cli(LAB / "fixtures" / "invalid.jsonl")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "error: line 2: invalid input_tokens\n")
        self.assertEqual(result.stdout, "")

    def test_blank_export(self):
        result = run_rows("\n  \n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '{"runs": {}}\n')

    def test_truncated_record_reports_physical_line(self):
        result = run_rows('\n{"run_id":\n')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "error: line 2: invalid JSON\n")
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
