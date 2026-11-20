# Audit a split

## Reusable prompt

Check whether a development split and a held-out split measure new questions or new source families.

Inputs

- Development case manifest: <path or table>
- Held-out case manifest for the test owner: <path or table>
- Provenance map: <document family, copy, translation and revision>
- Index visibility rule: <same index or new-source test>

Compute intersections of query IDs, family IDs, and reference IDs. Check known paraphrases and linked revisions. If an overlap exists, report the smallest pair that proves it. If corpus visibility contradicts the test goal, name the misleading claim. Read the minimum fields needed. Keep held-out contents outside the candidate input.

Return the scope, case counts, overlap evidence, and pass or fail. List what the audit cannot detect from the supplied manifests.

## Filled example

Run the workshop audit for dev.json and leaky-holdout.json. Fail. LEAK-1 has a distinct ID, but it overlaps D05 in the Kite family and K12 reference. For the normal split, report six development and three held-out queries with disjoint source families and reference IDs. All corpus cards stay visible in both comparisons. Interpret the test as new questions over an existing index.

## Check

The deliberate leak must fail when query IDs alone look unique.
