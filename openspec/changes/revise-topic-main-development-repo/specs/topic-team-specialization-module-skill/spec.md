## MODIFIED Requirements

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL treat Topic Main Development Repository setup as topic env predecessor work and SHALL delegate only per-agent worktree and cwd-readiness materialization after topic-main readiness exists.

#### Scenario: Topic-main setup is not workspace-manager work in the canonical path
- **WHEN** the normal topic-team setup path needs `topic.repos.main`
- **THEN** `isomer-admin-topic-team-specialize` gets that evidence through `setup-topic-env` and `isomer-srv-topic-env-setup`
- **AND** it does not route canonical Topic Main Development Repository creation to `isomer-admin-topic-workspace-mgr`

#### Scenario: Setup agent workspace delegates agent worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under resolved `agent.workspace` paths
- **THEN** it routes per-agent worktree creation and cwd verification through `isomer-srv-agent-env-setup` after Topic Main Development Repository predecessor evidence exists
- **AND** it does not create the worktrees itself

#### Scenario: Workspace manager remains optional
- **WHEN** the operator asks for read-only topology inspection, branch helper operations, boundary summaries, or legacy compatibility diagnostics
- **THEN** the skill may route that bounded work to `isomer-admin-topic-workspace-mgr`
- **AND** it records that evidence separately from topic env materialization and agent env readiness evidence

### Requirement: Operator Owns Environment Setup Orchestration
The Topic Team Specialization module skill SHALL own the decision to create derived target specs and invoke Topic Workspace environment setup and Agent Workspace environment readiness setup in the normal operator flow.

#### Scenario: Topic setup is delegated only after derived topic target spec exists
- **WHEN** `isomer-admin-topic-team-specialize setup-topic-env` runs after registration and Topic Workspace Pixi binding evidence exists
- **THEN** it ensures `topic.intent.topic_env_requirements` and `topic.env.topic_setup_target_spec` exist or reports blockers
- **AND** it delegates Topic Main Development Repository setup, external repo acquisition, external projection materialization, Pixi mutation, and topic-root or repo-specific verification work to `isomer-srv-topic-env-setup`
- **AND** it records topic env setup evidence as Topic Workspace predecessor evidence
- **AND** it does not treat that evidence as per-Agent Workspace cwd readiness

#### Scenario: Agent setup is delegated after topic-main readiness exists
- **WHEN** `isomer-admin-topic-team-specialize setup-agent-workspace` receives a request for per-Agent Workspace cwd verification, selected-agent repair, or launch-facing Agent Workspace readiness
- **THEN** it ensures `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace env readiness, authoritative Agent Names, and Topic Main Development Repository predecessor evidence exist or reports blockers
- **AND** it delegates gate-driven Agent Workspace environment setup to `isomer-srv-agent-env-setup`

#### Scenario: Derived gates are orchestrator-owned in normal flow
- **WHEN** the normal topic-team setup flow creates operational target specs
- **THEN** `isomer-admin-topic-team-specialize` owns the creation or update of `topic.env.topic_setup_target_spec` and `topic.env.agent_setup_target_spec`
- **AND** direct service invocation may still accept explicit target specs outside the normal operator flow

## ADDED Requirements

### Requirement: Breaking Topic Team Setup Order
The Topic Team Specialization module skill SHALL present the revised setup order as a breaking replacement for old generated Topic Workspace internals.

#### Scenario: Revised order is canonical
- **WHEN** help text, workflow text, or operator documentation describes the normal setup path
- **THEN** it presents the order as `resolve-project`, `resolve-topic-intent`, `resolve-topic-env-gate`, create `topic.env.topic_setup_target_spec`, materialize topic env including Topic Main Development Repository and projections, `specialize-team` when team material is needed, `resolve-agent-env-gate`, create `topic.env.agent_setup_target_spec`, materialize agent env worktrees and cwd proof, `validate-topic-team`, and `finalize-topic-team`

#### Scenario: Old generated internals are not preserved
- **WHEN** existing generated `isomer-content/` internals conflict with the revised setup order
- **THEN** the skill reports that generated topic content should be recreated
- **AND** it does not require compatibility steps for the old internal layout
