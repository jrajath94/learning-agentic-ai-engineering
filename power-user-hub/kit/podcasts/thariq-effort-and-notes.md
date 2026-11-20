# Effort by task, plus implementation notes

Provenance: original synthesis from Thariq Shihipar on Latent Space, 28 Sep 2026. Quotes at 00:21:52, 00:25:24, 00:26:01, and 00:28:10. Page: https://latent.space/p/thariq/

He said code review and security should be high or max effort, and UI low or medium. He said most failures at high effort are the model considering the right fix and then not doing it. He said a new project might be better with no CLAUDE.md until a failure repeats, and that those lines change per model.

## Prompt

```text
Task type: {{review | security | api | ui}}
Repo: {{REPO_PATH}}
Change or question: {{WHAT_CHANGED}}

Set effort from the task type:
- review or security: high
- API or edge cases: medium
- UI layout: low

Do not edit yet.

1. Restate the goal in one sentence.
2. List the checks you would run. Use commands that already exist in this repo.
3. Write implementation notes: options you considered and the one you would not take, with the reason.
4. Stop.

If I reply "do the rejected option" or "go", implement only that, then run the checks and paste the output.
If a mistake shows up a second time in this repo, add one line to CLAUDE.md or AGENTS.md naming the mistake and the check. Do not add a line for a one-off.
```

## Self-check

The notes include a fix the model almost skipped. You can point at that line and tell it to do that fix. If the only output is "looks good", the prompt failed.
