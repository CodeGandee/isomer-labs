# Topic-local Agent Names and Flat Agent Worktrees

Agent Instance ids remain globally unique runtime identities, but Isomer Labs uses topic-local Agent Names for launch-facing Agent Workspace resolution. The flat default `agent.workspace` binding is `<topic-workspace>/agents/<agent-name>/` under `isomer-default.v1`. Each directory is a Git worktree for an agent-owned branch namespace such as `per-agent/<agent-name>/main`, while Workspace Runtime records bind the topic-local Agent Name to the globally unique Agent Instance id.

## Status

accepted

## Considered Options

- Store Agent Workspaces through `agent.workspace`, with `<topic-workspace>/agents/<agent-name>/` as the default binding.
- Derive Agent Workspace paths from globally unique Agent Instance ids.
- Nest Agent Workspaces under `<topic-workspace>/agents/<agent-team-instance-id>/<agent-instance-id>/`.
- Mirror design-time profile and role structure under `<topic-workspace>/agents/<topic-agent-team-profile-id>/<role-id>/`.
- Scope Agent Workspaces under Run directories.

## Consequences

- Workspace Runtime validation must reject duplicate Agent Instance ids across the Project-level runtime discovery surface.
- Repeated launch attempts and parallel Research Topics rely on Workspace Runtime records for globally unique Agent Instance identity and on topic-local Agent Names for stable per-topic filesystem names.
- Agent Team Instance membership, Run participation, role assignment, task participation, and the Agent Name to Agent Instance binding belong in Workspace Runtime records, not in the Agent Workspace directory hierarchy.
- The Workspace Path Resolver should derive launch-facing Agent Workspace paths from semantic label `agent.workspace`, the selected Topic Workspace, and `agent_name`. Under `isomer-default.v1`, this resolves to `<topic-workspace>/agents/<agent-name>/`. It may report compatibility diagnostics when older material provides only `agent_workspace_ref`.
