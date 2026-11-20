"""Demonstrate a duplicate local draft after a lost commit acknowledgement."""
import argparse
from contextlib import closing
import json
import os
import sqlite3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("db")
    parser.add_argument("--crash", action="store_true")
    args = parser.parse_args()
    with closing(sqlite3.connect(args.db)) as db:
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS drafts (attempt INTEGER PRIMARY KEY, slot TEXT)")
            db.execute("INSERT INTO drafts (slot) VALUES ('2026-W45')")
        if args.crash:
            os._exit(73)
        rows = db.execute("SELECT attempt, slot FROM drafts ORDER BY attempt").fetchall()
    print(json.dumps({"drafts": rows}))


if __name__ == "__main__":
    main()
