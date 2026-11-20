# Muse Code kit

No public Muse settings repo was fetched, so this folder has no copied SHA. The commands are from Meta's docs and the 5 Aug 2026 launch post, already cited as C35, C37, and C38.

## Install

```sh
curl -fsSL https://dev.meta.ai/install.sh | bash
muse --version
```

Before the first task, turn Contributor mode off if this repo has code you cannot send for training. The pricing page says subscriptions default to Contributor mode, and that mode permits training on prompts, code, files, context, and responses.

## First task

```text
/plan
{{ONE_BUG_AND_THE_TEST_COMMAND}}
```

Stop at the approval gate. `/grill` is the stress test of that plan. `/goal` is the long run. Do not start `/goal` until the plan names the test.

Headless:

```sh
export META_API_KEY={{KEY}}
muse exec "{{ONE_SENTENCE_AND_THE_TEST}}"
```

Windows: session messaging is unavailable. Workflows are not on every build. Both limits are in the Muse Code docs fetched 2026-11-20.
