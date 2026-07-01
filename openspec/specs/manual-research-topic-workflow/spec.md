# manual-research-topic-workflow Specification

## Purpose
TBD - created by archiving change add-manual-research-topic-workflow. Update Purpose after archive.
## Requirements
### Requirement: Human-Orchestrated Topic Research Preparation
The system SHALL provide an operator workflow that prepares a Research Topic for human-orchestrated v2 research with a default operator Topic Actor, optional additional Topic Actors, and no required formal Topic Agent Team material.

#### Scenario: Direct human-orchestrated request prepares topic and actors
- **WHEN** a Project Operator asks to prepare a topic for manual or human-orchestrated research with zero or more named workers
- **THEN** the workflow resolves or creates the Research Topic, ensures Project Manifest-backed Topic Workspace registration, initializes or validates Workspace Runtime, delegates Topic Workspace environment setup, validates Topic Main Development Repository readiness, delegates missing Topic Actor or Topic Actor Workspace work to the Topic Workspace Manager, and reports blockers
- **AND** it does not require a Topic Agent Team Profile, Agent Team Instance, formal Agent Workspace, Houmao launch dossier, or Houmao-managed agent launch

#### Scenario: Operator Topic Actor Workspace is created by default
- **WHEN** common topic preparation runs without an explicit user opt-out
- **THEN** it asks the Topic Workspace Manager to create or reuse a Topic Actor named `operator`
- **AND** it asks the Topic Workspace Manager to materialize that actor's Topic Actor Workspace with `default_cwd_label` set to `topic.actors.workspace`

#### Scenario: User can opt out of operator Topic Actor Workspace
- **WHEN** the user explicitly says not to create the `operator` Topic Actor or its Topic Actor Workspace
- **THEN** preparation records the opt-out and continues when no selected later step requires operator actor context
- **AND** any later step that requires the missing operator actor reports a repairable blocker instead of silently recreating it

#### Scenario: Existing team material is preserved
- **WHEN** human-orchestrated preparation runs in a Topic Workspace that already has Topic Agent Team Profile or Agent Team Instance material
- **THEN** the workflow preserves and reports that material instead of treating it as mutually exclusive with Topic Actors

### Requirement: Manual Workflow Consumes Workspace Manager Actor Topology
The human-orchestrated research workflow SHALL consume Topic Actor topology prepared by the Topic Workspace Manager rather than owning Topic Actor CRUD.

#### Scenario: Requested actors are delegated to workspace manager
- **WHEN** a manual research request names additional manually controlled workers
- **THEN** the workflow routes Topic Actor registration, reuse, update, materialization, repair, or archive work to `isomer-admin-topic-workspace-mgr`
- **AND** it resumes research bootstrap only after the selected Topic Actor bindings and Topic Actor Workspaces are ready or reported as blocked

#### Scenario: Actors do not share topic-main as required cwd
- **WHEN** multiple Topic Actors are prepared for one Research Topic
- **THEN** the manual workflow receives each actor's resolved Topic Actor Workspace cwd from the Topic Workspace Manager
- **AND** `topic.repos.main` remains the integration surface and Git anchor rather than the required cwd for every actor

### Requirement: Actor Readiness Signals
The system SHALL define readiness signals for human-orchestrated Topic Actor research.

#### Scenario: Actor readiness is accepted without formal team files
- **WHEN** actor readiness is checked for a selected Topic Workspace
- **THEN** it requires the selected Research Topic ref, registered Topic Workspace, initialized Workspace Runtime, `topic.intent.overview`, topic environment readiness evidence, ready `topic.repos.main`, materialized topic research record labels, v2 placeholder binding guidance, requested Topic Actor bindings, and requested Topic Actor Workspace readiness
- **AND** it does not require `team-profile/`, a Topic Agent Team Profile, formal `agent.workspace` labels, per-Agent Instance cwd proof, Agent Team Instance records, or Agent Instance records

#### Scenario: Missing actor-level signal blocks actor readiness
- **WHEN** a required Topic Actor readiness signal is missing or invalid
- **THEN** the readiness check reports the exact missing actor name, semantic label or artifact expected, and operator workflow that can prepare it

### Requirement: Topic Actor Start Pack
The system SHALL produce start packs for users who manually start coding agents inside prepared Topic Actor Workspaces.

#### Scenario: Start pack tells the user where each actor runs
- **WHEN** human-orchestrated preparation succeeds
- **THEN** the authoritative start pack is recorded as a Topic Workspace research record
- **AND** the start pack names each Topic Actor, runtime kind, role kind, resolved actor cwd, branch, Topic Workspace id, Research Topic id, relevant v2 research skills, bootstrap/readiness report, and storage binding references
- **AND** the workflow writes a small actor-local copy or pointer inside the Topic Actor Workspace for startup convenience

#### Scenario: Start pack explains accepted artifact writes
- **WHEN** the start pack describes research artifact handling
- **THEN** it directs each Topic Actor to use skill-local `placeholder-bindings.md` and `isomer-cli ext research records` for accepted research artifacts
- **AND** it distinguishes durable Topic Workspace records from editable files, notebooks, and source changes in Topic Actor Workspaces, Agent Workspaces, or `topic.repos.main`

### Requirement: Operation Summary for Actor Topology
The system SHALL write or update a topic operation summary that reports the active human-orchestrated and formal team topology.

#### Scenario: Summary records Topic Actor topology
- **WHEN** human-orchestrated research preparation completes
- **THEN** `isomer-topic-summary.md` or its recorded equivalent lists current Topic Actors, Topic Actor Workspaces, topic-main integration surface, storage surfaces, placeholder binding entrypoints, optional formal team refs, blockers, and next actions

