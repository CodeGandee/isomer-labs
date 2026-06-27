## Why

The current Topic Workspace design still spreads worker-facing Isomer material across top-level `repos/topic-main/*` directories and a separate `.isomer-agent/` support area, which makes existing repositories look more fictional than they need to and leaves no clear channel for large peer-readable artifacts that should not be committed before other agents can inspect them. We need a single `topic-main/isomer-managed/` namespace that separates Git-tracked Isomer injections, untracked agent-owned sharing, and untracked topic-owned sharing while keeping worker agents launched inside their own Git worktrees.

## What Changes

- **BREAKING**: Replace the current `.isomer-agent/` support-root convention with `isomer-managed/` inside each `topic-main` worktree.
- **BREAKING**: Move Isomer-specific worker-facing collaboration directories from top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` into `repos/topic-main/isomer-managed/...` so existing repositories keep their native top-level shape.
- Define three `isomer-managed/` regimes: Git-tracked Isomer-injected material, untracked agent-owned peer-readable material, and untracked topic-owned shared material with read-only or writable policy.
- Add an owner/reader contract for agent-owned large or temporary share material: the current agent owns its local share, peer agents read it through generated links or explicit paths, and writes by readers are diagnostics unless a policy grants them.
- Add topic-owned non-Git shared surfaces that can be exposed into agent worktrees without committing large files, including read-only surfaces and writable shared drop zones.
- Keep Git branch exchange as the primary collaboration channel, use untracked `isomer-managed/` sharing for large or temporary peer-visible material, and keep topic-owned Pixi tasks as the explicit tool/API channel.
- Update path resolution, Workspace Runtime records, topic workspace manager skill guidance, documentation, and lifecycle metadata to use the new namespace and to detect legacy `.isomer-agent/` or top-level collaboration paths.

## Capabilities

### New Capabilities

- `isomer-managed-sharing-layout`: Defines the canonical `topic-main/isomer-managed/` worker-facing namespace, its tracked and untracked regimes, agent-owned share contract, topic-owned share contract, generated-link policy, and legacy diagnostics.

### Modified Capabilities

- `workspace-path-resolution`: Resolve and record `isomer-managed/` path surfaces instead of `.isomer-agent/` support paths or top-level `topic-main` collaboration directories.
- `workspace-runtime-persistence`: Persist Agent Workspace metadata, path plans, validation issues, and runtime initialization expectations for `isomer-managed/` surfaces.
- `topic-workspace-manager-skill`: Prepare and validate `repos/topic-main/isomer-managed/`, per-agent worktrees, generated links, ignore policy, branch ownership, and conflict diagnostics.
- `topic-team-specialization-module-skill`: Ensure `setup-agent-workspace` delegates to the topic workspace manager for the new layout and reports `isomer-managed/` evidence.
- `research-lifecycle-state`: Record Agent Workspace worktree metadata against `isomer-managed/` boundaries rather than `.isomer-agent/` support boundaries.
- `isomer-documentation-system-guide`: Update docs to describe the standardized `isomer-managed/` layout, worker visibility boundary, and migration guidance.

## Impact

This affects `docs/topic-workspace-definition.md`, selected system docs, the canonical domain-language notes, `src/isomer_labs/paths.py`, runtime/path-plan data structures, validation diagnostics, unit tests around path surfaces and skill validation, `skillset/operator/isomer-admin-topic-workspace-mgr`, and `skillset/operator/isomer-admin-topic-team-specialize/references/setup-agent-workspace.md`. It does not add external dependencies, change the rule that agents launch with `agents/<agent-name>` as cwd, or claim filesystem-grade isolation.
