# Gas Town Lite (solo form)

Purpose: town discipline with no town software.
Inputs: goal list, worker sessions, one ledger file.

LEDGER FORM (one markdown file):
## <PREFIX>-<NUMBER> <TASK TITLE>
State: open | running | gated | done | killed
Worker: <SESSION NAME>
Gate: <CHECK THAT MUST PASS BEFORE MERGE>
Notes: <ONE LINE, UPDATED AT EACH CHECK IN>

COORDINATOR PROMPT (at each check in):
Read the ledger. For each running task: read the worker last
output, name its state in one word (working, stalled, zombie,
gated), and act by rule: stalled gets one nudge, zombie gets
a restart from the ledger notes, gated waits for the human.
Merges run one at a time, gate first.
Escalation: P0 stop all work. P1 coordinator decides.
P2 log and continue.

VERIFY: the ledger alone can restart any task after a full
session loss.
STOP: two workers on one file means the split was wrong.
Replan the split.
