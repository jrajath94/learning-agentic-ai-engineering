# Analyze evaluation errors

## Purpose

Analyze sensor badge benchmark errors.

## Inputs

Full rule shifted scores: 30, 31, 25 correct out of 100 for seeds 7, 19, 43. Sensor-only: 84, 83, 82.

## Constraints

Use error records and metrics.json. Do not claim statistical certainty.

## Output

Report per-seed errors, compare with ordinary split, and identify badge shift as the designed condition.

## Verification

Check full shifted errors equal 70, 69, 75 and sensor-only errors equal 16, 17, 18.

## Stop

Stop if row counts do not equal 100 per seed and split.
