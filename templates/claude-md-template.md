# CLAUDE.md template (Ghostty shape, for a Python service)
# Rule: each line must map to a past agent error or a hard fact.
# Cap: 50 lines. Review each 6 months with an ablation pass.

## Commands
Build: <exact build command>
Test all: <exact test command>
Test one: <targeted test command with filter> (prefer this, full suite is slow)
Lint: <exact lint command>
Format: <exact format command>

## Scoped areas
<Sub area>: build with <variant command>, test with <variant command>
<One portability or platform rule from a real past break>

## Map
Core: <path/>
API: <path/>
Tests: <path/>

## Hard rules
<One prohibition per line. Example: never edit files under migrations/.>
<The log file path and the rule: read the log for sign in links and errors.>
