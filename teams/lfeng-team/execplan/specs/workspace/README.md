# Workspace Specs

## Purpose

Generated workspace contract for the DeepResearch loop: agent work roots, branch/worktree policy,
shared resources, run-artifact layout, and preservation/cleanup rules. Inputs for `prepare-workspace`
(adapted to `houmao-utils-workspace-mgr`). This contract DESCRIBES the layout; it does not create
anything.

## Contents

- `workspace.toml`: the workspace policy (flavor, roots, branches/worktrees, artifacts, per-agent policies, knowledge-pack extension points, preservation, readiness).
