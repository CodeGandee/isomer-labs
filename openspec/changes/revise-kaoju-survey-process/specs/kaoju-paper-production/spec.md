## ADDED Requirements

### Requirement: Paper Drafting Requires Accepted Audit and Synthesis
The system SHALL start canonical paper drafting only from an accepted Audit Report and the exact accepted synthesis revisions needed for the paper.

#### Scenario: Required inputs are ready
- **WHEN** `draft-paper` resolves an accepted Audit Report, Field Summary, Related-Work Catalog, and Claim Status Table for the requested paper line
- **THEN** it records those exact revisions as paper input refs
- **AND** optional source digests, ledgers, dossiers, comparisons, and trial results are included only when they have the required accepted audit disposition

#### Scenario: Required input is missing or ambiguous
- **WHEN** a required input is missing, unaudited, stale, or has competing accepted candidates
- **THEN** drafting pauses with the affected refs and required resolution
- **AND** the system does not recover by parsing an arbitrary rendered Markdown file or choosing solely by timestamp

### Requirement: MyST Is the Canonical Paper Format
The system SHALL use MyST as the only canonical content format for new Kaoju papers.

#### Scenario: Initial paper structure is authored
- **WHEN** accepted inputs are ready for paper drafting
- **THEN** the write skill creates `kaoju:paper-structure-myst` with the intended sections, claim and source placeholders, citation roles, display placeholders, and evidence boundaries
- **AND** the structure is stored as a MyST `.md` file with a registered Artifact Core Record

#### Scenario: Paper structure is filled
- **WHEN** the actor accepts the structure or requests the paper draft
- **THEN** the write skill creates `kaoju:paper-draft-myst` by filling the structure from accepted evidence
- **AND** unsupported, contradicted, or unresolved claims remain qualified or visibly marked rather than being converted into confident prose

#### Scenario: Legacy LaTeX exists
- **WHEN** a topic contains `kaoju:survey-manuscript` or `kaoju:writing-template` records
- **THEN** the system keeps them readable as historical records
- **AND** it does not infer canonical MyST content from them without an explicit actor-authorized intake and provenance record

### Requirement: Paper Claims and Revisions Remain Traceable
Canonical paper work SHALL maintain `kaoju:citation-map` and `kaoju:paper-revision-log` artifacts that connect paper content to accepted evidence and prior revisions.

#### Scenario: Claim-bearing draft content is recorded
- **WHEN** the write skill adds or revises a claim, citation, table, figure, limitation, or comparison in the MyST draft
- **THEN** the citation map records the MyST locator, claim or display role, accepted evidence refs, and support or contradiction posture
- **AND** the revision log records the actor, reason, input revisions, output revision, affected sections, and validation result

#### Scenario: Evidence is withdrawn or superseded
- **WHEN** an accepted input is later withdrawn, refuted, or superseded
- **THEN** paper status reports the affected draft locations through the citation map
- **AND** the current draft is not represented as publication-ready until the impact is resolved and audited

### Requirement: Markdown Is a Derived Review View
The system SHALL permit a deterministic `kaoju:paper-draft-md` review view derived from the current MyST draft and SHALL never treat it as canonical paper state.

#### Scenario: Markdown review view is requested
- **WHEN** the actor requests a plain Markdown view
- **THEN** the paper service derives it from a selected `kaoju:paper-draft-myst` revision, records the source revision and converter diagnostics, and registers `kaoju:paper-draft-md`
- **AND** MyST directives or constructs that cannot be represented faithfully are reported explicitly

#### Scenario: Derived Markdown is edited
- **WHEN** a Markdown review export differs from its source after external editing
- **THEN** the system does not apply it as canonical content
- **AND** it directs the actor to the MyST template or draft editing path

### Requirement: MyST Templates Can Be Exported for Manual Editing
The system SHALL export the current MyST paper structure or template to an actor-selected directory together with a versioned manifest.

#### Scenario: Template export succeeds
- **WHEN** the actor requests a template export and supplies an authorized path or accepts a resolved Topic Workspace path
- **THEN** the system writes the MyST template as a `.md` file, writes `kaoju:paper-template-manifest`, and registers `kaoju:paper-template-export`
- **AND** the manifest records source record id and revision, base digest, source-digest refs, paper line id, tied draft ref, export directory, template filename, and export time

#### Scenario: Export target is unsafe or ambiguous
- **WHEN** the target would overwrite unrecognized content, cannot be resolved, or lacks required authorization
- **THEN** the export stops before mutation and reports the exact target problem
- **AND** no successful export artifact is registered

### Requirement: Revised MyST Templates Are Validated and Applied
The system SHALL apply an externally edited MyST template only after manifest, concurrency, placeholder, source, and structural validation.

#### Scenario: Edited template is valid and current
- **WHEN** `apply-template` receives a matching export manifest, unchanged base revision, valid MyST, consistent placeholders, available source refs, and required sections
- **THEN** it creates or revises the current `kaoju:paper-template-myst`
- **AND** the write skill regenerates `kaoju:paper-draft-myst` and appends `kaoju:paper-revision-log`

#### Scenario: Export base is stale
- **WHEN** the active MyST template or structure changed after export
- **THEN** the system reports a concurrency conflict with the base and current revisions
- **AND** it leaves canonical template and draft state unchanged

#### Scenario: Edited template is invalid
- **WHEN** the edited template has invalid MyST, missing required sections, unresolved placeholders, unknown source refs, or inconsistent citation roles
- **THEN** the system returns structured diagnostics tied to file locations
- **AND** it does not create a new active template or draft revision

### Requirement: TeX Is Initialized as a Derived Publication Artifact
The system SHALL create `kaoju:paper-template-tex` and `kaoju:paper-draft-tex` as derived artifacts from selected canonical MyST revisions.

#### Scenario: TeX initialization succeeds with complete conversion
- **WHEN** the selected MyST template and draft use supported structures
- **THEN** the paper service creates TeX template and draft files with lineage to their MyST sources
- **AND** it records conversion tool identity, source checksums, citation inputs, included files, and diagnostics

#### Scenario: Conversion requires agent repair
- **WHEN** MyST directives, tables, citations, floats, raw blocks, or venue rules cannot be converted faithfully
- **THEN** the initializer marks the affected TeX locations and returns a non-terminal repair requirement
- **AND** the write agent directly inspects and edits the TeX files before build readiness

#### Scenario: Script output is not accepted without inspection
- **WHEN** TeX was initialized mechanically
- **THEN** the system requires a recorded agent inspection result before it can be selected for PDF build
- **AND** successful file creation alone does not establish publication readiness

### Requirement: PDF Builds Use Registered Execution
The system SHALL compile an inspected TeX draft through the `document_build` Research Operation Extension Point and an Execution Adapter Command Request.

#### Scenario: PDF build succeeds
- **WHEN** an inspected `kaoju:paper-draft-tex` and its template and bibliography inputs pass preflight
- **THEN** the system executes the selected registered toolchain, captures exact tool and version, inputs, commands, logs, outputs, resource use, and terminal status
- **AND** it registers `kaoju:paper-compile-log`, `kaoju:paper-pdf`, and `kaoju:paper-pdf-revision-log` with lineage to the built TeX revision

#### Scenario: Build requires fallback
- **WHEN** the preferred toolchain is unavailable or incompatible
- **THEN** the system records the concrete blocker or failure before using an authorized fallback
- **AND** the fallback remains visible in the compile log and PDF revision record

#### Scenario: PDF validation fails
- **WHEN** compilation succeeds but PDF inspection finds missing pages, unresolved references, malformed structure, broken citations, clipped displays, or other required validation failures
- **THEN** the build remains non-accepted and returns the TeX repair route
- **AND** a later attempt creates a distinct build Run and compile log

### Requirement: Publication-Facing Paper Output Uses a Human Gate
The system SHALL apply the configured publication Gate policy before marking a paper PDF or publication bundle as accepted publication-facing output.

#### Scenario: Draft or PDF awaits publication decision
- **WHEN** the paper reaches the configured publication checkpoint
- **THEN** the system presents the exact canonical MyST revision, derived TeX and PDF refs, audit state, validation result, known limitations, and build provenance
- **AND** it waits for the human Gate decision before publication acceptance

#### Scenario: Gate rejects or requests revision
- **WHEN** the human rejects publication or asks for changes
- **THEN** the system preserves the generated artifacts and decision provenance
- **AND** it returns to the applicable MyST, template, TeX repair, or evidence stage without overwriting prior Runs

### Requirement: Every Paper Artifact Is File-Backed and Discoverable
Every durable paper structure, template, draft, export, manifest, map, log, TeX tree, and PDF SHALL have a state-DB entry linked to authoritative file content.

#### Scenario: Paper artifact is queried
- **WHEN** a skill or actor requests the current paper artifact by semantic id and paper line
- **THEN** the system resolves it through the scoped state-DB query and returns its content locator, status, revision, checksum, validation, lineage, and provenance
- **AND** the caller does not scan the Topic Workspace for candidate files

#### Scenario: Paper source tree contains multiple files
- **WHEN** a TeX template or draft is stored as a directory tree
- **THEN** its Artifact content locator points to a versioned checksummed directory manifest
- **AND** the manifest references the entry point, included files, bibliography, assets, and generated outputs without embedding their bytes in DB metadata
