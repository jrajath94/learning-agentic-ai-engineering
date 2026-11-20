"""Run a fixed candidate plan and checkpoint each development decision."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile

from evaluate import (
    BASELINE, assert_disjoint, compare, evaluate, load_split, read_json, trace_queries,
)


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"


def digest(filenames, fixtures):
    hasher = hashlib.sha256()
    for filename in filenames:
        path = fixtures / filename
        if filename.endswith(".py"):
            path = HERE / filename
        contents = path.read_bytes()
        hasher.update(filename.encode() + b"\0")
        hasher.update(hashlib.sha256(contents).digest())
    return hasher.hexdigest()


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_inputs(fixtures):
    corpus = read_json(fixtures / "corpus.json")
    plan = read_json(fixtures / "plan.json")
    candidate_names = [candidate["name"] for candidate in plan["candidates"]]
    if not 0 < plan["candidate_budget"] <= len(candidate_names):
        raise ValueError("Candidate budget must fit the plan")
    if len(set(candidate_names + [BASELINE["name"]])) != len(candidate_names) + 1:
        raise ValueError("Candidate names must be unique")
    return corpus, plan


def input_digest(fixtures):
    return digest(
        ("corpus.json", "dev.json", "plan.json", "retriever.py", "evaluate.py", "run.py"),
        fixtures,
    )


def develop(fixtures, out, stop_after=None):
    corpus, plan = load_inputs(fixtures)
    cases = load_split(fixtures, "dev.json", corpus)
    checkpoint = out / "checkpoint.json"
    signature = input_digest(fixtures)
    if checkpoint.exists():
        state = read_json(checkpoint)
        if state["input_digest"] != signature:
            raise ValueError("Checkpoint inputs changed. Use a new output directory.")
    else:
        result = evaluate(corpus, cases, plan, BASELINE)
        state = {
            "input_digest": signature,
            "budget": plan["candidate_budget"],
            "baseline": result,
            "incumbent": BASELINE["name"],
            "ledger": [],
        }
        write_json(checkpoint, state)

    if stop_after is not None and not 0 <= stop_after <= state["budget"]:
        raise ValueError("Pause limit must fit the candidate budget")
    limit = state["budget"] if stop_after is None else stop_after
    for attempt in range(len(state["ledger"]), limit):
        config = plan["candidates"][attempt]
        candidate = evaluate(corpus, cases, plan, config)
        comparison = compare(state["baseline"], candidate, plan["minimum_recall_gain"])
        incumbent = next(
            (entry["result"] for entry in state["ledger"]
             if entry["result"]["config"]["name"] == state["incumbent"]),
            state["baseline"],
        )
        candidate_recall = Fraction(candidate["metrics"]["macro_recall"])
        incumbent_recall = Fraction(incumbent["metrics"]["macro_recall"])
        promote = comparison["accepted"] and candidate_recall > incumbent_recall
        if promote:
            state["incumbent"] = config["name"]
        state["ledger"].append({
            "attempt": attempt + 1,
            "result": candidate,
            "comparison_to_baseline": comparison,
            "decision": "keep" if promote else "discard",
            "incumbent_after": state["incumbent"],
        })
        write_json(checkpoint, state)

    count = len(state["ledger"])
    status = "budget exhausted" if count == state["budget"] else "paused"
    print(f"development: {count}/{state['budget']} candidates, {status}, incumbent={state['incumbent']}")
    return state


def inspect_holdout(fixtures, out):
    checkpoint = read_json(out / "checkpoint.json")
    report_path = out / "holdout-report.json"
    if report_path.exists():
        raise ValueError("Holdout report exists. Keep the locked decision.")
    if checkpoint["input_digest"] != input_digest(fixtures):
        raise ValueError("Checkpoint inputs changed. Use the locked inputs.")
    if len(checkpoint["ledger"]) != checkpoint["budget"]:
        raise ValueError("Complete the development plan before holdout.")
    corpus, plan = load_inputs(fixtures)
    holdout_digest = digest(("holdout.json",), fixtures)
    if holdout_digest != plan["holdout_digest"]:
        raise ValueError("Holdout does not match the frozen plan.")
    dev = load_split(fixtures, "dev.json", corpus)
    holdout = load_split(fixtures, "holdout.json", corpus)
    assert_disjoint(dev, holdout)
    configs = {config["name"]: config for config in [BASELINE] + plan["candidates"]}
    baseline = evaluate(corpus, holdout, plan, BASELINE)
    candidate = evaluate(corpus, holdout, plan, configs[checkpoint["incumbent"]])
    comparison = compare(baseline, candidate, plan["minimum_recall_gain"])
    report = {
        "input_digest": checkpoint["input_digest"],
        "holdout_digest": holdout_digest,
        "baseline": baseline,
        "candidate": candidate,
        "comparison": comparison,
        "decision": "accept candidate" if comparison["accepted"] else "retain baseline",
    }
    write_json(report_path, report)
    print(f"holdout: {report['decision']}, recall gain={comparison['recall_gain']}, "
          f"precision gain={comparison['precision_gain']}")
    return report


def audit_split(fixtures, holdout_file):
    corpus = read_json(fixtures / "corpus.json")
    dev = load_split(fixtures, "dev.json", corpus)
    holdout = load_split(fixtures, holdout_file, corpus)
    assert_disjoint(dev, holdout)
    print(f"split audit: PASS ({len(dev)} development queries, {len(holdout)} held-out queries)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    develop_parser = commands.add_parser("dev")
    develop_parser.add_argument("--out", type=Path, required=True)
    develop_parser.add_argument("--stop-after", type=int)
    holdout_parser = commands.add_parser("holdout")
    holdout_parser.add_argument("--out", type=Path, required=True)
    explain_parser = commands.add_parser("explain")
    explain_parser.add_argument("query_id")
    explain_parser.add_argument("--config", default="baseline")
    audit_parser = commands.add_parser("audit")
    audit_parser.add_argument("--holdout-file", default="holdout.json")
    args = parser.parse_args()
    try:
        if args.command == "dev":
            develop(FIXTURES, args.out, args.stop_after)
        elif args.command == "holdout":
            inspect_holdout(FIXTURES, args.out)
        elif args.command == "audit":
            audit_split(FIXTURES, args.holdout_file)
        elif args.command == "explain":
            corpus, plan = load_inputs(FIXTURES)
            configs = {config["name"]: config for config in [BASELINE] + plan["candidates"]}
            case = next(
                (row for row in load_split(FIXTURES, "dev.json", corpus)
                 if row["id"] == args.query_id),
                None,
            )
            if case is None or args.config not in configs:
                raise ValueError("Use a development query ID and a declared configuration")
            trace = trace_queries(corpus, [case], plan, configs[args.config])[0]
            print(json.dumps(trace, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
