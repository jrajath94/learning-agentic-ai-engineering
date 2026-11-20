# Turn a brief into an engineering decision

## Filled prompt

Write a local decision note for the AI engineering lead after `results/draft.txt`. The context is tool response time and source retrieval quality. Preserve the sandbox scope of SRC-101 and the failed-query count in SRC-103. Recommend one controlled follow-up with a threshold declared in advance. Keep any new value marked as a proposed design value. Assume no live telemetry.

## Reference response

Decision: Test cache reuse before any broader release. The sandbox median fell from 800 ms to 510 ms across 40 runs on one runner. Four of 30 synthetic retrieval queries lacked a relevant result in the first three. Proposed design: Compare cached and uncached runs on the same fixture per query. Set a median latency reduction threshold of 20% before the experiment. Hold the number of missing relevant results at four or fewer on the same 30 queries. Production error rates and live retrieval effects: Not in source.

## Reusable prompt

Prepare a local decision note for `{{owner}}` from `{{verified_sources}}`. State `{{decision}}`. Preserve `{{metrics}}`, `{{units}}` and `{{scope}}`. Propose `{{follow_up}}` with a threshold specified before data collection. Mark each unknown as `Not in source.` Mark each proposed value as a design value. Keep the decision with `{{owner}}`.
