# Block npm in a PreToolUse hook

Provenance: Matt Pocock, 25 Feb 2026, https://www.youtube.com/watch?v=3CSi8QAoN-s, 00:04:02 to 00:04:37. He described the script. This is not a copy of block npm.sh from his repo.

Spoken contract:

- Event: PreToolUse, any bash tool, in settings.json.
- If the command starts with npm, echo `use pnpm not npm` and exit 2.
- Otherwise let it run.
- Make the script executable with chmod +x.

Use this only in a repo whose package manager is pnpm. A repo that uses npm should not get this hook.
