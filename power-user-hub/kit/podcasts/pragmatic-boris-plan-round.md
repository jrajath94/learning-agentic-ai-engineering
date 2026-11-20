# Plan, then the next tab

Provenance: original synthesis from Boris Cherny on The Pragmatic Engineer, 4 Mar 2026, about 33:50 to 38:15 and 42:19 to 45:59. Transcript mirror: https://sozai.app/transcript/building-claude-code-boris-cherny/ and the same timestamps on https://www.usetranscribe.io/yt/julbw1JuAz0/claude-code-ai-impact. He said there is no single correct workflow. Do not treat this file as his config.

## When to use

You already know this repo. You have two to five tasks that do not edit the same files.

## Prompt

```text
Repo: {{REPO_PATH}}
Task: {{ONE_SENTENCE_TASK}}
Done when: {{FAILING_TEST_OR_COMMAND}}

Stay in plan mode. Do not edit files.

Read the repo. Name the files you would change and the files you would not touch.
Write the plan as numbered steps. Each step names a file and the check that proves that step.
Stop and wait.

If I reply "go", implement only that plan.
After the edit, run: {{FAILING_TEST_OR_COMMAND}}
Paste the command and the last 20 lines of output.
If the check fails, stop. Do not widen the change.
```

## How he said he runs several

Start this prompt in tab 1. While it plans, start the same shape in tab 2 on a different task. He uses Shift+Tab twice for plan mode in the terminal. Overflow goes to the desktop app, which sets up git worktrees so he does not have to run `git worktree` himself. Phone sessions run in the cloud and need a SessionStart hook to configure the environment. He did not paste that hook on this episode.

## Self-check

The plan names files before any diff exists. The test command is one you ran yourself, not a sentence from the model. A second person, or a second session that did not see the implementation chat, reviews the diff. He said their CI review catches about 80 percent of bugs and a person still approves.
