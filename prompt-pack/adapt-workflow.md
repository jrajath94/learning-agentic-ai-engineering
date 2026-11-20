# Adapt one workflow to my repository

Use this prompt after you complete a workshop with its supplied fixtures. Attach the named files before you start.

## My task

Replace these values.
- Repository and revision: <path and commit>
- Observable problem: <one input and its wrong or missing result>
- User who needs the result: <role>
- Allowed output paths: <paths>
- Existing verification command: <command from this repository>
- Available budget: <time, model calls or cost ceiling>

Read the repository instructions and existing entry point. Confirm the named files exist. Follow one representative input from the entry point to the output. Cite function names and data fields. If a domain rule is missing, identify that rule before code changes that depend on it.

Return a transfer table. Each row must map a workshop concept to a concrete file or state field here. Cover the task contract, evidence input, model decision, deterministic validation, persistent state, failure boundary, acceptance test and final human decision. Mark a concept absent when this workflow does not need it.

Choose one change that repairs the observed problem. Preserve the interface used by existing callers. Show the smallest failing test before the patch. Then implement and run the same test, a boundary test, and the existing checks that exercise the changed behavior.

Record the exact revision or file hashes beside each result. Compare the produced artifact with the acceptance criteria. Stop when those criteria pass or when a missing dependency prevents a meaningful test. State unrun checks explicitly.

## Filled task

My internal retrieval helper returns deployment advice from an old manual. The input is “How do I roll back the canary?” The expected evidence is the current rollback section. The current output cites an archived full-deploy section. Allowed edits are the retrieval filter and its tests. Keep the response schema stable. Use one small fixture with a current document, an archived document and a distractor. Accept the change only if the archived document cannot displace the current rollback evidence, and a current unrelated question still retrieves its own document.

The repository path and command are placeholders until the agent inspects my checkout. Do not invent them.
