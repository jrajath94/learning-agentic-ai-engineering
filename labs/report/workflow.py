"""Build a draft support report from a local CSV."""

import argparse
import csv
import hashlib
import io
import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Literal

Stage = Literal["read", "draft", "review", "failed"]
RECIPE = "support-review-v1"
MAX_BYTES = 16_384
MAX_ROWS = 100
MAX_CALLS = 4
MAX_RETRIES = 1


class TransientToolError(Exception):
    """A local operation can succeed on a retry."""


class InvalidSource(Exception):
    """The source does not satisfy the input contract."""


@dataclass
class TaskState:
    key: str
    stage: Stage = "read"
    calls: int = 0
    retries: int = 0
    rows: list[dict] = field(default_factory=list)
    events: list[str] = field(default_factory=list)


def atomic_write(path: Path, body: str) -> None:
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(body)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def read_source(raw: bytes) -> list[dict]:
    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8")), strict=True)
        if reader.fieldnames != ["id", "category", "open_days", "status"]:
            raise InvalidSource("invalid columns")
        rows = []
        seen = set()
        for row in reader:
            if len(rows) >= MAX_ROWS:
                raise InvalidSource("row limit exceeded")
            if None in row or any(value is None for value in row.values()):
                raise InvalidSource("invalid row width")
            row_id = row["id"]
            if not row_id.isascii() or not row_id.isalnum() or row_id in seen:
                raise InvalidSource("invalid or duplicate id")
            if row["category"] not in {"access", "billing", "shipping"}:
                raise InvalidSource("invalid category")
            if row["status"] not in {"open", "closed"}:
                raise InvalidSource("invalid status")
            days = int(row["open_days"])
            if not 0 <= days <= 3650:
                raise InvalidSource("invalid open_days")
            seen.add(row_id)
            rows.append(dict(id=row_id, category=row["category"],
                             open_days=days, status=row["status"]))
        return rows
    except (ValueError, csv.Error) as error:
        raise InvalidSource("invalid source value") from error


def render(rows: list[dict], key: str) -> str:
    opened = [row for row in rows if row["status"] == "open"]
    aged = sorted(
        (row for row in opened if row["open_days"] >= 7),
        key=lambda row: (-row["open_days"], row["id"]),
    )

    def references(part: list[dict]) -> str:
        return ", ".join(row["id"] for row in part) or "none"

    entries = [
        "# Support queue review",
        "",
        "Status: Draft for human review",
        "",
        f"Open requests: {len(opened)} [Source rows: {references(opened)}].",
        f"Open for at least 7 days: {len(aged)} [Source rows: {references(aged)}].",
        "",
        "| Request | Category | Open days |",
        "| --- | --- | ---: |",
    ]
    entries += [
        f"| {row['id']} | {row['category']} | {row['open_days']} |" for row in aged
    ]
    entries += ["", "Source: supplied CSV. Look up source rows by the id column.",
                f"Task fingerprint (SHA-256): {key}", ""]
    return "\n".join(entries)


def matches_draft(path: Path, body: str) -> bool:
    expected = body.encode("utf-8")
    try:
        with path.open("rb") as draft:
            return draft.read(len(expected) + 1) == expected
    except FileNotFoundError:
        return False


def run(path: Path, out: Path, reader: Callable[[bytes], list[dict]] = read_source,
        writer: Callable[[Path, str], None] = atomic_write) -> TaskState:
    # Use one writer per output directory.
    with path.open("rb") as file:
        raw = file.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise InvalidSource("byte limit exceeded")
    key = hashlib.sha256(RECIPE.encode() + b"\x00" + raw).hexdigest()
    out.mkdir(parents=True, exist_ok=True)
    checkpoint = out / "state.json"
    artifact = out / "draft.md"
    state = TaskState(**json.loads(checkpoint.read_text())) if checkpoint.exists() else TaskState(key)
    if state.key != key:
        raise InvalidSource("checkpoint belongs to different input or recipe")
    if state.stage not in {"read", "draft", "review", "failed"}:
        raise InvalidSource("invalid checkpoint stage")

    def save() -> None:
        atomic_write(checkpoint, json.dumps(asdict(state), indent=2) + "\n")

    if state.stage == "review":
        # Compare contents before treating a previous result as complete.
        if matches_draft(artifact, render(state.rows, key)):
            return state
        state.stage = "draft"
        state.events.append("draft restored from checkpoint")
        save()

    while state.stage in {"read", "draft"}:
        if state.calls >= MAX_CALLS:
            state.stage = "failed"
            state.events.append("tool call limit reached")
            save()
            break
        state.calls += 1
        save()
        try:
            if state.stage == "read":
                state.rows = reader(raw)
                state.stage = "draft"
            else:
                body = render(state.rows, key)
                if not matches_draft(artifact, body):
                    writer(artifact, body)
                if not matches_draft(artifact, body):
                    raise TransientToolError("draft verification failed")
                state.stage = "review"
        except (TransientToolError, OSError):
            state.events.append(f"local tool error at {state.stage}")
            if state.retries >= MAX_RETRIES:
                state.stage = "failed"
            else:
                state.retries += 1
        except InvalidSource as error:
            state.events.append(str(error))
            state.stage = "failed"
        save()
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    state = run(args.source, args.out)
    print(f"Stage={state.stage} Calls={state.calls} Retries={state.retries}")
    raise SystemExit(0 if state.stage == "review" else 1)
