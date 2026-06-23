# Design: Globally Unique Agent Instance ids

## Context

ADR 0023 accepted that Agent Instance ids are globally unique by design and that Agent Workspaces use the flat layout `<topic-workspace>/agents/<agent-instance-id>/`. The current implementation in `src/isomer_labs/runtime/store.py` generates ids as `{team_id}-{role_slug}`, which is only unique within one Agent Team Instance. Tests and profile fixtures still reference the old placeholder `agent-workspaces/<profile>/<role>` layout. This design closes that gap.

## Goals / Non-Goals

**Goals:**
- Make every Agent Instance id globally unique within a Project.
- Derive every default Agent Workspace path from the globally unique Agent Instance id.
- Add Workspace Runtime validation that rejects duplicate Agent Instance ids across the Project.
- Update tests and fixtures to remove stale placeholder workspace paths.
- Keep Agent Workspace directory layout flat under `<topic-workspace>/agents/`.

**Non-Goals:**
- Changing the Topic Workspace layout or runtime directory set.
- Adding filesystem-level access control for Agent Workspaces.
- Changing Houmao adapter manifests or launch material structure.
- Reintroducing nested `agent-workspaces/<profile>/<role>` directories.

## Decisions

1. **Use a deterministic global id with embedded team and role context.**
   Agent Instance ids will be generated as `agent-<uuid>` or a deterministic slug that includes a project-scoped counter. The chosen form is `agent-<topic-workspace-id>-<team-instance-counter>-<role-slug>-<uuid-short>` so that directories remain readable while still being globally unique. This satisfies ADR 0023 without losing human inspectability.

2. **Generate ids inside `WorkspaceRuntimeStore.create_agent_team_instance`.**
   The store already has access to the Topic Workspace and Agent Team Instance context. It will generate ids there and pass them into `AgentInstanceRecord` and the Agent Workspace path plan.

3. **Record path plans before creating directories.**
   The existing `record_path_plan` call already runs before `mkdir`. This ordering stays the same; only the surface name and path change.

4. **Validate uniqueness at creation time and in `runtime validate`.**
   At creation, the store checks `agent_instances` for an existing id before inserting. During validation, a new check scans all Topic Workspaces in the Project for duplicate Agent Instance ids and reports them as workspace issues.

5. **Update tests only where fixtures reference stale paths.**
   The `agent_workspace_ref` field in test profile fixtures is a placeholder and can be removed or updated to the new default. Assertions that inspect workspace paths must expect the new flat layout.

## Risks / Trade-offs

- [Risk] Existing tests may encode the old `{team_id}-{role}` id shape. → Mitigation: update test fixtures and assertions as part of this change; no production migration is needed because no Agent Team Instances have been launched in production.
- [Risk] Long ids make directory names harder to read in file explorers. → Mitigation: include a short role slug and team counter in the id; the uuid component is truncated to 8 characters.
- [Risk] Future adapters may assume role-derived ids. → Mitigation: adapters receive Agent Instance records via Workspace Runtime and should use the `id` field, not derive ids from role names.

## Migration Plan

No runtime migration is required. This change affects only new Agent Team Instance creation. Existing records in test databases are recreated by tests.

## Open Questions

- Should the global id include the Agent Team Instance id verbatim, or only a counter? The chosen design uses a counter for brevity.
- Should profile fixtures retain `agent_workspace_ref` as an explicit override, or remove it and rely on the default? The chosen design removes stale explicit overrides and lets the resolver use the default.
