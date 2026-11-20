# Supervisor watcher spec (Mods form, with cost terms)
Trigger: run only after a turn that edited files, ran commands,
or made 8 or more tool calls.
Act: fork the talk. Read the fork. Return a verdict with two
parts: concerns (shortcuts, buried facts, uncommitted work at
risk) and one next step as an action the human can fire.
Cost log: record fires, turns watched, and input tokens per
check, per week.
Worth test: the watcher stays only if it surfaces a fact the
human would have missed, makes a call easier, or lets the
human act with no distraction. Two dead weeks means a rewrite
of the trigger or a cut.
Trust note: the watcher runs with full permissions and is not
sandboxed. Source access is a hard need.
Off switch: one command, tested.
