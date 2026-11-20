# Copy a contract into one real task

Copy this directory into a temporary task folder outside your production data. Fill TASK.md first. Use AGENTS.example.md only after you adapt its paths and conventions to the destination repository.

1. Record one input and the expected result in TASK.md.
2. Replace the illustrative acceptance rows with your domain rules.
3. Run the existing baseline command and record it in RUN-LOG.jsonl.
4. Save a small checkpoint after a verified milestone.
5. Ask a fresh reviewer to use REVIEW.md against the final revision.

The examples describe a retrieval helper for a deployment manual. They do not describe your employer's systems. Use synthetic documents for the first attempt. Keep actual access policy with the destination repository.

| File | When to use it |
| --- | --- |
| TASK.md | Define one output and its scope |
| ACCEPTANCE.csv | Derive exact test cases |
| AGENTS.example.md | Store stable repository facts |
| CHECKPOINT.md | Resume after an interruption |
| RUN-LOG.jsonl | Record commands and observed outcomes |
| REVIEW.md | Review one final revision |
| EVAL-CARD.md | Explain what a metric measures |
| SOURCE-CARD.md | Connect a claim to original evidence |
| DECISIONS.md | Preserve why one design was chosen |
| BUDGET.json | Set an explicit attempt limit |
| OWNERSHIP.csv | Assign independent outputs |
| RECALL.csv | Reconstruct the idea after a delay |
