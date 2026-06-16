# Execplan Package: DeepResearch

## Purpose

Generated operational material for the **DeepResearch** general-purpose autonomous research loop — a
Houmao `loop-pro` tree-loop rooted at the Orchestrator. Derived from `../intention/`; `manifest.toml`
is the authoritative index of this revision. This directory is generated material, not the editable
source of truth.

## Contents

- `manifest.toml`: package index (generated-source posture, plan revision, artifact paths, omissions).
- `specs/`: machine-readable loop contracts (collab/topology, comms, state, workspace).
- `skills/`: generated skill packages installed into agents.
- `agents/`: concrete agent bindings, role prompts, notifier prompts.
- `harness/`: loop-local deterministic command surface — implemented runnable harness (`bin/` + `src/`), with `commands.toml` as the registry surface.
- `docs/`: human support views (README, start-runbook, credentials, publication-quality, research-contract, claude-effort).
