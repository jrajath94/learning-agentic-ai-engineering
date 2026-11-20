# Record a fact only after the command succeeds

Provenance: original synthesis from Practical AI episode 352, 9 Apr 2026, hosts Chris and Daniel, about 23:09 to 23:40. Transcript: https://practicalai.show/352/transcript

They were describing memory behavior they said was visible in the Claude Code source leak the day before. This file does not copy that source. It uses only the rule they stated in public: do not write "I ran the test" into memory unless the terminal shows the test ran.

## Prompt

```text
Task: {{TASK}}
Check: {{COMMAND}}

Run the check.
If the exit code is not 0, write nothing to CLAUDE.md, AGENTS.md, or any memory file.
Paste the exit code and the last 30 lines.

Only if the exit code is 0, append this single line to {{MEMORY_FILE}}:

{{DATE}} {{COMMAND}} exit 0

Do not write a summary of what you intended to do.
Do not mark a file as created unless `ls` on that path succeeds in the same turn.
```

## Self-check

The memory line appears only next to a command you can re-run. A failed command leaves the memory file unchanged. `git diff` shows no other edits.
