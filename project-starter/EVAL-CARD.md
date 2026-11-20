# State what this evaluation measures

## Question

Does the change retrieve current evidence for the selected queries?

## Unit

One query with a fixed set of acceptable document IDs.

## Split

Assign document families before choosing development examples. Keep the final evaluation queries out of iterative prompt edits. Record the split rule and dataset hash.

## Metric

Recall at k equals the number of relevant documents in the first k results divided by the number of relevant documents for that query. Define the behavior when a query has zero relevant documents. Also inspect exact document IDs.

## Decision rule

<minimum quality, regression limit and latency or cost condition>

## Error slices

Version conflicts, vocabulary mismatch, no evidence, duplicates and unrelated current documents.

## Limits

A synthetic corpus tests the mechanism. Validate the same cases on approved representative data before making a production claim.
