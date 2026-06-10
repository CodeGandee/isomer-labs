# Harness src

## Purpose

Implementation modules for the DeepResearch harness CLI.

## Contents

- `cli.py`: click command groups (state, record, handoff, wakeup, email, findings, claim, evidence, bo, lit, git, experiment, result, metric, render, outline, manuscript, control) + selfcheck.
- `records.py`: schema-validated generic record writer (RECORD_MAP) — the only state write path.
- `db.py`: sqlite connect + init from schema.sql + seed.
- `invariants.py`: runs specs/state/invariants.toml + FK integrity for `state validate`.
- `mail.py`: templated-mail validate/render (jsonschema + jinja2).
- `paths.py`, `envelope.py`: layout + common output envelope.
