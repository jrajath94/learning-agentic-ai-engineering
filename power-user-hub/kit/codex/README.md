# Codex kit

## Install

```sh
mkdir -p .codex
cp kit/codex/config.toml.sample .codex/config.toml
cp kit/codex/AGENTS.md AGENTS.md
```

If `gpt-6.1-sol` is not on your account, change `model` to one `codex` lists. The sample page says to do that.

Leave `sandbox_mode` at `read-only` until a task needs writes, then set the narrowest mode you will accept. `approval_policy = "on-request"` matches the sample.

## Run

```sh
codex
```

Paste `kit/prompts/tdd-loop.md` for a bug, or `kit/prompts/review.md` for a diff. Dots, if your plan has them, can start a Codex task. That task spends Codex usage. The chat with the dot does not, per the 29 Sep 2026 launch post.
