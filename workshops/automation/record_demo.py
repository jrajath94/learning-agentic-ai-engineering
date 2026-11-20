"""Capture a clean workflow replay, crash traces and test results."""
import argparse
import json
from pathlib import Path
import sqlite3
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Use a new output directory.")
    args = parser.parse_args()
    args.output.mkdir(parents=True)

    def command(script, *arguments, code=0):
        result = run([sys.executable, "-B", script, *map(str, arguments)],
                     cwd=HERE, capture_output=True, encoding="utf-8", timeout=20)
        if result.returncode != code:
            raise RuntimeError(f"Expected exit {code}. Got {result.returncode}. {result.stderr}")
        return result

    with TemporaryDirectory() as folder:
        def execute(db, action, *arguments, code=0):
            return command("briefing.py", action, "--db", Path(folder) / (db + ".sqlite3"),
                           *arguments, code=code)

        def submit(db, *extra, feed="posts.jsonl", code=0):
            return execute(db, "run", "--feed", "fixtures/" + feed, "--week", "2026-W45", *extra, code=code)

        def inspect(db):
            return json.loads(execute(db, "inspect").stdout)

        def save_output(name, process):
            (args.output / name).write_text(process.stdout, encoding="utf-8")

        clean = json.loads(submit("clean").stdout)
        clean_state = inspect("clean")
        draft_text = execute("clean", "draft").stdout
        clean_retry = json.loads(submit("clean").stdout)
        assert clean["outcome"] == "staged" and clean_retry["outcome"] == "reused"
        assert inspect("clean") == clean_state
        write_json(args.output / "inspect.json", clean_state)
        (args.output / "draft.txt").write_text(draft_text, encoding="utf-8")
        save_output("schema.json", command("briefing.py", "schema"))
        save_output("tool-calls.json", execute("clean", "tool-calls", "--calls", "fixtures/tool-calls.json"))

        cases = []
        for point, code in [("before-draft-commit", 72), ("after-draft-commit", 73)]:
            exit_result = submit(point, "--crash", point, code=code)
            state_after_exit = inspect(point)
            receipt = json.loads(submit(point).stdout)
            state_after_retry = inspect(point)
            assert state_after_retry == clean_state
            assert execute(point, "draft").stdout == draft_text
            cases.append({"injection": point, "exit": exit_result.returncode,
                          "stdout_after_exit": exit_result.stdout,
                          "state_after_exit": {field: state_after_exit[field] for field in
                                               ("state", "events", "draft", "evidence")},
                          "retry": receipt, "state_after_retry": state_after_retry["state"],
                          "identical_to_clean_draft_and_state": state_after_retry == clean_state})
        broken_path = Path(folder) / "broken.sqlite3"
        broken_exit = command("broken_stage.py", broken_path, "--crash", code=73)
        broken_retry = json.loads(command("broken_stage.py", broken_path).stdout)
        write_json(args.output / "replay.json", {"clean": clean, "clean_retry": clean_retry,
                                               "crashes": cases, "broken": {
                                                   "exit": broken_exit.returncode, **broken_retry}})
        submit("conflict", feed="conflict.jsonl")
        write_json(args.output / "conflict-inspect.json", inspect("conflict"))
        save_output("conflict-draft.txt", execute("conflict", "draft"))
        submit("poisoned", feed="poisoned-result.jsonl")
        save_output("poisoned-draft.txt", execute("poisoned", "draft"))

    tests = command("-m", "unittest", "discover", "-s", ".", "-v")
    (args.output / "tests.txt").write_text(
        f"Python {sys.version.split()[0]}\nSQLite {sqlite3.sqlite_version}\n\n" + tests.stderr,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
