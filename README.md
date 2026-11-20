# Learning Agentic AI Engineering

Open **[index.html](index.html)** after you extract the complete branch archive. The guide runs directly from disk. Navigation, search, diagrams, folding maps, fonts, and the local labs work offline.

## Start with one result

Use Python 3.10 or later. From the directory that contains `index.html`, run:

```sh
python3 -B labs/replay.py lab-output
```

Use a fresh output path. The original service must fail its regression check. The repaired service, benchmark, and report workflow must pass. Read the [worked labs](labs.html) beside the [recorded observations](labs/evidence/runs.json).

## Read or maintain the edition

- [Learning paths](paths.html) connect short sessions to a concrete artifact.
- [Researcher usage](usage.html) explains the published figures and includes an interactive token budget.
- [Field notes](fieldnotes.html) connect practitioner posts and podcasts to code, experiments, and review decisions.
- [Product index](products.html) records versions, interfaces, and access limits.
- [Source library](sources.html) distinguishes public claims and evidence limits.
- [Audit](audit.html) records the scope, repairs, and verification.
- The files in `fragments/` contain editable chapters. `data/` holds source records and figure placement. `assets/` contains the local fonts, diagrams, Mermaid files, and Markdown for the maps.

Rebuild the HTML and local search index after you edit a chapter:

```sh
python3 -B scripts/build.py
python3 -B scripts/verify.py
```

The font licenses are in `assets/fonts/`. External source material remains subject to its original terms. The published-source cutoff and local experiment date are November 20, 2026. Live accounts, deployment, customer contact, and paid API calls are outside the lab runs.

