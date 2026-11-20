# Test whether one agent can replace a specialist subagent

## Filled example

Repository: `/work/billing-api` at commit `8bd31ca`.

Task: Check invoice export behavior when the customer has a shipping surcharge.

Current workflow: A main Claude Code session delegates surcharge cases to a `billing-auditor` subagent. The subagent returns a short review.

Candidate workflow: Replace `billing-auditor` with a skill that the main session loads before invoice export work.

Known cases: Use ten fixture requests. Write the expected result before either workflow runs.

| Request | Expected result |
|---|---|
| Shipping surcharge | Include the surcharge once in the invoice total. |
| Valid tax exemption | Apply the exemption and record its certificate ID. |
| Missing address | Reject the export and report the address field. |
| Retry of one export | Return the same invoice ID and create no duplicate. |
| Duplicate invoice event | Keep one ledger entry. |
| Zero-value invoice | Export zero without adding a fee. |
| Currency conversion | Use the fixture exchange rate and retain the source currency. |
| Canceled order | Exclude it from the export. |
| Late fee | Add the fixture fee once and cite its rule ID. |
| Normal invoice | Export the expected amount and invoice ID. |

Runs: Use a fresh session for each case. Run each case twice with each workflow. Keep the code revision, model, tools, temperature setting if exposed, and request text fixed. Do not let either workflow read the expected results.

Score: Record correct answers, omitted constraints, unsupported answers, tool calls, token use when available, and elapsed time. Compare each case. Do not compare only the total score.

Stop rule: Keep the subagent if the skill workflow misses any critical surcharge or tax rule. Keep it if the subagent finds a defect that the skill workflow misses. Accept the skill only if it matches or exceeds the subagent on every critical case and adds no unsupported answer. Stop after twenty runs per workflow. Report the result as inconclusive if either workflow has a missing run or changed input.

## Reusable prompt

Repository and revision: `<path and commit>`

Repeated task: `<observable task and trigger>`

Current specialist subagent: `<prompt file, tools, and output>`

Candidate skill: `<skill file and loading rule>`

Known cases: `<10 fixed requests and expected answers>`

Allowed tools and files: `<paths and read or write limits>`

For each case, start a fresh session. Run both workflows on identical inputs and the same revision. Hide expected answers until scoring. Record per-case correctness, critical omissions, unsupported claims, tool calls, token use if exposed, and elapsed time. Keep runs separate. Do not change the prompt, fixture, checker, or model during this comparison.

Stop when the fixed run limit is reached, a critical case fails, or an input changes. Accept the candidate only if it passes every critical case and does not add unsupported answers. Report each case and each run. Do not infer general quality from one total score.
