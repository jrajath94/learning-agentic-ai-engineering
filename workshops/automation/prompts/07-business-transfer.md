# Adapt the briefing to a business decision

## Filled prompt

Propose an offline Friday support brief for a team that manages refunds. Use only a synthetic export. One fixture says `Nine of 50 cases exceeded 24 hours.` Its scope is `One region in one week. Escalations excluded.` Preserve case identifier privacy. Give a data contract, allowed side effects, the decision owner and acceptance checks. Keep a customer contact operation outside the tool catalog.

## Reference response

A source contains a stable batch ID, date, title, result and scope. The source contains aggregate counts only. Stage one draft per week and export bytes. Copy the nine cases and denominator of 50 together with the scope. The support lead decides whether to compare other regions. A replay verifies one stage per export. A fixture with a missing denominator produces a manual review item. Contact and refund approval require separate authority.

## Reusable prompt

Adapt the local workflow for `{{business_question}}`. Use `{{safe_fixture}}` with `{{data_contract}}`. Keep `{{protected_fields}}` outside the export. Restrict writes to `{{allowed_effect}}`. Require a decision by `{{owner}}`. Give an exact claim with its denominator and scope. Define tests for duplicates, unavailable data and an attempted call to `{{disallowed_action}}`.
