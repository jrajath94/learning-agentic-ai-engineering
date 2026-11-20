# Trace rollup workshop

Use Python 3.8 or later. Use Git 2.28 or later for the branch exercise.
Run this command from this directory to replay both lessons in a temporary repository.

```sh
python3 -B verify.py
```

Open the engineering workshop page for the manual procedure, exact outputs, and exercises.
Use `evidence/run.txt` to compare the verified result.
The replay uses only synthetic inputs, Python, and Git.
An agent is optional. Use the prompt files as human checklists or paste one prompt at a time.

| Path | Purpose |
| --- | --- |
| lab/ | Starting repository with the defect, public CLI, fixtures, and four smoke tests |
| variants/test_retries.py | Implementation branch regression tests |
| variants/candidate.py | First implementation, which the review can disprove |
| variants/test_review.py | Independent review cases |
| variants/repaired.py | Repaired aggregation module |
| diagrams/ | Mermaid sources for the three workshop figures |
| prompts/ | Filled prompts and versions for another repository |
| evidence/run.txt | Recorded command results from the replay |

Run the broken CLI directly from the starting repository.

```sh
cd lab
python3 -B -m trace_rollup fixtures/nightly.jsonl
python3 -B -m unittest discover -s tests -v
```

The initial tests pass. The nightly report overcounts nightly-a.
Keep the workshop's original files as references.
Use the manual procedure's disposable copy for edits.
