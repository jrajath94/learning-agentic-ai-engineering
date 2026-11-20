# Define the workflow contract

Use this prompt before code changes. It yields decisions that you can make into tests.

## Filled prompt

Design a local weekly AI research brief. Read `fixtures/posts.jsonl` for ISO week `2026-W45`. Produce one SQLite source snapshot and one text draft per exact export. Use a Python standard library process. Limit output to `DRAFT FOR REVIEW`. The owner of the brief checks the source, scope and proposed use. Make a state table for invalid input, a process stop before draft commit and a stop after commit. State the source of the run key and the acceptance check for each transition. Use the fixture. Do not use network access.

## Reference response

| Observation | Workflow action | Acceptance check |
| --- | --- | --- |
| Seven records include one mirror, one invalid shape and one outside week | Keep four sources and three audit issues | `inspect` returns four source IDs and three issues |
| Valid snapshot exists and draft transaction stops before commit | Resume from the source snapshot | Same run key. Retry stages three items |
| Draft commit succeeds and the process stops before its reply | Return the existing receipt | Same draft key. One draft row |
| The export bytes change | Create another run for the same week | Different run key. Two review candidates |

The run key uses the policy version, week and export SHA-256. The draft key uses the stage version and run key. Review state requires a human decision.

## Reusable prompt

Design a `{{purpose}}` workflow for `{{local_input}}` and `{{period_rule}}`. Use `{{runtime}}`. Limit effects to `{{allowed_effects}}`. Hold `{{review_gate}}` for `{{review_owner}}`. Make a state table for `{{input_failures}}`, `{{before_commit_failure}}` and `{{after_commit_failure}}`. Give a stable key for each durable result. Write a check for each transition. Use `{{test_fixture}}` as your only data source.
