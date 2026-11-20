#!/bin/sh
# Checks the kit is present and the local red-green demo still fails then passes.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
need="
claude/CLAUDE.md
claude/settings.json
claude/skills/tdd/SKILL.md
codex/AGENTS.md
codex/config.toml.sample
gemini-antigravity/GEMINI.md
muse/README.md
grok-bot/README.md
prompts/review.md
scripts/tdd-demo.sh
"
for rel in $need; do
  [ -z "$rel" ] && continue
  if [ ! -f "$ROOT/$rel" ]; then
    echo "missing $rel"
    exit 1
  fi
done
echo "kit files present"
sh "$ROOT/scripts/tdd-demo.sh"
