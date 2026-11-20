"""Check ranking, paired metrics, split boundaries, and checkpoint recovery."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from evaluate import BASELINE, assert_disjoint, compare, evaluate, load_split, read_json, score_query
from retriever import rank
from run import FIXTURES, develop, inspect_holdout


class WorkshopTests(unittest.TestCase):
    def setUp(self):
        self.corpus = read_json(FIXTURES / "corpus.json")
        self.plan = read_json(FIXTURES / "plan.json")
        self.dev = load_split(FIXTURES, "dev.json", self.corpus)

    def test_rank_ties_and_ignores_nonmatches(self):
        documents = [
            {"id": "b", "title": "Cover", "body": "Check check clips"},
            {"id": "a", "title": "Clips", "body": "Check fit"},
            {"id": "c", "title": "Seal", "body": "Fit"},
        ]
        self.assertEqual(
            [(row["id"], row["score"]) for row in rank(documents, "CHECK!", 3)],
            [("a", 1), ("b", 1)],
        )

    def test_d01_matches_hand_calculation(self):
        case = self.dev[0]
        baseline = evaluate(self.corpus, [case], self.plan, BASELINE)["rows"][0]
        revised = evaluate(self.corpus, [case], self.plan, self.plan["candidates"][2])["rows"][0]
        self.assertEqual([row["id"] for row in baseline["ranked"]], ["K01", "K02"])
        self.assertEqual([row["id"] for row in revised["ranked"]], ["K11", "K12"])
        self.assertEqual(revised["ranked"][0]["body_hits"], ["jam"])
        self.assertEqual(revised["ranked"][0]["title_hits"], ["jam", "kite"])
        self.assertEqual((baseline["recall"], baseline["precision"]), ("0", "0"))
        self.assertEqual((revised["recall"], revised["precision"]), ("1", "1"))

    def test_fixed_slot_precision_and_no_reference(self):
        row = score_query(self.dev[2], [{"id": "R11"}], 2)
        self.assertEqual((row["recall"], row["precision"]), ("1", "1/2"))
        row = score_query(self.dev[-1], [], 2)
        self.assertIsNone(row["recall"])
        self.assertEqual(row["precision"], "0")
        with self.assertRaisesRegex(ValueError, "Invalid ranked list"):
            score_query(self.dev[2], [{"id": "R11"}, {"id": "R11"}], 2)

    def test_validate_groups_and_reject_leak(self):
        holdout = load_split(FIXTURES, "holdout.json", self.corpus)
        assert_disjoint(self.dev, holdout)
        leaky = load_split(FIXTURES, "leaky-holdout.json", self.corpus)
        with self.assertRaisesRegex(ValueError, "kite.*K12"):
            assert_disjoint(self.dev, leaky)

    def test_model_does_not_need_row_labels_to_rank(self):
        case = self.dev[0]
        original = rank(self.corpus, case["query"], 2)
        reworded_labels = {**case, "relevant": ["K02"], "critical": True}
        changed = rank(self.corpus, reworded_labels["query"], 2)
        self.assertEqual(original, changed)
        self.assertNotEqual(score_query(case, original, 2), score_query(reworded_labels, changed, 2))

    def test_compare_rejects_a_changed_label(self):
        cases = self.dev[:1]
        baseline = evaluate(self.corpus, cases, self.plan, BASELINE)
        changed = [{**cases[0], "critical": True}]
        candidate = evaluate(self.corpus, changed, self.plan, BASELINE)
        with self.assertRaisesRegex(ValueError, "fixed labels"):
            compare(baseline, candidate, "1/10")

    def test_checkpoint_resumes_to_same_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            partial = develop(FIXTURES, root / "resume", 2)
            self.assertEqual(partial["incumbent"], "titles")
            with self.assertRaisesRegex(ValueError, "Complete the development plan"):
                inspect_holdout(FIXTURES, root / "resume")
            resumed = develop(FIXTURES, root / "resume")
            fresh = develop(FIXTURES, root / "fresh")
            self.assertEqual(resumed, fresh)
            self.assertEqual(
                [entry["decision"] for entry in resumed["ledger"]],
                ["discard", "keep", "keep", "discard"],
            )
            self.assertEqual(resumed["incumbent"], "combined")

    def test_checkpoint_rejects_dev_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixtures = root / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            develop(fixtures, root / "run", 1)
            path = fixtures / "dev.json"
            path.write_text(path.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "Checkpoint inputs changed"):
                develop(fixtures, root / "run")

    def test_holdout_is_frozen_and_critical_case_blocks_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixtures = root / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            develop(fixtures, root / "run")
            label_path = fixtures / "holdout.json"
            original = label_path.read_text()
            changed = json.loads(original)
            changed[-1]["query"] += " check"
            label_path.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "frozen plan"):
                inspect_holdout(fixtures, root / "run")
            label_path.write_text(original)
            report = inspect_holdout(fixtures, root / "run")
            self.assertEqual(report["decision"], "retain baseline")
            self.assertEqual(report["comparison"]["recall_gain"], "0")
            self.assertEqual(report["comparison"]["precision_gain"], "1/6")
            self.assertEqual(report["comparison"]["new_critical_misses"], {"H03": ["V11"]})
            with self.assertRaisesRegex(ValueError, "Holdout report exists"):
                inspect_holdout(fixtures, root / "run")


if __name__ == "__main__":
    unittest.main()
