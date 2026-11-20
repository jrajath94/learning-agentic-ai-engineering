# Lab results, executed 20 November 2026

Environment: Python 3.12.3, pytest 9.1.1, this VM. Evidence cutoff: 20 November 2026 (execution day, earlier than 30 November 2026).

## Lab 1, Python service
Command: python3 -m pytest -q in labs/lab1
Result: 5 passed in 0.02s.
Coverage: first page slice (bug fix), second page, priority filter (feature), filter plus page, complete act.
Baseline bug: start = page * per_page skips page one. Fix: start = (page - 1) * per_page.

## Lab 2, retrieval benchmark
Command: python3 benchmark.py in labs/lab2
Corpus: 200 synthetic docs, 4 topics, 20 queries, k = 5, 3 repeats, seed 42.
Result: keyword precision at 5 = 1.0, 1.0, 1.0. TF-IDF precision at 5 = 1.0, 1.0, 1.0.
Time per run: keyword 0.0407s, TF-IDF 0.0603s.
Hard variant, seed 7, 6 of 15 words cross-topic noise: both methods 1.0 on all repeats.
Finding: ceiling effect. Synthetic topics split too clean. This test cannot rank both methods.
Next test: queries with words shared by two topics, plus human judged relevance on real docs.

## Lab 3, business cited report
Command: python3 make_report.py in labs/lab3
Result: rows = 60. Confidence split: High 16, Medium-High 9, Medium 13, Medium-Low 18, Low 2, Low-Medium 2.
Artifact: labs/lab3/report_artifact.md, a review ready draft. No send, post or spend act ran.
