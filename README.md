# Agentic AI engineering craft edition

Extract the complete archive and open [index.html](index.html). The guide includes worked projects, source-code studies, prompt files, fixtures, exercises and recorded failures. The rendered pages, diagrams, search, fonts and practice controls work offline.

## Complete one project

- [Repository to reviewed patch](workshop-engineering.html) follows an overcounted trace through a contract, failing tests, a first patch, independent review and final integration.
- [Retrieval and evaluation](workshop-research.html) traces exact retrieval scores, a fixed candidate budget, leakage and a held-out rejection.
- [Durable tool workflows](workshop-automation.html) validates evidence, commits a briefing and tests retries around real process crashes.
- [Adapt a workflow](workflow-kit.html) provides editable task contracts, prompts, checkpoints, review records and a transfer routine.

Use Python 3.10 or later and Git 2.28 or later. The local programs use the Python standard library. The manual shell examples use macOS Terminal, Linux or WSL. From the directory that contains `index.html`, run:

```sh
python3 -B scripts/replay-workshops.py workshop-output
```

Use a new output directory. The runner checks intentional failures and expected successful results. It records commands, exit statuses and output artifacts. The local fixtures are synthetic. Optional live-agent handoffs require your chosen agent and its access.

## Read the implementations

[Source studies](resource-study.html) include ten guided reads with function pointers, paper traces, counterexamples, exercises and worked answers. [Community practice](community.html) connects selected Reddit, X, Substack and GitHub examples to testable methods. [The search record](data/community-search-log.json) states observed engagement, ranking windows and access gaps.

[Recorded runs](run-viewer.html) shows the actual workshop outputs. Three browser screenshots appear beside the relevant lesson steps. [From posts to practice](social-practice.html) records the Instagram, Threads and TikTok search and turns available evidence into bounded experiments.

The [source coverage map](studies/coverage.json) maps the original 131 records to study exercises or reference use. The [source library](sources.html) adds source locations for the deeper reads. The evidence cutoff is November 20, 2026.

## Use the files

| Directory | Contents |
| --- | --- |
| `workshops/` | Programs, fixtures, prompts, Mermaid sources and recorded results |
| `prompt-pack/` | Reusable contracts, filled examples and adaptation prompts |
| `project-starter/` | Task, acceptance, review, budget and checkpoint templates |
| `studies/` | Editable study guides, diagrams and source coverage |
| `fragments/` | Editable chapter HTML |
| `data/` | Source records, diagram placement and verification |
| `assets/` | Local fonts, diagrams, search index and scripts |

## Rebuild the edition

The generated HTML uses local assets. Rebuild chapter HTML with Python:

```sh
python3 -B scripts/build.py
python3 -B scripts/verify.py
```

If you edit the study Markdown, run `python3 -B scripts/build-studies.py` first. That authoring step needs Pandoc. If you edit Mermaid sources, use `scripts/render-diagrams.py` with an installed Mermaid CLI. These authoring dependencies are optional for reading and running the supplied edition.

The [audit](audit.html) records verification and its scope. Font licenses remain in `assets/fonts/`. Original external source material retains its own terms.
