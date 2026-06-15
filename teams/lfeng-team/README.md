# lfeng-team Workspace

This directory contains a snapshot of the **DeepScientist v1.0** research-automation prototype, extracted for the `lfeng-team` workstream.

## Source

- **Branch:** `origin/v1.0`
- **Commit:** `73a38a3`
- **Commit message:** `Update Houmao-DeepResearch loop`
- **Parent history:** `d900a23` — `Initial commit: DeepScientist v0.1`

These files were introduced on `2026-06-15` by checking out the `origin/v1.0` tree into this workspace.

## What Is Here

The prototype is organized into four top-level folders:

- **`execplan/`** — the core execution system
  - `agents/` — agent profiles and notifier prompts (orchestrator, scout-ideator, analyst, experimenter, reviewer, writer)
  - `harness/` — Python CLI, command envelopes, SQLite records, mail routing, and command catalog
  - `packs/` — adapters for tasks such as figure polish, nature data/figure/polishing, paper-to-PPT, paper plotting, and science packaging
  - `skills/` — DeepResearch event handlers for receipts, self-wakeup, task requests/results, orchestrator ticks, etc.
  - `specs/` — collaboration topology, comms schemas and templates, SQL state schema, invariants, and workspace layout
  - `ops/` — operational assets for running the loop
  - `docs/` — runbooks and reference documentation

- **`intention/`** — high-level loop overview and intent documentation

- **`runs/`** — prepared workspace notes for runs

- **`shared/`** — shared working directories
  - `baseline/` — baseline artifacts
  - `objective/` — objective definitions

## Relationship to Other Branches

- `main` is the current **isomer-labs** project (Pixi-managed Python package, `src/isomer_labs/`, OpenSpec tooling, `AGENTS.md`).
- `origin/v0.1` is the original **DeepScientist v0.1** commit.
- `origin/v1.0` builds on `v0.1` with the Houmao-DeepResearch loop update.

This workspace is a standalone copy of the `v1.0` tree; it does not share Git history with the `main` branch.
