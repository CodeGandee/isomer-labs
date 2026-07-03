## Why

After a Topic Workspace is fully initialized and research begins, accepted records, runtime rows, generated views, actor-local material, and research state can change in many places. Operators need a durable, agent-readable way to return a Topic Workspace to its post-initialization/pre-research state without relying on Git stash, project-root Git history, or ad hoc filesystem deletion.

## What Changes

- Add structured Topic Workspace reset checkpoints that record the exact post-initialization baseline as structured research/runtime records with generated Markdown review views.
- Add a reset planning surface that compares the current Topic Workspace to a checkpoint and reports which structured records, runtime rows, generated views, and local support surfaces would be preserved, destructively deleted, regenerated, skipped, or blocked.
- Add an explicit reset apply surface that executes an approved plan using structured Workspace Runtime operations and file operations only where they are derived from recorded semantic labels, deleting unpreserved post-checkpoint reset candidates rather than retaining them.
- Treat non-preserved post-checkpoint contents under managed actor and agent workspace roots as reset candidates, so manual and Agent Team support workspaces return to the checkpoint baseline too.
- Update Topic Creator and Topic Manager guidance so `topic.workspace.summary` becomes the operator-owned first checkpoint boundary while ordinary research outputs after the checkpoint are reset candidates.
- Allow later research-preparation skills to explicitly update the reset checkpoint when their preparation should survive a Topic Workspace reset; if they do not update it, their outputs remain post-checkpoint state and must be redone after reset.
- Exclude all Git operations from this change: no project-root Git tracking, no stash use, no branch reset, no commit creation, and no Git ref management.

## Capabilities

### New Capabilities

- `topic-workspace-reset-checkpoints`: Structured checkpoint, reset-plan, and reset-apply behavior for returning a selected Topic Workspace to a recorded post-initialization state without Git operations.

### Modified Capabilities

- None.

## Impact

- Affected code: Workspace Runtime models/schema/store/validation, research record structured artifact formats, `isomer-cli project` command surface, operator skill guidance under `skillset/operator`, and research-preparation guidance that chooses to preserve its own setup across reset.
- Affected APIs: new Python and CLI APIs for checkpoint creation, checkpoint update, reset plan inspection, reset application, and checkpoint listing/showing.
- Affected storage: new topic-scoped Workspace Runtime records for reset checkpoints and reset plans; generated Markdown views remain derived review material.
- Dependencies: no new external service dependency and no Git dependency for reset behavior.
