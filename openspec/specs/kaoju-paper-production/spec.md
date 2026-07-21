# kaoju-paper-production Specification

## Purpose
TBD - created by syncing change revise-kaoju-survey-process. Update Purpose after archive.
## Requirements
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
- **THEN** the write skill selects a typed structure profile from the accepted direction, records the taxonomy, comparison, empirical, general, or other supported profile and rationale, and creates `kaoju:paper-structure-myst` with intended sections, claim and source placeholders, citation roles, typed display placeholders, and evidence boundaries
- **AND** the actor may revise the proposed structure before the MyST `.md` file becomes an accepted registered Artifact

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

#### Scenario: Figure or table is included
- **WHEN** the structure or draft requires a figure or table
- **THEN** the figure or table content is stored as a separate file-backed Artifact and the MyST file contains a typed placeholder with its stable ref
- **AND** the citation map records the display role, evidence refs, caption or interpretation status, and insertion locator

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
The system SHALL export a selected named canonical template tree to a stable actor-editable working directory with reserved synchronization metadata while retaining the artifacts-database record as canonical state.

#### Scenario: Template export succeeds
- **WHEN** the actor requests a template export and supplies an authorized path or accepts a resolved Topic Workspace path
- **THEN** the system assigns an automatic export revision, writes the MyST template as a `.md` file, writes `kaoju:paper-template-manifest`, and registers `kaoju:paper-template-export`
- **AND** the manifest records source record id and revision, base digest, source-digest refs, paper line id, tied draft ref, export revision, export directory, template filename, and export time

#### Scenario: Managed export target is selected
- **WHEN** the actor accepts the default Topic Workspace export target
- **THEN** the service creates a versioned directory for the automatic export revision
- **AND** it does not overwrite an earlier export

#### Scenario: Export target is unsafe or ambiguous
- **WHEN** the target would overwrite unrecognized content, cannot be resolved, or lacks required authorization
- **THEN** the export stops before mutation and reports the exact target problem
- **AND** no successful export artifact is registered

#### Scenario: Default template export succeeds
- **WHEN** the actor requests export without a name or target
- **THEN** the system exports canonical `main` to `<topic-workspace>/intent/derived/writing-template/main/`
- **AND** the directory mirrors the current tree, contains `.isomer-template-export.json`, and is reported as non-canonical

#### Scenario: Named template export succeeds
- **WHEN** the actor exports `<template-name>` without an explicit target
- **THEN** the system resolves the exchange root and writes `<resolved-root>/<template-name>/`
- **AND** metadata records the stable canonical ref, state token, canonical and exported digests, actual path, and time

#### Scenario: Registered export status is inspected
- **WHEN** export status is queried
- **THEN** the system recomputes available tree digests excluding reserved metadata and reports unchanged, edited, missing, identity-invalid, and canonical-changed posture
- **AND** it does not interpret changed file meaning

#### Scenario: Clean target can be refreshed
- **WHEN** a recognized working tree has not changed since export
- **THEN** export can refresh it from current canonical state and update its metadata
- **AND** it does not create a version-numbered sibling directory

#### Scenario: Edited target is protected
- **WHEN** the working tree differs from its recorded exported digest
- **THEN** deterministic export stops and reports canonical and working state
- **AND** it does not overwrite or mechanically merge the edits

#### Scenario: Export reconciliation is agentic
- **WHEN** the actor asks to combine canonical changes with an edited working tree
- **THEN** the Kaoju agent interprets both arbitrary trees and prepares the desired working result
- **AND** recording that result as an export observation does not make it canonical

### Requirement: Revised MyST Templates Are Validated and Applied
The system SHALL expose low-level create and update operations for mutable named templates while requiring the Kaoju agent to construct or reconcile any candidate whose high-level meaning is not already known.

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

#### Scenario: Edited template orphans grounded content
- **WHEN** the edited template removes an optional section that still owns grounded claims or display content
- **THEN** the system reports each orphaned content ref and requires explicit actor confirmation before apply
- **AND** removal of a required section remains a validation error that confirmation cannot bypass

#### Scenario: Agent-prepared tree updates an existing name
- **WHEN** the agent prepares a clean candidate for target name `main` and supplies its expected current state token
- **THEN** the CLI verifies concurrency, path safety, tree integrity, reserved-file exclusion, actor, source, and change summary and atomically updates stable `main`
- **AND** it does not retain prior template content automatically

#### Scenario: Low-level file or metadata edit is applied
- **WHEN** an authorized caller puts or removes one safe relative file or patches allowed JSON metadata with the current state token
- **THEN** the CLI applies the edit atomically to the same named state and returns the new token and digest
- **AND** service-controlled identity, scope, digest, and audit fields cannot be patched

#### Scenario: Another named template replaces the target
- **WHEN** the caller updates target `<target-name>` from known named source `<source-name>` with the current target state token
- **THEN** the CLI copies exact source content and applicable metadata into the stable target state
- **AND** it does not invoke agentic merge or alter the source template

#### Scenario: Arbitrary source requires agent interpretation
- **WHEN** a user-edited directory must be combined with current target content
- **THEN** the Kaoju agent inspects both, resolves or asks about semantic choices, and constructs a candidate before invoking low-level update
- **AND** isomer-cli does not convert or merge the arbitrary source automatically

#### Scenario: Concurrent target change rejects update
- **WHEN** the supplied expected state token is stale
- **THEN** the mutation fails with current token and digest diagnostics
- **AND** the current tree and metadata remain unchanged

#### Scenario: Missing target requires explicit create
- **WHEN** an agent prepares content from topic `main/` but database template `main` does not exist
- **THEN** it invokes explicit create after explaining the initial registration
- **AND** update does not silently become create

#### Scenario: Template update does not silently revise drafts
- **WHEN** mutable named template state changes
- **THEN** existing drafts retain the template name, stable ref, and digest observed when they were produced
- **AND** consuming the new state requires an explicit drafting or reconciliation action

### Requirement: TeX Is Initialized as a Derived Publication Artifact
The system SHALL create `kaoju:paper-template-tex` and `kaoju:paper-draft-tex` as derived artifacts from selected canonical MyST revisions, following the agent-mediated composition contract: MyST holds all TeX content, TeX drift is presentation-only, and the agent fills the real venue template rather than relying on mechanical conversion.

#### Scenario: TeX initialization succeeds with a fill contract
- **WHEN** the selected MyST template and draft use supported structures and an adopted venue template exists
- **THEN** the paper service materializes the real template tree, scaffolds the draft TeX tree with lineage to its MyST sources, and writes a fill manifest of composition obligations
- **AND** it records the template compatibility fingerprint, tool identity, source checksums, citation inputs, included files, and diagnostics
- **AND** obligations cover frontmatter-to-title mapping, abstract and keywords environments, section mapping, bibliography materialization, tables, floats, and venue constructs

#### Scenario: Existing TeX template remains compatible
- **WHEN** a later MyST revision preserves the selected venue or document class, toolchain policy, and required construct set
- **THEN** the system reuses the current `kaoju:paper-template-tex` and regenerates only `kaoju:paper-draft-tex`
- **AND** prior human TeX-template refinements remain intact

#### Scenario: TeX template compatibility changes
- **WHEN** the venue or document class, toolchain policy, or required MyST construct set changes incompatibly
- **THEN** the system creates a revision of `kaoju:paper-template-tex` before regenerating the TeX draft
- **AND** it records the changed fingerprint dimensions and migration diagnostics

#### Scenario: Conversion requires agent repair
- **WHEN** MyST directives, tables, citations, floats, raw blocks, or venue rules cannot be converted faithfully
- **THEN** the initializer marks the affected TeX locations and returns a non-terminal repair requirement
- **AND** the write agent directly inspects and edits the TeX files before build readiness

#### Scenario: Mechanical pass-through is reported, not hidden
- **WHEN** scaffolded TeX contains raw frontmatter, placeholder title or author, literal Title or Abstract sections, citation keys without a bibliography, or unrepaired markers
- **THEN** the initializer or validator reports each as an unfilled obligation with file location
- **AND** the tree cannot be recorded as inspected or build-ready while any obligation is open

#### Scenario: Script output is not accepted without inspection
- **WHEN** TeX was initialized mechanically
- **THEN** the system requires a recorded agent fill and inspection result before it can be selected for PDF build
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

#### Scenario: Approved build admits bounded non-material repair
- **WHEN** an approved PDF build fails because of a presentation-only or TeX syntax problem that preserves canonical MyST content and evidence meaning
- **THEN** the write agent may repair the TeX artifact and retry automatically within the recorded attempt bound
- **AND** every attempt creates a distinct build Run and compile log with the exact repair and lineage

#### Scenario: Build repair would be material
- **WHEN** a proposed repair changes canonical paper content, evidence meaning, dependencies, toolchain policy, or resource limits
- **THEN** the system pauses for a revised plan and the applicable human Gate
- **AND** it does not apply the material repair under the prior build authorization

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

### Requirement: Canonical MyST Templates Are Mutable Named Topic Records
The system SHALL store each canonical MyST-oriented paper template tree as one stable mutable `kaoju:paper-template-myst` record identified by a path-safe name within a Topic Workspace.

#### Scenario: Named templates coexist in one namespace
- **WHEN** templates named `main`, `conference-a`, and `main-before-methodology-change` exist
- **THEN** each name resolves one independent current record and current tree
- **AND** the system assigns no special snapshot meaning to any name

#### Scenario: Canonical template has arbitrary tree shape
- **WHEN** a template contains one or more MyST, configuration, include, asset, or guidance files
- **THEN** the canonical record stores the current tree through a managed directory manifest with file integrity and path-safety metadata
- **AND** it does not require a fixed entrypoint, section set, or universal template schema

#### Scenario: Ordinary update preserves stable identity
- **WHEN** accepted content or allowed metadata changes for an existing name
- **THEN** the system atomically updates the same stable named record and returns a new state token and digest
- **AND** it does not create a historical template-content revision, `revision_of`, or `supersedes` record

#### Scenario: Omitted paper-use or export name resolves to main
- **WHEN** a paper drafting or export operation does not receive an explicit template name
- **THEN** it resolves canonical template `main`
- **AND** it does not select another named template by timestamp, paper line, path, or record order

### Requirement: Saved Template States Are Ordinary Named Copies
The system SHALL preserve a template state only through an explicit create operation that copies it to another ordinary name in the same template namespace.

#### Scenario: Agent explicitly preserves main
- **WHEN** the user or agent creates `main-before-change` from current template `main`
- **THEN** the system creates an ordinary named template with the exact source tree and allowed metadata observed at copy time
- **AND** both names remain independently mutable and usable

#### Scenario: Copy has no snapshot classification
- **WHEN** a caller lists or shows the copied template
- **THEN** it has the same semantic id, binding, fields, and operations as every other named template
- **AND** the database stores no snapshot type, flag, parent lifecycle, retention policy, or special list

#### Scenario: Ordinary update does not create a copy
- **WHEN** a user or agent updates a named template without first requesting another name
- **THEN** only the selected named current state changes
- **AND** the prior content is not retained as a restorable template by contract

#### Scenario: Known named state replaces another template
- **WHEN** the actor explicitly replaces target template `main` from named template `main-before-change`
- **THEN** the system copies the source tree and applicable authored metadata exactly into stable target `main`
- **AND** it performs no merge and leaves the source name unchanged

### Requirement: Underspecified Template Updates Use Ordered Source Discovery
The Kaoju agent SHALL discover a template source in a fixed order when the user asks to update the paper template in the current artifacts database without supplying a template name, canonical ref, template path, or export path.

#### Scenario: One registered export was edited
- **WHEN** exactly one eligible registered export has a current tree digest different from its recorded exported digest
- **THEN** the agent selects that export directory and its recorded target name
- **AND** it does not fall through to the topic `main` directory

#### Scenario: Several registered exports were edited
- **WHEN** more than one eligible export was edited or an edited export has ambiguous identity
- **THEN** the agent presents the concrete names, refs, and paths and asks the user which source to use
- **AND** it does not select by modification time or record order

#### Scenario: No edited export and topic main directory exists
- **WHEN** no eligible edited export exists and `<topic-workspace>/intent/derived/writing-template/main/` exists in the current Topic Workspace
- **THEN** the agent uses that directory as source and targets name `main` unless consistent export metadata identifies it more precisely
- **AND** this fallback does not depend on a database template named `main` existing

#### Scenario: No discoverable source exists
- **WHEN** no eligible edited export exists and the current Topic Workspace has no writing-template `main/` directory
- **THEN** the agent asks the user which template or directory to use
- **AND** it does not infer a source from an unrelated database record

#### Scenario: Explicit input bypasses discovery
- **WHEN** the update request supplies a template name, canonical ref, template path, or export path
- **THEN** the agent validates and uses that explicit selection
- **AND** it does not replace it through implicit discovery

### Requirement: Paper Templates Have Separate Content and LaTeX Roles
The system SHALL represent a MyST-oriented content template and a LaTeX presentation template as distinct named template roles with independent state, defaults, validation, exchange paths, and lineage.

#### Scenario: Both main templates exist
- **WHEN** a Topic Workspace contains content template `main` and LaTeX template `main`
- **THEN** each name resolves one stable record in its own template namespace
- **AND** selecting, updating, exporting, archiving, or deleting one does not select or mutate the other

#### Scenario: User names the template role
- **WHEN** a user identifies a content template, MyST template, LaTeX template, TeX template, document class, style bundle, or presentation template
- **THEN** the Kaoju workflow resolves the corresponding template role without asking an unrelated template question
- **AND** an unqualified request is clarified only when the surrounding task cannot distinguish content authoring from LaTeX presentation

#### Scenario: Omitted name resolves within one role
- **WHEN** a content-template or LaTeX-template operation omits the template name
- **THEN** it resolves `main` in the already selected role
- **AND** it does not resolve by timestamp, paper line, path order, or the other role's `main`

### Requirement: Named LaTeX Templates Are Mutable Topic Stock
The system SHALL store each accepted LaTeX presentation template as one stable mutable named `KAOJU:PAPER-TEMPLATE-LATEX` managed directory tree within a Topic Workspace.

#### Scenario: Multi-file LaTeX template is stocked
- **WHEN** an agent prepares an authorized directory containing a safe entrypoint, classes, styles, bibliography styles, includes, assets, and a valid composition contract
- **THEN** the system records its exact managed tree, stable ref, name, state token, tree digest, authored metadata, source refs, and mutation audit
- **AND** it preserves the tree shape rather than flattening files into a generated preamble

#### Scenario: Existing LaTeX stock is updated
- **WHEN** an authorized update supplies the current state token and a validated prepared replacement tree
- **THEN** the system atomically replaces the same stable named record and returns a new token and digest
- **AND** existing paper drafts retain the exact LaTeX snapshot they previously observed

#### Scenario: LaTeX stock is exported and edited
- **WHEN** the actor exports a named LaTeX template and later edits the registered working directory
- **THEN** export status reports the working-copy drift and an authorized update can promote the assessed tree using optimistic concurrency
- **AND** the working copy never becomes stocked state merely because its files changed

### Requirement: LaTeX Composition Uses an Exact Stocked Template State
The system SHALL derive `KAOJU:PAPER-TEMPLATE-TEX` and `KAOJU:PAPER-DRAFT-TEX` from an exact canonical MyST draft and an exact observed named LaTeX template state.

#### Scenario: Default LaTeX composition succeeds
- **WHEN** a paper requests TeX composition without an explicit LaTeX name and `latex/main` is ready
- **THEN** the composer snapshots its complete tree and records the stable ref, name, state token, digest, entrypoint, composition contract, build profile, and source provenance
- **AND** the derived TeX draft is self-contained and linked separately to its canonical MyST draft and presentation snapshot

#### Scenario: No default LaTeX stock exists
- **WHEN** composition omits a LaTeX name and no ready `latex/main` exists
- **THEN** the workflow pauses with the missing named-template requirement and stock or adoption routes
- **AND** it does not silently generate an `article` preamble or select a paper-line TeX revision

#### Scenario: Content template changes
- **WHEN** the canonical content-template digest changes while the selected LaTeX stock and composition contract remain unchanged
- **THEN** the change can require a new MyST draft and TeX draft but does not itself revise the stocked LaTeX template or its presentation fingerprint
- **AND** content-template and LaTeX-template drift remain independently reportable

#### Scenario: Mechanical conversion requires repair
- **WHEN** MyST constructs cannot be composed faithfully through the selected LaTeX contract
- **THEN** the composer records file-located diagnostics and requires direct agent inspection of the paper-specific TeX tree
- **AND** repairs remain paper-local unless the actor explicitly authorizes a stocked LaTeX-template update

### Requirement: PDF Builds Consume the Pinned LaTeX Presentation
The system SHALL compile the self-contained TeX draft through its declared entrypoint and verify its pinned LaTeX snapshot before dispatching registered document execution.

#### Scenario: Template and draft agree
- **WHEN** the TeX draft manifest and supplied template snapshot identify the same ref and digest
- **THEN** the builder compiles the composed tree through the declared registered build profile and entrypoint
- **AND** it records the exact input tree, entrypoint, engine, commands, logs, output PDF, and lineage

#### Scenario: Template argument mismatches the draft
- **WHEN** a build supplies a template ref that differs from the draft's pinned template snapshot
- **THEN** preflight rejects the build without execution and reports both refs
- **AND** it does not merely validate the unrelated template and compile the draft anyway

#### Scenario: Entrypoint is not main.tex
- **WHEN** the selected composition contract declares another safe TeX entrypoint
- **THEN** the builder compiles that entrypoint and validates the correspondingly named PDF output
- **AND** it does not hard-code `main.tex` or `main.pdf`

### Requirement: Template Drift Is Explicit and Non-Propagating
The system SHALL distinguish working-copy drift, stocked-template drift, and paper-local repair drift.

#### Scenario: Stock changed after composition
- **WHEN** a current named LaTeX template has a different state token or digest from a TeX draft's observed state
- **THEN** paper status reports the draft as presentation-stale and preserves both identities
- **AND** it does not rewrite the draft or rebuild automatically

#### Scenario: Paper repair differs from stock
- **WHEN** an inspected TeX draft contains presentation repairs not present in its template snapshot
- **THEN** the revision record classifies those repairs as paper-local
- **AND** only an explicit template update can promote them into named LaTeX stock

### Requirement: Existing Topic Workspaces Migrate Without Losing History
The system SHALL migrate existing Topic Workspaces to the content-template and LaTeX-template contract while preserving all historical paper and template records.

#### Scenario: Existing named MyST state is migrated
- **WHEN** a Topic Workspace contains an existing mutable named `KAOJU:PAPER-TEMPLATE-MYST` record
- **THEN** migration annotates and validates it as a content template without changing its stable ref or tree bytes
- **AND** new exchange metadata and status output use the content-template role

#### Scenario: Active TeX presentation is adopted
- **WHEN** an actor supplies one unambiguous current `KAOJU:PAPER-TEMPLATE-TEX` or legacy `KAOJU:WRITING-TEMPLATE` ref plus valid LaTeX composition metadata
- **THEN** migration copies its source tree into named LaTeX stock and records explicit adoption provenance
- **AND** it leaves the source record, revision lineage, builds, drafts, and PDFs unchanged

#### Scenario: Presentation candidate is ambiguous
- **WHEN** a Topic Workspace has several plausible presentation candidates and no explicit selection
- **THEN** migration reports their refs, scopes, digests, entrypoints, and current posture without creating `latex/main`
- **AND** it resumes only after an actor selects or prepares the intended source

### Requirement: Venue LaTeX Template Adoption Packs Full Template Content
The system SHALL adopt a LaTeX venue template by packing the complete actor-selected template tree (entrypoint source, class files, included files, assets) into managed artifact storage, and SHALL reject placeholder or reference-only shims presented as a venue template.

#### Scenario: Actor adopts a real template tree
- **WHEN** the actor selects a template directory and says it is the venue template to store
- **THEN** the template procedure copies the whole directory content into managed storage and creates the template record with per-file checksums and authored metadata
- **AND** the stored entrypoint is the actual venue template source, usable for composition without external lookup

#### Scenario: A shim is presented as a venue template
- **WHEN** the candidate directory's entrypoint is a short hand-written file that merely names or checksums an external official template without containing its structure
- **THEN** adoption validation rejects the candidate and reports that the real template tree is required
- **AND** no template record is created or updated from the shim

#### Scenario: Venue structure is present
- **WHEN** a template claims a specific venue (for example IEEE Transactions)
- **THEN** validation checks the stored tree actually contains that venue's document class and title, author, abstract, and keywords constructs
- **AND** missing venue constructs are reported before the template can be selected for composition
