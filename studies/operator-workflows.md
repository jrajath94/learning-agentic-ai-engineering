# Turn a briefing into a verifiable routine

Prepare one local briefing before you set a schedule. Give every claim a source record. Test an interrupted write and a missing source before you let the routine repeat.

## Read the operator workflow

Lauren Tan's November 18 article separates a desired result from the steps it takes to get there. It asks the bot to restate the goal, the process and the operator's decisions before it acts. The appointment example asks which source wins when a message and the booking system disagree. Tan also describes stable identifiers for data across apps and schedules after a process works on demand. [Full article capture](https://www.teapawt.org/poteto/article/2123159537016533493) · [DO04](../sources.html#DO04)

Tan's October 31 guide and follow-up separate scheduled work from event-triggered work. She says to filter events first and warns about triggers that fire too often. Her Tibot post describes a daily or hourly digest, relevance screening, translation and optional account actions. These are reported capabilities. The captures provide neither a coverage test nor an itemized usage record. [DO01](../sources.html#DO01) · [DO02](../sources.html#DO02)

In the release post, Tan describes one bot that requests objections, watches the build and assigns test work. A second bot receives high-priority findings. Tan says she decides whether to include a fix in the current release or defer it. The linked pstack skill makes the test handoff concrete. It asks for the real launch command, a usable state check, a repeatable action and evidence of side effects. [DO03](../sources.html#DO03) · [DO07](../sources.html#DO07)

In the conference transcript, Tan uses the boundary between Electron's main and renderer processes to illustrate an import rule. At 1:11:00 she moves to runtime evidence and feature maps. A report workflow can apply both ideas. Give one component the draft path. Give the checker rules for which fields each source can prove. The timestamp uses the conference livestream clock. [Conference transcript](https://ai.engineer/code/2026/talks/lauren-tan) · [DO05](../sources.html#DO05)

Greg Isenberg's November 11 thread reports a separate bot for each serious project and a twice-daily content pass. A secondary guide points to 31:26 for the content example. The video and its captions did not load. Use the example to choose a testable schedule, and leave the subscription and spending claims open. [DO06](../sources.html#DO06) · [DO08](../sources.html#DO08)

## Set the source rules before you draft

The goal is a release supervisor's one-screen brief before a 16:00 UTC decision. Assume a synthetic workday. The ticket tracker establishes the issue state. The calendar establishes the review time. Chat can flag a conflict for the reviewer. A chat summary has no authority to change either field.

| Source record | Input | Expected treatment |
| --- | --- | --- |
| `tracker:T-17:2` | Ticket T-17 is blocked | Include the blocker and this revision. |
| `chat:91` | A message calls T-17 ready | Keep as a conflict note. |
| `calendar:CL-04:1` | Review is at 16:00 UTC | Include the time and this event revision. |
| `chat:92` | A message says 15:00 UTC | Keep as a conflict note. |
| `chat:93` | A greeting | Drop before any model call. |

Ask the assistant to restate the source rules before it drafts. Check that it assigns each field to the right source. Then run one local dry run with all five rows. The expected brief has two factual claims with two supporting IDs. It can list both conflicts as separate review items. Give the checker the normalized records directly so it can compare each fact with its source.

## Test a retry and a source failure

Set one draft key for the routine and UTC date. Store the source snapshot digest next to the draft. Write to a temporary file and then replace the final file in the same directory. If an earlier attempt committed the same snapshot, return that draft. If the key is already present with changed inputs, return a revision request to the reviewer.

Interrupt the first attempt before the final write. Replay the same snapshot twice. Expect one complete draft. Run again without the calendar and expect a missing-source state with the blocker only. A stale chat timestamp cannot satisfy the calendar check.

A local Python fixture reproduced those results. It accepted two of five input rows, wrote no final draft before the simulated interruption and saved one draft after retry. A changed snapshot went to review. A separate run flagged the missing calendar. The fixture checked local state and claim selection. It did not use a model, live connector or scheduler. [Test record](../data/operator-search-log.json)

From the guide folder, run `python3 studies/operator-fixture.py`. The script includes the five synthetic rows. File replacement assumes one writer. For concurrent calls, use the [SQLite procedure](../workshop-automation.html). <a href="../studies/operator-fixture.py" download>Download the Python fixture</a>

## Adapt this to your next briefing

Choose one recurring decision. Write the two facts the reviewer needs and the source for each. Add one conflict, one irrelevant event and one missing source to your trial. Start with a manual run. Compare its result to your expected claims and record how many items reached the model. Use a scheduled draft only after you can repeat the check. Give the operator one pause control and a short review queue. <a href="prompt-pack/operator-routine.md" download>Download the schedule prompt</a>

## Retrieve from memory

1. Which source can establish the review time?
2. When can a retry reuse a draft?
3. What must the checker see beyond the visible brief?

## Worked answers

1. The calendar event at the recorded revision establishes the review time.
2. Reuse a committed draft when its run key and source digest both match.
3. Check source references, the separate conflict list and the committed file after retry.
