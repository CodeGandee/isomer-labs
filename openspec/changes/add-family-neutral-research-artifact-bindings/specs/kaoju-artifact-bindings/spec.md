## ADDED Requirements

### Requirement: Kaoju Artifact Semantics Are Storage-Neutral
The Kaoju extension SHALL define one shared artifact semantic registry whose entries describe durable survey meanings independently of storage implementation.

#### Scenario: Semantic entry avoids physical binding
- **WHEN** an agent reads a Kaoju artifact semantic entry
- **THEN** the entry provides a stable `kaoju:<semantic-id>`, meaning, required semantic content, producer, consumer, and update intent
- **AND** it does not prescribe a filesystem path, record kind, semantic label, format profile, or CLI command

#### Scenario: Active skills use registered semantic ids
- **WHEN** active Kaoju guidance names an accepted durable output
- **THEN** it uses an exact semantic id registered in the shared artifact semantic registry
- **AND** unregistered or ambiguous durable output semantics are reported by validation

### Requirement: Kaoju Artifact Bindings Are Separate and Complete
Each production Kaoju skill that produces accepted durable records SHALL provide a separate `artifact-bindings.md` authority mapping its semantic ids to actual research-record operations.

#### Scenario: Binding row is complete
- **WHEN** `artifact-bindings.md` binds a Kaoju semantic id
- **THEN** the row names its storage item, record kind, existing semantic label, family-neutral format profile, producer, consumer, payload role, lineage policy, revision policy, query metadata, and normal validate and create command shape
- **AND** the page defines list, show, revise or follow-up, metadata update, on-demand render or export, and archive behavior applicable to the row

#### Scenario: Binding coverage is bidirectional
- **WHEN** the Kaoju binding validator compares the shared semantic registry, active skill references, binding pages, and built-in profile catalog
- **THEN** it rejects missing, extra, duplicated, cross-family, or unresolved semantic ids and profiles
- **AND** each diagnostic names the family, semantic id, affected file, line when available, and violated binding rule

#### Scenario: Shared skill does not own physical bindings
- **WHEN** the Kaoju shared skill is inspected
- **THEN** it owns common semantic vocabulary and cross-stage recording rules
- **AND** producer skill binding pages remain the authority for physical and API binding decisions

### Requirement: Kaoju Structured Payload Is Canonical
Accepted structured Kaoju records SHALL use managed JSON payload snapshots as canonical machine-readable state.

#### Scenario: Accepted payload has common display and identity fields
- **WHEN** a Kaoju binding creates or revises a structured record
- **THEN** its validated payload contains non-empty `title`, `summary`, `artifact_family: "kaoju"`, `semantic_id`, `artifact_type`, and a `sections` object
- **AND** the payload semantic id and family match the binding and selected format profile

#### Scenario: Human-facing view is derived
- **WHEN** an agent or user needs Markdown, CSV, a matrix, a dossier, or another readable representation of a structured Kaoju record
- **THEN** it uses an on-demand render or explicit export from the canonical record
- **AND** later agents do not parse or edit that representation as canonical structured state

#### Scenario: Plain output remains pre-promotion state
- **WHEN** a Kaoju procedure creates staging JSON, notes, tables, logs, reports, or other operation-local files before acceptance
- **THEN** those files follow the resolved worker output policy
- **AND** they become accepted durable records only through the applicable binding

### Requirement: Kaoju Binding Inventory Covers Core Survey Objects
The production Kaoju binding inventory SHALL cover every core durable object required by its procedures and helpers.

#### Scenario: Core semantic inventory is present
- **WHEN** the shared registry and binding pages are inspected
- **THEN** they cover workspace readiness, Survey Contract, Comparison Intent Document, Proceed Decision, Discovery Ledger, Related-Work Catalog and its deltas, curated intake delta, Source Digest, Source Access Blocker, Claim-Evidence Ledger, material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, theory comparison, Comparison Matrix, Audit Report, Claim Status Table, Field Summary, Kaoju Dossier, terminal report, method-trial Runs, and comparison Runs

#### Scenario: New durable output needs a disposition
- **WHEN** a later Kaoju skill adds an accepted durable output
- **THEN** it adds a semantic registry entry, binding row, and family-neutral profile or records an explicit non-structured binding disposition
- **AND** validation rejects an undocumented implicit storage choice

### Requirement: Kaoju Records Preserve Lineage and Revision Meaning
Kaoju binding pages SHALL define canonical lineage and revision behavior for every bound semantic id.

#### Scenario: Current-state object is revised
- **WHEN** accepted content changes for a Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, current terminal status, or another binding marked as current state
- **THEN** the agent uses research-record revision so the prior record remains historical and the new record becomes the explicit latest candidate

#### Scenario: Delta and audit remain separate records
- **WHEN** a curated intake, direction expansion, audit, follow-up, or bounded repair produces new evidence
- **THEN** it creates a separate descendant record with its immediate parent refs and applicable `derived_from` or `follow_up_to` lineage
- **AND** it does not overwrite the base survey artifact

#### Scenario: Run fidelity is not revised away
- **WHEN** a faithful Run fails and an adapted or repaired Run follows
- **THEN** each Run remains a separate record with its own purpose, fidelity, inputs, outputs, and lineage
- **AND** the later Run does not revise or replace the earlier verdict

### Requirement: Large Research Materials Remain Referenced
Kaoju structured records SHALL reference rather than embed large or externally governed research materials.

#### Scenario: Material manifest records exact identity
- **WHEN** a repository, paper file, dataset, model, checkpoint, generated-data directory, raw output, or log is acquired or registered
- **THEN** the applicable bound manifest record stores its immutable locator, revision or digest, source class, size when known, access and license posture, managed-link or file Artifact refs, observed time, staleness policy, and Provenance Record refs
- **AND** the structured payload does not contain the material bytes or repository tree

#### Scenario: Dataset manifest is not the dataset store
- **WHEN** `manage-dataset` registers, refreshes, or removes a local dataset
- **THEN** the Topic Dataset Manifest is revised through its binding while link mutation remains owned by the Topic Workspace owner
- **AND** removal never deletes or rewrites the external dataset

### Requirement: Kaoju Workspace Bootstrap Validates Storage Readiness
`isomer-kaoju-workspace-mgr` SHALL establish binding and storage readiness before ordinary Kaoju skills write accepted durable records.

#### Scenario: Bootstrap validates complete contract
- **WHEN** Kaoju storage bootstrap runs for a Research Topic
- **THEN** it resolves Effective Topic Context and fresh Workspace Runtime state, required `topic.records.*` labels, the family-neutral provider and selected profiles, shared semantic registry, selected skill bindings, topic-level binding index, dataset-manifest posture, relevant latest records, worker output policy, and reset-checkpoint posture

#### Scenario: Bootstrap records readiness or blocker
- **WHEN** all required surfaces and bindings resolve
- **THEN** it records a Kaoju binding index and Workspace Readiness record through their bindings
- **AND** when a required label, profile, binding, query surface, owner, or reset decision is unavailable, it records an explicit blocker and prevents affected accepted writes

#### Scenario: Reset survival is explicit
- **WHEN** bootstrap records or user-selected survey records should survive a Topic Workspace reset
- **THEN** the workspace manager updates the selected reset checkpoint with exact record, payload, export, semantic-label, actor, and provenance refs
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

