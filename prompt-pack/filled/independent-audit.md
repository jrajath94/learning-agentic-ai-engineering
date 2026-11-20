# Run an independent audit

## Purpose

Audit the queue report count.

## Inputs

Claim: four open requests and three aged-open requests. Source: requests.csv. Draft cites R01, R03, R04, R05 and R04, R01, R05.

## Constraints

Recompute from source fields. Do not use draft totals as input.

## Output

List qualifying rows and check the age threshold is inclusive at seven days.

## Verification

Compare source-derived IDs to both cited sets. Check R06 exclusion.

## Stop

Stop if CSV content differs from the cited source.
