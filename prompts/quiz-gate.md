# Quiz Gate (Litt usage rule form)

Purpose: gate a merge or a ship on real understanding.
Inputs: the explainer page for the change (see explain-diff).

FLOW:
1. The reviewer reads the explainer, not the raw diff.
2. The reviewer answers the five quiz questions in writing,
   with no source open.
3. Score: 5 of 5 ships. 4 of 5: the missed area gets a
   re-read of that explainer section and a retest.
   3 or under: the explainer is wrong or thin. Fix the
   explainer first, then retest.
4. Log the score next to the change record.

AUTHOR RULE (for the explainer writer):
Questions test the change: why it exists, what breaks
without it, the data path, the edge case, and the rollback.
No gotchas. Each wrong answer in the key names the trap it
tests.
VERIFY: scores exist for the last ten changes.
STOP: a change with no explainer gets no quiz and no ship,
unless the human waives in writing in the change record.
