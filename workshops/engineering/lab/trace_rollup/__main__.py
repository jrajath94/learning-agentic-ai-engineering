import argparse
import json
from pathlib import Path
import sys

from .aggregate import rollup
from .records import TraceError, read_records


def main():
    parser = argparse.ArgumentParser(description="Summarize terminal eval results.")
    parser.add_argument("source", type=Path, help="Path to a UTF-8 JSONL export")
    args = parser.parse_args()
    try:
        with args.source.open(encoding="utf-8") as stream:
            report = rollup(read_records(stream))
    except (OSError, UnicodeError, TraceError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
