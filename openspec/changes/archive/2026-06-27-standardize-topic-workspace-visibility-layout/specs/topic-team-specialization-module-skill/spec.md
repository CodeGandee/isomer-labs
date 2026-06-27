## MODIFIED Requirements

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL delegate standardized Git-backed Agent Workspace repository and worktree preparation to `isomer-admin-topic-workspace-mgr` when a specialized topic team needs the `repos/topic-main` layout.

#### Scenario: Setup agent workspace delegates Git worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under `<topic-workspace-dir>/agents/<agent-name>`
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` rather than creating the worktrees itself

#### Scenario: Static setup records delegated workspace plans
- **WHEN** delegated Git-backed workspace setup has completed
- **THEN** `setup-agent-workspace`, `validate-topic-team`, or `finalize-topic-team` may report the returned agent names, Agent Workspace paths, branch names, derived compatibility refs, boundary docs, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Delegation preserves static boundary
- **WHEN** Topic Team Specialization delegates Git-backed workspace setup
- **THEN** it still does not create Agent Instances, mutate Workspace Runtime records, launch agents, or invoke Execution Adapters

#### Scenario: Missing delegated setup blocks static readiness
- **WHEN** the specialized topic team requires Git-backed Agent Workspaces and no successful topic workspace manager output exists
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker rather than claiming static material readiness

#### Scenario: Plain static directory setup is not standard worker layout
- **WHEN** `setup-agent-workspace` is asked to prepare launch-facing worker Agent Workspaces
- **THEN** it treats non-Git static directories as a blocker or explicit exception rather than as the standard Topic Workspace worker layout

## ADDED Requirements

### Requirement: Topic Team Workspace Evidence Language
The Topic Team Specialization module skill SHALL use topic-local agent names and worker visibility terms when reporting Agent Workspace setup evidence.

#### Scenario: Setup output uses agent names
- **WHEN** `setup-agent-workspace` reports prepared workspaces
- **THEN** it reports `agent_names`, `agent_workspace_paths`, `branch_plan`, `topic_main_repo`, `records_root`, and blockers instead of using `agent-key` as the user-facing term

#### Scenario: Setup output names worker visibility boundary
- **WHEN** `finalize-topic-team` summarizes static setup evidence
- **THEN** it distinguishes worker-visible material under `repos/topic-main` from owner-preserved records under `records/*` and runtime internals under `runtime/`
