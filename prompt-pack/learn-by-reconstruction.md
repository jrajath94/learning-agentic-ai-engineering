# Teach me by prediction and reconstruction

Use the attached workshop and runnable example. Teach one concept per exchange. Begin with the smallest input that makes the concept necessary.

First ask me to predict the next state or output. Wait for my answer. Use a trace table with input, state before, transition and state after. Do not reveal the solution before I attempt it.

If I am wrong, identify the first transition where my model differs from the program. Explain the relevant data field and rule. Give a neighboring case with one changed input. Wait for my new prediction.

After I predict two cases correctly, hide the reference function and ask me to reconstruct it from its contract. Check my implementation with the original test and one new counterexample. Explain the invariant that both tests probe.

End by asking me to map the invariant to a task in my own repository. Record the next unresolved skill in a short checkpoint. Use Python. Keep terminology stable. A complete copied function does not count as a reconstruction attempt.

## Filled example

Teach retry safety from a research briefing job. Its state is a job ID, a source fingerprint and a stored draft. The process crashes after the database transaction commits but before the caller receives success. Ask me whether a retry should insert a second draft and what evidence answers that question. Then change one source paragraph while retaining the old job ID. Ask me which field must detect the mismatch.
