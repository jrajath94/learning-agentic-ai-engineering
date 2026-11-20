# Explain Diff (Litt gist structure)

Purpose: one self contained HTML explainer for a code change,
with a quiz gate. Built on the structure of Geoffrey Litt
public explain-diff skill gist.

PROMPT:
Please make me a rich, interactive explanation of the specified
code change: <DIFF OR PR>.
Write with the clarity and flow of Martin Kleppmann.
Structure, in this order:
1. Background: the system around the change. A deep background
   for a beginner first, then a narrow background on the exact
   area the change touches. Explore the code wide first.
2. Intuition: the essence before the detail. Concrete examples
   with toy data. Diagrams in number, from a small set of
   diagram families. No ASCII diagrams.
3. Code: walk the change grouped by idea, in reader order,
   never in file order.
4. Quiz: five questions, medium difficulty, real understanding,
   no gotchas. Each answer gives right or wrong feedback at
   once, with a note on why.
Format: one self contained HTML file, CSS and JS inside, one
long page, section headers, table of contents, no tabs.
Code in pre tags. Save outside the repo with a name that
starts with today date in YYYY-MM-DD- form.
GATE: the human reads the explainer before the raw diff and
passes the quiz before the change ships.
