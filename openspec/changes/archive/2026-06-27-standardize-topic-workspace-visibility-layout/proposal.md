## Why

The current contracts mix worker-visible collaboration files with topic-owner runtime records at the Topic Workspace root: specs and code still default to root `artifacts/`, `tasks/`, `runs/`, `views/`, `logs/`, and fallback Agent Workspace paths based on `agent-instance-id`, while newer docs and skills are moving toward `repos/topic-main` plus per-agent Git worktrees. This change standardizes the Topic Workspace layout before more skills, fixtures, runtime records, and Houmao launch behavior build on contradictory path semantics.

## What Changes

- Add a canonical Topic Workspace visibility layout: worker-facing collaboration lives in `repos/topic-main` and per-agent worktrees under `agents/<agent-name>`, while topic-owner preserved records live under root `records/` and runtime internals live under root `runtime/`.
- **BREAKING**: Stop treating root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, and `logs/` as normal worker-visible Topic Workspace surfaces; worker-visible variants move under `repos/topic-main/`.
- **BREAKING**: Standardize per-agent directories as `<topic-workspace>/agents/<agent-name>` Git worktrees on agent-owned branches, rather than defaulting to `<topic-workspace>/agents/<agent-instance-id>` or operator-authored arbitrary `agent_workspace_ref` paths.
- Define the branch language: `topic-owner/main` is the owner-managed topic branch, `per-agent/<agent-name>/main` is the default worker branch, and future per-agent branches stay under `per-agent/<agent-name>/`.
- Make inter-agent communication order explicit: Git operations across `topic-main` worktrees are primary, symlinked shared directories are secondary, and topic-owned Pixi tasks or APIs are the principled tool-mediated channel.
- Revise runtime and path-resolution contracts so path plans record `repos/topic-main`, `agents/`, `records/*`, and runtime internals, and so generated run/task/artifact/view/log records outside `topic-main` are owner-preserved records, not worker collaboration directories.
- Revise operator skills and validation to use `agent-name` consistently, create worktrees from `repos/topic-main`, write symlinks into per-agent worktrees only for approved shared surfaces, and report the new boundaries.
- Revise docs, domain language, fixtures, and tests that currently teach root collaboration directories, `agent-key`, or `agent_workspace_ref` as the primary planning concept.

## Capabilities

### New Capabilities
- `topic-workspace-visibility-layout`: Canonical Topic Workspace and Agent Workspace visibility, ownership, directory layout, branch naming, and communication-channel semantics.

### Modified Capabilities
- `workspace-path-resolution`: Replace root worker-visible path defaults with `repos/topic-main`, `records/*`, runtime internals, and `agents/<agent-name>` worktree path semantics.
- `workspace-runtime-persistence`: Update runtime initialization, path-plan persistence, Agent Team Instance creation, and validation so runtime records use the new layout and do not silently create old root collaboration directories.
- `topic-workspace-manager-skill`: Rename planning language from agent key to agent name, manage topic-owner and per-agent branches, create symlinked shared surfaces from `repos/topic-main`, and validate owner/worker boundaries.
- `topic-team-specialization-module-skill`: Make `setup-agent-workspace` delegate the standardized worktree layout and record returned agent names, branches, paths, and blockers as static setup evidence.
- `topic-agent-team-profile-specialization`: Replace `agent_workspace_ref` as the primary authored planning concept with agent-name workspace planning, while preserving derived path refs for compatibility and launch-facing validation.
- `research-lifecycle-state`: Record Agent Workspace lifecycle state in terms of Agent Instance ownership plus stable topic-local agent name and branch/worktree refs.
- `houmao-cli-adapter-layer`: Launch or prepare each mapped managed agent from the recorded Agent Workspace worktree as cwd and keep adapter payloads outside worker-visible collaboration surfaces unless explicitly published.
- `isomer-admin-project-manager-skill`: Update runtime and Project guidance so operators understand `records/`, `runtime/`, `repos/topic-main`, and `agents/<agent-name>` boundaries.
- `isomer-documentation-system-guide`: Require docs to describe the standardized Topic Workspace layout, worker visibility boundary, communication channels, and migration posture.

## Impact

- Affected code includes `src/isomer_labs/paths.py`, `src/isomer_labs/workspace_refs.py`, `src/isomer_labs/runtime/models.py`, `src/isomer_labs/runtime/schema.py`, `src/isomer_labs/runtime/store.py`, runtime validation modules, team profile and packet validation, Houmao adapter launch/materialization code, and CLI command output/tests around runtime initialization and team instance creation.
- Affected skills include `skillset/operator/isomer-admin-topic-workspace-mgr`, `skillset/operator/isomer-admin-topic-team-specialize`, and `skillset/operator/isomer-admin-project-mgr`; research-paradigm contract copies may need wording updates if they imply old root path surfaces.
- Affected docs include the canonical domain language in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`, `docs/topic-workspace-definition.md`, `docs/concepts.md`, `docs/runtime-and-files.md`, `docs/system-design.md`, `docs/workflows.md`, `docs/isomer-cli.md`, and stale getting-started or troubleshooting examples.
- Existing fixtures and tests that assert `agent_workspace_ref`, `agent-key`, `agent-workspaces/`, `agents/<agent-instance-id>`, or root `artifacts/tasks/runs/views/logs` defaults will need deliberate migration or compatibility assertions.
