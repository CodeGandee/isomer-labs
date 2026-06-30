## MODIFIED Requirements

### Requirement: Command-Style Agent Env Subcommands
The service skill SHALL use a lean top-level router, grouped short kebab-case subcommands, and one executable reference page per subcommand.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-srv-agent-env-setup`
- **THEN** the top-level `SKILL.md` instructs the agent to select one subcommand from grouped `Subcommands` sections
- **AND** the top-level workflow loads only the selected reference page before executing that page's `## Workflow`

#### Scenario: Public subcommands exist
- **WHEN** the skill lists public subcommands
- **THEN** Procedural Subcommands include `resolve-agent-env-context`, `require-topic-env-ready`, `require-topic-main-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `create-agent-worktrees`, and `verify-agent-env-gate`
- **AND** Misc Subcommands include `help` and `setup-agent-env`
- **AND** the normal public subcommand list does not include a mutating `ensure-topic-main-repository` step

#### Scenario: Full flow is directly callable
- **WHEN** the user invokes `setup-agent-env` or gives a concrete Agent Workspace env setup request without naming another subcommand
- **THEN** the skill orchestrates `resolve-agent-env-context`, `require-topic-env-ready`, `require-topic-main-ready`, `read-agent-env-gate` when direct derivation is needed, `plan-agent-workspaces`, `derive-agent-env-gate` or target-spec validation, `create-agent-worktrees`, and `verify-agent-env-gate` in order
- **AND** it verifies every authoritative planned Agent Name before reporting overall readiness

#### Scenario: Direct verification can target one authoritative agent
- **WHEN** the user invokes `verify-agent-env-gate` for one Agent Name present in authoritative topic-team material
- **THEN** the skill may verify only that Agent Name's worktree and derived gate commands
- **AND** it reports the result as selected-agent partial readiness evidence, not overall readiness

#### Scenario: Unknown selected agent blocks verification
- **WHEN** the user invokes a selected-agent direct subcommand for an Agent Name absent from authoritative topic-team material
- **THEN** the service reports an Agent Workspace planning blocker
- **AND** it does not infer the agent from directories, branches, or ad hoc maps

#### Scenario: Reference pages are executable
- **WHEN** a subcommand reference page is inspected
- **THEN** it contains a `## Required Inputs` section before `## Workflow`
- **AND** it contains a numbered `## Workflow`
- **AND** the workflow ends with a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Main Development Repository and Agent Worktrees
The service skill SHALL require a prepared Topic Main Development Repository as predecessor evidence and SHALL prepare per-agent Agent Workspace worktrees using semantic labels and deterministic branch namespaces.

#### Scenario: Topic Main Development Repository readiness is required
- **WHEN** `require-topic-main-ready` runs
- **THEN** it checks Topic Workspace predecessor evidence from `isomer-srv-topic-env-setup` for the resolved `topic.repos.main`, owner branch posture, Isomer-managed namespace, projection labels relevant to the agent gate, and blockers
- **AND** it reports a repair next action to `isomer-srv-topic-env-setup` when topic-main readiness is missing, stale, blocked, or failed

#### Scenario: Agent env setup does not initialize topic-main
- **WHEN** `setup-agent-env`, `create-agent-worktrees`, or `verify-agent-env-gate` runs
- **THEN** it does not create, initialize, configure, repair, reset, or rewrite `topic.repos.main`
- **AND** it does not create external repo projections inside topic-main

#### Scenario: Agent worktree uses prepared topic-main
- **WHEN** `create-agent-worktrees` prepares Agent Name `alice`
- **THEN** it creates or validates the resolved `agent.workspace` path as a Git worktree of the already-prepared resolved `topic.repos.main`
- **AND** the default branch is `per-agent/alice/main`

#### Scenario: Existing matching worktree is ready
- **WHEN** the resolved `agent.workspace` path already exists as the expected worktree on the expected branch
- **THEN** the service reports it as ready instead of creating another worktree

#### Scenario: Existing nonmatching path blocks creation
- **WHEN** the resolved `agent.workspace` path exists but is not the expected worktree
- **THEN** the service reports a blocker and does not overwrite, delete, move, clean, reset, or reinitialize the path

#### Scenario: Duplicate branch checkout is rejected
- **WHEN** `per-agent/<agent-name>/main` is already checked out in another worktree of the Topic Main Development Repository
- **THEN** the service reports a blocker instead of force-moving or deleting the existing checkout

## ADDED Requirements

### Requirement: Topic Main Projection Predecessor Evidence
The agent environment setup service skill SHALL consume external repo projection evidence from topic env setup when per-agent cwd verification depends on projected external repositories.

#### Scenario: Agent gate references external projection
- **WHEN** `topic.env.agent_setup_target_spec` requires an external repo projection to be visible from each Agent Workspace cwd
- **THEN** the service checks predecessor evidence for the relevant projection entry in `topic.repos.main.projections.manifest`
- **AND** it verifies the projection path from each target `agent.workspace` cwd without recreating the projection

#### Scenario: Missing projection routes repair to topic env
- **WHEN** a required external repo projection is missing, stale, blocked, or inconsistent with the agent gate
- **THEN** the service reports a repair next action to `isomer-srv-topic-env-setup`
- **AND** it does not create a substitute projection under the Agent Workspace
