# Find why a prompt cache changed the bill

Record the prefix and usage for each request. Calculate cost from token categories. Use fixed rates in the exercise so a price change cannot explain your result.

## Start offline

Work the case below before you inspect the original source. The trace, exercise and worked answers are complete offline. The [local token rollup](../workshops/engineering/lab/trace_rollup/aggregate.py) gives you a related counting exercise. Follow input and output totals separately before you introduce cache categories. The optional upstream links at the end need an internet connection.

## Calculate three requests

Use a synthetic stable prefix of 2,000 tokens. Add 400 tokens of task-specific input. Assume an eligible cache breakpoint at the end of the stable prefix. Assume the second request can find the first entry. The counts below are fixtures, separate from API measurements.

| Request | Total input | Cache read | Cache write | Ordinary input | Output |
| --- | ---: | ---: | ---: | ---: | ---: |
| A. Write the stable prefix | 2,400 | 0 | 2,000 | 400 | 200 |
| B. Reuse the prefix | 2,400 | 2,000 | 0 | 400 | 200 |
| C. Change the first instruction | 2,400 | 0 | 2,000 | 400 | 200 |

Use toy rates per 1,000 tokens: 1 credit for ordinary input, 0.1 for cache reads, 1.25 for cache writes and 4 for output. A costs `0.4 + 2.5 + 0.8 = 3.7` credits. B costs `0.4 + 0.2 + 0.8 = 1.4`. C costs 3.7. The total is 8.8. Three requests at the toy ordinary rate with the same output would cost 9.6. Record the cost of the whole run. A cold write can raise the first request's cost before later reads repay it.

Now put a unique job label before the developer instructions in each request. Predict that the old breakpoint after the stable prefix will fail to match. Move the label to the part after the breakpoint. Predict which eligible prefix can match. The service result can still depend on model, settings, timing and availability. Use usage counters to check the prediction.

## Find the accounting mistake

Suppose a reporter multiplies all 2,400 input tokens in B by the ordinary rate and adds the 2,000 cache reads again. It reports `2.4 + 0.2 + 0.8 = 3.4` credits. The same 2,000 tokens appear in two categories. Require the ledger to reconcile input counts before it records cost.

Suppose a second reporter sees the same output token count in A and B and calls the cache a miss. It measures the wrong quantity. The experiment asks whether the input prefix was reused. Compare the read count and cost. Keep latency separate, since a single slow response is insufficient evidence about cache state.

## Adapt the ledger

Build a local ledger with request ID, API surface, model, cache mode, ordered tool set version, prefix version, measured counters and a rate card identifier. Feed it A, B and C. Add a row where cache reads plus cache writes exceed total input. Reject that row. Add a row whose cache write field is missing. Require a named billing mode before you interpret that absence as zero.

Compare two synthetic traces. In one, a compaction operation changes the retained context before the breakpoint. In the other, a new question appends to the same prefix. Predict the cache effect and label the assumptions behind each prediction.

## Check your solution

The ledger reports 8.8 credits for the fixture. Each input token belongs to one category in that calculation. The row with invalid counts fails. The reader can identify the first changed input or setting and distinguish a prediction from reported usage.

## Retrieve from memory

1. What does the second cookbook request preserve?
2. Why does a cached input token stay in total input?
3. Which records let you explain a cache miss without the complete prompt text?

## Worked answers

1. It preserves the prior message prefix and tool definitions, then appends a user message.
2. Total input counts all input categories. Cached input has a distinct rate.
3. Use the API surface, model, cache mode, prefix version, tool set version and usage counters.

## Optional source inspection

Read OpenAI's [prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching#how-caching-works) at “How caching works,” “How prefix matching works,” and “Request 1 · Response usage.” Open [examples/Prompt_Caching101.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/Prompt_Caching101.ipynb) and search for `completion_run` and `main` under the first example. The docs and notebook use mutable links read on 2026-11-20.

The cookbook sends two Chat Completions requests with unchanged tool definitions. It appends a second user message and prints usage. Inspect the cells to see why a second user message in a demo differs from a transcript with an assistant reply and tool results. The example reads `usage.prompt_tokens_details.cached_tokens`. For a Responses API ledger, use `usage.input_tokens_details` and identify whether the selected model and cache mode report a separate write count. Use the API shape and rate rules for the chosen run.
