# Claude Code kit

## Install

```sh
mkdir -p .claude/skills
cp kit/claude/CLAUDE.md CLAUDE.md
cp kit/claude/settings.json .claude/settings.json
cp -R kit/claude/skills/tdd .claude/skills/tdd
```

Edit the `{{PLACEHOLDERS}}` in `CLAUDE.md` and `settings.json` before the first session.

`settings.json` follows the PostToolUse shape Boris Cherny published on 2 Jan 2026 (formatter after Write or Edit). The command is a placeholder. It is not his repo file and has no commit SHA.

`skills/tdd/SKILL.md` is a verbatim copy. See `skills/tdd/PROVENANCE.md` for the SHA.

## Run

Open Claude Code in the repo. For a bug you already understand, use `kit/prompts/tdd-loop.md`. For a review, use `kit/prompts/review.md`.

`kit/scripts/tdd-demo.sh` runs the red-then-green loop with Python, no model, so you can see the failure before the fix.
