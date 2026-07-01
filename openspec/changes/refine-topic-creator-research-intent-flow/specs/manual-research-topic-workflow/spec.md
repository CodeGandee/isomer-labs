## MODIFIED Requirements

### Requirement: Human-Orchestrated Topic Research Preparation
The system SHALL provide an operator workflow that prepares a Research Topic for human-orchestrated v2 research with a default operator Topic Actor, optional additional Topic Actors, and no required formal Topic Agent Team material.

#### Scenario: Direct human-orchestrated request prepares topic and actors
- **WHEN** a Project Operator asks to prepare a topic for manual or human-orchestrated research with zero or more named workers
- **THEN** the workflow first obtains concrete Research Topic substance from the prompt, a supplied Markdown file, selected context, or a registered concrete topic statement
- **AND** it blocks before deriving a topic id, naming a Topic Workspace, registering a topic, creating directories, writing `topic-overview.md`, writing `topic-env-gate.md`, writing `actor-definitions.md`, or writing derived actor env gates when concrete topic substance is missing or generic
- **AND** after a Research Topic and Topic Workspace are registered or otherwise available for semantic path resolution, it creates or validates `topic.intent.overview` through `create-research-intent`
- **AND** it creates or refines `topic.intent.topic_env_requirements` through `define-topic-env` and waits for user verification unless running under `fast-forward`
- **AND** it initializes or validates Workspace Runtime, delegates Topic Workspace environment setup from the verified topic env gate, validates Topic Main Development Repository readiness, creates or refines `topic.intent.actor_definitions` through `define-actors`, delegates missing Topic Actor or Topic Actor Workspace work to the Topic Workspace Manager, verifies derived actor env gates, and reports blockers
- **AND** it does not require a Topic Agent Team Profile, Agent Team Instance, formal Agent Workspace, Houmao launch dossier, or Houmao-managed agent launch

#### Scenario: Operator Topic Actor Workspace is created by default
- **WHEN** common topic preparation runs without an explicit user opt-out
- **THEN** `define-actors` creates or reuses a default actor definition for `operator`
- **AND** it asks the Topic Workspace Manager to create or reuse a Topic Actor named `operator`
- **AND** it asks the Topic Workspace Manager to materialize that actor's Topic Actor Workspace with `default_cwd_label` set to `topic.actors.workspace`
- **AND** `setup-actors` creates or validates derived actor env gates and verifies the operator actor cwd environment

#### Scenario: User can opt out of operator Topic Actor Workspace
- **WHEN** the user explicitly says not to create the `operator` Topic Actor or its Topic Actor Workspace
- **THEN** preparation records the opt-out and continues when no selected later step requires operator actor context
- **AND** any later step that requires the missing operator actor reports a repairable blocker instead of silently recreating it

#### Scenario: Existing team material is preserved
- **WHEN** human-orchestrated preparation runs in a Topic Workspace that already has Topic Agent Team Profile or Agent Team Instance material
- **THEN** the workflow preserves and reports that material instead of treating it as mutually exclusive with Topic Actors

### Requirement: Actor Readiness Signals
The system SHALL define readiness signals for human-orchestrated Topic Actor research.

#### Scenario: Actor readiness is accepted without formal team files
- **WHEN** actor readiness is checked for a selected Topic Workspace
- **THEN** it requires the selected Research Topic ref, registered Topic Workspace, initialized Workspace Runtime, `topic.intent.overview` created or validated by `create-research-intent`, verified or fast-forward accepted `topic.intent.topic_env_requirements`, topic environment readiness evidence, ready `topic.repos.main`, materialized topic research record labels, v2 placeholder binding guidance, `topic.intent.actor_definitions`, requested Topic Actor bindings, requested Topic Actor Workspace readiness, `topic.env.actor_env_gates`, and actor cwd verification evidence
- **AND** it does not require `team-profile/`, a Topic Agent Team Profile, formal `agent.workspace` labels, per-Agent Instance cwd proof, Agent Team Instance records, or Agent Instance records

#### Scenario: Missing actor-level signal blocks actor readiness
- **WHEN** a required Topic Actor readiness signal is missing or invalid
- **THEN** the readiness check reports the exact missing actor name, semantic label or artifact expected, and operator workflow that can prepare it
