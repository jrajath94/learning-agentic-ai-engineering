# Repo rules for Codex

Provenance: original synthesis. The chain (global file, then one file per directory, closer file later, 32 KiB default cap) is the behavior Mert Ozen checked against OpenAI's docs for CLI 0.169.0 on 15 Nov 2026. The 32768 byte cap also appears in the official sample config fetched 2026-11-20.

- Test with `{{TEST_COMMAND}}`.
- Do not edit `{{GENERATED_DIR}}`.
- Done means the test command exits 0 and a person has read `git diff`.
- Do not read `{{SECRET_DIR}}`.
