# Calculate a rank trace

## Reusable prompt

Explain one query from the scorer's inputs to the evidence result.

Inputs

- Query and reference IDs: <query and labels>
- Score rule and tie rule: <rules>
- Candidate cards: <titles and bodies>
- Result slots: <k>

List original query terms. List all added terms and their source rule. For each plausible card, compute title hits, body hits, and rank score. Resolve ties by the stated rule. Then compute the top-k intersection with the reference IDs. Give recall and precision as fractions. Leave recall undefined on an empty reference set.

Return a score table and one trace with retrieved IDs, missed IDs, extra IDs, and both fractions. Keep evidence about rank separate from an inference about user intent.

## Filled example

D01 tokens are kite, feed, blockage. Add jam under the tight aliases. K11 has one body hit and two title hits, for a score of five. K12 has the same score and follows K11 by ID. K01 and K02 each score two. With K11 and K12 in two slots, recall and precision both equal 2/2.

## Check

Run the baseline and combined **explain** commands. Compare the printed tokens, IDs, and fractions to the hand trace.
