## ADDED Requirements

### Requirement: Topic Workspace Manager Delegates Agent Env Readiness
The topic workspace manager skill SHALL route service-safe per-agent environment verification to `isomer-srv-agent-env-setup` when Agent Workspace cwd readiness is requested.

#### Scenario: Env readiness request routes to service
- **WHEN** the operator asks `isomer-admin-topic-workspace-mgr` to prove that prepared Agent Workspaces pass the environment gate
- **THEN** the skill routes to `isomer-srv-agent-env-setup setup-agent-env` or a specific service subcommand
- **AND** it preserves the selected Research Topic, Topic Workspace, role binding source, and semantic path expectations in the service request

#### Scenario: Static Git-only flow remains available
- **WHEN** the operator asks only for Git-backed workspace topology preparation
- **THEN** the skill may continue to run `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `validate-worktrees`, and `summarize` without requiring per-agent env-gate execution

#### Scenario: Service output is consumed as evidence
- **WHEN** the agent env setup service returns output
- **THEN** the topic workspace manager summary includes the returned `source_agent_env_gate_path`, `agent_env_gate_path`, readiness by agent, worktree status by agent, semantic paths, commands run, blockers, and next operator action

### Requirement: Topic Workspace Manager Preserves Service Boundaries
The topic workspace manager skill SHALL distinguish static workspace topology readiness from agent env readiness and runtime readiness.

#### Scenario: Git readiness does not imply env readiness
- **WHEN** `validate-worktrees` reports Git topology as ready
- **THEN** the skill does not claim that the Topic Workspace Pixi env passes from every Agent Workspace cwd unless `isomer-srv-agent-env-setup` evidence says so

#### Scenario: Agent env readiness does not imply runtime readiness
- **WHEN** service evidence reports Agent Workspace env readiness as ready
- **THEN** the topic workspace manager still does not claim Agent Instance creation, Workspace Runtime records, Houmao launch, or Execution Adapter readiness

#### Scenario: Service blockers remain visible
- **WHEN** the service reports an unsafe path, missing topic env readiness, failing cwd gate command, or nonmatching worktree
- **THEN** the topic workspace manager reports that blocker without silently repairing it
