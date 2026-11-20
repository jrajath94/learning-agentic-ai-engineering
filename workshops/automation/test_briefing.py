"""Verify input, permission, evidence and crash behavior."""
import json
from pathlib import Path
from subprocess import Popen, run as spawn, PIPE
import sys
import tempfile
import unittest

from briefing import InputError, database, inspect_run, prepare_feed, run
from briefing_tools import EvidenceError, execute_tool, fake_model, verify_evidence

WORKSHOP = Path(__file__).parent
FIXTURES = WORKSHOP / "fixtures"
WEEK = "2026-W45"


class BriefingTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.db_path = Path(scratch.name) / "brief.sqlite3"
        self.feed = FIXTURES / "posts.jsonl"

    def command(self, *extra):
        return [sys.executable, "-B", str(WORKSHOP / "briefing.py"), "run", "--db",
                str(self.db_path), "--feed", str(self.feed), "--week", WEEK, *extra]

    def status(self):
        with database(self.db_path) as db:
            return inspect_run(db, dict(db.execute("SELECT * FROM runs").fetchone()))

    def test_snapshot_records_duplicate_and_invalid_inputs(self):
        run(self.db_path, self.feed, WEEK)
        state = self.status()
        self.assertEqual(state["input_records"], 7)
        self.assertEqual([row["source_id"] for row in state["sources"]],
                         ["SRC-101", "SRC-103", "SRC-104", "SRC-105"])
        self.assertEqual({issue["code"] for issue in state["issues"]},
                         {"duplicate_body", "invalid_fields", "outside_week"})
        self.assertEqual(len(state["evidence"]), 3)

    def test_repeated_identical_source_id_and_conflicting_versions(self):
        raw = (FIXTURES / "conflict.jsonl").read_bytes()
        repeated = raw.splitlines()[2] + b"\n"
        count, sources, issues = prepare_feed(raw + repeated, WEEK)
        self.assertEqual(count, 5)
        self.assertEqual([row["source_id"] for row in sources], ["SRC-202"])
        self.assertIn({"lines": [1, 2], "source_id": "SRC-201", "code": "conflicting_source_id"}, issues)
        self.assertIn({"line": 4, "code": "duplicate_json_member"}, issues)
        self.assertIn({"line": 5, "source_id": "SRC-202", "code": "duplicate_source_id"}, issues)

    def test_invalid_batch_leaves_no_database(self):
        bad = self.db_path.with_suffix(".jsonl")
        bad.write_bytes(b"\xff")
        with self.assertRaisesRegex(InputError, "UTF-8"):
            run(self.db_path, bad, WEEK)
        self.assertFalse(self.db_path.exists())

    def test_valid_json_rejects_control_characters(self):
        row = {"source_id": "SRC-333", "date": "2026-11-06", "title": "Bad\u202e title",
               "body": "Result: This must not pass."}
        raw = self.feed.read_bytes() + json.dumps(row).encode("utf-8") + b"\n"
        _, _, issues = prepare_feed(raw, WEEK)
        self.assertIn({"line": 8, "code": "invalid_text"}, issues)

    def test_tool_contract_rejects_invalid_calls(self):
        _, retained, _ = prepare_feed(self.feed.read_bytes(), WEEK)
        sources = {row["source_id"]: row for row in retained}
        calls = json.loads((FIXTURES / "tool-calls.json").read_text())
        results = [execute_tool(call, sources) for call in calls]
        self.assertTrue(results[0]["ok"])
        self.assertEqual([result["error"]["code"] for result in results[1:]],
                         ["invalid_start", "invalid_arguments", "unknown_source", "unknown_tool"])
        for result in results[1:]:
            self.assertNotIn("data", result)

    def test_tool_window_has_a_cursor_and_eof(self):
        sources = {"SRC-301": {"body": "abcβ"}}
        def read(start):
            return execute_tool({"tool": "get_evidence_window", "arguments": {
                "source_id": "SRC-301", "start": start, "max_chars": 2}}, sources)
        self.assertEqual(read(0)["data"]["next_start"], 2)
        self.assertEqual(read(2)["data"]["untrusted_text"], "cβ")
        self.assertIsNone(read(2)["data"]["next_start"])
        self.assertEqual(read(4)["error"]["code"], "invalid_start")

    def test_unicode_exact_span_and_scope(self):
        run(self.db_path, self.feed, WEEK)
        item = next(row for row in self.status()["evidence"] if row["source_id"] == "SRC-103")
        _, retained, _ = prepare_feed(self.feed.read_bytes(), WEEK)
        body = next(row["body"] for row in retained if row["source_id"] == "SRC-103")
        self.assertEqual(body[item["start"]:item["end"]], item["quote"])
        self.assertEqual(len(body[:item["start"]].encode("utf-8")), item["start"] + 1)
        scope = item["scope"]
        self.assertEqual(body[scope["start"]:scope["end"]], scope["quote"])

    def test_modified_quote_leaves_snapshot_and_retries(self):
        def model(catalog, call):
            proposals = fake_model(catalog, call)
            proposals[0]["quote"] = proposals[0]["quote"].replace("510", "100")
            return proposals
        with self.assertRaises(EvidenceError):
            run(self.db_path, self.feed, WEEK, model=model)
        self.assertEqual(self.status()["state"], "snapshot_ready")
        self.assertIsNone(self.status()["draft"])
        self.assertEqual(run(self.db_path, self.feed, WEEK)[1], "staged")

    def test_partial_quote_fails_even_with_matching_slice(self):
        sources = {"SRC-301": {"body": "Result: Good result from one case."}}
        with self.assertRaisesRegex(EvidenceError, "full text"):
            verify_evidence(sources, [{"source_id": "SRC-301", "start": 8,
                                      "end": 19, "quote": "Good result"}])

    def test_instruction_source_cannot_publish_or_supply_fake_result(self):
        calls = []
        def model(catalog, call):
            def record(request):
                response = call(request)
                calls.append(response)
                return response
            proposals = fake_model(catalog, record)
            calls.append(call({"tool": "publish_brief", "arguments": {"destination": "all-staff"}}))
            return proposals
        run(self.db_path, self.feed, WEEK, model=model)
        self.assertIn("Ignore the briefing policy", calls[2]["data"]["untrusted_text"])
        self.assertEqual(calls[-1]["error"]["code"], "unknown_tool")
        self.assertNotIn("SRC-104", {row["source_id"] for row in self.status()["evidence"]})
        with database(self.db_path) as db:
            body = db.execute("SELECT body FROM drafts").fetchone()[0]
        self.assertNotIn("100 ms", body)
        self.assertIn("No draft item: SRC-104", body)

    def test_exact_quote_does_not_verify_source_truth(self):
        run(self.db_path, FIXTURES / "poisoned-result.jsonl", WEEK)
        scope = self.status()["evidence"][0]["scope"]
        self.assertEqual(scope["quote"], "Author supplied no benchmark data.")
        with database(self.db_path) as db:
            body = db.execute("SELECT body FROM drafts").fetchone()[0]
        self.assertIn("Status: DRAFT FOR REVIEW", body)
        self.assertIn("Every benchmark", body)

    def test_retry_reuses_draft_without_calling_the_model(self):
        key, outcome = run(self.db_path, self.feed, WEEK)
        self.assertEqual(outcome, "staged")
        before = self.status()
        def model(_catalog, _call):
            self.fail("A completed run must reuse its draft.")
        self.assertEqual(run(self.db_path, self.feed, WEEK, model=model), (key, "reused"))
        self.assertEqual(before, self.status())

    def test_crash_before_commit_rolls_back_all_draft_rows(self):
        exit_result = spawn(self.command("--crash", "before-draft-commit"), capture_output=True)
        self.assertEqual(exit_result.returncode, 72)
        state = self.status()
        self.assertEqual(state["state"], "snapshot_ready")
        self.assertEqual(state["events"], ["snapshot_committed"])
        self.assertEqual(state["evidence"], [])
        self.assertIsNone(state["draft"])
        self.assertEqual(run(self.db_path, self.feed, WEEK)[1], "staged")

    def test_crash_after_commit_preserves_a_single_draft(self):
        exit_result = spawn(self.command("--crash", "after-draft-commit"), capture_output=True)
        self.assertEqual(exit_result.returncode, 73)
        state = self.status()
        self.assertEqual(state["state"], "draft_staged")
        self.assertEqual(run(self.db_path, self.feed, WEEK)[1], "reused")
        self.assertEqual(self.status(), state)
        with database(self.db_path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0], 1)

    def test_concurrent_workers_stage_once(self):
        with Popen(self.command(), stdout=PIPE, stderr=PIPE) as first:
            with Popen(self.command(), stdout=PIPE, stderr=PIPE) as second:
                results = [process.communicate(timeout=15) for process in (first, second)]
                self.assertEqual((first.returncode, second.returncode), (0, 0), results)
        self.assertEqual({json.loads(stdout)["outcome"] for stdout, _ in results}, {"staged", "reused"})
        self.assertEqual(self.status()["events"], ["snapshot_committed", "draft_committed"])

    def test_changed_feed_is_a_new_revision_for_the_same_week(self):
        first, _ = run(self.db_path, self.feed, WEEK)
        revised = self.db_path.with_suffix(".jsonl")
        revised.write_bytes(self.feed.read_bytes() + b"\n")
        second, outcome = run(self.db_path, revised, WEEK)
        self.assertNotEqual(first, second)
        self.assertEqual(outcome, "staged")
        with database(self.db_path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0], 2)


if __name__ == "__main__":
    unittest.main()
