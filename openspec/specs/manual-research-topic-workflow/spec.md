# manual-research-topic-workflow Specification

## Purpose
TBD - created by archiving change add-manual-research-topic-workflow. Update Purpose after archive.
## Requirements
### Requirement: Human-Orchestrated Topic Research Preparation
The system SHALL provide an operator workflow that prepares a Research Topic for human-orchestrated research with a default operator Topic Actor, optional additional Topic Actors, and no required formal Topic Agent Team material.

#### Scenario: Direct human-orchestrated request prepares topic and actors
- **WHEN** a Project Operator asks to prepare a topic for manual or human-orchestrated research with zero or more named workers
- **THEN** the workflow resolves or creates the Research Topic, ensures Project Manifest-backed Topic Workspace registration, initializes or validates Workspace Runtime, delegates Topic Workspace environment setup, validates Topic Main Development Repository readiness, delegates missing Topic Actor or Topic Actor Workspace work to `isomer-admin-topic-mgr`, writes or reports Topic Actor onboarding material, and reports blockers
- **AND** it does not require a Topic Agent Team Profile, Agent Team Instance, formal Agent Workspace, Houmao launch dossier, Houmao-managed agent launch, selected v2 research skills, or v2 placeholder binding readiness

#### Scenario: Operator Topic Actor Workspace is created by default
- **WHEN** common topic preparation runs without an explicit user opt-out
- **THEN** it asks `isomer-admin-topic-mgr` to create or reuse a Topic Actor named `operator`
- **AND** it asks `isomer-admin-topic-mgr` to materialize that actor's Topic Actor Workspace with `default_cwd_label` set to `topic.actors.workspace`

#### Scenario: User can opt out of operator Topic Actor Workspace
- **WHEN** the user explicitly says not to create the `operator` Topic Actor or its Topic Actor Workspace
- **THEN** preparation records the opt-out and continues when no selected later step requires operator actor context
- **AND** any later step that requires the missing operator actor reports a repairable blocker instead of silently recreating it

#### Scenario: Existing team material is preserved
- **WHEN** human-orchestrated preparation runs in a Topic Workspace that already has Topic Agent Team Profile or Agent Team Instance material
- **THEN** the workflow preserves and reports that material instead of treating it as mutually exclusive with Topic Actors

### Requirement: Manual Workflow Consumes Topic Manager Actor Topology
The human-orchestrated research workflow SHALL consume Topic Actor topology prepared by the Topic Manager rather than owning Topic Actor CRUD.

#### Scenario: Requested actors are delegated to topic manager
- **WHEN** a manual research request names additional manually controlled workers
- **THEN** the workflow routes Topic Actor registration, reuse, update, materialization, repair, or archive work to `isomer-admin-topic-mgr actors-manage`, `actors-materialize`, or `actors-diagnose`
- **AND** it resumes research bootstrap only after the selected Topic Actor bindings and Topic Actor Workspaces are ready or reported as blocked

#### Scenario: Actors do not share topic-main as required cwd
- **WHEN** multiple Topic Actors are prepared for one Research Topic
- **THEN** the manual workflow receives each actor's resolved Topic Actor Workspace cwd from `isomer-admin-topic-mgr`
- **AND** `topic.repos.main` remains the integration surface and Git anchor rather than the required cwd for every actor

### Requirement: Actor Readiness Signals
The system SHALL define v2-independent readiness signals for human-orchestrated Topic Actor research.

#### Scenario: Actor readiness is accepted without formal team files
- **WHEN** actor readiness is checked for a selected Topic Workspace
- **THEN** it requires the selected Research Topic ref, registered Topic Workspace, initialized Workspace Runtime, `topic.intent.overview`, topic environment readiness evidence, ready `topic.repos.main`, requested Topic Actor bindings, requested Topic Actor Workspace readiness, actor support-label readiness, derived actor env gates, and actor cwd verification evidence
- **AND** it does not require `team-profile/`, a Topic Agent Team Profile, formal `agent.workspace` labels, per-Agent Instance cwd proof, Agent Team Instance records, Agent Instance records, selected v2 research skills, v2 placeholder binding guidance, or research storage bootstrap records

#### Scenario: Missing actor-level signal blocks actor readiness
- **WHEN** a required Topic Actor readiness signal is missing or invalid
- **THEN** the readiness check reports the exact missing actor name, semantic label or artifact expected, and operator workflow that can prepare it

### Requirement: Operation Summary for Actor Topology
The system SHALL write or update a topic operation summary that reports the active human-orchestrated and formal team topology without research-paradigm-specific bootstrap details.

#### Scenario: Summary records Topic Actor topology
- **WHEN** human-orchestrated research preparation completes
- **THEN** `topic.workspace.summary` or its recorded equivalent lists current Topic Actors, Topic Actor Workspaces, topic-main integration surface, actor onboarding material, optional formal team refs, blockers, and readiness evidence
- **AND** it does not require or report v2 placeholder binding entrypoints as operator readiness

### Requirement: Topic Actor Onboarding Material
The human-orchestrated topic preparation workflow SHALL produce v2-independent Topic Actor onboarding material as part of actor setup.

#### Scenario: Setup actors records actor onboarding material
- **WHEN** `isomer-admin-topic-creator setup-actors` creates or validates a selected Topic Actor
- **THEN** it reports or writes actor onboarding material that includes the actor name, actor kind, runtime kind, role kind, controller kind, resolved `topic.actors.workspace` cwd, branch, integration surface, support labels, boundary notes, verification evidence, and blockers
- **AND** it does not include selected v2 skills, v2 placeholder binding files, v2 bootstrap records, or accepted research artifact command shapes

#### Scenario: Actor onboarding can be local convenience material
- **WHEN** actor-local support labels such as `topic.actors.isomer_managed` or `topic.actors.links` resolve for a selected Topic Actor
- **THEN** the workflow MAY write or report an actor-local onboarding card or pointer for startup convenience
- **AND** it treats that material as operator onboarding guidance rather than an authoritative research record
