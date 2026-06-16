# Harness

## Purpose

The loop-local deterministic command surface for the DeepResearch loop: state/record bookkeeping,
control, comms rendering, findings/claims, self-wakeup + handoff ledgers, BO refiner, literature,
git, manuscript validators, and the domain-pluggable experiment/render commands. Agents reach state
only through these commands.

## Contents

- `commands.toml`: the command registry (authoritative surface; tier core vs domain-pluggable extension).
- `bin/deepresearch`, `src/`: the runnable harness entrypoint + implementation (click CLI in `src/cli.py`; `db.py`/`records.py`/`invariants.py`/`mail.py`/`paths.py`/`envelope.py`). **Implemented.**
- `schemas/command-envelope.schema.json`: harness-owned command envelope. **Implemented.**
- `tests/`: harness unit tests.
