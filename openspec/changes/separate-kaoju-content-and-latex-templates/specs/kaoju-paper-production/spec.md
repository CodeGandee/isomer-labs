## ADDED Requirements

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
