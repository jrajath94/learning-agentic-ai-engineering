# Review a claim against its exact source

## Filled prompt

Review the cache item in `results/draft.txt` against SRC-101 in `fixtures/posts.jsonl`. The proposed statement is `Cache reuse cut production latency by 36%`. Report the exact quote and offsets. Identify each claim the source supports. Keep the sample size and units. Give a sentence that can remain in the draft. State what source would be necessary to claim a production effect.

## Reference response

`SRC-101[60:133]` says `Cache reuse cut median tool latency from 800 ms to 510 ms across 40 runs.` `SRC-101[141:192]` limits the result to one workload, one runner and no production traffic. Retain the exact median and sample size. Suggested draft sentence: In a 40-run sandbox test on one workload and one runner, median tool latency fell from 800 ms to 510 ms with cache reuse. A production claim requires a representative production comparison with the same metric definition.

## Reusable prompt

Review `{{proposed_statement}}` against `{{source_id_and_body}}`. Use `{{offset_unit}}`. Report the exact quote, half-open offsets and scope. Preserve all units, sample sizes and conditions. Classify the unsupported parts. Suggest one sentence suitable for `{{review_audience}}`. Describe the evidence needed to support any stronger claim.
