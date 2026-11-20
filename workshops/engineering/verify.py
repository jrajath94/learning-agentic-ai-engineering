"""Run the trace workshop and record each decision gate."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
VARIANTS = ROOT / "variants"
BASELINE = ('{"runs": {"nightly-a": {"failed": 2, "input_tokens": 422, '
            '"output_tokens": 64, "passed": 2}, "nightly-b": {"failed": 1, '
            '"input_tokens": 245, "output_tokens": 42, "passed": 1}}}\n')
REPAIRED = ('{"runs": {"nightly-a": {"failed": 1, "input_tokens": 211, '
            '"output_tokens": 32, "passed": 1}, "nightly-b": {"failed": 1, '
            '"input_tokens": 245, "output_tokens": 42, "passed": 1}}}\n')
CONFLICT = "error: line 3: terminal result conflicts with line 1\n"


class Workshop:
    def __init__(self, directory):
        self.directory = directory
        self.repo = directory / "repo"
        self.implementation = directory / "implementation"
        self.review = directory / "review"
        self.probe = directory / "candidate-probe"
        self.record = []
        self.env = {
            **{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
        }

    def run(self, place, args, code=0):
        result = subprocess.run(
            args, cwd=place, env=self.env, text=True, capture_output=True,
            check=False,
        )
        if result.returncode != code:
            raise RuntimeError(
                f"{place.name} {args}: expected exit {code}, got {result.returncode}\n"
                f"{result.stdout}{result.stderr}"
            )
        return result

    def log(self, heading, item):
        self.record.extend((f"## {heading}", "", item, ""))

    def git(self, place, *args):
        return self.run(place, ["git", *args]).stdout.strip()

    def tests(self, place, heading, count, failures=0, names=None):
        result = self.run(
            place,
            [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
            code=1 if failures else 0,
        )
        if not re.search(rf"^Ran {count} tests? in ", result.stderr, re.MULTILINE):
            raise RuntimeError(result.stderr)
        if failures:
            if f"FAILED (failures={failures})" not in result.stderr:
                raise RuntimeError(result.stderr)
            actual_names = set(re.findall(r"^FAIL: (\w+)", result.stderr, re.MULTILINE))
            if actual_names != set(names):
                raise RuntimeError(result.stderr)
        else:
            if not result.stderr.rstrip().endswith("OK"):
                raise RuntimeError(result.stderr)
        lines = (
            line.rstrip() for line in result.stderr.splitlines()
            if re.match(r"^(?:test_|  test_|Ran |OK$|FAILED)", line)
        )
        clean_lines = (re.sub(r" in [0-9.]+s$", "", line) for line in lines)
        self.log(
            heading,
            f"{place.name} $ python3 -B -m unittest discover -s tests -v\n"
            f"exit {result.returncode}\n" + "\n".join(clean_lines),
        )

    def cli(self, place, fixture, stdout="", stderr="", code=0):
        task = ["-B", "-m", "trace_rollup", f"fixtures/{fixture}.jsonl"]
        result = self.run(place, [sys.executable, *task], code)
        if (result.stdout, result.stderr) != (stdout, stderr):
            raise RuntimeError(f"Unexpected result for {fixture}: {result}")
        self.log(
            f"{place.name} / {fixture}",
            f"{place.name} $ python3 {' '.join(task)}\nexit {code}\n"
            f"stdout: {stdout.rstrip() or '(empty)'}\n"
            f"stderr: {stderr.rstrip() or '(empty)'}",
        )

    def mutated_copy(self, name, before, after):
        target = self.directory / name
        shutil.copytree(self.repo, target, ignore=shutil.ignore_patterns(".git"))
        reducer = target / "trace_rollup" / "aggregate.py"
        original = reducer.read_text(encoding="utf-8")
        if original.count(before) != 1:
            raise RuntimeError("The negative control must change exactly one site")
        reducer.write_text(original.replace(before, after), encoding="utf-8")
        return target

    def negative_controls(self):
        global_key = self.mutated_copy(
            "global-case-id",
            "key = (record.run_id, record.case_id)",
            "key = record.case_id",
        )
        self.cli(
            global_key, "nightly",
            stderr="error: line 2: terminal result conflicts with line 1\n", code=2,
        )
        self.tests(
            global_key, "Negative control: use case ID across runs", 10, failures=2,
            names=["test_delivery_retry_counts_once_per_run_and_case",
                   "test_report_is_stable_when_lines_reverse"],
        )
        moving_line = self.mutated_copy(
            "overwrite-first-line",
            "            continue\n",
            "            seen[key] = (signature, record.line)\n            continue\n",
        )
        self.cli(moving_line, "nightly", stdout=REPAIRED)
        self.tests(
            moving_line, "Negative control: replace the first diagnostic line", 10, failures=2,
            names=["test_each_token_field_can_conflict_even_if_status_is_equal"],
        )

    def execute(self):
        shutil.copytree(ROOT / "lab", self.repo)
        self.log(
            "Environment",
            f"{self.git(self.repo, '--version')}\n{sys.version.split()[0]}\n"
            "Python and Git use a disposable repository. Times omitted.\n"
            "Git commits use a fixed synthetic date and lab identity.",
        )
        self.git(self.repo, "init", "-q", "-b", "main")
        self.git(self.repo, "config", "user.name", "Lab")
        self.git(self.repo, "config", "user.email", "lab@example.invalid")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-qm", "Record original rollup")
        base = self.git(self.repo, "rev-parse", "HEAD")
        if self.git(self.repo, "status", "--porcelain"):
            raise RuntimeError("The base index must be clean")

        self.cli(self.repo, "nightly", stdout=BASELINE)
        self.tests(self.repo, "Base smoke tests", 4)
        self.git(self.repo, "worktree", "add", "-q", "-b", "implement/retries",
                 str(self.implementation), base)
        self.git(self.repo, "worktree", "add", "-q", "-b", "review/cases",
                 str(self.review), base)
        self.log("Local branch start",
                 f"main, implement/retries, review/cases start at {base}")

        shutil.copy2(VARIANTS / "test_retries.py", self.implementation / "tests")
        self.tests(
            self.implementation, "Implementation tests on the base", 6, failures=2,
            names=["test_delivery_retry_counts_once_per_run_and_case",
                   "test_report_is_stable_when_lines_reverse"],
        )
        shutil.copy2(
            VARIANTS / "candidate.py", self.implementation / "trace_rollup" / "aggregate.py"
        )
        self.tests(self.implementation, "Candidate with implementation tests", 6)
        self.git(self.implementation, "add", "trace_rollup/aggregate.py",
                 "tests/test_retries.py")
        self.git(self.implementation, "commit", "-qm", "Count a delivery retry once")
        candidate = self.git(self.implementation, "rev-parse", "HEAD")

        shutil.copy2(VARIANTS / "test_review.py", self.review / "tests")
        self.git(self.review, "add", "tests/test_review.py")
        self.git(self.review, "commit", "-qm", "Add review counterexamples")
        review_pass = self.git(self.review, "rev-parse", "HEAD")
        self.git(self.repo, "worktree", "add", "-q", "--detach",
                 str(self.probe), candidate)
        shutil.copy2(self.review / "tests" / "test_review.py", self.probe / "tests")
        self.log(
            "Candidate and review scope",
            f"base {base}\n"
            f"candidate {candidate}\n"
            f"{self.git(self.repo, 'diff', '--name-only', base, candidate)}\n"
            f"review {review_pass}\n"
            f"{self.git(self.repo, 'diff', '--name-only', base, review_pass)}",
        )
        self.cli(
            self.probe, "conflict",
            stdout=('{"runs": {"daily": {"failed": 0, "input_tokens": 120, '
                    '"output_tokens": 24, "passed": 1}}}\n'),
        )
        self.tests(
            self.probe, "Candidate with independent review tests", 10, failures=3,
            names=["test_conflicting_status_rejects_report_at_physical_line",
                   "test_each_token_field_can_conflict_even_if_status_is_equal"],
        )

        shutil.copy2(
            VARIANTS / "repaired.py", self.implementation / "trace_rollup" / "aggregate.py"
        )
        self.git(self.implementation, "add", "trace_rollup/aggregate.py")
        self.git(self.implementation, "commit", "-qm", "Reject conflicting terminal results")
        fixed = self.git(self.implementation, "rev-parse", "HEAD")
        self.git(self.repo, "merge", "-q", "--ff-only", "implement/retries")
        self.git(self.repo, "merge", "-q", "--no-ff", "-m", "Integrate review cases",
                 "review/cases")
        joined = self.git(self.repo, "rev-parse", "HEAD")
        parents = self.git(self.repo, "show", "-s", "--format=%P", joined).split()
        if parents != [fixed, review_pass]:
            raise RuntimeError("Unexpected integration parents")
        if self.git(self.repo, "status", "--porcelain"):
            raise RuntimeError("The integrated worktree must be clean")
        self.log(
            "Combined revision",
            f"implementation {fixed}\nreview {review_pass}\nintegrated {joined}\n"
            "Both expected parent revisions are present. Working tree is clean.",
        )
        self.git(self.repo, "diff", "--check", base, joined)
        self.log("Diff check", "repo $ git diff --check BASE HEAD\nexit 0\nstdout: (empty)")
        self.tests(self.repo, "Combined revision tests", 10)
        self.cli(self.repo, "nightly", stdout=REPAIRED)
        self.cli(self.repo, "conflict", stderr=CONFLICT, code=2)
        self.cli(self.repo, "invalid", stderr="error: line 2: invalid input_tokens\n", code=2)
        self.cli(self.repo, "legacy",
                 stdout=('{"runs": {"legacy": {"failed": 1, "input_tokens": 7, '
                         '"output_tokens": 2, "passed": 1}}}\n'))
        self.negative_controls()
        return "\n".join(self.record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, help="Write the verification record here")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="trace-workshop-") as directory:
        record = Workshop(Path(directory)).execute()
    if args.record:
        args.record.write_text("# Trace rollup verification\n\n" + record, encoding="utf-8")
    print("Verified base, red tests, candidate, review counterexamples, and combined revision.")


if __name__ == "__main__":
    main()
