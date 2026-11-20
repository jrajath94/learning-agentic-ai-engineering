# Evidence chain
## Source records
### E01: repository and harness practice
### E03: evaluation design
### E07: release comparison
## Local observations
### Invoice service
#### Baseline returns 216 cents for a case that requires 217
### Sensor badge benchmark
#### Full rule scores 290 of 300 ordinary rows
#### Full rule scores 86 of 300 shifted rows
#### Sensor-only rule scores 249 of 300 shifted rows
### Support queue
#### R06 is old but closed
## Bounded recommendations
### Use exact integer rounding for invoice cents
### Test for input shift before relying on the badge
### Filter queue rows by status and age
### Stop at a human review boundary
## Limits
### Synthetic runs do not establish field performance
### A source claim does not prove local impact
