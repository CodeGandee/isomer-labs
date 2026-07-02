# topic-creator-skill Specification

## Purpose
TBD - created by archiving change add-topic-creator-skill. Update Purpose after archive.
## Requirements
### Requirement: Topic Creator Operator Skill
The repository SHALL provide a command-style operator skill named `isomer-admin-topic-creator` as the canonical user-facing workflow for initializing a Research Topic from empty or partial Project state to manual-research-ready Topic Workspace.

#### Scenario: Topic creator skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-creator/SKILL.md` and `skillset/operator/isomer-admin-topic-creator/agents/openai.yaml`
- **AND** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-topic-creator`

#### Scenario: Topic creator is the user-facing topic initialization entrypoint
- **WHEN** a user asks to create, initialize, prepare, or start a Research Topic for manual research from empty or partial Project state
- **THEN** the operator routes to `isomer-admin-topic-creator`
- **AND** the user does not need to know the separate project manager, topic manager, service setup, or research bootstrap skill sequence

### Requirement: Topic Creator Command Surface
The Topic Creator skill SHALL expose a command-style workflow with stage commands that can plan, run, resume, inspect, and repair topic initialization.

#### Scenario: Public commands are listed
- **WHEN** `isomer-admin-topic-creator help` runs or the skill is invoked without a prompt
- **THEN** it lists `help`, `plan`, `create`, `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, `start-manual-research`, `status`, and `repair`
- **AND** it prints what the skill does, required inputs, command functionalities, outputs, and guardrails

#### Scenario: Create runs the happy path
- **WHEN** the user invokes `create` with a concrete topic statement or registered topic ref
- **THEN** the workflow runs the topic initialization ladder from Project readiness through manual-research handoff where each stage is already satisfied, created, delegated, or reported as blocked
- **AND** it reports the next incomplete stage instead of asking the user to discover another operator skill

#### Scenario: Plan is dry-run
- **WHEN** the user invokes `plan`
- **THEN** the skill resolves the current Project and topic state, reports proposed stage actions, required inputs, expected delegated owners, command shapes, blockers, and next action
- **AND** it does not create or modify Project, Topic Workspace, runtime, repository, actor, bootstrap, or start-pack state

#### Scenario: Status explains progress
- **WHEN** the user invokes `status`
- **THEN** the skill reports which initialization stages are ready, blocked, skipped, or not started
- **AND** it names the next command that can advance the topic toward manual-research readiness

#### Scenario: Repair resumes from blockers
- **WHEN** the user invokes `repair` after a failed or partial topic initialization
- **THEN** the skill uses recorded state and Project Manifest-backed context to resume from the blocked stage
- **AND** it does not rerun already-ready destructive or expensive stages unless the user explicitly asks

### Requirement: Topic Creator Initialization Ladder
The Topic Creator skill SHALL define the ordered readiness ladder for making a Topic Workspace available for manual research.

#### Scenario: Blank state can reach manual-research readiness
- **WHEN** the user asks the Topic Creator to create a topic for manual research from a repository with no initialized Isomer Project
- **THEN** the skill ensures Project initialization, defines topic intent, registers the Research Topic and Topic Workspace, initializes or validates Workspace Runtime, prepares topic environment readiness, validates `topic.repos.main`, sets up selected Topic Actors, runs research bootstrap, and writes manual research start packs
- **AND** it reports each delegated skill or CLI surface used for those stages

#### Scenario: Partial state is reused
- **WHEN** some topic initialization stages already exist
- **THEN** the skill validates and reuses ready Project, topic, runtime, environment, actor, bootstrap, and start-pack evidence
- **AND** it only creates, delegates, or repairs missing or blocked stages

#### Scenario: Manual-research-ready output is explicit
- **WHEN** topic creation completes successfully
- **THEN** Essential Output reports the Project root, Research Topic ref, Topic Workspace ref, `topic.repos.main` readiness, Workspace Runtime status, Topic Actor roster, each selected actor cwd, v2 bootstrap status, start-pack record refs, blockers, and next action
- **AND** Complete Output includes commands run, semantic labels, delegated owner evidence, topic environment setup evidence, actor binding details, placeholder binding entrypoints, storage recording command shapes, and actor-local pointer paths

### Requirement: Topic Creator Delegates Lower-Level Ownership
The Topic Creator skill SHALL orchestrate existing owners rather than duplicating their lower-level mutation responsibilities.

#### Scenario: Project lifecycle remains delegated
- **WHEN** Project initialization, validation, cleanup, content-root relocation, topic listing, or generic Project diagnostics are needed
- **THEN** the Topic Creator delegates or routes that work to `isomer-admin-project-mgr` or supported `isomer-cli project ...` surfaces

#### Scenario: Topic environment remains delegated
- **WHEN** topic environment requirements, topic env target specs, Topic Main Development Repository setup, projection materialization, or topic-root verification are needed
- **THEN** the Topic Creator delegates setup to `isomer-srv-topic-env-setup` through the existing topic environment readiness workflow

#### Scenario: Initialized topic management remains delegated
- **WHEN** Topic Actor registration, update, archive, materialization, repair, diagnostics, branch validation, Topic Actor Workspace worktree setup, storage inspection, environment package mutation, or environment verification is needed after topic registration
- **THEN** the Topic Creator delegates that work to `isomer-admin-topic-mgr` or the backed CLI and service surfaces selected by that manager

#### Scenario: Topic Creator finalization can consume topic manager evidence
- **WHEN** Topic Creator finalization summarizes initialized-topic readiness
- **THEN** it may consume `isomer-admin-topic-mgr` status, actor, storage, environment, or validation evidence as delegated owner evidence
- **AND** it does not prescribe a next research command or claim research-paradigm v2 bootstrap readiness from topic-manager evidence alone

#### Scenario: Formal team specialization is separate
- **WHEN** the user asks to adapt or instantiate a Domain Agent Team Template
- **THEN** the Topic Creator hands off to `isomer-admin-topic-team-specialize`
- **AND** it does not treat manual Topic Actor readiness as formal Topic Agent Team Profile material, Agent Workspace readiness, or Agent Team Instance creation

### Requirement: Topic Creator Requires Concrete Research Topic Input
The Topic Creator skill SHALL require concrete user-given Research Topic substance before it derives a topic id, names or creates a Topic Workspace, registers a Research Topic, or writes research intent files.

#### Scenario: Prompt supplies concrete topic
- **WHEN** the user invokes Topic Creator with a concrete Research Topic in the prompt
- **THEN** the skill can use that prompt as topic source material for topic id derivation and later research intent creation
- **AND** it records the source as user prompt material in outputs that summarize topic input

#### Scenario: Markdown file supplies concrete topic
- **WHEN** the user provides a Markdown file that contains a concrete Research Topic or topic brief
- **THEN** the skill can use that file as topic source material after reading it
- **AND** it records the file path or ref as source material for `create-research-intent`

#### Scenario: Existing context supplies concrete topic
- **WHEN** selected Project or registered topic context contains a concrete Research Topic statement
- **THEN** the skill can use that context as topic source material
- **AND** it does not ask the user to restate the topic solely because the topic was not in the immediate prompt

#### Scenario: Missing topic blocks workspace naming
- **WHEN** no concrete Research Topic can be found in the prompt, source files, context, or registered topic statement
- **THEN** the skill asks the user for the actual Research Topic
- **AND** it does not derive a topic slug, choose a Topic Workspace path, create directories, register a topic, write `topic-overview.md`, write `topic-env-gate.md`, write `actor-definitions.md`, or write derived actor env gates

#### Scenario: Generic topic blocks workspace naming
- **WHEN** the only available topic material is a generic placeholder such as `default`, `default Research Topic`, or another non-substantive statement
- **THEN** the skill treats the topic as missing
- **AND** it blocks before creating or overwriting topic workspace or intent material

### Requirement: Topic Creator Separates Topic Input from Research Intent Creation
The Topic Creator skill SHALL separate lower-level topic input resolution from the user-facing `create-research-intent` subcommand, and `create-research-intent` SHALL only own the topic overview.

#### Scenario: Topic input helper resolves source and identity
- **WHEN** Topic Creator needs to prepare a new topic from user source material
- **THEN** it uses a lower-level helper stage to resolve topic source material, derive or confirm a path-safe topic id, and identify the Topic Workspace candidate
- **AND** that helper does not write `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, or derived env gates

#### Scenario: Create research intent writes topic overview only
- **WHEN** `create-research-intent` runs with concrete topic source material and a registered or candidate Topic Workspace
- **THEN** it creates or updates `topic.intent.overview`
- **AND** the default-layout resolved file is `<topic-workspace>/intent/src/topic-overview.md`
- **AND** it does not write `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates`

#### Scenario: Create research intent requires a resolvable Topic Workspace
- **WHEN** no registered or candidate Topic Workspace can resolve `topic.intent.overview`
- **THEN** `create-research-intent` reports a blocker naming the missing Topic Workspace or semantic path evidence
- **AND** it does not guess an intent path

#### Scenario: Create research intent output is user-editable
- **WHEN** `create-research-intent` writes `topic.intent.overview`
- **THEN** the file includes the Research Topic, goal or objectives, scope, success metrics when known, required datasets when known, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source material
- **AND** it records uncertainty as assumptions or open questions instead of inventing missing details

### Requirement: Topic Creator Defines Topic Environment Before Setup
The Topic Creator skill SHALL use `define-topic-env` to create or refine topic environment source intent before `setup-topic-env` derives gates or installs anything.

#### Scenario: Define topic env writes source gate
- **WHEN** `define-topic-env` runs after `topic.intent.overview` exists
- **THEN** it creates or refines `topic.intent.topic_env_requirements`
- **AND** the default-layout resolved file is `<topic-workspace>/intent/src/topic-env-gate.md`
- **AND** it captures topic-level runnable requirements, expected repositories, datasets, tools, runtime assumptions, unavailable resources, success criteria, and open setup questions

#### Scenario: Define topic env waits for verification outside fast-forward
- **WHEN** `define-topic-env` runs outside `fast-forward`
- **THEN** it presents the generated or refined `topic.intent.topic_env_requirements` to the user for verification
- **AND** `setup-topic-env` does not proceed until the user accepts, revises, or supplies equivalent verified topic env intent

#### Scenario: Fast-forward may accept generated topic env gate
- **WHEN** `define-topic-env` runs as part of `fast-forward`
- **THEN** it may continue without an interactive verification stop
- **AND** it reports generated assumptions, open questions, and the resolved topic env gate path before `setup-topic-env` proceeds

#### Scenario: Setup topic env derives and installs from source gate
- **WHEN** `setup-topic-env` runs after a verified or fast-forward accepted `topic.intent.topic_env_requirements` exists
- **THEN** it reads the topic env gate, creates or validates derived setup gates including `topic.env.topic_setup_target_spec`, and delegates installation, Pixi configuration, repository setup, and command verification to the topic env setup owner
- **AND** it reports blockers instead of inventing a missing topic env gate or claiming readiness without derived gate evidence

### Requirement: Topic Creator Defines Actors Before Actor Setup
The Topic Creator skill SHALL use `define-actors` to create actor intent before `setup-actors` materializes actor workspaces or verifies actor env gates.

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
- **THEN** it delegates actor registration and workspace materialization to `isomer-admin-topic-mgr`, creates or validates derived actor env gates at `topic.env.actor_env_gates`, and verifies the gates from each actor's resolved `topic.actors.workspace`
- **AND** the default-layout derived gate file is `<topic-workspace>/intent/derived/actor-env-gates.md`
- **AND** it reports blockers instead of claiming actor readiness when workspace material, derived gates, or gate verification evidence is missing

### Requirement: Topic Creator Fast-Forward Uses Research Intent Step
The Topic Creator `fast-forward` workflow SHALL run topic input resolution, `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, and `setup-actors` in staged order before bootstrap or handoff stages depend on their outputs.

#### Scenario: Fast-forward initializes topic intent before setup
- **WHEN** `fast-forward` runs for a new or partial topic
- **THEN** it resolves concrete topic input, ensures or creates Project Manifest-backed Research Topic and Topic Workspace registration when needed, runs `create-research-intent`, runs `define-topic-env`, runs `setup-topic-env`, runs `define-actors`, runs `setup-actors`, and only then proceeds to bootstrap and start-pack stages
- **AND** `setup-topic-env` consumes `topic.intent.topic_env_requirements` as source intent when deriving operational setup work
- **AND** `setup-actors` consumes `topic.intent.actor_definitions` and verifies derived actor env gates

#### Scenario: Existing topic intent is reused
- **WHEN** `topic.intent.overview` already exists and matches the selected concrete Research Topic
- **THEN** `fast-forward` reuses it
- **AND** it does not overwrite it unless the user asks to revise research intent or the file is stale or inconsistent

#### Scenario: Stale topic intent blocks or repairs
- **WHEN** `topic.intent.overview` exists but conflicts with the selected Research Topic statement
- **THEN** Topic Creator reports the conflict
- **AND** it routes repair through `create-research-intent` after user confirmation rather than silently overwriting the file

### Requirement: Topic Creator Help Presents Research Intent Flow
The Topic Creator skill SHALL present `create-research-intent`, `define-topic-env`, and `define-actors` as separate user-facing subcommands, and SHALL not present `define-topic` as the owner of research intent material.

#### Scenario: Help lists create research intent
- **WHEN** Topic Creator help is printed
- **THEN** it lists `create-research-intent` with wording that says it creates or updates `topic.intent.overview`
- **AND** it explains that `topic.intent.overview` resolves by default to `<topic-workspace>/intent/src/topic-overview.md`

#### Scenario: Help lists env and actor definition steps
- **WHEN** Topic Creator help is printed
- **THEN** it lists `define-topic-env` with wording that says it creates or refines `topic.intent.topic_env_requirements` and waits for user verification unless in `fast-forward`
- **AND** it lists `define-actors` with wording that says it creates or refines `topic.intent.actor_definitions` and defaults to the `operator` actor when actor details are absent

#### Scenario: Help does not advertise define-topic for intent writing
- **WHEN** Topic Creator help is printed
- **THEN** it does not claim that `define-topic` writes topic intent
- **AND** any compatibility mention of `define-topic` routes users to `create-research-intent`

#### Scenario: Validator rejects stale command surface
- **WHEN** operator skill validation scans `isomer-admin-topic-creator`
- **THEN** it requires `create-research-intent`, `define-topic-env`, `define-actors`, the topic-input gate wording, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, and `topic.env.actor_env_gates`
- **AND** it reports stale command guidance that treats `define-topic` as the research intent writer
