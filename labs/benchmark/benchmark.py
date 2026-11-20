"""Generate synthetic splits and compare three fixed classifiers."""

import argparse
import csv
import json
import random
from pathlib import Path

SEEDS = (7, 19, 43)
MODELS = ("majority", "full", "sensor")


def make_split(seed: int, split: str, size: int) -> list[dict]:
    rng = random.Random(seed * 10 + {"train": 0, "test": 1, "shift": 2}[split])
    rows = []
    for index in range(size):
        label = rng.randrange(2)
        sensor = round(rng.gauss(1.3 * label, 0.7), 4)
        match_rate = 0.12 if split == "shift" else 0.96
        badge = label if rng.random() < match_rate else 1 - label
        rows.append(
            dict(id=f"{seed}-{split}-{index:03}", split=split,
                 sensor=sensor, badge=badge, label=label)
        )
    return rows


def predict(row: dict, model: str, threshold: float, majority: int) -> int:
    if model == "majority":
        return majority
    if model == "sensor":
        return int(row["sensor"] >= threshold)
    if abs(row["sensor"] - threshold) >= 1.25:
        return int(row["sensor"] >= threshold)
    return row["badge"]


def write_csv(path: Path, rows: list[dict], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(out: Path) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    data, errors, metrics = [], [], []
    for seed in SEEDS:
        train = make_split(seed, "train", 200)
        ordinary = make_split(seed, "test", 100)
        shift = make_split(seed, "shift", 100)
        data.extend(train + ordinary + shift)
        majority = int(2 * sum(row["label"] for row in train) > len(train))
        threshold = max(
            (step / 20 for step in range(-10, 31)),
            key=lambda value: sum(
                predict(row, "sensor", value, majority) == row["label"]
                for row in train
            ),
        )
        for split in (ordinary, shift):
            for model in MODELS:
                wrong = 0
                for row in split:
                    prediction = predict(row, model, threshold, majority)
                    if prediction != row["label"]:
                        wrong += 1
                        errors.append(dict(id=row["id"], split=row["split"],
                                           model=model, expected=row["label"],
                                           predicted=prediction))
                metrics.append(dict(seed=seed, split=split[0]["split"], model=model,
                                    correct=len(split) - wrong, total=len(split),
                                    threshold=threshold if model == "sensor" else None))
    write_csv(out / "data.csv", data, ("id", "split", "sensor", "badge", "label"))
    write_csv(out / "errors.csv", errors, ("id", "split", "model", "expected", "predicted"))
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    for item in run(args.out):
        print("{seed} {split:5} {model:8} {correct:3}/{total}".format(**item))
