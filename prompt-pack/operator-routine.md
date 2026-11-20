# Prepare a briefing routine

Replace the bracketed fields before use. First ask the assistant to produce the contract and manual trial plan. Configure a schedule only after you approve the trial result.

## Prompt

Prepare a draft briefing for [decision and reviewer]. Use only [named read-only sources]. Return a result by [UTC time and timezone rule].

Restate the goal and the workflow before you act. Make a table of each required fact, its authoritative source and the check for it. Resolve conflicts by the declared authority. Keep unresolved conflicts in a separate review list. Label any missing source.

Use these event filters [filters]. Drop irrelevant events before you call a model. Preserve each accepted source ID and revision. Keep the source time window [window]. Ask for the missing rule if the source or time window is ambiguous.

Use a stable run key [routine ID and scheduled date]. Save the source snapshot digest with the draft. Reuse a committed draft with the same key and digest. Return changed inputs to review when the same key already has a draft.

Write one local draft and one check receipt. Include factual claims, source references, unresolved conflicts and counts before and after the filter. Run the following trials [normal, conflict, missing source, repeat and interrupted write]. Report observed output for each trial.

Keep publication, messages and account actions outside the draft workflow. Stop before schedule setup until I approve the trigger, scope, review destination and pause control.

## Filled example

Prepare the daily release briefing for the operator. Use the local ticket tracker export for ticket state and the calendar export for the launch review time. A chat note can supply a conflict flag. Require T-17 at revision 2 to appear as blocked. Require the calendar review at 16:00 UTC. Drop greetings. Keep X, email and publishing tools outside the task.

Use one draft key per UTC date. Run a normal fixture and one with the calendar missing. Simulate interruption before the final write. Repeat the exact input twice. Require one draft and report the accepted source IDs. Route a changed snapshot with the same key to the operator.

After approval, propose a draft-only run at 09:00 UTC on workdays. Name the review destination and the control that pauses the routine. Keep recurrence disabled until the operator approves that proposal.
