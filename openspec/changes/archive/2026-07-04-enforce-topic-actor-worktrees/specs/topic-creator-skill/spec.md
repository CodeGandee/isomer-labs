## MODIFIED Requirements

### Requirement: Topic Creator Defines Actors Before Actor Setup
The Topic Creator skill SHALL use `define-actors` to create actor intent before `setup-actors` materializes actor workspaces or verifies actor env gates, and SHALL require actor worktree readiness evidence before claiming actor readiness.

#### Scenario: Define actors writes actor definitions
- **WHEN** `define-actors` runs with requested actor information
- **THEN** it creates or refines `topic.intent.actor_definitions`
- **AND** the default-layout resolved file is `<topic-workspace>/intent/src/actor-definitions.md`
- **AND** each actor definition includes actor name, duty, intended usage, expected cwd label, controller/runtime assumptions when known, and that actor's source env gate requirements

#### Scenario: Define actors defaults to operator actor
- **WHEN** `define-actors` is invoked without further actor information
- **THEN** it creates or refines a default `operator` actor definition
- **AND** requests such as "create the operator actor" have the same effect

#### Scenario: Setup actors derives gates and verifies workspaces
- **WHEN** `setup-actors` runs after `topic.intent.actor_definitions` exists
- **THEN** it delegates actor registration and workspace materialization to `isomer-op-topic-mgr`, creates or validates derived actor env gates at `topic.env.actor_env_gates`, and verifies the gates from each actor's resolved `topic.actors.workspace`
- **AND** the default-layout derived gate file is `<topic-workspace>/intent/derived/actor-env-gates.md`
- **AND** it reports blockers instead of claiming actor readiness when workspace material, derived gates, or gate verification evidence is missing

#### Scenario: Setup actors requires topic-main worktree evidence
- **WHEN** `setup-actors` evaluates whether a selected Topic Actor is ready
- **THEN** it treats the actor workspace as ready only when delegated Topic Manager evidence shows the resolved `topic.actors.workspace` is a worktree of the resolved `topic.repos.main` on the expected actor branch
- **AND** it reports the delegated blocker instead of continuing to actor env gate verification when that worktree evidence is missing or invalid
