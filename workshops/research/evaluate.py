"""Measure retrieved document IDs against reference labels."""
from fractions import Fraction
import json
from pathlib import Path

from retriever import candidate_aliases, rank


BASELINE = {"name": "baseline", "title_weight": 0, "aliases": "none"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_split(fixtures, filename, corpus):
    rows = read_json(fixtures / filename)
    documents = {document["id"]: document for document in corpus}
    if len(documents) != len(corpus):
        raise ValueError("Duplicate document ID")
    if not rows or len({row["id"] for row in rows}) != len(rows):
        raise ValueError(f"Empty split or duplicate query ID: {filename}")
    groups = {document["group"] for document in corpus}
    for row in rows:
        relevant = row["relevant"]
        if row["group"] not in groups:
            raise ValueError(f"Unknown source family: {row['id']}")
        if len(set(relevant)) != len(relevant):
            raise ValueError(f"Duplicate reference: {row['id']}")
        if row["critical"] and not relevant:
            raise ValueError(f"Critical query requires a reference: {row['id']}")
        for document_id in relevant:
            if document_id not in documents:
                raise ValueError(f"Unknown document {document_id}: {row['id']}")
            if documents[document_id]["group"] != row["group"]:
                raise ValueError(f"Reference crosses a source family: {row['id']}")
    return rows


def assert_disjoint(dev, holdout):
    groups = {row["group"] for row in dev} & {row["group"] for row in holdout}
    queries = {row["id"] for row in dev} & {row["id"] for row in holdout}
    documents = {doc for row in dev for doc in row["relevant"]} & {
        doc for row in holdout for doc in row["relevant"]
    }
    if groups or queries or documents:
        raise ValueError(
            f"Split overlap: groups={sorted(groups)}, "
            f"queries={sorted(queries)}, relevant_docs={sorted(documents)}"
        )


def score_query(case, ranked, k):
    expected = set(case["relevant"])
    retrieved = [result["id"] for result in ranked]
    if len(set(retrieved)) != len(retrieved) or len(retrieved) > k:
        raise ValueError(f"Invalid ranked list: {case['id']}")
    hits = sorted(expected & set(retrieved))
    return {
        "id": case["id"],
        "group": case["group"],
        "slice": case["slice"],
        "query": case["query"],
        "critical": case["critical"],
        "expected": sorted(expected),
        "ranked": ranked,
        "hits": hits,
        "missed": sorted(expected - set(retrieved)),
        "extra": [document_id for document_id in retrieved if document_id not in expected],
        "recall": str(Fraction(len(hits), len(expected))) if expected else None,
        "precision": str(Fraction(len(hits), k)),
    }


def mean(values):
    fractions = [Fraction(value) for value in values]
    return str(sum(fractions) / len(fractions)) if fractions else None


def summarize(rows):
    positive = [row for row in rows if row["expected"]]
    no_evidence = [row for row in rows if not row["expected"]]
    return {
        "cases": len(rows),
        "positive_cases": len(positive),
        "macro_recall": mean(row["recall"] for row in positive),
        "macro_precision": mean(row["precision"] for row in positive),
        "no_evidence_cases": len(no_evidence),
        "no_evidence_false_returns": sum(bool(row["ranked"]) for row in no_evidence),
        "critical_incomplete": [row["id"] for row in rows if row["critical"] and row["missed"]],
    }


def trace_queries(corpus, cases, plan, config):
    k = plan["k"]
    if k < 1:
        raise ValueError("k must be positive")
    aliases = candidate_aliases(plan, config["aliases"])
    return [
        score_query(case, rank(corpus, case["query"], k, config["title_weight"], aliases), k)
        for case in cases
    ]


def evaluate(corpus, cases, plan, config):
    rows = trace_queries(corpus, cases, plan, config)
    metrics = summarize(rows)
    if metrics["positive_cases"] == 0:
        raise ValueError("Evaluation requires at least one positive case")
    slices = {
        name: summarize([row for row in rows if row["slice"] == name])
        for name in sorted({row["slice"] for row in rows})
    }
    return {"config": config, "k": plan["k"], "metrics": metrics, "slices": slices, "rows": rows}


def compare(reference, candidate, minimum_recall_gain):
    baseline = reference["metrics"]
    result = candidate["metrics"]
    recall_gain = Fraction(result["macro_recall"]) - Fraction(baseline["macro_recall"])
    precision_gain = Fraction(result["macro_precision"]) - Fraction(baseline["macro_precision"])
    old_rows = {row["id"]: row for row in reference["rows"]}
    new_rows = {row["id"]: row for row in candidate["rows"]}
    if reference["k"] != candidate["k"] or old_rows.keys() != new_rows.keys():
        raise ValueError("Comparison requires the same cases and evidence budget")
    label_fields = ("expected", "query", "group", "critical", "slice")
    if any(
        old_rows[key][field] != new_rows[key][field]
        for key in old_rows for field in label_fields
    ):
        raise ValueError("Comparison requires fixed labels")
    new_critical_misses = {
        query_id: sorted(set(row["missed"]) - set(old_rows[query_id]["missed"]))
        for query_id, row in new_rows.items()
        if row["critical"] and set(row["missed"]) - set(old_rows[query_id]["missed"])
    }
    guards = {
        "minimum_recall_gain": recall_gain >= Fraction(minimum_recall_gain),
        "no_precision_loss": precision_gain >= 0,
        "no_increase_in_false_returns": (
            result["no_evidence_false_returns"] <= baseline["no_evidence_false_returns"]
        ),
        "no_new_critical_miss": not new_critical_misses,
    }
    return {
        "recall_gain": str(recall_gain),
        "precision_gain": str(precision_gain),
        "new_critical_misses": new_critical_misses,
        "guards": guards,
        "accepted": all(guards.values()),
    }
