## MODIFIED Requirements

### Requirement: Large Research Materials Remain Referenced
Kaoju records SHALL reference rather than embed large, binary, directory-shaped, externally governed, or repository material.

#### Scenario: Material manifest records exact identity
- **WHEN** a repository, paper file, dataset, model, checkpoint, generated-data directory, raw output, log, wiki tree, TeX tree, viewer deployment, or PDF is externally acquired or registered
- **THEN** the applicable record stores or links its immutable locator, revision or digest, source class, size when known, access and license posture, managed-link or Artifact refs, observed time, staleness policy, and Provenance Record refs
- **AND** structured payloads and DB metadata do not contain the material bytes or directory tree

#### Scenario: Repository material records external acquisition evidence
- **WHEN** a Canonical External Repository is accepted as Kaoju material
- **THEN** its Artifact records or links the semantic repository label, requested and resolved source locators, observed immutable commit or digest, acquisition method, sanitized external command evidence, relationship basis, limitations, and verification time
- **AND** it does not depend on a `repository_acquisition` extension point, an Isomer-generated Git command request, or raw credential-bearing output

#### Scenario: Directory artifact uses a checksummed manifest
- **WHEN** accepted content contains multiple files
- **THEN** its Artifact content locator points to a versioned manifest listing member paths, media types, sizes, checksums, entry points, and external refs
- **AND** later discovery resolves the manifest through the DB rather than scanning the directory

#### Scenario: Dataset manifest is not the dataset store
- **WHEN** `manage-dataset` registers, refreshes, or removes a local dataset
- **THEN** the Topic Dataset Manifest is revised through its binding while link mutation remains owned by the Topic Workspace owner
- **AND** removal never deletes or rewrites the external dataset

### Requirement: Every Survey-Process Durable Output Has a State-DB Entry
Every durable record named by a survey-process use case SHALL be registered in the Topic Workspace state DB and linked to authoritative filesystem or Canonical External Repository content.

#### Scenario: Durable artifact is accepted
- **WHEN** a Kaoju procedure accepts a structured record, ordinary file, directory export, registered repository, script, log, environment ref, Run result, or PDF
- **THEN** it creates an Artifact Core Record with semantic id metadata, artifact kind, status, timestamps, locator kind, locator or semantic label, content link, checksum or immutable identity when applicable, and provenance links
- **AND** success is not reported until Artifact registration completes

#### Scenario: External repository topology is registered before Artifact acceptance
- **WHEN** a Kaoju procedure accepts repository content acquired through external commands
- **THEN** it first requires the verified existing path to resolve through its non-main `topic.repos.*` binding and then records the applicable Artifact revision
- **AND** a filesystem checkout without semantic registration remains pre-acceptance material rather than a successful durable output

#### Scenario: Agent looks for an artifact
- **WHEN** a skill needs an existing direction, reading list, source, paper, wiki, environment, trial, audit, or synthesis artifact
- **THEN** it queries the state DB by semantic id, scope, status, lineage, or stable ref
- **AND** it does not scan the Topic Workspace directory tree as a fallback

#### Scenario: DB and content disagree
- **WHEN** the DB entry points to missing or checksum-mismatched content or its repository identity disagrees with the observed registered path
- **THEN** the system reports stale or corrupt artifact state and the recovery route
- **AND** the DB entry remains discoverable for diagnosis rather than being silently ignored or revised
