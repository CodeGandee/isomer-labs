## ADDED Requirements

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
- **THEN** it delegates actor registration and workspace materialization to the Topic Workspace Manager, creates or validates derived actor env gates at `topic.env.actor_env_gates`, and verifies the gates from each actor's resolved `topic.actors.workspace`
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
