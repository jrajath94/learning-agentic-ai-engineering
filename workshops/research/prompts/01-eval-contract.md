# Define the evaluation contract

## Reusable prompt

Write the contract for a comparison before you see the scores.

Inputs

- Task and user decision: <task and decision>
- Output unit and fixed budget: <unit and limit>
- Reference source: <labeled set and owner>
- Cost budget: <candidate count, time, or calls>
- High-impact failures: <list>
- Release rule: <minimum change and guards>

State what evidence qualifies and who assigns the label. Define every numerator and denominator. Give a rule for an empty reference set, a short result list, and a failed run. Specify which version of each input to freeze. Name one claim this experiment can support and one question it leaves open.

Return a table with metric, calculation, population, and threshold. Return a separate paragraph with holdout ownership and a stop rule. Ask for a missing threshold before you assign it.

## Filled example

Compare two manual card retrievers with the same two evidence slots. Grade each positive query by relevant IDs retrieved divided by relevant IDs for recall. Divide relevant IDs retrieved by two for precision. Aggregate the positive cases by the mean of per-query values. Track an empty-label query by whether a card appears. Require a recall gain of at least 1/10, no precision loss, no added false returns, and no new critical misses. Stop after four development candidates. The test owner alone scores the locked choice on a fresh group split.

## Check

Find the denominator for D01 and then for D03. Check that a missing run never counts as a zero precision success.
