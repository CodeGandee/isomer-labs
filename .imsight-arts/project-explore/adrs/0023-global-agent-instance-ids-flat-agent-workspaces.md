# Global Agent Instance ids and Flat Agent Workspaces

Agent Instance ids are globally unique by design, so Isomer Labs will use the flat default Agent Workspace layout `<topic-workspace>/agents/<agent-instance-id>/` inside each Topic Workspace. This avoids nesting Agent Workspaces under Agent Team Instance ids while still allowing Workspace Runtime to validate that each Agent Workspace belongs to exactly one Agent Instance and that each Agent Instance participates in the appropriate Agent Team Instance, Run, and Research Task records.

## Status

accepted

## Considered Options

- Store Agent Workspaces directly under `<topic-workspace>/agents/<agent-instance-id>/`.
- Nest Agent Workspaces under `<topic-workspace>/agents/<agent-team-instance-id>/<agent-instance-id>/`.
- Mirror design-time profile and role structure under `<topic-workspace>/agents/<topic-agent-team-profile-id>/<role-id>/`.
- Scope Agent Workspaces under Run directories.

## Consequences

- Workspace Runtime validation must reject duplicate Agent Instance ids across the Project-level runtime discovery surface.
- Repeated or parallel Agent Team Instances rely on globally unique Agent Instance ids rather than path nesting to avoid Agent Workspace collisions.
- Agent Team Instance membership, Run participation, role assignment, and task participation belong in Workspace Runtime records, not in the Agent Workspace directory hierarchy.
- The Workspace Path Resolver should derive the default Agent Workspace path from the selected Topic Workspace and Agent Instance id as `<topic-workspace>/agents/<agent-instance-id>/`.
