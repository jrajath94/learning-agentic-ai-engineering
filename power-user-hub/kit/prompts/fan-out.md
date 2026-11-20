# Two tasks, two directories

Provenance: original synthesis. Boris Cherny, 4 Mar 2026, 33:50, uses one checkout per tab. Andrej Karpathy, No Priors, 20 Mar 2026, describes separate checkouts so one functionality does not collide with another.

```text
You are in {{DIR}}. The other task is not in this directory. Do not read {{OTHER_DIR}}.

Task: {{TASK}}
Check: {{TEST_COMMAND}}

Plan the files inside {{DIR}} only. Wait for "go".
After "go", implement and run the check. Paste the exit code.
```

Start a second session with the directories swapped.
