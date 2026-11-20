# Turn a public workflow claim into a test

Input: <original post URL or supplied export>.
Target outcome: <what I want to reproduce>.
Local example: <small fixture or repository>.

Read the original post and every linked artifact needed to understand the claimed result. Record the author, date, product version, observed engagement metric and access gaps. If no metric is visible, write “Not observed”. A repost shares the original source lineage.

Extract the narrow claim and its denominator. Identify the input, actions, output, comparison and acceptance rule. Locate the repository revision, function, prompt or experiment record that supports the claim. Record missing components explicitly.

Find a credible counterexample or failure condition. Explain which assumption differs. Do not turn popularity into technical evidence.

Design a small local experiment with a baseline and one changed variable. Fix the dataset, environment and acceptance rule first. Write expected observations for both success and failure. Report elapsed work and review effort separately if you measure them.

Produce an implementation plan and reusable prompt grounded in those findings. Label any mechanism you infer. Stop if the artifact is unavailable and the claim cannot be tested with supplied evidence.

## Filled example

A post says four agents finish a repository task faster. Define the task as adding a CSV importer with duplicate handling. Compare one agent with four workers on the same revision and fixtures. The four-worker version assigns discovery, implementation, adversarial tests and independent review. Count total completion time, integration fixes, all model usage and human review. Both runs must pass the same acceptance tests. If a helper agent cannot see the fixture, its opinion cannot establish correctness.
