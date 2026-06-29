## ADDED Requirements

### Requirement: External Repository Projection Regime
The system SHALL use `isomer-managed/topic-owned/{readonly,writable}/extern/` as the only standard developer-facing location for external repository projections inside Topic Main Development Repository.

#### Scenario: Read-only external projection is topic-owned
- **WHEN** a canonical external repository is exposed to topic-main for read-only use
- **THEN** the projection path is under `isomer-managed/topic-owned/readonly/extern/`
- **AND** boundary and setup material describe it as topic-owned read-only projection material

#### Scenario: Writable external projection is topic-owned
- **WHEN** a canonical external repository is exposed to topic-main for write use
- **THEN** the projection path is under `isomer-managed/topic-owned/writable/extern/`
- **AND** boundary and setup material state the write policy and whether writes affect a copy, clone, worktree, or explicitly authorized source

#### Scenario: Projection content is ignored
- **WHEN** the standard `isomer-managed/.gitignore` policy is prepared
- **THEN** it ignores `topic-owned/` projection content
- **AND** external projection content is not tracked by default through topic-main Git history

### Requirement: Tracked Projection Manifest
The system SHALL record external repository projection metadata as tracked Isomer material.

#### Scenario: Projection manifest lives in tracked manifests
- **WHEN** external projections are prepared or validated
- **THEN** metadata is written to `isomer-managed/tracked/manifests/extern-projections.toml`
- **AND** the manifest is small tracked coordination material rather than a projection content directory

#### Scenario: Projection manifest documents access intent
- **WHEN** the projection manifest records a projection
- **THEN** it names whether the projection is read-only or writable
- **AND** it names the projection mode, canonical source label, canonical source path, projected path, status, and blockers

### Requirement: Main Repository Root Is Not Polluted
The system SHALL keep Isomer-created external repo projections out of the Topic Main Development Repository root.

#### Scenario: Top-level extern is not created
- **WHEN** topic env setup projects external repos into topic-main
- **THEN** it does not create `extern/` at the topic-main root
- **AND** it keeps Isomer-created projection paths under `isomer-managed/`

#### Scenario: Existing user extern is not adopted
- **WHEN** an existing user topic-main repository already contains a root `extern/` directory
- **THEN** Isomer does not treat that path as the standard external projection root
- **AND** setup uses or reports only the semantic Isomer-managed projection roots
