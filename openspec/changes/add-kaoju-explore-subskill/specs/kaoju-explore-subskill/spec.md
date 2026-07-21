# kaoju-explore-subskill Specification

## ADDED Requirements

### Requirement: Explore subskill exists as a protected Kaoju member
The system SHALL provide a protected subskill `isomer-kaoju-explore` below `isomer-ext-kaoju-entrypoint` for interactive, read-only survey planning.

#### Scenario: Subskill is discoverable
- **WHEN** the packaged Kaoju entrypoint is inspected
- **THEN** it contains `subskills/isomer-kaoju-explore/SKILL-MAIN.md`
- **AND** it contains `subskills/isomer-kaoju-explore/agents/openai.yaml`
- **AND** it does not contain `subskills/isomer-kaoju-explore/artifact-bindings.md`

#### Scenario: Subskill is declared in the process contract
- **WHEN** the Kaoju process contract is loaded
- **THEN** `isomer-kaoju-explore` appears in `protected_members`
- **AND** its `member_name` is `explore`
- **AND** its `invocation_designator` is `isomer-ext-kaoju-entrypoint->explore`

### Requirement: Explore maintains an in-memory planning discussion
The explore subskill SHALL inspect existing Kaoju and project state and ask the user targeted clarification questions without writing durable artifacts.

#### Scenario: Default exploration mode
- **WHEN** a user invokes `$isomer-ext-kaoju-entrypoint use explore to <task>`
- **THEN** the subskill loads the default `auto` exploration mode
- **AND** it inspects read-only context such as the current Research Topic, prior Direction Set, reading lists, examined items, and active Runs
- **AND** it builds an in-memory coverage map of planning dimensions

#### Scenario: No artifacts by default
- **WHEN** the explore subskill is running
- **THEN** it does not invoke `project artifacts put` or `project artifacts revise`
- **AND** it does not begin a Run
- **AND** it does not create a Gate or Service Request
- **AND** it does not write files to the Topic Workspace or project directory

### Requirement: Explore asks up to five clarification questions
The explore subskill SHALL present sequential questions with a proposed option, pros/cons, motivation, example, and implication. Batch mode is available only when the user explicitly requests it.

#### Scenario: Sequential question format
- **WHEN** the subskill needs a clarification
- **THEN** it presents exactly one question at a time
- **AND** it includes a proposed option and a short pros/cons table
- **AND** it states why the answer matters and what happens downstream

#### Scenario: Question cap
- **WHEN** the subskill has asked five questions
- **THEN** it stops asking and produces a plan from the answers collected

### Requirement: Explore returns an agreed plan on consent
The explore subskill SHALL summarize the agreed plan and recommended public invocation, then ask the user to confirm before any durable work begins.

#### Scenario: Plan summary
- **WHEN** no material ambiguity remains or the user signals proceed
- **THEN** the subskill returns a plan containing the selected command, scope, evidence strategy, output form, risks, and exact public invocation

#### Scenario: Consent is required
- **WHEN** the explore subskill proposes a plan
- **THEN** it asks the user for explicit confirmation
- **AND** it does not proceed to the selected command without that confirmation

### Requirement: Explore supports context-specific subcommands
The explore subskill SHALL define subcommands for different Kaoju contexts so that future expansion does not require new top-level entrypoint commands.

#### Scenario: Subcommand inventory
- **WHEN** the subskill is inspected
- **THEN** it declares subcommands including `auto`, `directions`, `reading-list`, `intake`, `comparison`, `trial`, `paper`, `wiki`, and `help`
- **AND** each subcommand owns a page under `subskills/isomer-kaoju-explore/commands/`

#### Scenario: Auto routing
- **WHEN** the user does not name a context
- **THEN** the `auto` subcommand selects the most relevant context from the prompt and existing state
- **AND** it routes to that context's subcommand page

### Requirement: Explore distinguishes itself from welcome
The explore subskill SHALL be scoped to planning a concrete task, while `isomer-ext-kaoju-welcome` remains scoped to newcomer orientation.

#### Scenario: Welcome does not plan
- **WHEN** a user asks for orientation or command learning
- **THEN** `isomer-ext-kaoju-welcome` answers without invoking `isomer-kaoju-explore`

#### Scenario: Explore does not teach
- **WHEN** a user invokes `explore`
- **THEN** it does not reproduce the curated onboarding patterns of `isomer-ext-kaoju-welcome`
- **AND** it focuses on resolving the supplied task into an executable plan
