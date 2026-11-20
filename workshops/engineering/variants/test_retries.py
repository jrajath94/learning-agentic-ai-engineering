import json
import unittest

from test_baseline import LAB, run_cli, run_rows


EXPECTED = {"runs": {
    "nightly-a": {"passed": 1, "failed": 1, "input_tokens": 211, "output_tokens": 32},
    "nightly-b": {"passed": 1, "failed": 1, "input_tokens": 245, "output_tokens": 42},
}}


class RetryTests(unittest.TestCase):
    def test_delivery_retry_counts_once_per_run_and_case(self):
        result = run_cli(LAB / "fixtures" / "nightly.jsonl")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, json.dumps(EXPECTED, sort_keys=True) + "\n")

    def test_report_is_stable_when_lines_reverse(self):
        fixture = LAB / "fixtures" / "nightly.jsonl"
        lines = fixture.read_text(encoding="utf-8").splitlines()
        result = run_rows("\n".join(reversed(lines)) + "\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, json.dumps(EXPECTED, sort_keys=True) + "\n")


if __name__ == "__main__":
    unittest.main()
