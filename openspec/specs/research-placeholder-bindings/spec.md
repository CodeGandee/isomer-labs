# research-placeholder-bindings Specification

## Purpose
Define the production DeepSci placeholder binding pages and validation rules that map skill-local placeholders to accepted research record operations without replacing method prose with concrete storage paths.
## Requirements
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
- **WHEN** `isomer-deepsci-workspace-mgr` builds `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`
- **THEN** it reads each relevant skill's `migrate/placeholders.md` and `placeholder-bindings.md`

#### Scenario: Binding registry records status
- **WHEN** a placeholder target is backed by implemented CLI support
- **THEN** the registry marks that binding available
- **AND** when support is planned, custom-needed, blocked, or deferred, the registry records that status instead of inventing an untracked path

### Requirement: Placeholder Bindings Use Global Isomer CLI
Active non-dev placeholder binding pages SHALL present record CRUD commands using the globally installed `isomer-cli` executable.

#### Scenario: Binding commands omit pixi prefix
- **WHEN** a non-dev `placeholder-bindings.md` row gives an `isomer-cli ext research records` create, list, show, update, or delete command
- **THEN** the command starts with `isomer-cli`
- **AND** it does not start with `pixi run isomer-cli`

#### Scenario: Binding metadata is preserved
- **WHEN** implementation removes the Pixi prefix from placeholder binding command rows
- **THEN** it preserves placeholders, record kinds, semantic labels, profiles, skill names, producer and consumer fields, metadata JSON, body flags, and content names

### Requirement: Placeholder Bindings Use Structured Payload Commands
Active production DeepSci placeholder binding pages SHALL present payload-first research record command shapes for accepted generated artifacts whose Artifact Format Profile or schema/template inputs can be resolved by the artifact-format processing engine.

#### Scenario: Binding names payload contract
- **WHEN** `placeholder-bindings.md` describes a placeholder backed by a structured Artifact Format Profile
- **THEN** the binding names the record kind, semantic label, format profile ref, schema ref or schema-bearing format profile, Jinja2 Markdown template ref when known, expected payload file role, default generated Markdown content name when durable Markdown is expected, and whether CLI naming overrides are allowed
- **AND** production DeepSci defaults use refs under `isomer:deepsci/record-format/*`

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

### Requirement: Placeholder Binding Metadata Uses Active DeepSci Names
Active production DeepSci placeholder binding pages SHALL use `isomer-deepsci-*` skill names in binding metadata and example commands.

#### Scenario: Binding command skill flag uses DeepSci namespace
- **WHEN** a non-dev `placeholder-bindings.md` row gives an `isomer-cli ext research records` create, list, show, update, or delete command for a production DeepSci skill
- **THEN** the command uses the active `isomer-deepsci-<purpose>` value in `--skill`
- **AND** it does not use an old `isomer-rsch-<purpose>` value

#### Scenario: Producer and consumer metadata uses active DeepSci namespace
- **WHEN** a binding row names producer or consumer skill fields for production DeepSci skills
- **THEN** those fields use `isomer-deepsci-*` names for skill-specific producers and consumers
- **AND** historical `isomer-rsch-*` names appear only in passive provenance or migration context

### Requirement: Placeholder Bindings Describe Query-index Metadata
Active production DeepSci placeholder binding pages SHALL describe expected relationship, file, and GUI facet metadata for structured research records.

#### Scenario: Binding names expected relationship metadata
- **WHEN** a `placeholder-bindings.md` row describes a structured record profile that normally consumes, produces, routes to, supports, supersedes, summarizes, or cites other records
- **THEN** the binding guidance names the expected relationship intent and the record refs or payload fields an agent should preserve at write time

#### Scenario: Binding names expected file metadata
- **WHEN** a structured placeholder normally produces or cites durable files, operation-set outputs, rendered Markdown, figures, logs, configs, raw results, or manifests
- **THEN** the binding guidance names the expected file role, semantic label, and source payload field or output location pattern when known

#### Scenario: Binding names expected GUI facets
- **WHEN** a structured placeholder normally carries GUI-relevant ideas, route decisions, metrics, claims, artifact lists, or generic scalar facts
- **THEN** the binding guidance names those expected facets and the profile or payload section that drives extraction

#### Scenario: Skills are not required to hand-author every index row
- **WHEN** a binding describes query-index metadata for a structured profile
- **THEN** it can rely on profile-driven extractors for derived facet rows while still requiring agents to preserve explicit authored refs that only the producing skill knows

### Requirement: Placeholder Bindings Use Payload-file Records
Active production DeepSci placeholder binding pages SHALL describe accepted structured outputs as payload-file records rather than durable generated Markdown files.

#### Scenario: Binding names payload file write
- **WHEN** `placeholder-bindings.md` describes a structured placeholder output
- **THEN** the binding tells the agent to draft a JSON payload file, validate it, and create or update the durable record through `isomer-cli ext research records` so the runtime snapshots the payload into managed record storage

#### Scenario: Binding omits default durable Markdown
- **WHEN** a binding gives the normal accepted-output create or update command
- **THEN** the command does not request default durable Markdown materialization for the structured record

#### Scenario: Binding describes on-demand rendering
- **WHEN** a binding mentions human review of a structured record
- **THEN** it points to an on-demand show, render, query, or explicit export command rather than a normally generated Markdown file path

#### Scenario: Binding validation rejects Markdown state
- **WHEN** the validation harness inspects active production DeepSci placeholder bindings
- **THEN** it reports guidance that treats generated Markdown as canonical structured state, expects generated Markdown to grow across rounds, or requires later agents to parse generated Markdown for structured fields

### Requirement: Placeholder Bindings Name Artifact Lineage
Production DeepSci placeholder binding pages SHALL describe expected canonical lineage metadata for structured records that derive from, revise, select, merge, or follow up prior records.

#### Scenario: Binding row expects parents
- **WHEN** a placeholder binding describes a record that is normally produced from prior artifacts, evidence, decisions, runs, or route state
- **THEN** the binding guidance names the expected parent record refs, parent roles, lineage kind, and whether a generation group is expected

#### Scenario: Binding row expects revision behavior
- **WHEN** a placeholder binding describes a current-state snapshot, selected hypothesis, draft, route decision, or paper-facing artifact that may be revised
- **THEN** the binding guidance states whether agents should use record revision, create a follow-up child, or update only metadata/status

#### Scenario: Binding row separates lineage from relationship hints
- **WHEN** a structured record also needs evidence refs, file refs, claim refs, citations, or GUI facets
- **THEN** the binding guidance distinguishes canonical lineage inputs from optional `--relationships-json`, `--files-json`, and `--index-hints-json`

### Requirement: Idea-stage Bindings Preserve Generation Groups
Idea-stage placeholder bindings SHALL preserve enough lineage information to reconstruct candidate siblings and selected paths.

#### Scenario: Candidate frontier is recorded
- **WHEN** an agent records a candidate idea frontier
- **THEN** the binding guidance requires parent refs to the raw slate or source evidence and a generation group for serious candidates when separate candidate records are created

#### Scenario: Selected hypothesis is recorded
- **WHEN** an agent records a selected hypothesis
- **THEN** the binding guidance requires lineage parents for the selected candidate or pre-idea draft and the decision record that selected it

#### Scenario: Rejected and deferred ideas are recorded
- **WHEN** an agent records rejected or deferred ideas
- **THEN** the binding guidance preserves their shared parent set or generation group so future agents can see they were siblings of the selected route

### Requirement: Placeholder Bindings Declare Idea-bearing Payload Sections
Active production DeepSci placeholder binding pages SHALL declare exact idea-bearing payload sections for structured records that create, select, reject, defer, merge, subsume, or follow up Research Ideas.

#### Scenario: Idea-producing binding names source path pattern
- **WHEN** a `placeholder-bindings.md` row describes an idea-producing structured profile such as raw idea slate, candidate idea frontier, pre-idea draft, selected hypothesis, selected idea draft, rejected/deferred ideas, route decision, or paper-facing idea seed
- **THEN** the binding guidance names the payload section or path pattern that contains idea entries
- **AND** it distinguishes those entries from filter notes, report summaries, decision context, and provenance fields

#### Scenario: Binding command preserves exact source path
- **WHEN** a binding instructs an agent to record canonical Research Idea data for an idea-bearing record
- **THEN** the guidance tells the agent to pass exact item paths such as `$.sections.raw_ideas[0]` to `ext research ideas realize` or record-create idea convenience metadata
- **AND** it forbids collection paths, payload-root paths, generated Markdown paths, and context-only note paths as Primary Idea realization sources
- **AND** it treats executable profile-to-section mapping as owned by the shared CLI/runtime source-fragment registry rather than by free-form skill prose

### Requirement: Placeholder Binding Validation Checks Idea Source Contracts
The placeholder binding validation harness SHALL check active DeepSci idea-producing bindings for exact source-fragment guidance.

#### Scenario: Missing idea source guidance is reported
- **WHEN** validation inspects an active production DeepSci binding for an idea-producing structured profile and no idea-bearing section or source path pattern is documented
- **THEN** validation reports the skill, placeholder, and missing source-fragment guidance

#### Scenario: Broad path guidance is reported
- **WHEN** validation finds a binding that tells agents to realize Primary Ideas to a payload root, list path, generated Markdown file, or context-only section
- **THEN** validation reports the binding as violating the Primary Idea source contract

### Requirement: Placeholder Bindings Declare Display Fields
Active production DeepSci placeholder binding pages SHALL instruct agents to author supported v2 structured payloads with canonical `title` and `summary` fields for payload roots and idea-bearing entries.

#### Scenario: Binding names payload display fields
- **WHEN** `placeholder-bindings.md` describes a structured payload-backed accepted artifact
- **THEN** the binding guidance names the supported v2 profile or schema and required top-level `title` and `summary` fields
- **AND** it describes `summary` as the brief display description consumed by records, query index, and GUI views

#### Scenario: Binding names idea entry display fields
- **WHEN** a binding describes an idea-producing structured profile
- **THEN** the binding guidance states that each idea-bearing entry must include non-empty `title` and `summary`
- **AND** it distinguishes those fields from aliases, source-local labels, route notes, filter notes, and provenance fields

#### Scenario: Binding avoids one-liner guidance
- **WHEN** a production DeepSci placeholder binding gives active create, update, import, or realization guidance
- **THEN** it does not instruct agents to author `one_liner` as an accepted display field
- **AND** any historical mention of `one_liner` is marked as legacy migration context

#### Scenario: Binding avoids v1 guidance for new writes
- **WHEN** a production DeepSci placeholder binding gives active create or update guidance for structured records
- **THEN** it does not instruct agents to use `structured-record.v1` or a v1-backed profile for new accepted records
- **AND** any v1 mention is marked as legacy validation, repair, or migration context

### Requirement: Placeholder Binding Validation Checks Display Guidance
The placeholder binding validation harness SHALL detect missing or stale display-contract guidance in active production DeepSci binding pages.

#### Scenario: Missing payload display guidance is reported
- **WHEN** validation inspects a structured payload binding without required top-level `title` and `summary` guidance
- **THEN** validation reports the skill, placeholder, and missing display-field guidance

#### Scenario: Missing idea display guidance is reported
- **WHEN** validation inspects an idea-producing binding without per-entry `title` and `summary` guidance
- **THEN** validation reports the skill, placeholder, profile, and missing idea display-field guidance

#### Scenario: Stale one-liner guidance is reported
- **WHEN** validation finds active production binding guidance that treats `one_liner` as the accepted display field
- **THEN** validation reports the stale guidance and directs the binding to use `summary`

#### Scenario: Stale v1 guidance is reported
- **WHEN** validation finds active production binding guidance that uses `structured-record.v1` for new accepted structured records
- **THEN** validation reports the stale guidance and directs the binding to use the supported v2 contract

