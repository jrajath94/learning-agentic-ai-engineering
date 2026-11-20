"""Check a fake tool catalog, preview bounds, and rating rates."""

from fractions import Fraction
from hashlib import sha256
import json


OPEN_PROJECT = {
    "name": "open_project",
    "inputSchema": {"type": "object", "required": ["project_id"]},
}
CHECK_STATUS = {"name": "status", "inputSchema": {"type": "object"}}


def preview_tool(required):
    return {"name": "preview", "inputSchema": {"type": "object", "required": required}}


def tool_names(catalog):
    return sorted(tool["name"] for tool in catalog)


def catalog_digest(catalog):
    by_name = sorted(catalog, key=lambda tool: tool["name"])
    canonical = json.dumps(by_name, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def refresh_catalog(cached, current, notification):
    if notification == "notifications/tools/list_changed":
        return current
    return cached


def preview(state, requested_revision):
    if state["revision"] is None:
        return "unavailable"
    if requested_revision != state["revision"]:
        return "stale_revision"
    return "ready"


def proof_at_revision(receipts, revision):
    return [row["check"] for row in receipts if row["revision"] == revision and row["exit"] == 0]


def shared_ports(receipts):
    ports = [row["port"] for row in receipts]
    return len(ports) != len(set(ports))


def replay_plan(states):
    boundary = next((position for position, state in enumerate(states) if state != "complete"), len(states))
    return ["reuse"] * boundary + ["run"] * (len(states) - boundary)


def vertical_fit(safe_rows, label_rows):
    return safe_rows[0] <= label_rows[0] and label_rows[1] <= safe_rows[1]


def rating_rate(useful, exposures):
    if exposures is None:
        return None
    return Fraction(useful, exposures)


def main():
    home = [CHECK_STATUS, OPEN_PROJECT]
    project_v1 = [CHECK_STATUS, OPEN_PROJECT, preview_tool(["project_id"])]
    project_v2 = [CHECK_STATUS, OPEN_PROJECT, preview_tool(["project_id", "revision"])]
    stale_cache = refresh_catalog(home, project_v1, None)
    assert "preview" not in tool_names(stale_cache)
    client_cache = refresh_catalog(home, project_v1, "notifications/tools/list_changed")
    assert "preview" in tool_names(client_cache)

    assert tool_names(project_v1) == tool_names(project_v2)
    assert catalog_digest(project_v1) != catalog_digest(project_v2)
    assert catalog_digest(project_v2) == catalog_digest(list(reversed(project_v2)))
    assert preview({"revision": "r2"}, "r1") == "stale_revision"
    assert preview({"revision": "r2"}, "r2") == "ready"
    assert preview({"revision": None}, "r2") == "unavailable"

    receipts = [
        {"check": "unit", "revision": "candidate", "exit": 0, "port": 4173},
        {"check": "ui", "revision": "base", "exit": 0, "port": 4173},
    ]
    assert proof_at_revision(receipts, "candidate") == ["unit"]
    assert shared_ports(receipts)
    receipts[1]["port"] = 4174
    assert not shared_ports(receipts)
    assert replay_plan(["complete", "failed", "complete"]) == ["reuse", "run", "run"]

    assert vertical_fit((35, 90), (36, 44))
    assert not vertical_fit((35, 90), (31, 48))
    assert rating_rate(20, 1000) == Fraction(2, 100)
    assert rating_rate(12, 100) == Fraction(12, 100)
    assert rating_rate(12, None) is None

    print("Only the candidate check counts. Separate worktrees can request the same port.")
    print("Replay reuses the prefix and repeats the completed step after a failure.")
    print("Refresh exposes preview. Name-only comparison misses the schema change.")
    print("Schema digest detects the change. Stale and closed preview calls are rejected.")
    print("Bounds: fits, clips. Rates: 2%, 12%, unknown when exposures are absent.")


if __name__ == "__main__":
    main()
