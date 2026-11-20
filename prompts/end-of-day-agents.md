# End of Day Agents (Hashimoto form)

Purpose: end the day with agents that hand you a warm start.
Inputs: today project list, open issues, one vague idea.
Time box: 30 minutes. Reports only. No public replies by agents.

PROMPT A (survey), one per option:
Survey <LIBRARY OR OPTION> for <USE>. Return: what it does,
pros, cons, recent activity, license, community sentiment,
and a fit call for our stack with one reason. Cite sources.

PROMPT B (probe), one per vague idea:
Attempt <IDEA> as a throwaway spike in a scratch folder.
Goal is light, not a ship. Return: what worked, what broke,
the shape of a real build, and a kill or keep call.

PROMPT C (triage), via the gh CLI:
Read open issues and PRs for <REPO>. Return a report only:
group by theme, flag near certain agent wins, name the human
only items, and draft no public text.

MORNING RULE: filter reports to slam dunks. Run one win at a
time in the background. Notifications off. Check at breaks.
VERIFY: each report names sources and a call. No agent posted
in public.
STOP: a probe that needs a design call stops and reports.
