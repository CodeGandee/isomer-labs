## ADDED Requirements

### Requirement: Kaoju Create-Topic Initializes Extension-Local Derived Intent
The public Kaoju `create-topic` command SHALL coordinate generic topic prerequisites and complete extension-local derived-intent initialization without adding Kaoju behavior to the generic Topic Creator.

#### Scenario: Create-topic starts from concrete topic substance
- **WHEN** a user invokes Kaoju `create-topic` for a new concrete Research Topic
- **THEN** the entrypoint delegates Project, Topic Workspace, Workspace Runtime, and `topic.intent.overview` prerequisites to `isomer-op-entrypoint->topic-create`
- **AND** it passes no Kaoju mindset seed, template tree, schema, or extension path into the generic owner

#### Scenario: Generic prerequisites become ready
- **WHEN** the selected Topic Workspace has a concrete overview and ready Workspace Runtime
- **THEN** the entrypoint invokes `isomer-kaoju-topic-creator` to create missing Mindset Sources and invoke the typed template ensure-defaults operation
- **AND** successful completion reports all three mindset keys plus content and LaTeX `main` stock and their plural exchange paths

#### Scenario: Initialization is repeated
- **WHEN** the user repeats `create-topic` for a partially or fully initialized Kaoju topic
- **THEN** the protected owner validates and preserves each valid existing Source, named template record, and protected edited export
- **AND** it resumes only missing work and reports per-resource created, preserved, invalid, drifted, and conflicting posture

#### Scenario: Ordinary research action finds missing initialization
- **WHEN** a concrete Kaoju research action selects a topic that never completed explicit Kaoju initialization
- **THEN** the entrypoint preserves missing-mindset optionality and packaged writing-template fallback behavior
- **AND** it does not invoke topic create-missing, ensure-defaults, or exchange materialization implicitly

#### Scenario: Kaoju installation is inspected
- **WHEN** the Kaoju pack is installed or upgraded
- **THEN** installation makes packaged mindset and writing-template defaults available and validates their package contract
- **AND** it does not enumerate Topic Workspaces or create topic-owned Sources, records, exports, or bindings

### Requirement: Kaoju Explains and Applies Editable Derived Intent
The public Kaoju entrypoint SHALL explain recognized derived materials after topic initialization and SHALL route a later request to apply user edits according to each material's semantic owner and lifecycle.

#### Scenario: Topic initialization completes
- **WHEN** explicit Kaoju `create-topic` creates or preserves the selected topic's Mindset Sources, named content and LaTeX `main` stock, and safe exports
- **THEN** the agent reports the actual recognized `intent/derived` paths, intended usage, supported adjustments, validation constraints, and application route for each material
- **AND** it explains that adjustments may occur before the next initialization stage or after later Topic Workspace use

#### Scenario: Initialization reaches its requested boundary
- **WHEN** topic initialization and its derived-material handoff succeed
- **THEN** the agent stops before environment setup, actor setup, a research Run, paper drafting, or another later stage unless the user's original request explicitly included that target
- **AND** the handoff tells the user how to request application after editing supported material

#### Scenario: User asks to apply modified derived materials
- **WHEN** the user says “I have modified the derived materials, now apply them” or equivalent wording for one selected topic
- **THEN** the entrypoint inventories recognized changed material, performs a complete read-only preflight, validates Mindset Sources, and routes changed writing-template exports to the write owner for assessed typed promotion
- **AND** it returns per-material validated, promoted, unchanged, invalid, conflicting, or unsupported posture

#### Scenario: Generated derived output was edited
- **WHEN** the apply request finds a changed environment target specification or another service-owned generated derived file
- **THEN** the agent identifies the corresponding source intent and owning regeneration route
- **AND** it does not treat the changed generated file as an authoritative direct override

#### Scenario: Apply completes for future work
- **WHEN** one or more supported derived changes are accepted
- **THEN** the agent states that later Runs and newly created or explicitly reinitialized paper work will observe the new state
- **AND** active and completed Runs, Mindset Records, paper drafts, TeX snapshots, PDFs, and other historical Artifacts remain unchanged

#### Scenario: User requests retrospective compatibility
- **WHEN** the user explicitly asks to make past material compatible with newer derived intent
- **THEN** the agent requires exact historical targets and desired outputs and routes a separate revision or regeneration workflow
- **AND** it creates new revisions or derived Artifacts with provenance rather than rewriting old snapshots or unrelated past material

## MODIFIED Requirements

### Requirement: Kaoju Write Guidance Is MyST-First
`isomer-kaoju-write` SHALL treat mutable named topic-owned MyST template records and MyST draft Artifacts as canonical, immutable packaged templates as fallback inputs, and exported template directories, Markdown, TeX, and PDF as non-canonical exchange, review, or publication material.

#### Scenario: Write skill starts a paper with topic stock
- **WHEN** accepted audit and synthesis inputs are available and the explicit or role-local default content template resolves to topic stock
- **THEN** the skill interprets its current tree and entrypoint metadata and creates paper state with the selected stable ref, state token, and observed digest
- **AND** it does not create legacy `kaoju:writing-template` state

#### Scenario: Write skill starts a paper with packaged fallback
- **WHEN** accepted audit and synthesis inputs are available, no content template is explicit, and topic-owned content `main` is verified absent
- **THEN** the skill consumes checked packaged content `main` and records its packaged identity, resource version, digest, and fallback source
- **AND** it does not create a named topic record or write `intent/derived/writing-templates`

#### Scenario: TeX requires semantic repair
- **WHEN** the paper service initializes TeX from current MyST paper state and selected topic-owned or packaged LaTeX stock
- **THEN** the write skill inspects and repairs directives, tables, citations, floats, raw blocks, and venue structure before build readiness
- **AND** a compiler exit does not replace inspection

#### Scenario: User requests export without a name
- **WHEN** the user asks to get, edit, or export a content or LaTeX template without naming one
- **THEN** the skill selects role-local topic-owned or packaged-default `main` and exports to `<topic.paper.template_exchange_root>/<kind>/main/`
- **AND** the resolved built-in path uses `intent/derived/writing-templates`, and the skill reports that the directory is non-canonical

#### Scenario: Unnamed database update finds an edited export
- **WHEN** the user asks to update the current database template without any locator and exactly one registered export of the selected role is edited
- **THEN** the skill selects that export and its recorded target name before constructing the update candidate
- **AND** it does not prefer topic role-local `main` merely because it exists

#### Scenario: Unnamed database update falls back to topic main
- **WHEN** no eligible edited export exists and the current Topic Workspace contains `<topic.paper.template_exchange_root>/<kind>/main/`
- **THEN** the skill uses that directory as source and target name `main`, subject to consistent role and export metadata
- **AND** it does not require database `main` to exist before selecting the source

#### Scenario: Unnamed database update remains ambiguous
- **WHEN** several edited exports qualify, an edited export has inconsistent identity, or neither an edited export nor selected-role topic `main` exists
- **THEN** the skill asks the user to select a concrete template or path and presents discovered candidates
- **AND** packaged fallback does not authorize creation or update of mutable topic stock

#### Scenario: Explicit source bypasses discovery
- **WHEN** the database-update request names a template, canonical ref, template path, or export path
- **THEN** the skill validates and uses the explicit source and performs agentic construction as needed
- **AND** it does not run implicit source discovery or packaged fallback

#### Scenario: User requests an explicit saved copy
- **WHEN** the user asks to preserve the current template before an edit
- **THEN** the skill chooses or confirms a new ordinary template name and invokes create-from-template
- **AND** it does not attach snapshot type or lifecycle metadata

#### Scenario: Agent chooses to preserve a state
- **WHEN** the agent determines that an explicit saved copy is useful and the request authorizes that additional named template
- **THEN** it reports the chosen name and creates the copy before mutation
- **AND** ordinary updates do not create copies silently

#### Scenario: User restores from a named copy
- **WHEN** the user asks to restore or replace target `main` from another name
- **THEN** the skill invokes exact update-from-template with current target state token
- **AND** the source named template remains unchanged

#### Scenario: User requests a merge
- **WHEN** the user asks to merge current target state with another named template or editable directory
- **THEN** the skill interprets both inputs, asks about material ambiguity, constructs a new candidate, and invokes low-level update
- **AND** it does not invoke generic CLI merge or treat the source name as a special snapshot
