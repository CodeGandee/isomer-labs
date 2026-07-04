## MODIFIED Requirements

### Requirement: Skill Placeholder Binding Pages
The system SHALL provide a `placeholder-bindings.md` page for each active production DeepSci research skill that defines `migrate/placeholders.md`.

#### Scenario: Binding page exists beside placeholder registry
- **WHEN** an active production DeepSci research skill contains `migrate/placeholders.md`
- **THEN** the skill also contains `placeholder-bindings.md`

#### Scenario: Binding page preserves placeholder tokens
- **WHEN** `placeholder-bindings.md` lists a placeholder from `migrate/placeholders.md`
- **THEN** it preserves the exact placeholder token as metadata and does not replace it with a concrete path in workflow prose

#### Scenario: Binding page points to storage operations
- **WHEN** an agent needs to create, read, update, or archive a durable placeholder output
- **THEN** `placeholder-bindings.md` names the storage item class, default semantic label, artifact profile, and `isomer-cli ext research records` command shape to use

### Requirement: Placeholder Binding Coverage Validation
The system SHALL validate that active production DeepSci placeholder binding pages cover the placeholders registered by each skill.

#### Scenario: Missing binding page is reported
- **WHEN** validation inspects an active production DeepSci skill with `migrate/placeholders.md` and no `placeholder-bindings.md`
- **THEN** validation reports the missing binding page

#### Scenario: Missing placeholder binding is reported
- **WHEN** validation finds a placeholder in `migrate/placeholders.md` that is absent from `placeholder-bindings.md`
- **THEN** validation reports the unbound placeholder and the skill that owns it

#### Scenario: Extra placeholder binding is reported
- **WHEN** validation finds a placeholder in `placeholder-bindings.md` that is not registered in `migrate/placeholders.md`
- **THEN** validation reports the extra binding so migration drift can be repaired

### Requirement: Research Workspace Manager Binding Aggregation
The research workspace manager skill SHALL treat local placeholder binding pages as the source material for the post-specialization binding registry.

#### Scenario: Workspace manager reads binding pages
- **WHEN** `isomer-rsch-workspace-mgr` builds `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`
- **THEN** it reads each relevant skill's `migrate/placeholders.md` and `placeholder-bindings.md`

#### Scenario: Binding registry records status
- **WHEN** a placeholder target is backed by implemented CLI support
- **THEN** the registry marks that binding available
- **AND** when support is planned, custom-needed, blocked, or deferred, the registry records that status instead of inventing an untracked path

### Requirement: Placeholder Bindings Use Structured Payload Commands
Active production DeepSci placeholder binding pages SHALL present payload-first research record command shapes for accepted generated artifacts whose Artifact Format Profile or schema/template inputs can be resolved by the artifact-format processing engine.

#### Scenario: Binding names payload contract
- **WHEN** `placeholder-bindings.md` describes a placeholder backed by a structured Artifact Format Profile
- **THEN** the binding names the record kind, semantic label, format profile ref, schema ref or schema-bearing format profile, Jinja2 Markdown template ref when known, expected payload file role, default generated Markdown content name when durable Markdown is expected, and whether CLI naming overrides are allowed
- **AND** DeepScientist-provided production defaults use refs under `isomer:deepsci/record-format/*`

#### Scenario: Binding create command uses payload file
- **WHEN** a binding row gives the normal create command for an accepted structured research artifact
- **THEN** the command uses `isomer-cli ext research records create` with `--format-profile` or explicit schema/template inputs and a payload file
- **AND** it includes `--render markdown` when the structured artifact is expected to materialize a Markdown view
- **AND** it does not use direct `--body-file` Markdown authoring as the normal accepted-artifact path for that structured format

#### Scenario: Binding includes validation step
- **WHEN** a binding page explains how an agent should create a structured research record
- **THEN** it includes or references a validation step using `isomer-cli ext research records validate` before the final create or update operation

#### Scenario: Binding preserves stable metadata
- **WHEN** placeholder binding command shapes move from direct body files to payload-first records
- **THEN** they preserve placeholder token, record kind, semantic label, format profile ref, skill name, producer, consumer, topic actor metadata hooks, lifecycle refs when applicable, metadata JSON, default generated content name, naming override policy, and content naming intent

#### Scenario: Binding validation checks generated content naming
- **WHEN** validation inspects an active production DeepSci structured binding that expects durable Markdown materialization
- **THEN** it reports the binding if no default generated content name exists and no CLI naming override is explicitly allowed

### Requirement: Placeholder Bindings Exclude Direct Body Sources
Active production DeepSci placeholder binding pages SHALL exclude direct body-file authoring from accepted structured artifact guidance.

#### Scenario: Structured binding omits direct body command
- **WHEN** a placeholder binding row describes an accepted structured research artifact
- **THEN** the normal create or update command uses a JSON payload file
- **AND** it does not include `--body` or `--body-file` as the source for that accepted structured artifact

#### Scenario: Structured format does not rely on Markdown parsing
- **WHEN** a placeholder binding names a structured format profile or schema/template inputs and generated Markdown output
- **THEN** the binding requires the agent to author the JSON payload that drives the generated Markdown
- **AND** it does not require later agents, validators, or GUIs to extract structured fields from the generated Markdown body

### Requirement: Placeholder Binding Validation Covers Payload-first Contracts
The placeholder binding validation harness SHALL check payload-first guidance for active production DeepSci bindings that describe structured records.

#### Scenario: Missing payload command is reported
- **WHEN** validation inspects an active production DeepSci `placeholder-bindings.md` entry for a structured format and no payload-file create or update command is present
- **THEN** validation reports the placeholder, skill, and missing structured command shape

#### Scenario: Direct body command is reported for structured format
- **WHEN** validation inspects an active production DeepSci binding row for a structured format and the normal accepted-artifact command uses direct `--body-file` Markdown authoring
- **THEN** validation reports the row

#### Scenario: Bare profile flag is reported
- **WHEN** validation inspects an active production DeepSci structured binding command that uses `--profile` for an Artifact Format Profile ref
- **THEN** validation reports the command and directs the binding to use `--format-profile`

#### Scenario: Missing validation step is reported
- **WHEN** an active production DeepSci binding page provides structured payload create or update guidance without a validation step or validation command reference
- **THEN** validation reports the missing validation guidance for that skill

## ADDED Requirements

### Requirement: Placeholder Bindings Use Production Skill Names
Active production DeepSci placeholder binding pages SHALL use suffixless skill identities in skill, producer, consumer, and example command metadata.

#### Scenario: Binding metadata omits v2 suffixes
- **WHEN** an active production DeepSci `placeholder-bindings.md` file is inspected
- **THEN** its `--skill`, `--producer`, `--consumer`, metadata JSON, and prose examples use `isomer-rsch-*` names without `-v2`

#### Scenario: Binding paths use production root
- **WHEN** active docs or validation guidance points to placeholder binding pages
- **THEN** it uses `skillset/research-paradigm/deepsci/*/placeholder-bindings.md` paths rather than `skillset/research-paradigm/v2/*/placeholder-bindings.md`
