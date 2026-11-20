# Fleet Day (Cherny form)

Purpose: run a parallel fleet day with plan mode and proof.
Inputs: task list, repo rule file, verify commands.

SETUP:
1. One worktree or checkout per task. Name tabs by task.
2. Each session starts in plan mode. Prompt:
   Do not write code yet. Plan <TASK>. Name files, steps,
   risks, and the check that proves each step.
3. Review each plan. Edit until the plan reads right.
4. Switch to auto accept. Let the plan one shot the build.
5. End prompt for each session:
   Prove this works. Run <VERIFY COMMAND> and show the output.
   Then run the code simplifier pass on your own diff.

RULES:
- A correction ends with: Update your CLAUDE.md so you don't
  make that mistake again.
- Bugs: paste the report thread, add the word fix, let the
  agent run the repair end to end.
- Long tasks: name a stop limit in turns and a check at end.
VERIFY: each task ends with command output or a screenshot,
never a claim.
STOP: a session that fails its check twice returns to plan mode.
