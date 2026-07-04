## MODIFIED Requirements

### Requirement: Topic Actor Management Commands
The Topic Manager skill SHALL manage Topic Actor CRUD, materialization, repair, archive, and diagnostics as initialized-topic topology operations, and SHALL require Topic Actor Workspace readiness to mean a matching worktree of the resolved `topic.repos.main`.

#### Scenario: Actor management uses topic manager
- **WHEN** a user or operator asks to list, show, register, update, archive, materialize, repair, or diagnose Topic Actors
- **THEN** `isomer-op-topic-mgr actors-manage`, `actors-materialize`, or `actors-diagnose` performs or guides the operation through the supported `project topic-actors ...` CLI surface
- **AND** Topic Workspace Manifest actor bindings remain the topology and path-resolution authority

#### Scenario: Actor workspace materialization stays actor scoped
- **WHEN** `actors-materialize` creates or repairs a Topic Actor Workspace
- **THEN** it uses `topic.repos.main` as the Git anchor, resolves `topic.actors.workspace` for the selected Topic Actor, and uses the `per-topic-actor/<topic-actor-name>/main` default branch namespace
- **AND** it keeps Topic Actor names separate from Agent Names and Agent Instance ids

#### Scenario: Missing actor worktree is created from topic-main
- **WHEN** `actors-materialize` prepares Topic Actor `operator` and the resolved `topic.actors.workspace` path does not exist
- **THEN** it creates the path as a Git worktree of the resolved `topic.repos.main` repository
- **AND** the default branch is `per-topic-actor/operator/main`

#### Scenario: Existing matching actor worktree is ready
- **WHEN** the resolved `topic.actors.workspace` path already exists as a worktree of the resolved `topic.repos.main` on the expected actor branch
- **THEN** `actors-materialize` and `actors-diagnose` report the Topic Actor Workspace as ready instead of creating another worktree

#### Scenario: Existing nonmatching actor path blocks readiness
- **WHEN** the resolved `topic.actors.workspace` path exists but is not the expected worktree of the resolved `topic.repos.main` on the expected actor branch
- **THEN** `actors-materialize` and `actors-diagnose` report a blocker and do not overwrite, delete, move, clean, reset, or reinitialize the path

#### Scenario: Duplicate actor branch checkout is rejected
- **WHEN** the expected `per-topic-actor/<topic-actor-name>/main` branch is already checked out in another worktree of the Topic Main Development Repository
- **THEN** `actors-materialize` reports a blocker instead of force-moving or deleting the existing checkout

#### Scenario: Non-Git topic-main blocks actor worktree readiness
- **WHEN** the resolved `topic.repos.main` path is missing or is not a Git repository
- **THEN** actor materialization and diagnostics report that Topic Main Development Repository readiness is required before Topic Actor Workspace readiness
- **AND** they do not claim readiness from a placeholder actor directory
