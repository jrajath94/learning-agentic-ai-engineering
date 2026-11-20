# Design a controlled experiment

## Purpose

Test whether badge use causes the shifted accuracy drop.

## Inputs

Use synthetic benchmark, seeds 7, 19, 43; 100 ordinary and 100 shifted test rows per seed.

## Constraints

Fit threshold on training only. Compare full and sensor-only rules on identical rows.

## Output

Pre-register accuracy by split and three seed-level comparisons. Save data, predictions, configuration, and errors. Stop after all three seeds or a fixed compute cap.

## Verification

Verify split isolation, identical test rows, and metric calculation from predictions.

## Stop

Stop if test labels influence fitting or rule selection.
