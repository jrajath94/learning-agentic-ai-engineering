# Review score slices and counterexamples

## Reusable prompt

Inspect paired case results before you explain an aggregate change.

Inputs

- Baseline and candidate case traces: <paths>
- Group and slice definitions: <fields>
- Critical and no-evidence rules: <contract>
- Fixed budget and baseline threshold: <values>

Check that the traces use identical cases, labels, and slot counts. List positive and empty-reference counts per slice. Compare hit and miss IDs within each pair. Identify one result that explains a gain and one result that challenges the proposed cause. Distinguish behavior in the sample from a prediction about other data.

Return a table with slice, count, baseline, candidate, and paired example ID. Then return the smallest counterexample and the score rule that caused it.

## Filled example

H01 gains two jam references. H03 loses V11 and receives two door gasket cards. Mean recall stays at 2/3 because each query gets one vote. Precision changes from 1/3 to 1/2. The ambiguous alias slice has one case. That case supports a ranking explanation and blocks acceptance under the critical guard.

## Check

Verify that every slice claim includes a case count. Leave the false-return rate unmeasured when the slice has zero empty-reference cases.
