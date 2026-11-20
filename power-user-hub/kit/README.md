# Kit

Drop-in files for the walkthroughs. Placeholders are `{{LIKE_THIS}}`. Fill them before use.

| Path | What it is |
| --- | --- |
| `claude/` | CLAUDE.md, a PostToolUse hook file, and a verbatim TDD skill |
| `codex/` | Sample config keys from OpenAI's docs, plus a short AGENTS.md |
| `gemini-antigravity/` | A project GEMINI.md and the upstream excerpt with its SHA |
| `muse/` | Install and `/plan` steps from Meta's docs. No copied settings repo |
| `grok-bot/` | Permission setup from the 18 Nov 2026 changelog. No copied settings repo |
| `prompts/` | Prompts for the TDD loop, review, and Grok drafts |
| `podcasts/` | Prompts tied to four episodes |
| `scripts/tdd-demo.sh` | Red then green, local Python, no model |
| `scripts/verify.sh` | Checks these files exist, then runs the demo |
| `setup.sh` | Copies the Claude and Codex files into the current repo |

```sh
sh kit/scripts/verify.sh
```

From a repo you are willing to change:

```sh
sh /path/to/power-user-hub/kit/setup.sh
```
