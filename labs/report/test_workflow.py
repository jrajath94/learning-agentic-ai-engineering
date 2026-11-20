import json
import tempfile
import unittest
from pathlib import Path

from workflow import (InvalidSource, MAX_BYTES, MAX_CALLS, TransientToolError,
                      atomic_write, read_source, run)

SOURCE = Path(__file__).with_name("requests.csv")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.out = Path(directory.name)

    def test_draft_quality_and_idempotence(self):
        first = run(SOURCE, self.out)
        draft = self.out / "draft.md"
        before = draft.stat().st_mtime_ns
        body = draft.read_text()
        self.assertIn("Open requests: 4 [Source rows: R01, R03, R04, R05]", body)
        self.assertIn("Open for at least 7 days: 3 [Source rows: R04, R01, R05]", body)
        self.assertNotIn("R06", body)
        self.assertIn("Draft for human review", body)
        self.assertEqual((first.stage, first.calls), ("review", 2))
        self.assertEqual(run(SOURCE, self.out), first)
        self.assertEqual(draft.stat().st_mtime_ns, before)

    def test_transient_failure_then_success(self):
        attempts = 0

        def read_once(raw):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise TransientToolError("simulated read failure")
            return read_source(raw)

        state = run(SOURCE, self.out, reader=read_once)
        self.assertEqual((state.stage, state.calls, state.retries), ("review", 3, 1))

    def test_repeated_error_stops(self):
        def fail(raw):
            raise TransientToolError("simulated read failure")

        state = run(SOURCE, self.out, reader=fail)
        self.assertEqual((state.stage, state.calls, state.retries), ("failed", 2, 1))
        self.assertFalse((self.out / "draft.md").exists())

    def test_crash_after_draft_write_resumes_without_second_write(self):
        def stop_after_write(path, body):
            atomic_write(path, body)
            raise KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            run(SOURCE, self.out, writer=stop_after_write)
        draft = self.out / "draft.md"
        original_time = draft.stat().st_mtime_ns
        resumed = run(SOURCE, self.out)
        self.assertEqual((resumed.stage, resumed.calls), ("review", 3))
        self.assertEqual(draft.stat().st_mtime_ns, original_time)

    def test_missing_draft_recovers_and_corrupt_draft_hits_call_limit(self):
        run(SOURCE, self.out)
        draft = self.out / "draft.md"
        expected = draft.read_text()
        draft.unlink()
        self.assertEqual(run(SOURCE, self.out).stage, "review")
        draft.write_bytes(b"\xff")
        self.assertEqual(run(SOURCE, self.out).stage, "review")
        self.assertEqual(draft.read_text(), expected)
        draft.unlink()
        state = run(SOURCE, self.out)
        self.assertEqual((state.stage, state.calls), ("failed", MAX_CALLS))

    def test_writer_must_produce_verified_artifact(self):
        state = run(SOURCE, self.out, writer=lambda path, body: None)
        self.assertEqual((state.stage, state.calls, state.retries), ("failed", 3, 1))

    def test_invalid_source_and_changed_input(self):
        other = self.out / "other.csv"
        other.write_text("id,status\nR01,open\n")
        run(SOURCE, self.out)
        with self.assertRaises(InvalidSource):
            run(other, self.out)
        separate = self.out / "separate"
        self.assertEqual(run(other, separate).stage, "failed")
        self.assertIn("invalid columns", json.loads((separate / "state.json").read_text())["events"])

    def test_excess_bytes_stop_before_checkpoint(self):
        large = self.out / "large.csv"
        large.write_bytes(b"a" * (MAX_BYTES + 1))
        with self.assertRaises(InvalidSource):
            run(large, self.out)
        self.assertFalse((self.out / "state.json").exists())
