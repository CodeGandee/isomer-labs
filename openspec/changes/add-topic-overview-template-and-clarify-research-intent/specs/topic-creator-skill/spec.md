## ADDED Requirements

### Requirement: Topic Creator Provides a Canonical Topic Overview Template
The Topic Creator skill SHALL include a template file that defines the canonical Markdown structure for `topic.intent.overview`.

#### Scenario: Template file exists in skill bundle
- **WHEN** the `isomer-op-topic-creator` skill bundle is inspected
- **THEN** it contains `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md`
- **AND** the template defines the sections used by `create-research-intent` and `clarify-research-intent`

#### Scenario: Packaged assets include the template
- **WHEN** packaged system skills are materialized
- **THEN** `templates/topic-overview.md` is copied alongside the rest of the `isomer-op-topic-creator` skill

### Requirement: Topic Creator Exposes a Clarify Research Intent Subcommand
The Topic Creator skill SHALL expose a user-facing interactive subcommand named `clarify-research-intent` that refines an existing `topic.intent.overview` by asking focused questions and updating the file directly.

#### Scenario: Clarify research intent is listed as a misc subcommand
- **WHEN** `isomer-op-topic-creator help` is printed
- **THEN** it lists `clarify-research-intent` under Misc Subcommands
- **AND** it describes the subcommand as interactive and scoped to refining the existing topic overview

#### Scenario: Clarify research intent loads existing intent
- **WHEN** the user invokes `clarify-research-intent`
- **THEN** it resolves `topic.intent.overview`
- **AND** it reports a blocker if the overview is missing instead of guessing content

#### Scenario: Clarify research intent scans template coverage
- **WHEN** `clarify-research-intent` runs with an existing overview
- **THEN** it scores each template section as Clear, Partial, or Missing
- **AND** it builds a ranked queue of clarification questions from sections that materially affect topic scope, objectives, assumptions, open questions, or later setup
- **AND** it asks the user to resolve open questions rather than inferring missing substance

#### Scenario: Clarify research intent asks one question at a time
- **WHEN** `clarify-research-intent` has a non-empty question queue
- **THEN** it asks exactly one focused question per turn
- **AND** it presents an option table when there are two to five meaningful alternatives
- **AND** every question includes Motivation, Example, Proposed, and Implication
- **AND** it waits for user input before mutating the overview

#### Scenario: Clarify research intent updates the overview directly
- **WHEN** the user answers a clarification question
- **THEN** the answer is written to the relevant section of `topic.intent.overview`
- **AND** obsolete or contradicted text is replaced rather than duplicated
- **AND** resolved questions are removed from `## Open Questions`
- **AND** unresolved lower-priority questions remain in `## Open Questions` with enough context for later runs

#### Scenario: Clarify research intent is not automatic
- **WHEN** `fast-forward` or `run-to` runs
- **THEN** neither workflow invokes `clarify-research-intent`
- **AND** if the overview is too vague for automatic stages, the workflow stops and recommends `clarify-research-intent`

#### Scenario: Clarify research intent reference page follows clarify-topic style
- **WHEN** `references/clarify-research-intent.md` is inspected
- **THEN** it contains `## Workflow`, `## Coverage and Clarity Scan`, `## Question Format`, `## Sequential Clarification Loop`, `## Direct Topic Overview Integration`, `## Prerequisite Artifacts`, and `## Guardrails` sections
- **AND** its structure matches `isomer-op-topic-team-specialize/references/clarify-topic.md`
- **AND** its coverage categories reflect the Topic Creator template sections rather than team-specialization concerns

## MODIFIED Requirements

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
- **AND** it populates the file from `templates/topic-overview.md`
- **AND** it strips the template's `> Example:` blocks from the written file
- **AND** it does not write `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates`

#### Scenario: Create research intent requires a resolvable Topic Workspace
- **WHEN** no registered or candidate Topic Workspace can resolve `topic.intent.overview`
- **THEN** `create-research-intent` reports a blocker naming the missing Topic Workspace or semantic path evidence
- **AND** it does not guess an intent path

#### Scenario: Create research intent output is user-editable
- **WHEN** `create-research-intent` writes `topic.intent.overview`
- **THEN** the file includes the sections from `templates/topic-overview.md`
- **AND** sections with available substance are filled with the Research Topic, goal or objectives, scope, success metrics when known, required datasets when known, explicitly mentioned repositories, explicitly mentioned libraries or tools, assumptions, open questions, and source material
- **AND** sections without available substance are kept as empty headings
- **AND** the `## Additional Requirements` section and its `### Preferences` and `### Constraints` subsections are left in a placeholder state for the user to fill in, even when other sections can be partially populated
- **AND** it records uncertainty as assumptions or open questions instead of inventing missing details

### Requirement: Topic Creator Help Presents Research Intent Flow
The Topic Creator skill SHALL present `create-research-intent`, `define-topic-env`, `define-actors`, and `clarify-research-intent` as separate user-facing subcommands, and SHALL not present `define-topic` as the owner of research intent material.

#### Scenario: Help lists create research intent
- **WHEN** Topic Creator help is printed
- **THEN** it lists `create-research-intent` with wording that says it creates or updates `topic.intent.overview` from the canonical template
- **AND** it explains that `topic.intent.overview` resolves by default to `<topic-workspace>/intent/src/topic-overview.md`

#### Scenario: Help lists clarify research intent
- **WHEN** Topic Creator help is printed
- **THEN** it lists `clarify-research-intent` with wording that says it interactively refines an existing `topic.intent.overview`

#### Scenario: Help lists env and actor definition steps
- **WHEN** Topic Creator help is printed
- **THEN** it lists `define-topic-env` with wording that says it creates or refines `topic.intent.topic_env_requirements` and waits for user verification unless in `fast-forward`
- **AND** it lists `define-actors` with wording that says it creates or refines `topic.intent.actor_definitions` and defaults to the `operator` actor when actor details are absent

#### Scenario: Help does not advertise define-topic for intent writing
- **WHEN** Topic Creator help is printed
- **THEN** it does not claim that `define-topic` writes topic intent
- **AND** any compatibility mention of `define-topic` routes users to `create-research-intent`

#### Scenario: Validator rejects stale command surface
- **WHEN** operator skill validation scans `isomer-op-topic-creator`
- **THEN** it requires `create-research-intent`, `clarify-research-intent`, `define-topic-env`, `define-actors`, the topic-input gate wording, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, and `topic.env.actor_env_gates`
- **AND** it reports stale command guidance that treats `define-topic` as the research intent writer
