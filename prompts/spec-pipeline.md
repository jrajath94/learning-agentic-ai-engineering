# Spec Pipeline (Reed and Osmani form)

Purpose: turn a rough idea into spec.md, prompt_plan.md, and todo.md.
Inputs: IDEA (one paragraph), constraints, definition of done.
Run in a strong chat model first, then a reasoning model.

STEP 1 PROMPT (idea honing):
Ask me one question at a time about the idea below until the idea
is fully specified: user, scope, data, edge cases, and what done
means. Then compile the answers into a developer-ready spec and
save it as spec.md.
IDEA: <paste>

STEP 2 PROMPT (plan):
Read spec.md. Produce prompt_plan.md. Each step is a single prompt
in a code block. Each prompt stands alone: it names the files, the
behavior, and the test for that step. Break each step down twice.
No step may leave code that no later step integrates.

STEP 3 PROMPT (state):
Can you make a todo.md that I can use as a checklist? Be thorough.
One line per plan step, in plan order.

EXECUTION RULE: paste one prompt at a time. Run its test. Check the
todo item. Never paste two steps in one message.
VERIFY: spec holds no open question; plan steps each name a test;
todo count equals plan step count.
STOP: any step that leaves orphan code means the plan is wrong.
Fix the plan, not the code.
