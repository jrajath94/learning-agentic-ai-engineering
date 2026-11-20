import json
import unittest

from test_baseline import LAB, run_cli, run_rows


class ReviewTests(unittest.TestCase):
    def test_conflicting_status_rejects_report_at_physical_line(self):
        result = run_cli(LAB / "fixtures" / "conflict.jsonl")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr, "error: line 3: terminal result conflicts with line 1\n"
        )

    def test_each_token_field_can_conflict_even_if_status_is_equal(self):
        first = {
            "case_id": "table-08", "run_id": "daily", "status": "pass",
            "input_tokens": 23, "output_tokens": 0,
        }
        for field in ("input_tokens", "output_tokens"):
            with self.subTest(field=field):
                altered = {**first, field: first[field] + 1}
                rows = "\n".join(map(json.dumps, (first, first, altered)))
                result = run_rows(rows)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertEqual(
                    result.stderr, "error: line 3: terminal result conflicts with line 1\n"
                )

    def test_ids_remain_distinct_after_validation(self):
        first = {
            "run_id": "daily", "case_id": "one", "status": "pass",
            "input_tokens": 5, "output_tokens": 2,
        }
        second = {**first, "case_id": " one"}
        result = run_rows("\n".join(map(json.dumps, (first, second))))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {"runs": {"daily": {
                "passed": 2, "failed": 0,
                "input_tokens": 10, "output_tokens": 4,
            }}},
        )

    def test_invalid_repeated_delivery_is_still_invalid(self):
        first = {
            "run_id": "daily", "case_id": "one", "status": "pass",
            "input_tokens": 5, "output_tokens": 2,
        }
        second = {**first, "input_tokens": True}
        result = run_rows("\n".join(map(json.dumps, (first, second))))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "error: line 2: invalid input_tokens\n")


if __name__ == "__main__":
    unittest.main()
