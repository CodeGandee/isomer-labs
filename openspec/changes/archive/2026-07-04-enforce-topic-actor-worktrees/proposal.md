## Why

Topic Actor Workspaces are intended to be Git worktrees of `topic.repos.main`, but existing actor directories can be treated as ready without proving that Git relationship. This leaves manually launched actors without the same repository content, guidance files, branch isolation, and verification behavior expected from formal Agent Workspaces.

## What Changes

- Require Topic Actor Workspace materialization and diagnostics to validate that each selected `topic.actors.workspace` is a worktree of the resolved `topic.repos.main`.
- Treat an existing path that is not the expected worktree as a blocker instead of silently accepting it.
- Keep the default actor branch namespace as `per-topic-actor/<topic-actor-name>/main`.
- Clarify that Topic Actors and formal Agents differ by controller and launch path, not by whether their workspaces are Git worktrees of topic-main.
- Require actor setup and onboarding readiness to include worktree evidence before claiming actor readiness.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `topic-manager-skill`: Tighten actor materialization, repair, and diagnostics so existing actor workspace paths must be validated as the expected topic-main worktree.
- `topic-creator-skill`: Require `setup-actors` to consume actor worktree readiness evidence before reporting actor readiness.
- `manual-research-topic-workflow`: Clarify that manually controlled Topic Actors receive topic-main worktree workspaces, with launch provenance as the actor/agent distinction.
- `topic-workspace-manifest`: Require actor workspace metadata and validation to distinguish matching worktrees from non-worktree path collisions.

## Impact

- Affected code: `src/isomer_labs/workspace/actors.py` and any CLI surfaces used by `project topic-actors ...` diagnostics or materialization.
- Affected skills: Topic Manager actor setup and verification references, Topic Creator actor setup references, and any actor onboarding text that describes the actor cwd.
- Affected behavior: previously created plain actor directories may become blocked until migrated, removed, or replaced by a valid topic-main worktree.
