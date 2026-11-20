# Proof Demand (Ball form)

Purpose: replace a status claim with a proof artifact.
Inputs: the change, the claim, the surface.

PROMPT:
Give me irrefutable proof that this works now: <CLAIM>
Set up what you need in a throwaway environment. Return:
1. The exact steps you ran.
2. Screenshots, video, or a test matrix that shows the
   behavior, before and after where a change is claimed.
3. The raw command output for each check.
4. A list of what you did not test.

WAKE FORM (for deploys):
In <TIME>, check again: deploy state, error rates, and the
user visible behavior of <SURFACE>. Report proof or the
defect, with the artifact attached.

VERIFY: a human can re-run step 1 from the report alone.
STOP: proof that rests on the agent own summary text fails.
Artifacts or it did not happen.
