# PR prep

Provenance: original synthesis. Boris Cherny, 4 Mar 2026, about 42:19: a model review is first, a person still approves. He also said to tell Claude to start three agents and then dedupe false positives. This prompt is the single-session version.

```text
Range: {{BASE}}...HEAD
Test: {{TEST_COMMAND}}

Run the test. Paste the exit code.
Summarize the diff in five lines a reviewer can check against the files.
List risks: migrations, auth, payments, generated files.
Do not push. Do not merge.
```
