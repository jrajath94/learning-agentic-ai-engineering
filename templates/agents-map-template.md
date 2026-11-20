# AGENTS.md as a map (OpenAI harness form)
# Cap near 100 lines. This file points. Docs hold the depth.

## Start here
Architecture and layer order: docs/architecture.md
Design docs index, with a verification state per doc: docs/design/
Quality grades per domain and layer: docs/quality.md
Active plans, with progress and decision logs: docs/plans/active/
Tech debt register: docs/plans/tech-debt.md

## Layer law
Dependencies flow one way: Types -> Config -> Repo -> Service -> Runtime -> UI
Cross cutting parts enter via Providers only.

## Golden principles
Prefer the shared utility package over a hand rolled helper.
No YOLO data probing: validate at the boundary or use the typed SDK.
<Add one principle per repeated drift find.>

## Checks an agent can run
<LogQL or log path for logs> <PromQL or metric path for metrics>
<The one command that proves a change works>
