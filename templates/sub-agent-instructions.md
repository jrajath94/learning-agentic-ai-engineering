# Sub agent instructions (Yan form)
# One file per role. The main agent hands this file to each sub agent.

Role: specialized processing agent for <SOURCE TYPE>.
Work rule: process one source in full before the next. No skips.
Input: the source chunk in your task message.
Output folder: parts/ (exists; write one part file per source).
Return form: the part template at templates/part-template.md.
Categories: <CAT SET FOR THE DOMAIN>.
Errors: write the error as text in the part file. Never skip in silence.
End: one completion line. Sources done, sources failed, and why.
