## ADDED Requirements

### Requirement: Operator Owns Environment Setup Orchestration
The Topic Team Specialization module skill SHALL own the decision to invoke Topic Workspace environment setup, Git-backed Agent Workspace topology setup, and Agent Workspace environment readiness setup.

#### Scenario: Topic setup is delegated only from operator topic setup
- **WHEN** `isomer-admin-topic-team-specialize setup-topic-env` runs after registration and Topic Workspace Pixi binding evidence exists
- **THEN** it delegates Topic Workspace dependency, repo acquisition, Pixi mutation, and topic-root verification work to `isomer-srv-topic-env-setup`
- **AND** it records topic env setup evidence as Topic Workspace predecessor evidence
- **AND** it does not treat that evidence as per-Agent Workspace cwd readiness

#### Scenario: Agent setup is delegated only from operator agent workspace setup
- **WHEN** `isomer-admin-topic-team-specialize setup-agent-workspace` receives a request for `agent-env-gate.md`, per-Agent Workspace cwd verification, selected-agent repair, or launch-facing Agent Workspace readiness
- **THEN** it ensures a usable `user-intent/src/agent-env-gate.md` exists or asks for the missing per-agent readiness target
- **AND** after Topic Workspace environment readiness and Git topology evidence exist, it delegates gate-driven Agent Workspace environment setup to `isomer-srv-agent-env-setup`

#### Scenario: Git topology remains workspace manager work
- **WHEN** Git-backed `topic.repos.main`, per-agent `agent.workspace` worktrees, branch plans, worker-facing support paths, or Workspace Boundary material are needed
- **THEN** Topic Team Specialization delegates that topology to `isomer-admin-topic-workspace-mgr`
- **AND** it records the workspace manager evidence separately from topic env setup evidence and agent env setup evidence

### Requirement: Validation Distinguishes Topic and Agent Readiness Evidence
The Topic Team Specialization module skill SHALL validate topic environment readiness and Agent Workspace readiness as separate static setup evidence streams.

#### Scenario: Topic env evidence cannot satisfy agent env evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` reads setup evidence
- **THEN** readiness from `isomer-srv-topic-env-setup` may satisfy only Topic Workspace environment setup evidence
- **AND** per-Agent Workspace cwd readiness requires `isomer-srv-agent-env-setup` evidence when that proof was requested

#### Scenario: Missing agent env proof is explicit
- **WHEN** per-Agent Workspace cwd verification was requested but `isomer-srv-agent-env-setup` evidence is missing
- **THEN** Topic Team Specialization reports an explicit blocker or deferral for Agent Workspace environment readiness
- **AND** it does not infer readiness from topic-root verification, Pixi install success, or Git topology readiness
