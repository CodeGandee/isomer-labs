# Specs

## Purpose

Generated machine-readable contracts for the DeepResearch loop. `collab/collab-overview.md` is the
process-first authority; all other contracts derive from it.

## Contents

- `collab/`: process overview + machine-readable tree-loop topology.
- `comms/`: templated-mail registry, payload schemas, and Markdown renderers.
- `state/`: sqlite control-plane schema, state authority, invariants, seed, and record-apply schemas.
- `workspace/`: workspace policy (roots, branch/worktree, artifacts, preservation).
