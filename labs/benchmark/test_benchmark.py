import csv
import tempfile
import unittest
from pathlib import Path

from benchmark import run


class BenchmarkTests(unittest.TestCase):
    def test_splits_metrics_and_error_accountability(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            results = run(out)
            with (out / "data.csv").open(newline="") as file:
                data = list(csv.DictReader(file))
            with (out / "errors.csv").open(newline="") as file:
                errors = list(csv.DictReader(file))
            self.assertEqual(len(data), 1200)
            by_id = {row["id"]: row for row in data}
            self.assertEqual(len(by_id), len(data))
            self.assertFalse(any(row["split"] == "train" for row in errors))
            self.assertTrue(all(by_id[row["id"]]["label"] == row["expected"] for row in errors))
            self.assertEqual(len(errors), sum(row["total"] - row["correct"] for row in results))
            scores = {(row["seed"], row["split"], row["model"]): row["correct"] for row in results}
            for seed in (7, 19, 43):
                self.assertGreater(scores[seed, "test", "full"], scores[seed, "test", "sensor"])
                self.assertGreater(scores[seed, "shift", "sensor"], scores[seed, "shift", "full"])
                self.assertGreater(scores[seed, "shift", "sensor"], scores[seed, "shift", "majority"])
