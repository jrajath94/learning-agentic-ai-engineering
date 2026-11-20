"""Verify a synthetic briefing draft with Python 3 and a temporary directory."""

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory


INPUTS = [
    {"kind": "ticket", "ref": "tracker:T-17:2", "value": "blocked"},
    {"kind": "conflict", "ref": "chat:91", "value": "T-17 ready"},
    {"kind": "calendar", "ref": "calendar:CL-04:1", "value": "2026-11-20T16:00:00Z"},
    {"kind": "conflict", "ref": "chat:92", "value": "launch at 15:00 UTC"},
    {"kind": "irrelevant", "ref": "chat:93", "value": "hello"},
]

DRAFT_NAME = "release-briefing-2026-11-20.json"


def prepare_draft(directory, records, interrupt=False):
    final = directory / DRAFT_NAME
    pending = final.with_suffix(".tmp")
    snapshot = json.dumps(records, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(snapshot).hexdigest()

    if final.exists():
        current = json.loads(final.read_text(encoding="utf-8"))
        if current["source_digest"] == digest:
            return "reused"
        return "review_new_revision"

    facts = [row for row in records if row["kind"] in {"ticket", "calendar"}]
    conflicts = [row for row in records if row["kind"] == "conflict"]
    fields_present = {row["kind"] for row in facts}
    missing = sorted({"ticket", "calendar"} - fields_present)
    state = "source_missing" if missing else "draft"
    draft = {
        "state": state,
        "source_digest": digest,
        "counts": {
            "input": len(records),
            "facts": len(facts),
            "conflicts": len(conflicts),
            "discarded": len(records) - len(facts) - len(conflicts),
        },
        "facts": facts,
        "conflicts": conflicts,
        "missing": missing,
    }
    pending.write_text(json.dumps(draft, indent=2) + "\n", encoding="utf-8")
    if interrupt:
        return "interrupted"
    pending.replace(final)
    return state


def main():
    with TemporaryDirectory() as directory_name:
        directory = Path(directory_name)
        final = directory / DRAFT_NAME
        assert prepare_draft(directory, INPUTS, interrupt=True) == "interrupted"
        assert not final.exists()
        assert prepare_draft(directory, INPUTS) == "draft"
        assert prepare_draft(directory, INPUTS) == "reused"
        assert len(list(directory.glob("*.json"))) == 1
        assert not final.with_suffix(".tmp").exists()
        draft = json.loads(final.read_text(encoding="utf-8"))
        assert draft["counts"] == {"input": 5, "facts": 2, "conflicts": 2, "discarded": 1}
        assert [(row["ref"], row["value"]) for row in draft["facts"]] == [
            ("tracker:T-17:2", "blocked"),
            ("calendar:CL-04:1", "2026-11-20T16:00:00Z"),
        ]
        assert [row["ref"] for row in draft["conflicts"]] == ["chat:91", "chat:92"]
        assert prepare_draft(directory, INPUTS[:-1]) == "review_new_revision"
        assert draft == json.loads(final.read_text(encoding="utf-8"))

    with TemporaryDirectory() as directory_name:
        directory = Path(directory_name)
        without_calendar = [row for row in INPUTS if row["kind"] != "calendar"]
        assert prepare_draft(directory, without_calendar) == "source_missing"
        draft = json.loads((directory / DRAFT_NAME).read_text(encoding="utf-8"))
        assert draft["missing"] == ["calendar"]
        assert [row["ref"] for row in draft["facts"]] == ["tracker:T-17:2"]

    print("Five inputs. Two facts. Two conflicts. One discarded event.")
    print("No draft after interruption. One draft after retry.")
    print("Changed snapshot went to review. Missing calendar was reported.")


if __name__ == "__main__":
    main()
