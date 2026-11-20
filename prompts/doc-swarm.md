# Doc Swarm (Yan form)

Purpose: split a source set across sub agents, merge to one file.
Inputs: SOURCE LIST file, sub agent instruction file, templates.

MAIN PROMPT:
Read the source list. Split it into <N> near equal chunks.
For each chunk, spawn one sub agent with this message:
You are Agent <NUMBER>. Read the instructions at
<PATH/sub-agent.md> and execute it. Here are the sources
to process: <CHUNK>
Wait for all reports. Then read the part files and merge
into <OUTPUT FILE> in the merge template form.

SUB AGENT RULES (in the instruction file):
Process one source in full before the next. Write each part
to the parts folder in the part template form. Errors return
as text in the part file, never as a silent skip. End with a
completion line: sources done, sources failed, and why.
VERIFY: part count equals source count. The merge names each
failed source in a gaps section.
STOP: a chunk with half its sources failed stops the merge
for a human call.
