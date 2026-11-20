# Capsule PRD (Reddit Proto form)

Purpose: turn a design frame or a feature ask into a PRD that
an agent can build from in a clean repo.
Inputs: the frame or ask, the design token and component map,
CI and review feedback on past capsules.

PROMPT:
Build a feature capsule for <FEATURE>.
1. Walk the design map: name each token, component, and
   surface this feature touches, with the production match
   for each. Flag each part with no production match.
2. Read the CI and review feedback on the last capsules in
   this area. Fold each repeat note into a rule for this build.
3. Write the PRD: user goal, acceptance criteria in test
   form, detail notes, and links to the source frames.
4. Build in a sibling repo. Keep the production repo clean.
   Return a draft PR with screenshots of each state.
VERIFY: each acceptance item maps to one screenshot or test.
STOP: a part with no production match stops the capsule for
a human call. No invented components.
