## MODIFIED Requirements

### Requirement: Human-Orchestrated Topic Research Preparation
The system SHALL provide an operator workflow that prepares a Research Topic for human-orchestrated v2 research with a default operator Topic Actor, optional additional Topic Actors, no required formal Topic Agent Team material, and a terminal Topic Workspace readiness summary.

#### Scenario: Direct human-orchestrated request prepares topic and actors
- **WHEN** a Project Operator asks to prepare a topic for manual or human-orchestrated research with zero or more named workers
- **THEN** the workflow resolves or creates the Research Topic, ensures Project Manifest-backed Topic Workspace registration, initializes or validates Workspace Runtime, delegates Topic Workspace environment setup, validates Topic Main Development Repository readiness, delegates missing Topic Actor or Topic Actor Workspace work to the Topic Workspace Manager, runs research bootstrap, runs Topic Creator `finalize`, writes `topic.workspace.summary`, and reports blockers
- **AND** it does not require a Topic Agent Team Profile, Agent Team Instance, formal Agent Workspace, Houmao launch dossier, or Houmao-managed agent launch
- **AND** it does not route the user to a next research step after readiness reporting

#### Scenario: Operator Topic Actor Workspace is created by default
- **WHEN** common topic preparation runs without an explicit user opt-out
- **THEN** it asks the Topic Workspace Manager to create or reuse a Topic Actor named `operator`
- **AND** it asks the Topic Workspace Manager to materialize that actor's Topic Actor Workspace with `default_cwd_label` set to `topic.actors.workspace`

#### Scenario: User can opt out of operator Topic Actor Workspace
- **WHEN** the user explicitly says not to create the `operator` Topic Actor or its Topic Actor Workspace
- **THEN** preparation records the opt-out and continues when no selected later step requires operator actor context
- **AND** any later step that requires the missing operator actor reports a repairable blocker instead of silently recreating it
- **AND** Topic Creator `finalize` records actor readiness as skipped when no other actors were requested

#### Scenario: Existing team material is preserved
- **WHEN** human-orchestrated preparation runs in a Topic Workspace that already has Topic Agent Team Profile or Agent Team Instance material
- **THEN** the workflow preserves and reports that material instead of treating it as mutually exclusive with Topic Actors

### Requirement: Operation Summary for Actor Topology
The system SHALL write or update a topic workspace summary that reports the active human-orchestrated and formal team topology without turning Topic Creator into a research-step router.

#### Scenario: Summary records Topic Actor topology
- **WHEN** human-orchestrated research preparation completes or reaches a reportable blocker
- **THEN** `topic.workspace.summary`, defaulting to `<topic-workspace>/isomer-topic-workspace-summary.md`, lists current Topic Actors, Topic Actor Workspaces, topic-main integration surface, storage surfaces, placeholder binding entrypoints, optional formal team refs, ready surfaces, verified checks, skipped optional work, and blockers
- **AND** the summary does not require a `next actions` section
- **AND** Topic Creator terminal output reports ready, verified, and blocked state without prescribing the next research command
