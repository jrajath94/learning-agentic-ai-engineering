"""Stage a local weekly research brief from a versioned JSONL export."""
import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata

from briefing_tools import (
    EvidenceError, MAX_BODY_CHARS, SOURCE_ID, TOOL_SCHEMA, execute_tool, fake_model, verify_evidence,
)

POLICY = "weekly-research-v1"
FEED_FIELDS = {"source_id", "date", "title", "body"}
MAX_FEED_BYTES = 256_000
MAX_RECORDS = 40
SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_key TEXT PRIMARY KEY,
    week TEXT NOT NULL,
    feed_sha256 TEXT NOT NULL,
    policy TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('snapshot_ready', 'draft_staged')),
    input_records INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS sources (
    run_key TEXT NOT NULL REFERENCES runs,
    source_id TEXT NOT NULL,
    date TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    body_sha256 TEXT NOT NULL,
    PRIMARY KEY (run_key, source_id)
);
CREATE TABLE IF NOT EXISTS issues (
    run_key TEXT NOT NULL REFERENCES runs,
    ordinal INTEGER NOT NULL,
    detail TEXT NOT NULL,
    PRIMARY KEY (run_key, ordinal)
);
CREATE TABLE IF NOT EXISTS drafts (
    run_key TEXT PRIMARY KEY REFERENCES runs,
    idempotency_key TEXT NOT NULL UNIQUE,
    body TEXT NOT NULL,
    body_sha256 TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evidence (
    run_key TEXT NOT NULL REFERENCES drafts,
    source_id TEXT NOT NULL,
    detail TEXT NOT NULL,
    PRIMARY KEY (run_key, source_id),
    FOREIGN KEY (run_key, source_id) REFERENCES sources (run_key, source_id)
);
CREATE TABLE IF NOT EXISTS events (
    run_key TEXT NOT NULL REFERENCES runs,
    ordinal INTEGER NOT NULL,
    step TEXT NOT NULL,
    PRIMARY KEY (run_key, ordinal)
);
"""


class InputError(ValueError):
    pass


def digest(value):
    raw = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.sha256(raw).hexdigest()


def compact_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("duplicate_json_member")
        result[key] = value
    return result


def reject_constant(_value):
    raise InputError("invalid_json")


def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_members, parse_constant=reject_constant)


def week_bounds(week):
    match = re.fullmatch(r"([0-9]{4})-W([0-9]{2})", week)
    if match is None:
        raise InputError("Use an ISO week such as 2026-W45.")
    try:
        start = date.fromisocalendar(int(match[1]), int(match[2]), 1)
        return start, start + timedelta(days=7)
    except (ValueError, OverflowError) as error:
        raise InputError("Use a valid ISO week.") from error


def safe_text(value, limit, allow_newline=False):
    if type(value) is not str or not value.strip() or len(value) > limit:
        return False
    for character in value:
        if allow_newline and character == "\n":
            continue
        if unicodedata.category(character) in {"Cc", "Cf", "Cs", "Zl", "Zp"}:
            return False
    return True


def validate_source(row):
    if type(row) is not dict or set(row) != FEED_FIELDS:
        raise InputError("invalid_fields")
    if type(row["source_id"]) is not str or SOURCE_ID.fullmatch(row["source_id"]) is None:
        raise InputError("invalid_source_id")
    day = row["date"]
    if type(day) is not str or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day) is None:
        raise InputError("invalid_date")
    try:
        published = date.fromisoformat(day)
    except ValueError as error:
        raise InputError("invalid_date") from error
    if not safe_text(row["title"], 160) or not safe_text(row["body"], MAX_BODY_CHARS, True):
        raise InputError("invalid_text")
    return published


def prepare_feed(raw, week):
    start, end = week_bounds(week)
    if len(raw) > MAX_FEED_BYTES:
        raise InputError("Feed exceeds 256000 bytes.")
    try:
        lines = raw.decode("utf-8").split("\n")
    except UnicodeDecodeError as error:
        raise InputError("Feed must use UTF-8.") from error
    count = sum(bool(line.strip()) for line in lines)
    if count > MAX_RECORDS:
        raise InputError("Feed exceeds 40 nonblank records.")
    issues = []
    groups = defaultdict(list)
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = read_json(line)
            published = validate_source(row)
        except InputError as error:
            issues.append({"line": number, "code": str(error)})
            continue
        except (ValueError, RecursionError):
            issues.append({"line": number, "code": "invalid_json"})
            continue
        if not start <= published < end:
            issues.append({"line": number, "code": "outside_week", "source_id": row["source_id"]})
            continue
        groups[row["source_id"]].append((number, row))
    retained = []
    seen_bodies = {}
    for source_id, records in sorted(groups.items()):
        if any(row != records[0][1] for _, row in records):
            issues.append({"lines": [number for number, _ in records],
                           "code": "conflicting_source_id", "source_id": source_id})
            continue
        number, row = records[0]
        for duplicate_line, _ in records[1:]:
            issues.append({"line": duplicate_line, "code": "duplicate_source_id", "source_id": source_id})
        body_sha256 = digest(row["body"])
        if body_sha256 in seen_bodies:
            issues.append({"line": number, "code": "duplicate_body", "source_id": source_id,
                           "retained_source_id": seen_bodies[body_sha256]})
            continue
        seen_bodies[body_sha256] = source_id
        retained.append({**row, "body_sha256": body_sha256})
    if not retained:
        raise InputError("No valid sources in the selected week. Inspect and correct the feed.")
    return count, retained, issues


@contextmanager
def database(path, create=False):
    if not create and not Path(path).is_file():
        raise InputError("Database does not exist. Run the workflow first.")
    db = sqlite3.connect(path, timeout=10, isolation_level=None)
    try:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        if create:
            db.executescript(SCHEMA)
        yield db
    finally:
        db.close()


@contextmanager
def write_transaction(db):
    db.execute("BEGIN IMMEDIATE")
    try:
        yield
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise


def make_run_key(week, feed_sha256):
    return "run_" + digest(compact_json([POLICY, week, feed_sha256]))


def make_draft_key(key):
    return "draft_" + digest(compact_json(["stage-draft-v1", key]))


def stage_snapshot(db, key, week, feed_sha256, count, retained, issues):
    with write_transaction(db):
        if db.execute("SELECT 1 FROM runs WHERE run_key = ?", (key,)).fetchone():
            return
        db.execute("INSERT INTO runs VALUES (?, ?, ?, ?, 'snapshot_ready', ?)",
                   (key, week, feed_sha256, POLICY, count))
        db.executemany("INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?)", [
            (key, row["source_id"], row["date"], row["title"], row["body"], row["body_sha256"])
            for row in retained
        ])
        db.executemany("INSERT INTO issues VALUES (?, ?, ?)", [
            (key, ordinal, compact_json(issue)) for ordinal, issue in enumerate(issues, start=1)
        ])
        db.execute("INSERT INTO events VALUES (?, 1, 'snapshot_committed')", (key,))


def load_sources(db, key):
    rows = db.execute("SELECT * FROM sources WHERE run_key = ? ORDER BY source_id", (key,))
    return {row["source_id"]: dict(row) for row in rows}


def render_draft(week, key, sources, evidence):
    lines = [f"AI research brief for {week}", "Status: DRAFT FOR REVIEW",
             "Input: Local export. Source claims require review.", f"Run: {key}", ""]
    for number, item in enumerate(evidence, start=1):
        source_id = item["source_id"]
        source = sources[source_id]
        lines.append(f"{number}. {json.dumps(source['title'], ensure_ascii=False)} [{source_id}, {source['date']}]")
        lines.append(f"   Source claim [{item['start']}:{item['end']}]: {item['quote']}")
        scope = item["scope"]
        if scope is None:
            lines.append("   Scope: Not in source.")
        else:
            lines.append(f"   Scope [{scope['start']}:{scope['end']}]: {scope['quote']}")
        lines.append("")
    if not evidence:
        lines.extend(["No eligible Result lines. Review the snapshot before use.", ""])
    for source_id in sorted(set(sources) - {item["source_id"] for item in evidence}):
        lines.append(f"No draft item: {source_id}")
    lines.extend(["", "Review: Check source authenticity, scope and what decision the result supports."])
    return "\n".join(lines) + "\n"


def stage_draft(db, key, body, evidence, crash):
    with write_transaction(db):
        if db.execute("SELECT 1 FROM drafts WHERE run_key = ?", (key,)).fetchone():
            return "reused"
        db.execute("INSERT INTO drafts VALUES (?, ?, ?, ?)",
                   (key, make_draft_key(key), body, digest(body)))
        db.executemany("INSERT INTO evidence VALUES (?, ?, ?)", [
            (key, item["source_id"], compact_json(item)) for item in evidence
        ])
        db.execute("UPDATE runs SET state = 'draft_staged' WHERE run_key = ?", (key,))
        db.execute("INSERT INTO events VALUES (?, 2, 'draft_committed')", (key,))
        if crash == "before-draft-commit":
            os._exit(72)
    if crash == "after-draft-commit":
        os._exit(73)
    return "staged"


def run(db_path, feed_path, week, crash=None, model=fake_model):
    with Path(feed_path).open("rb") as feed:
        raw = feed.read(MAX_FEED_BYTES + 1)
    count, retained, issues = prepare_feed(raw, week)
    feed_sha256 = digest(raw)
    key = make_run_key(week, feed_sha256)
    with database(db_path, create=True) as db:
        stage_snapshot(db, key, week, feed_sha256, count, retained, issues)
        if db.execute("SELECT 1 FROM drafts WHERE run_key = ?", (key,)).fetchone():
            return key, "reused"
        sources = load_sources(db, key)
        proposals = model(tuple(sources), lambda request: execute_tool(request, sources))
        evidence = verify_evidence(sources, proposals)
        body = render_draft(week, key, sources, evidence)
        return key, stage_draft(db, key, body, evidence, crash)


def choose_run(db, key):
    if key:
        row = db.execute("SELECT * FROM runs WHERE run_key = ?", (key,)).fetchone()
        if row is None:
            raise InputError("Run key was not found.")
        return dict(row)
    rows = db.execute("SELECT * FROM runs ORDER BY run_key LIMIT 2").fetchall()
    if len(rows) != 1:
        raise InputError("Use list-runs and supply one run key with --key.")
    return dict(rows[0])


def inspect_run(db, selected):
    key = selected["run_key"]
    sources = [{name: value for name, value in row.items() if name not in {"body", "run_key"}}
               for row in load_sources(db, key).values()]
    issues = db.execute("SELECT detail FROM issues WHERE run_key = ? ORDER BY ordinal", (key,))
    evidence = db.execute("SELECT detail FROM evidence WHERE run_key = ? ORDER BY source_id", (key,))
    events = db.execute("SELECT step FROM events WHERE run_key = ? ORDER BY ordinal", (key,))
    draft = db.execute("SELECT idempotency_key, body_sha256 FROM drafts WHERE run_key = ?", (key,)).fetchone()
    return {**selected, "sources": sources, "issues": [json.loads(row[0]) for row in issues],
            "evidence": [json.loads(row[0]) for row in evidence], "events": [row[0] for row in events],
            "draft": dict(draft) if draft else None}


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("run")
    start.add_argument("--db", required=True)
    start.add_argument("--feed", required=True)
    start.add_argument("--week", required=True)
    start.add_argument("--crash", choices=("before-draft-commit", "after-draft-commit"))
    for name in ("inspect", "draft", "tool-calls", "list-runs"):
        command = commands.add_parser(name)
        command.add_argument("--db", required=True)
        if name != "list-runs":
            command.add_argument("--key")
        if name == "tool-calls":
            command.add_argument("--calls", required=True)
    commands.add_parser("schema")
    args = parser.parse_args()
    try:
        if args.command == "schema":
            result = TOOL_SCHEMA
        elif args.command == "run":
            key, outcome = run(args.db, args.feed, args.week, args.crash)
            result = {"run_key": key, "outcome": outcome}
        else:
            with database(args.db) as db:
                db.execute("BEGIN")
                if args.command == "list-runs":
                    result = [dict(row) for row in db.execute("SELECT * FROM runs ORDER BY run_key")]
                else:
                    selected = choose_run(db, args.key)
                    key = selected["run_key"]
                    if args.command == "inspect":
                        result = inspect_run(db, selected)
                    elif args.command == "draft":
                        row = db.execute("SELECT body FROM drafts WHERE run_key = ?", (key,)).fetchone()
                        if row is None:
                            raise InputError("The run has no staged draft.")
                        sys.stdout.write(row["body"])
                        return 0
                    else:
                        with Path(args.calls).open("rb") as call_file:
                            raw_calls = call_file.read(MAX_FEED_BYTES + 1)
                        if len(raw_calls) > MAX_FEED_BYTES:
                            raise InputError("Tool call input exceeds 256000 bytes.")
                        try:
                            calls = read_json(raw_calls.decode("utf-8"))
                        except (ValueError, RecursionError) as error:
                            raise InputError("Tool call input must be valid UTF-8 JSON with unique keys.") from error
                        if type(calls) is not list or len(calls) > 40:
                            raise InputError("Use an array of up to 40 tool call objects.")
                        sources = load_sources(db, key)
                        result = [execute_tool(call, sources) for call in calls]
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
