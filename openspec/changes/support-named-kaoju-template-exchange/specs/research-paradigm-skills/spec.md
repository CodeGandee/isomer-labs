## MODIFIED Requirements

### Requirement: Kaoju Skills Separate Research Judgment from Deterministic Operations
Production Kaoju skills SHALL own arbitrary template construction, interpretation, and reconciliation while delegating named-template CRUD, export inspection, state-token checks, integrity validation, and atomic mutation to typed Isomer CLI and owner services.

#### Scenario: Skill performs research judgment
- **WHEN** a procedure selects a direction, appraises a source, forms a claim, writes prose, interprets a template tree, reconciles template changes, identifies entrypoints, repairs TeX semantics, or recommends a trial design
- **THEN** the responsible Kaoju skill performs and records that judgment with evidence and actor provenance

#### Scenario: Skill needs deterministic support
- **WHEN** the procedure lists, reads, creates, updates, copies, replaces, archives, or exports a named template; calculates digests; resolves a managed path; edits allowed metadata; initializes a conversion; executes a trial; or builds a PDF
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned state tokens, paths, digests, diagnostics, and refs
- **AND** it does not directly update SQL or managed Artifact files

#### Scenario: Arbitrary directory drives an update
- **WHEN** a user asks to update a database template from an arbitrary directory
- **THEN** the Kaoju skill inspects the source and current target, prepares the intended candidate, records its assessment, and invokes low-level template update with the expected target state token
- **AND** it does not delegate high-level conversion or merge decisions to isomer-cli

#### Scenario: Known named source replaces target
- **WHEN** the user explicitly asks to replace one named template with another known named template
- **THEN** the skill invokes exact named-template replacement after reporting source and target
- **AND** it does not construct a merge unless the user requested one

### Requirement: Kaoju Write Guidance Is MyST-First
`isomer-kaoju-write` SHALL treat mutable named MyST-oriented template records and MyST draft Artifacts as canonical and SHALL treat exported template directories, Markdown, TeX, and PDF as non-canonical exchange, review, or publication material.

#### Scenario: Write skill starts a paper
- **WHEN** accepted audit and synthesis inputs are available
- **THEN** the skill resolves the explicitly named template or canonical `main`, interprets its current tree and entrypoint metadata, and creates paper state with the selected stable ref and observed digest
- **AND** it does not create legacy `kaoju:writing-template` state

#### Scenario: User requests export without a name
- **WHEN** the user asks to get, edit, or export the paper template without naming one
- **THEN** the skill selects canonical `main` and exports to resolved `intent/derived/writing-template/main/`
- **AND** it reports that the directory is non-canonical

#### Scenario: Unnamed database update finds an edited export
- **WHEN** the user asks to update the current database template without any locator and exactly one registered export is edited
- **THEN** the skill selects that export and its recorded target name before constructing the update candidate
- **AND** it does not prefer topic `main/` merely because it exists

#### Scenario: Unnamed database update falls back to topic main
- **WHEN** no eligible edited export exists and the current Topic Workspace contains `intent/derived/writing-template/main/`
- **THEN** the skill uses that directory as source and target name `main`, subject to consistent export metadata
- **AND** it does not require database `main` to exist before selecting the source

#### Scenario: Unnamed database update remains ambiguous
- **WHEN** several edited exports qualify, an edited export has inconsistent identity, or neither an edited export nor topic `main/` exists
- **THEN** the skill asks the user to select a concrete template or path and presents discovered candidates
- **AND** it does not choose by timestamp or unrelated database record order

#### Scenario: Explicit source bypasses discovery
- **WHEN** the database-update request names a template, canonical ref, template path, or export path
- **THEN** the skill validates and uses the explicit source and performs agentic construction as needed
- **AND** it does not run implicit source discovery

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

#### Scenario: TeX requires semantic repair
- **WHEN** the paper service initializes TeX from current MyST template state
- **THEN** the write skill inspects and repairs directives, tables, citations, floats, raw blocks, and venue structure before build readiness
- **AND** a compiler exit does not replace inspection
