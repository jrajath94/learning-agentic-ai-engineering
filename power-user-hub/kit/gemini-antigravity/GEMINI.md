# How to work in this repo

Provenance: original synthesis for a project that is not the Gemini CLI repo.

The shape (purpose, commands, what not to run) follows `GEMINI.md` at the root of https://github.com/google-gemini/gemini-cli commit `addc194f5bc414e7134c2bd6a414a40e1b4cbbed`. That file is the CLI's own build instructions, including `npm run preflight`. Do not paste those commands into an unrelated repo. A verbatim excerpt is in `GEMINI.md.upstream-excerpt`.

- Purpose: {{ONE_SENTENCE}}
- Test: `{{TEST_COMMAND}}`
- Do not run: {{EXPENSIVE_OR_NIGHTLY_COMMANDS}}
- Do not edit: `{{GENERATED_DIR}}`
- A change is done when `{{TEST_COMMAND}}` exits 0.
