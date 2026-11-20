# Trace rollup repository

Read CONTRACT.md before you change report behavior.

Run the public CLI from this directory with `python3 -B -m trace_rollup FIXTURE`.
Run checks here with `python3 -B -m unittest discover -s tests -v`.
Use the Python standard library. Use synthetic fixtures.

Inspect trace_rollup/records.py for input validation.
Inspect trace_rollup/aggregate.py for totals.
Keep the CLI arguments, exit codes, and stdout contract intact.

Use the file scope in the task note.
Ask the task owner about any conflict with CONTRACT.md.
Do not infer a producer contract from example output.
