## MODIFIED Requirements

### Requirement: Kaoju Artifact Bindings Are Separate and Complete
The package SHALL provide one versioned machine-readable Kaoju binding registry that is separate from the storage-neutral semantic registry and complete for every active Kaoju semantic id.

#### Scenario: Binding entry is complete
- **WHEN** the binding registry maps a Kaoju semantic id
- **THEN** the entry names its artifact type, compatible record kind, default semantic label, family-neutral format profile, content mode, producer, consumers, required relationship roles, revision mode, scope-key policy, latest-selection policy, and validation and acceptance expectations
- **AND** it does not embed executable commands, provider payloads, credentials, or implementation-specific command bodies

#### Scenario: Binding coverage is bidirectional
- **WHEN** the Kaoju binding validator compares the shared semantic registry, active skill references, binding registry, schema and renderer assets, and built-in profile catalog
- **THEN** it rejects missing, extra, duplicated, cross-family, unresolved, or incompatible semantic ids, profiles, producers, consumers, scope policies, and content modes
- **AND** each diagnostic names the family, semantic id, affected file, line when available, and violated binding rule

#### Scenario: Skills resolve physical bindings through the registry
- **WHEN** a Kaoju skill needs to create, revise, or query an accepted durable output
- **THEN** it resolves the binding through `isomer-cli project artifacts describe` or the equivalent package service
- **AND** per-skill binding pages are generated summaries or concise references rather than independent physical binding authorities

#### Scenario: Binding selects a storage surface without defining an internal path
- **WHEN** a Kaoju binding selects a managed content mode and default Semantic Workspace Surface Label
- **THEN** the artifact service allocates a generic internal path from record kind and opaque record or revision identity
- **AND** the binding and producer do not declare, construct, or rely on a Kaoju-specific subdirectory convention

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
Kaoju bindings SHALL define canonical lineage, scope, and revision behavior for every semantic id.

#### Scenario: Scoped current-state object is revised
- **WHEN** accepted content changes for a direction set, direction-owned reading list, source-owned digest, artifact library, Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, paper structure, paper template, paper draft, current terminal status, or another binding marked as current state
- **THEN** the service creates a revision so the prior record remains historical and the new record becomes the explicit latest candidate for the same binding-defined scope
- **AND** records in another direction, source, paper line, or target scope remain independently current

#### Scenario: Delta and audit remain separate records
- **WHEN** a curated intake, direction expansion, audit, follow-up, bounded repair, template export, build attempt, wiki export, environment preparation, or trial produces event evidence
- **THEN** it creates a separate descendant record with immediate parent refs and applicable lineage roles
- **AND** it does not overwrite the base survey artifact or prior event

#### Scenario: Run fidelity is not revised away
- **WHEN** a faithful Run fails and an adapted or repaired Run follows
- **THEN** each Run remains a separate record with its own purpose, fidelity, inputs, outputs, timing, environment, and lineage
- **AND** the later Run does not revise or replace the earlier verdict

#### Scenario: Competing current candidates remain visible
- **WHEN** two non-superseded accepted records claim the same semantic id and scope
- **THEN** scoped latest lookup reports a conflict with both stable refs
- **AND** it does not select solely by timestamp

### Requirement: Large Research Materials Remain Referenced
Kaoju records SHALL reference rather than embed large, binary, directory-shaped, externally governed, or repository material.

#### Scenario: Material manifest records exact identity
- **WHEN** a repository, paper file, dataset, model, checkpoint, generated-data directory, raw output, log, wiki tree, TeX tree, viewer deployment, or PDF is acquired or registered
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

## ADDED Requirements

### Requirement: Every Survey-Process Durable Output Has a State-DB Entry
Every durable record named by a survey-process use case SHALL be registered in the Topic Workspace state DB and linked to authoritative filesystem or canonical repository content.

#### Scenario: Durable artifact is accepted
- **WHEN** a Kaoju procedure accepts a structured record, ordinary file, directory export, repository, script, log, environment ref, Run result, or PDF
- **THEN** it creates an Artifact Core Record with semantic id metadata, artifact kind, status, timestamps, locator kind, locator or semantic label, content link, checksum or immutable identity when applicable, and provenance links
- **AND** success is not reported until registration completes

#### Scenario: Agent looks for an artifact
- **WHEN** a skill needs an existing direction, reading list, source, paper, wiki, environment, trial, audit, or synthesis artifact
- **THEN** it queries the state DB by semantic id, scope, status, lineage, or stable ref
- **AND** it does not scan the Topic Workspace directory tree as a fallback

#### Scenario: DB and content disagree
- **WHEN** the DB entry points to missing or checksum-mismatched content
- **THEN** the system reports stale or corrupt artifact state and the recovery route
- **AND** the DB entry remains discoverable for diagnosis rather than being silently ignored
