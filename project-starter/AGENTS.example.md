# Repository facts for this task

Replace the bracketed fields with verified facts before use.

## Entry points

- User-facing command: <existing command>
- Core implementation: <file and function>
- Input schema: <file or documented fields>
- Regression checks: <existing command>

## Domain rules

Write only stable rules established by the project owner, code or tests. Put task-specific guesses in TASK.md. For the illustrative retrieval task, current document versions must take precedence over archived versions when the query concerns the current service.

## Verification

Run the smallest check that reproduces the reported defect. After the repair, run that check and the existing checks for affected callers. Record any unrun command and its reason.

## Output

Keep the patch within the named task. Return the final revision, exact commands, observed results and open questions. Use paths relative to the repository.
