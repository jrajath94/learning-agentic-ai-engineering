#!/bin/sh
# Copy Claude and Codex starter files into the current repo.
# An existing destination is skipped. The script continues with the next file.
set -eu
KIT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
DEST=${1:-.}
copy() {
  src=$1
  dst=$2
  if [ -e "$DEST/$dst" ]; then
    echo "skip $dst (already exists)"
    return
  fi
  mkdir -p "$DEST/$(dirname "$dst")"
  cp "$src" "$DEST/$dst"
  echo "wrote $dst"
}
copy "$KIT/claude/CLAUDE.md" CLAUDE.md
copy "$KIT/claude/settings.json" .claude/settings.json
copy "$KIT/claude/skills/tdd/SKILL.md" .claude/skills/tdd/SKILL.md
copy "$KIT/codex/AGENTS.md" AGENTS.md
copy "$KIT/codex/config.toml.sample" .codex/config.toml
echo "Edit the {{PLACEHOLDERS}} before you start an agent."
