# Retrieve current rollback evidence

## Problem

A query for a canary rollback retrieves an archived deployment paragraph. The answer must cite current rollback instructions.

## Inputs

Use three synthetic documents for the first attempt: current rollback, archived deployment and an unrelated current service. Assign a stable document ID, version and status to each.

## Output

Return ranked document IDs and scores through the existing retrieval interface. The caller and response schema stay compatible.

## Acceptance

Use ACCEPTANCE.csv. Confirm the expected result from the document content before you ask an agent to implement a rule.

## Scope

Allowed implementation path: <fill from checkout>.
Existing verification command: <fill from checkout>.
Baseline revision: <fill from checkout>.
Output artifact: <fill relative path>.

## Open question

If two current documents disagree, which system owns the version rule? Resolve that rule before the implementation depends on it.
