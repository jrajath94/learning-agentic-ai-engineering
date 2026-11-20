"""Run all labs twice and record commands, elapsed time, and verification."""

import argparse
import hashlib
import json
import os
import platform
import shlex
import subprocess
import sys
import time
from pathlib import Path


def main(output: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []
    digests = []
    for trial in (1, 2):
        directory = output / f"trial-{trial}"
        directory.mkdir()
        commands = (
            ("service-original", ("-m", "unittest", "discover", "-s", "labs/service"), 1),
            ("service-updated", ("-m", "unittest", "discover", "-s", "labs/service"), 0),
            ("benchmark-test", ("-m", "unittest", "discover", "-s", "labs/benchmark"), 0),
            ("benchmark-run", ("labs/benchmark/benchmark.py", "--out", str(directory / "benchmark")), 0),
            ("workflow-test", ("-m", "unittest", "discover", "-s", "labs/report"), 0),
            ("workflow-run", ("labs/report/workflow.py", "labs/report/requests.csv",
                              "--out", str(directory / "report")), 0),
            ("workflow-restart", ("labs/report/workflow.py", "labs/report/requests.csv",
                                  "--out", str(directory / "report")), 0),
        )
        for label, arguments, expected in commands:
            env = dict(os.environ)
            env.pop("LAB_BASELINE", None)
            if label == "service-original":
                env["LAB_BASELINE"] = "1"
            cmd = [sys.executable, "-B", *arguments]
            started = time.perf_counter()
            result = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
            elapsed_ms = round(1000 * (time.perf_counter() - started), 2)
            visible = ["python3", "-B", *(
                arg.replace(str(output), "EVIDENCE") for arg in arguments
            )]
            records.append(dict(
                trial=trial, label=label,
                command=("LAB_BASELINE=1 " if label == "service-original" else "") + shlex.join(visible),
                expected_exit=expected, exit_code=result.returncode,
                elapsed_ms=elapsed_ms,
                output=(result.stdout + result.stderr).replace(str(root) + os.sep, ""),
            ))
            if result.returncode != expected:
                raise RuntimeError(f"{label}: {result.stdout}{result.stderr}")
        digest = {}
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                digest[str(path.relative_to(directory))] = hashlib.sha256(path.read_bytes()).hexdigest()
        digests.append(digest)
    if digests[0] != digests[1]:
        raise RuntimeError("Generated lab artifacts differ across fresh trials")
    evidence = dict(
        python=platform.python_version(), implementation=platform.python_implementation(),
        os=platform.system(), os_version=platform.mac_ver()[0] or platform.release(),
        architecture=platform.machine(), records=records, matching_artifact_sha256=digests[0],
    )
    (output / "runs.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"{len(records)} commands verified. {len(digests[0])} artifact hashes match.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
