## ADDED Requirements

### Requirement: Skill Overview Template Tracks Source Template
The Topic Creator skill SHALL keep its bundled `templates/topic-overview.md` identical to `tests/topics/topic-template.md` so that `topic.intent.overview` always follows the current project convention.

#### Scenario: Template matches the source file
- **WHEN** the skill bundle is inspected or `create-research-intent` loads the canonical template
- **THEN** `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md` contains the same sections and guidance as `tests/topics/topic-template.md`
- **AND** those sections are `Research Topic`, `Motivation`, `Topic Breakdown` with `Do's` and `Don'ts`, `Expected Outcome`, and `Related Links`

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
- **AND** it does not write `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates`

#### Scenario: Create research intent requires a resolvable Topic Workspace
- **WHEN** no registered or candidate Topic Workspace can resolve `topic.intent.overview`
- **THEN** `create-research-intent` reports a blocker naming the missing Topic Workspace or semantic path evidence
- **AND** it does not guess an intent path

#### Scenario: Create research intent output is user-editable
- **WHEN** `create-research-intent` writes `topic.intent.overview`
- **THEN** the file includes the Research Topic, Motivation, Topic Breakdown with `Do's` and `Don'ts`, Expected Outcome, and Related Links
- **AND** it strips any template `>` example blocks from the written file
- **AND** it records uncertainty as assumptions or open questions instead of inventing missing details

### Requirement: Topic Creator Help Presents Research Intent Flow
The Topic Creator skill SHALL present `create-research-intent`, `define-topic-env`, and `define-actors` as separate user-facing subcommands, and SHALL not present `define-topic` as the owner of research intent material.

#### Scenario: Help lists create research intent
- **WHEN** Topic Creator help is printed
- **THEN** it lists `create-research-intent` with wording that says it creates or updates `topic.intent.overview` from the canonical template
- **AND** it explains that `topic.intent.overview` resolves by default to `<topic-workspace>/intent/src/topic-overview.md`
- **AND** it mentions the new template sections `Research Topic`, `Motivation`, `Topic Breakdown`, `Expected Outcome`, and `Related Links`

#### Scenario: Help lists env and actor definition steps
- **WHEN** Topic Creator help is printed
- **THEN** it lists `define-topic-env` with wording that says it creates or refines `topic.intent.topic_env_requirements` and waits for user verification unless in `fast-forward`
- **AND** it lists `define-actors` with wording that says it creates or refines `topic.intent.actor_definitions` and defaults to the `operator` actor when actor details are absent

#### Scenario: Help does not advertise define-topic for intent writing
- **WHEN** Topic Creator help is printed
- **THEN** it does not claim that `define-topic` writes topic intent
- **AND** any compatibility mention of `define-topic` routes users to `create-research-intent`

### Requirement: Validator rejects stale command surface
The Topic Creator skill validator SHALL require the new research-intent subcommand and template language and SHALL reject stale guidance that treats `define-topic` as the research intent writer.

#### Scenario: Validator requires updated create-research-intent terms
- **WHEN** operator skill validation scans `isomer-op-topic-creator`
- **THEN** `create-research-intent.md` required terms cover `Research Topic`, `Motivation`, `Topic Breakdown`, `Do's`, `Don'ts`, `Expected Outcome`, `Related Links`, and stripping of `>` example blocks

#### Scenario: Validator requires updated clarify-research-intent terms
- **WHEN** operator skill validation scans `isomer-op-topic-creator`
- **THEN** `clarify-research-intent.md` required terms cover the new coverage categories: `Research Topic`, `Motivation`, `Topic Breakdown`, `Do's`, `Don'ts`, `Expected Outcome`, and `Related Links`

#### Scenario: Validator still rejects stale define-topic guidance
- **WHEN** operator skill validation scans `isomer-op-topic-creator`
- **THEN** it requires `create-research-intent`, `define-topic-env`, `define-actors`, the topic-input gate wording, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, and `topic.env.actor_env_gates`
- **AND** it reports stale command guidance that treats `define-topic` as the research intent writer
