# Label evidence cards

## Reusable prompt

Assign reference document IDs from a fixed corpus.

Inputs

- Corpus and version: <artifact and digest>
- Questions: <rows>
- Relevant evidence rule: <rule>
- Critical question rule: <owner decision>
- Document family field: <field name>

Use only the supplied corpus. Read the body of each plausible source. Include each source that supports the requested fact or procedure. Document the reason for each inclusion. Record hard negatives that share words but fail the evidence rule. Keep a question with no source as a valid empty list. If the question permits conflicting interpretations, flag it for review before you turn it into a scored case.

Return rows with id, group, slice, query, relevant, critical, and reason. Return hard negatives in a separate review table.

## Filled example

For D05, label the query "Kite blockage at exit". Use group "kite", slice "alias", references ["K12"], and critical false. K12 describes the exit path. K11 describes the tray and is a hard negative. For D06, label "moss warranty transfer" with an empty reference list. The Moss cards cover fit, storage, and cleaning.

## Check

Ask a second person to choose reference IDs without access to the first label. Resolve any difference by pointing to the pertinent source language.
