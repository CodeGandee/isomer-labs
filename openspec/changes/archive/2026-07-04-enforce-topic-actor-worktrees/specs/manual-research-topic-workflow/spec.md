## MODIFIED Requirements

### Requirement: Human-Orchestrated Topic Research Preparation
The system SHALL provide an operator workflow that prepares a Research Topic for human-orchestrated research with a default operator Topic Actor, optional additional Topic Actors, and no required formal Topic Agent Team material.

#### Scenario: Direct human-orchestrated request prepares topic and actors
- **WHEN** a Project Operator asks to prepare a topic for manual or human-orchestrated research with zero or more named workers
- **THEN** the workflow resolves or creates the Research Topic, ensures Project Manifest-backed Topic Workspace registration, initializes or validates Workspace Runtime, delegates Topic Workspace environment setup, validates Topic Main Development Repository readiness, delegates missing Topic Actor or Topic Actor Workspace work to `isomer-op-topic-mgr`, writes or reports Topic Actor onboarding material, and reports blockers
- **AND** it does not require a Topic Agent Team Profile, Agent Team Instance, formal Agent Workspace, Houmao launch dossier, Houmao-managed agent launch, selected v2 research skills, or v2 placeholder binding readiness

#### Scenario: Operator Topic Actor Workspace is created by default
- **WHEN** common topic preparation runs without an explicit user opt-out
- **THEN** it asks `isomer-op-topic-mgr` to create or reuse a Topic Actor named `operator`
- **AND** it asks `isomer-op-topic-mgr` to materialize that actor's Topic Actor Workspace with `default_cwd_label` set to `topic.actors.workspace`

#### Scenario: User can opt out of operator Topic Actor Workspace
- **WHEN** the user explicitly says not to create the `operator` Topic Actor or its Topic Actor Workspace
- **THEN** preparation records the opt-out and continues when no selected later step requires operator actor context
- **AND** any later step that requires the missing operator actor reports a repairable blocker instead of silently recreating it

#### Scenario: Existing team material is preserved
- **WHEN** human-orchestrated preparation runs in a Topic Workspace that already has Topic Agent Team Profile or Agent Team Instance material
- **THEN** the workflow preserves and reports that material instead of treating it as mutually exclusive with Topic Actors

#### Scenario: Manual actors use topic-main worktree workspaces
- **WHEN** human-orchestrated preparation creates or validates a Topic Actor Workspace
- **THEN** the workspace is a worktree of `topic.repos.main` on a Topic Actor branch even though the actor is controlled manually rather than launched by Isomer
- **AND** the workflow treats controller provenance, not Git workspace topology, as the distinction between a Topic Actor and a formal Agent Workspace

### Requirement: Manual Workflow Consumes Topic Manager Actor Topology
The human-orchestrated research workflow SHALL consume Topic Actor topology prepared by the Topic Manager rather than owning Topic Actor CRUD.

#### Scenario: Requested actors are delegated to topic manager
- **WHEN** a manual research request names additional manually controlled workers
- **THEN** the workflow routes Topic Actor registration, reuse, update, materialization, repair, or archive work to `isomer-op-topic-mgr actors-manage`, `actors-materialize`, or `actors-diagnose`
- **AND** it resumes research bootstrap only after the selected Topic Actor bindings and Topic Actor Workspaces are ready or reported as blocked

#### Scenario: Actors do not share topic-main as required cwd
- **WHEN** multiple Topic Actors are prepared for one Research Topic
- **THEN** the manual workflow receives each actor's resolved Topic Actor Workspace cwd from `isomer-op-topic-mgr`
- **AND** `topic.repos.main` remains the integration surface and Git anchor rather than the required cwd for every actor

#### Scenario: Actor workspace blockers stop manual bootstrap
- **WHEN** `isomer-op-topic-mgr` reports that a selected Topic Actor Workspace path is missing valid worktree evidence or collides with a nonmatching path
- **THEN** the manual workflow reports the blocker and does not write onboarding material that claims the actor cwd is ready
