# kaoju-artifact-bindings Specification

## Purpose
TBD - created by archiving change add-family-neutral-research-artifact-bindings. Update Purpose after archive.
## Requirements

### Requirement: Kaoju Artifact Semantics Are Storage-Neutral
The Kaoju extension SHALL define one shared artifact semantic registry whose entries describe durable survey meanings independently of storage implementation and are queryable through the package-owned Kaoju extension surface.

#### Scenario: Semantic entry avoids physical binding
- **WHEN** an agent reads a Kaoju artifact semantic entry returned by the extension or summarized by bundle-local shared guidance
- **THEN** the entry provides a stable canonical identifier such as `KAOJU:SURVEY-CONTRACT`, meaning, required semantic content, producer, consumer, and update intent
- **AND** it does not prescribe a filesystem path, record-store subpath, provider payload, or implementation command body

#### Scenario: Active skills use registered semantic ids
- **WHEN** active Kaoju guidance names an accepted durable output
- **THEN** it uses an exact registered `KAOJU:WHAT` identifier available from the shared Kaoju extension query
- **AND** it does not wrap the identifier in angle brackets, use a bare object name, or use lowercase or mixed case
- **AND** unregistered or ambiguous durable output semantics are reported by validation

### Requirement: Kaoju Artifact Bindings Are Separate and Complete
The package-owned Kaoju extension implementation SHALL provide one versioned machine-readable Kaoju binding registry that is separate from the storage-neutral semantic registry and complete for every active Kaoju semantic id.

#### Scenario: Binding entry is complete
- **WHEN** the binding registry maps a Kaoju semantic id
- **THEN** the entry names its artifact type, compatible record kind, default semantic label, family-neutral format profile, content mode, producer, consumers, required relationship roles, revision mode, scope-key policy, latest-selection policy, and validation and acceptance expectations
- **AND** it does not embed executable commands, provider payloads, credentials, or implementation-specific command bodies

#### Scenario: Binding coverage is bidirectional
- **WHEN** the Kaoju binding validator compares the shared semantic registry, active skill references, binding registry, schema and renderer assets, and built-in profile catalog
- **THEN** it rejects missing, extra, duplicated, cross-family, unresolved, aliased, non-uppercase, or incompatible semantic ids, profiles, producers, consumers, scope policies, and content modes
- **AND** each diagnostic names the family, semantic id, affected file, line when available, and violated binding rule

#### Scenario: Skills resolve physical bindings through the registry
- **WHEN** a Kaoju skill needs to create, revise, or query an accepted durable output
- **THEN** it resolves the binding through `isomer-cli project artifacts describe` or the equivalent package service
- **AND** per-skill binding pages are generated summaries or concise references rather than independent physical binding authorities

#### Scenario: Binding selects a storage surface without defining an internal path
- **WHEN** a Kaoju binding selects a managed content mode and default Semantic Workspace Surface Label
- **THEN** the artifact service allocates a generic internal path from record kind and opaque record or revision identity
- **AND** the binding and producer do not declare, construct, or rely on a Kaoju-specific subdirectory convention

#### Scenario: Skills discover and apply physical bindings
- **WHEN** a Kaoju skill needs to inspect a binding before creating, revising, or querying an accepted durable output
- **THEN** it discovers the contract through an exact command such as `isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT` and uses `isomer-cli project artifacts` for the topic-scoped operation
- **AND** the extension query and project artifact service resolve the same package-owned canonical registry

#### Scenario: Per-skill binding guidance remains a local projection
- **WHEN** a skill contains `artifact-bindings.md` or equivalent local guidance
- **THEN** that bundle-local page may summarize only the semantic ids and usage needed by its owning skill and directs the agent to the extension query for current binding data
- **AND** it does not name a registry filesystem path, become an independent physical binding authority, or repeat full executable command shapes

### Requirement: Kaoju Structured Payload Is Canonical
Accepted structured Kaoju records SHALL use validated file-backed JSON payloads as canonical machine-readable content, while non-structured artifacts SHALL use their registered ordinary file, directory manifest, external locator, or canonical repository reference as authoritative content.

#### Scenario: Accepted structured payload has common display and identity fields
- **WHEN** a Kaoju binding creates or revises a structured record
- **THEN** its validated JSON file contains non-empty `title`, `summary`, `artifact_family: "kaoju"`, `semantic_id`, `artifact_type`, and a `sections` object
- **AND** the payload semantic id, family, content mode, and selected format profile match the resolved binding

#### Scenario: Human-facing structured view is derived
- **WHEN** an agent or user needs Markdown, CSV, a matrix, a dossier, or another readable representation of a structured Kaoju record
- **THEN** it uses an on-demand render, registered view, explicit export, or worker-visible projection from the canonical JSON record
- **AND** later agents do not parse or edit that representation as canonical structured state

#### Scenario: Paper and material files remain authoritative
- **WHEN** an accepted binding registers MyST, Markdown, TeX, PDF, a script, a log, a downloaded source, a directory tree, or a canonical repository
- **THEN** the Artifact Core Record points to the actual file, a checksummed directory manifest, an authorized external locator, or the canonical repository identity
- **AND** state metadata does not replace or embed the artifact content

#### Scenario: Plain output remains pre-promotion state
- **WHEN** a Kaoju procedure creates staging JSON, notes, tables, logs, reports, or other operation-local files before acceptance
- **THEN** those files follow the resolved worker output policy
- **AND** they become accepted durable artifacts only through the applicable binding and state-DB registration

### Requirement: Kaoju Binding Inventory Covers Core Survey Objects
The production Kaoju binding inventory SHALL cover every durable object required by the legacy procedures and the ten survey-process use cases.

#### Scenario: Core semantic inventory is present
- **WHEN** the shared registry and binding registry are inspected
- **THEN** they cover workspace readiness, binding index, `kaoju:survey-contract`, Comparison Intent Document, `kaoju:proceed-decision`, `kaoju:discovery-ledger`, `kaoju:related-work-catalog` and its deltas, `kaoju:curated-intake-delta`, Source Digest, Source Access Blocker, `kaoju:claim-evidence-ledger`, material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, theory comparison, Comparison Matrix, Audit Report, `kaoju:claim-status-table`, `kaoju:field-summary`, Kaoju Dossier, terminal report, method-trial Runs, and comparison Runs

#### Scenario: Survey-process inventory is present
- **WHEN** the July 14 survey-process binding inventory is inspected
- **THEN** it includes exact bindings for `kaoju:direction-set`, `kaoju:reading-list`, `kaoju:artifact-library`, `kaoju:associated-source-code`, `kaoju:paper-structure-myst`, `kaoju:paper-template-myst`, `kaoju:paper-draft-myst`, `kaoju:paper-draft-md`, `kaoju:citation-map`, `kaoju:paper-template-export`, `kaoju:paper-template-manifest`, `kaoju:paper-revision-log`, `kaoju:paper-template-tex`, `kaoju:paper-draft-tex`, `kaoju:paper-pdf`, `kaoju:paper-compile-log`, `kaoju:paper-pdf-revision-log`, `kaoju:llm-wiki-export`, `kaoju:llm-wiki-metadata`, `kaoju:llm-wiki-viewer`, `kaoju:llm-wiki-viewer-manifest`, `kaoju:env-prep-plan`, `kaoju:env-gate-revision`, `kaoju:pixi-env-ref`, `kaoju:smoke-run-script`, `kaoju:smoke-run-result`, `kaoju:method-trial-plan`, and `kaoju:method-trial-result`
- **AND** existing `kaoju:method-trial-run`, evidence, catalog, decision, and synthesis bindings are reused where the use cases name them

#### Scenario: Legacy writing semantics have migration disposition
- **WHEN** `kaoju:writing-template`, `kaoju:survey-manuscript`, `kaoju:paper-build-run`, `kaoju:paper-validation-report`, or `kaoju:publication-bundle` remains readable
- **THEN** the binding registry marks its legacy or compatibility status and permitted migration relationships
- **AND** no legacy TeX record is treated as canonical MyST content

#### Scenario: New durable output needs a disposition
- **WHEN** a later Kaoju skill adds an accepted durable output
- **THEN** it adds a semantic registry entry, binding entry, and family-neutral profile or records an explicit non-structured binding disposition
- **AND** validation rejects an undocumented implicit storage choice

### Requirement: Kaoju Records Preserve Lineage and Revision Meaning
Kaoju bindings SHALL define canonical lineage, scope, update, and revision behavior for every semantic id, including explicit mutable-state exceptions.

#### Scenario: Scoped current-state object is revised
- **WHEN** accepted content changes for a direction set, direction-owned reading list, source-owned digest, artifact library, Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, paper structure, paper template, paper draft, current terminal status, or another binding marked as current state
- **THEN** the service creates a revision so the prior record remains historical and the new record becomes the explicit latest candidate for the same binding-defined scope
- **AND** records in another direction, source, paper line, or target scope remain independently current

#### Scenario: Delta and audit remain separate records
- **WHEN** a curated intake, direction expansion, audit, follow-up, bounded repair, template export observation, template mutation audit, build attempt, wiki export, environment preparation, or trial produces event evidence
- **THEN** it creates the applicable separate evidence record with parent or subject refs
- **AND** it does not silently convert event evidence into restorable template content

#### Scenario: Run fidelity is not revised away
- **WHEN** a faithful Run fails and an adapted or repaired Run follows
- **THEN** each Run remains separate with its own purpose, inputs, outputs, timing, environment, and lineage
- **AND** the later Run does not replace the earlier verdict

#### Scenario: Competing current candidates remain visible
- **WHEN** two non-superseded accepted records claim the same semantic id and scope
- **THEN** scoped latest lookup reports a conflict with both stable refs
- **AND** it does not select solely by timestamp

#### Scenario: Ordinary scoped current-state object is revised
- **WHEN** accepted content changes for a direction set, direction-owned reading list, source-owned digest, artifact library, Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, paper structure, paper draft, current terminal status, or another binding marked as revisioned current state
- **THEN** the service creates a revision so the prior record remains historical and the new record becomes the explicit latest candidate for the same binding-defined scope
- **AND** records in another direction, source, paper line, or target scope remain independently current

#### Scenario: Mutable named template is updated
- **WHEN** accepted content or metadata changes for a binding-marked mutable named paper template
- **THEN** the service atomically updates its stable current record and lightweight audit evidence
- **AND** it does not apply the revisioned-current-state behavior used by other semantic ids

#### Scenario: Explicit named copy preserves template content
- **WHEN** a user or agent requires a restorable paper-template state
- **THEN** it creates another ordinary named template through the same binding
- **AND** no implicit historical revision or snapshot record is created

#### Scenario: Competing revisioned candidates remain visible
- **WHEN** two non-superseded accepted records claim the same revisioned semantic id and scope
- **THEN** scoped latest lookup reports a conflict with both stable refs
- **AND** this candidate-selection rule is not used for binding-enforced unique mutable template names

### Requirement: Large Research Materials Remain Referenced
Kaoju records SHALL reference rather than embed large, binary, directory-shaped, externally governed, or repository material.

#### Scenario: Material manifest records exact identity
- **WHEN** a repository, paper file, dataset, model, checkpoint, generated-data directory, raw output, log, wiki tree, TeX tree, viewer deployment, or PDF is externally acquired or registered
- **THEN** the applicable record stores or links its immutable locator, revision or digest, source class, size when known, access and license posture, managed-link or Artifact refs, observed time, staleness policy, and Provenance Record refs
- **AND** structured payloads and DB metadata do not contain the material bytes or directory tree

#### Scenario: Directory artifact uses a checksummed manifest
- **WHEN** accepted content contains multiple files
- **THEN** its Artifact content locator points to a versioned manifest listing member paths, media types, sizes, checksums, entry points, and external refs
- **AND** later discovery resolves the manifest through the DB rather than scanning the directory

#### Scenario: Dataset manifest is not the dataset store
- **WHEN** `manage-dataset` registers, refreshes, or removes a local dataset
- **THEN** the Topic Dataset Manifest is revised through its binding while link mutation remains owned by the Topic Workspace owner
- **AND** removal never deletes or rewrites the external dataset

#### Scenario: Repository material records external acquisition evidence
- **WHEN** a Canonical External Repository is accepted as Kaoju material
- **THEN** its Artifact records or links the semantic repository label, requested and resolved source locators, observed immutable commit or digest, acquisition method, sanitized external command evidence, relationship basis, limitations, and verification time
- **AND** it does not depend on a `repository_acquisition` extension point, an Isomer-generated Git command request, or raw credential-bearing output

### Requirement: Kaoju Workspace Bootstrap Validates Storage Readiness
`isomer-kaoju-workspace-mgr` SHALL establish semantic binding, scoped query, path, and storage readiness before ordinary Kaoju skills write accepted durable artifacts.

#### Scenario: Bootstrap validates complete contract
- **WHEN** Kaoju storage bootstrap runs for a Research Topic
- **THEN** it resolves Effective Topic Context and fresh Workspace Runtime state, required `topic.records.*` labels, the family-neutral provider and selected profiles, shared semantic registry, versioned binding registry, topic-level binding index, scoped query support, dataset-manifest posture, relevant latest records, worker output policy, and reset-checkpoint posture

#### Scenario: Bootstrap records readiness or blocker
- **WHEN** all required surfaces and bindings resolve
- **THEN** it records a Kaoju binding index and Workspace Readiness record through their bindings
- **AND** when a required label, profile, binding, scope index, query surface, owner, or reset decision is unavailable, it records an explicit blocker and prevents affected accepted writes

#### Scenario: Reset survival is explicit
- **WHEN** bootstrap records or user-selected survey records should survive a Topic Workspace reset
- **THEN** the workspace manager updates the selected reset checkpoint with exact record, content, export, semantic-label, actor, and provenance refs
- **AND** unpreserved post-checkpoint records remain subject to the accepted reset plan

### Requirement: Kaoju Survey Management Uses Bound Records
The `manage-survey` and `manage-dataset` helpers SHALL operate on canonical bound records through deterministic research-record queries.

#### Scenario: Survey list uses family and semantic filters
- **WHEN** a user invokes `manage-survey list`
- **THEN** the helper queries records with `artifact_family=kaoju` and optional semantic id, status, procedure, or latest-only filters
- **AND** results contain stable record id, semantic id, title, summary, version or revision state, procedure, terminal status, validation state, and canonical detail locator

#### Scenario: Show and status use canonical state
- **WHEN** a user invokes `manage-survey show` or `status`
- **THEN** the helper reads canonical record metadata and managed payloads, then follows explicit lineage and latest-state evidence
- **AND** it reports competing ready records as ambiguity instead of selecting solely by timestamp

#### Scenario: Export does not mutate survey state
- **WHEN** a user invokes `manage-survey export`
- **THEN** the helper renders or exports a selected canonical record through its profile and records export provenance when durable
- **AND** the export does not become a new latest survey state or evidence source

### Requirement: Every Survey-Process Durable Output Has a State-DB Entry
Every durable record named by a survey-process use case SHALL be registered in the Topic Workspace state DB and linked to authoritative filesystem or Canonical External Repository content.

#### Scenario: Durable artifact is accepted
- **WHEN** a Kaoju procedure accepts a structured record, ordinary file, directory export, registered repository, script, log, environment ref, Run result, or PDF
- **THEN** it creates an Artifact Core Record with semantic id metadata, artifact kind, status, timestamps, locator kind, locator or semantic label, content link, checksum or immutable identity when applicable, and provenance links
- **AND** success is not reported until Artifact registration completes

#### Scenario: Agent looks for an artifact
- **WHEN** a skill needs an existing direction, reading list, source, paper, wiki, environment, trial, audit, or synthesis artifact
- **THEN** it queries the state DB by semantic id, scope, status, lineage, or stable ref
- **AND** it does not scan the Topic Workspace directory tree as a fallback

#### Scenario: DB and content disagree
- **WHEN** the DB entry points to missing or checksum-mismatched content or its repository identity disagrees with the observed registered path
- **THEN** the system reports stale or corrupt artifact state and the recovery route
- **AND** the DB entry remains discoverable for diagnosis rather than being silently ignored or revised

#### Scenario: External repository topology is registered before Artifact acceptance
- **WHEN** a Kaoju procedure accepts repository content acquired through external commands
- **THEN** it first requires the verified existing path to resolve through its non-main `topic.repos.*` binding and then records the applicable Artifact revision
- **AND** a filesystem checkout without semantic registration remains pre-acceptance material rather than a successful durable output

### Requirement: Named Template Binding Uses Mutable State
The `kaoju:paper-template-myst` binding SHALL support one stable mutable current record per template name without automatic content revisions.

#### Scenario: Stable name owns one current record
- **WHEN** a template name is created
- **THEN** its Topic Workspace and template-name scope identify one stable record whose managed tree and authored metadata can be updated atomically
- **AND** ordinary lookup does not select among superseding candidates

#### Scenario: Update replaces current state
- **WHEN** content or allowed metadata changes with the expected state token
- **THEN** the binding updates the stable record's current managed tree, digest, metadata, token, and update time
- **AND** it creates no `revision_of`, `supersedes`, or historical template-content record

#### Scenario: Explicit saved state is another name
- **WHEN** the actor copies one template to a new name
- **THEN** the new record uses the same semantic id, binding, content mode, mutable-state behavior, and operations
- **AND** no binding field classifies it as a snapshot

#### Scenario: Canonical content supports arbitrary file trees
- **WHEN** a named template contains multiple files or no conventional main filename
- **THEN** its current content uses a managed directory manifest with checksummed safe relative paths
- **AND** the binding does not assert a universal internal template format

#### Scenario: Lightweight audit does not retain old content
- **WHEN** mutable named state changes
- **THEN** an audit event records name, stable ref, actor, operation, source refs, time, and before-and-after tokens and digests
- **AND** the event does not retain prior template bytes or become a restorable template

#### Scenario: Working directory remains non-canonical
- **WHEN** a named template is exported
- **THEN** the external working directory and export observation remain distinct from the mutable canonical record
- **AND** editing the directory does not change database state until explicit low-level CRUD succeeds
