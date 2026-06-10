# Harness

## Purpose

The loop-local deterministic command surface for the DeepResearch loop: state/record bookkeeping,
control, comms rendering, findings/claims, self-wakeup + handoff ledgers, BO refiner, literature,
git, manuscript validators, and the domain-pluggable experiment/render commands. Agents reach state
only through these commands.

## Contents

- `commands.toml`: the command registry (authoritative surface; tier core vs domain-pluggable extension).
- `bin/`, `src/`: command wrappers + implementation — **pending implementation** (see manifest `omitted_default_layers`).
- `schemas/command-envelope.schema.json`: harness-owned command envelope — pending implementation.
