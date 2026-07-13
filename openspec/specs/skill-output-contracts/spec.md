# skill-output-contracts Specification

## Purpose
Defines the shared Essential Output and Complete Output convention for non-research-paradigm skills.

## Requirements

### Requirement: Skills Split Output Contracts by Audience
Non-research-paradigm skills SHALL define output contracts with separate Essential Output and Complete Output sections, while every active Isomer skill SHALL follow the shared natural-language chat presentation rule.

#### Scenario: Essential and complete sections are present
- **WHEN** a skill outside `skillset/research-paradigm/*` has an output contract
- **THEN** the output contract includes an `Essential Output` section for default user-facing chat content
- **AND** it includes a `Complete Output` section for full handoff, audit, or debug detail

#### Scenario: Research paradigm split remains optional
- **WHEN** a skill is under `skillset/research-paradigm/*`
- **THEN** the Essential and Complete split requirement does not apply to that skill
- **AND** the skill still follows the shared natural-language presentation rule for its chat response
- **AND** its durable research evidence reporting remains governed by research-paradigm skill requirements

### Requirement: Essential Output Is the Default Chat Report
Skills SHALL report Essential Output by default using natural-language Markdown rather than program-style field serialization.

#### Scenario: Default output is concise and natural
- **WHEN** a user invokes a skill without asking for complete or machine-readable output
- **THEN** the skill reports only the essential user-facing information needed to understand the result
- **AND** it leads with the outcome and uses natural prose, descriptive Markdown sections when useful, and genuine lists
- **AND** it does not render named output items as `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record

#### Scenario: Named output items specify content
- **WHEN** an output contract names status, actions, paths, refs, readiness, validation, blockers, or next steps
- **THEN** those names specify information the answer must cover rather than literal chat labels
- **AND** the skill translates internal identifiers into readable domain language unless an exact identifier is itself important evidence

#### Scenario: Bookkeeping stays out of default output
- **WHEN** a default chat report is produced
- **THEN** semantic path diagnostics, storage profiles, provenance refs, full command logs, full readiness matrices, and complete evidence payloads are omitted unless they are essential to explain a blocker or user-facing result

#### Scenario: Complete output availability is discoverable
- **WHEN** important handoff or audit detail is omitted from Essential Output
- **THEN** the skill tells the user that Complete Output is available on request

### Requirement: Complete Output Is Available on Request
Skills SHALL report Complete Output when the user explicitly requests complete or audit-oriented detail, while treating presentation format as a separate choice.

#### Scenario: Natural language requests trigger complete content
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, or full output
- **THEN** the skill reports Complete Output using natural-language Markdown
- **AND** it may start with a short Essential Output summary before the complete details

#### Scenario: Machine-readable requests select serialization
- **WHEN** the user explicitly requests JSON or another machine-readable format
- **THEN** the skill serializes the applicable Essential or Complete information in that requested format
- **AND** it does not treat machine serialization as the default presentation of Complete Output

#### Scenario: Complete output preserves handoff detail
- **WHEN** Complete Output is requested
- **THEN** the skill includes all information needed by downstream operators or services to reconstruct the run, including relevant semantic labels, path diagnostics, evidence, command logs, mutation summaries, blockers, warnings, and next action

### Requirement: Complete Output Is Grouped by Purpose
Complete Output SHALL be grouped by purpose and presented as readable Markdown unless machine-readable serialization was explicitly requested.

#### Scenario: Complete information is grouped
- **WHEN** a skill documents or reports Complete Output
- **THEN** it groups information into descriptive sections such as outcome, identity, paths, readiness, operations, changes, evidence, diagnostics, blockers, and next step
- **AND** it includes only the sections relevant to the result

#### Scenario: Essential output remains human-first
- **WHEN** a skill documents Essential Output
- **THEN** it describes the facts the user needs in natural domain language
- **AND** it avoids exposing low-level storage-profile or path-source detail unless that detail is the result or blocker the user needs to see

### Requirement: Structured Artifacts Remain Distinct from Chat Presentation
Skills SHALL preserve exact schemas for structured artifacts and machine interfaces while summarizing their outcomes naturally in chat.

#### Scenario: Workflow produces a durable structured artifact
- **WHEN** a skill creates or updates a durable record, terminal report, manifest, receipt, configuration file, CLI payload, API payload, or other schema-governed artifact
- **THEN** the artifact follows its exact required field names and serialization
- **AND** the final chat response summarizes the artifact in natural-language Markdown instead of copying its field list as the answer

#### Scenario: Exact field is material evidence
- **WHEN** a field name, status token, identifier, command, or path is necessary to diagnose or hand off the result
- **THEN** the chat response may quote that exact value as evidence within a natural sentence or list item
- **AND** it does not convert the whole response into a pseudo-record

### Requirement: Skill Validation Enforces Natural Chat Presentation
Repository validation SHALL require the shared presentation rule in active skill entrypoints and reject machine-shaped chat contracts without rejecting legitimate structured schemas.

#### Scenario: Active skill contains presentation guidance
- **WHEN** validation inspects an active packaged, development, or Toolbox skill entrypoint
- **THEN** it confirms that normal chat uses natural-language Markdown and treats named output items as semantic coverage rather than literal response keys

#### Scenario: Machine-shaped chat contract is rejected
- **WHEN** a chat-facing Essential or Complete Output section prescribes bullets in the form `` `snake_case`: details `` without an explicit machine-readable or durable-artifact context
- **THEN** validation reports a natural-language presentation diagnostic

#### Scenario: Durable schema is accepted
- **WHEN** field tables, JSON, YAML, TOML, or exact keys occur in a section explicitly defining a durable artifact, CLI or API payload, configuration, receipt, manifest, or requested machine-readable output
- **THEN** validation accepts that structured guidance
