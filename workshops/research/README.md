# Local retrieval evaluation workshop

The revised retriever wins development and loses acceptance. Reproduce the decision with Python 3.8 or later. The workshop needs no packages, credentials, network access, or model.

Open the Research workshop chapter in the extracted guide for the full walkthrough, trace tables, formulas, exercises, and source notes.

## Run from this directory

```sh
python3 -B run.py audit
python3 -B run.py explain D01 --config baseline
python3 -B run.py explain D01 --config combined
python3 -B run.py explain D06 --config combined
python3 -B run.py dev --out session-01 --stop-after 2
python3 -B run.py dev --out session-01
python3 -B run.py holdout --out session-01
python3 -B -m unittest -v
```

On Windows, use `py -3` if that is the installed command. Use a fresh output directory for a new run. Use the same directory to resume the paused run. Leave the supplied records in place.

The deliberate leakage check exits with code 1 and names the borrowed family and reference.

```sh
python3 -B run.py audit --holdout-file leaky-holdout.json
```

## Files

| Path | Use |
| --- | --- |
| [retriever.py](retriever.py) | Tokenize and rank. Set title weight to zero and aliases to none for the baseline. |
| [evaluate.py](evaluate.py) | Validate the split, score evidence, and compare paired cases. |
| [run.py](run.py) | Run the development budget, checkpoint, and score the frozen choice. |
| [test_workshop.py](test_workshop.py) | Run nine checks with temporary output directories. |
| [fixtures/corpus.json](fixtures/corpus.json) | Inspect 22 synthetic source cards from seven families. |
| [fixtures/plan.json](fixtures/plan.json) | Inspect the candidate plan, budget, aliases, and frozen test digest. |
| [fixtures/dev.json](fixtures/dev.json) | Inspect six development queries and reference labels. |
| [fixtures/holdout.json](fixtures/holdout.json) | Inspect three held-out queries. Keep them separate during candidate selection. |
| [fixtures/leaky-holdout.json](fixtures/leaky-holdout.json) | Check a deliberately contaminated split. |
| [records/checkpoint-at-2.json](records/checkpoint-at-2.json) | Review the paused ledger with two completed candidates. |
| [records/checkpoint.json](records/checkpoint.json) | Review the complete ledger, per-query traces, and slice metrics. |
| [records/holdout-report.json](records/holdout-report.json) | Inspect the paired held-out decision. |
| [records/tests.txt](records/tests.txt) | Read captured test output. |
| [prompts](prompts/) | Open the nine reusable prompts with filled examples. |

## Expected decisions

At pause, the record has two candidates and the incumbent is titles. After resume, the record has four candidates and the incumbent is combined. Its development recall is 1 and precision is 3/5.

On holdout, mean recall stays at 2/3 and precision rises from 1/3 to 1/2. The candidate misses required card V11 on query H03. The minimum gain and critical guards fail. Retain the baseline.

This sample tests two evidence slots over a fixed index. It has one held-out ambiguous case and no held-out empty-reference case.

## Reproduce the supplied audit records

Run these commands from this directory with an unused `session-01`. Each JSON trace stays the same for the same inputs and configuration. Test timing varies by machine.

```sh
python3 -B run.py audit > session-split.txt
python3 -B run.py audit --holdout-file leaky-holdout.json > session-leak.txt 2>&1
python3 -B run.py explain D01 --config baseline > session-d01-baseline.json
python3 -B run.py explain D01 --config combined > session-d01-combined.json
python3 -B run.py explain D06 --config combined > session-d06-combined.json
python3 -B run.py dev --out session-01 --stop-after 2 > session-dev.txt
cp session-01/checkpoint.json session-01/checkpoint-at-2.json
python3 -B run.py dev --out session-01 >> session-dev.txt
python3 -B run.py holdout --out session-01 > session-holdout.txt
python3 -B -m unittest -v > session-tests.txt 2>&1
```

If you adapt the corpus, record a new experiment plan. Have the test owner compute the digest of the new held-out labels with the same digest function before tuning.

```sh
python3 -B -c 'from run import FIXTURES, digest; print(digest(("holdout.json",), FIXTURES))'
```
