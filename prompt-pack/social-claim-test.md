# Reproduce one workflow from a post

Attach the original public post, its available caption or transcript, and the linked implementation. Name the access you actually have. A search preview cannot establish actions that occur outside its text.

## Filled experiment

The post proposes parallel agents for a repository change. My task is an inspection export. It selects UTC timestamps strictly before 09:00 and rejects a timestamp without an offset. The baseline and candidate start from the same repository revision. Their acceptance cases, time budget and output format are fixed.

Use A at 08:00 UTC, B at 09:00 UTC and C at 04:30 with offset -04:00. The expected order is A,C. In a separate case, replace C with an offset-free timestamp. Expect a failure with the record ID and no partial output file.

Read the post's artifact. Extract its exact decomposition and identify any omitted step. Map each worker to a distinct output. A discovery worker reads the parser and existing checks. The implementation worker owns the exporter. The reviewer receives the final diff and original fixture. If the post shows simultaneous edits to the same file, describe how its integration resolves collisions or mark that detail unavailable.

Measure the complete attempt from the initial task to an accepted final artifact. Include retries, integration and review. Record all workers' model usage when available. Compare the output through the public command. Report the verdict and one failure that would change it.

## Reusable experiment

- Original source: <URL or local capture>
- Available evidence: <video, transcript, full caption, or preview>
- Observable claim: <specific behavior or measured improvement>
- Source implementation: <repo, file and revision or unavailable>
- Task: <one input and output>
- Baseline: <current method>
- Changed variable: <one mechanism from the post>
- Fixed conditions: <revision, fixtures, tool access, budget and acceptance cases>
- Counterexample: <an input that exposes the claimed mechanism's boundary>
- Measurement: <accepted result, elapsed work, review, and complete usage when reported>
- Stop: <acceptance passes, budget ends or no new hypothesis remains>

Return the source evidence, experiment files, exact commands and observations. Label unexecuted procedures. Keep unsupported details out of the reproduced method. A popularity count belongs in source metadata.
