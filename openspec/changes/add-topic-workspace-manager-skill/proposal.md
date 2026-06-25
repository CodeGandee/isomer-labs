## Why

Topic-local agents need a repeatable Git-backed collaboration layout inside each Topic Workspace so every Agent Workspace can have a private worktree while still sharing one topic-level repository anchor. Today Agent Workspace setup is described only as static directory preparation, while Workspace Runtime creation still derives generated Agent Instance paths and can ignore the `agent_workspace_ref` values that specialization already carries.

## What Changes

- Add a command-style operator skill, `isomer-admin-topic-workspace-mgr`, for preparing and validating a Topic Workspace Git layout.
- Standardize `<topic-workspace-dir>/repos/topic-main` as the shared topic repository used by topic-local agents.
- Standardize `<topic-workspace-dir>/agents/<agent-key>` as the per-agent Git worktree path, with default per-agent main branches named `per-agent/<agent-key>/main` and future per-agent branches under `per-agent/<agent-key>/<branch-name>`.
- Require the skill to write or validate Workspace Boundary material and profile or packet `agent_workspace_ref` values for planned Agent Workspaces.
- Teach runtime path planning and Agent Team Instance creation to honor approved `agent_workspace_ref` values instead of always deriving generated Agent Workspace paths.
- Keep the skill out of live launch: it does not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, or perform adapter operations.

## Capabilities

### New Capabilities

- `topic-workspace-manager-skill`: Defines the new operator skill for Git-backed Topic Workspace repository and Agent Workspace worktree preparation.

### Modified Capabilities

- `operator-admin-skills`: Add the new operator skill to the active operator skillset and validation expectations.
- `topic-team-specialization-module-skill`: Clarify that Git-backed Agent Workspace setup routes to the topic workspace manager skill rather than staying inside static specialization.
- `topic-agent-team-profile-specialization`: Make role-binding `agent_workspace_ref` values the profile and packet carrier for planned Git-backed Agent Workspace paths.
- `workspace-path-resolution`: Define how recorded or approved Agent Workspace refs become path plans for Agent Workspace resolution.
- `workspace-runtime-persistence`: Require Agent Team Instance creation to use approved role-binding Agent Workspace refs when present before deriving default generated paths.

## Impact

- Affects `skillset/operator/` by adding `isomer-admin-topic-workspace-mgr` with subcommand reference pages and UI metadata.
- Affects `skillset/operator/isomer-admin-topic-team-specialize` by narrowing `setup-agent-workspace` to delegate Git-backed workspace preparation when needed.
- Affects Workspace Runtime creation in `src/isomer_labs/runtime/store.py` and related validation so runtime records align with approved Agent Workspace refs.
- Affects profile and packet validation, skillset validation, OpenSpec specs, and unit tests for operator skill structure and Agent Workspace path behavior.
