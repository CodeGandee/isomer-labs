## ADDED Requirements

### Requirement: Path Plans Preserve Effective Semantic Identity
Workspace Runtime SHALL record Path Plans with enough semantic metadata to identify the effective surface that produced a durable path.

#### Scenario: Built-in path plan records semantic metadata
- **WHEN** runtime initialization, Agent Team Instance creation, or adapter materialization records a Path Plan for a built-in semantic label
- **THEN** the Path Plan stores semantic label, scope ref, compatibility surface id, `storage_profile` id, canonical path, source, and source detail

#### Scenario: Custom path plan records semantic metadata
- **WHEN** a durable runtime record depends on a path resolved from a valid custom semantic label
- **THEN** the Path Plan stores that custom semantic label, scope ref, `storage_profile` id, canonical path, source, source detail, and a snapshot of storage-profile-derived traits available from the effective catalog

#### Scenario: Path Plan source distinguishes env and manifest
- **WHEN** a Path Plan is selected from a generated semantic env var, compatibility env var, Topic Workspace Manifest binding, or default layout profile
- **THEN** the stored Path Plan source and source detail distinguish which source produced the path without storing unrelated environment values

### Requirement: Runtime Validation Compares Recorded and Configured Paths
Workspace Runtime validation SHALL compare recorded Path Plans with current configured semantic resolution without mutating historical records.

#### Scenario: Custom binding drift is reported
- **WHEN** a stored Path Plan for a custom semantic label differs from current configured resolution for that label and scope
- **THEN** runtime validation reports path-plan drift while preserving the stored Path Plan

#### Scenario: Removed custom label remains historical
- **WHEN** a stored Path Plan references a custom semantic label that is no longer declared in the Topic Workspace Manifest
- **THEN** runtime validation reports that the current binding is missing and keeps the historical Path Plan available for existing dependent records

#### Scenario: Drift does not rewrite dependent records
- **WHEN** validation detects drift between a Path Plan and current configured resolution
- **THEN** validation does not rewrite runtime rows, move files, delete files, or update Artifact locators automatically

### Requirement: Runtime Records Use Semantic Path Evidence Before File Dependency
Workspace Runtime SHALL store or reference semantic path evidence before a new durable runtime record depends on a project-local file path.

#### Scenario: New durable record references path evidence
- **WHEN** a new runtime record stores a project-local file ref after this change
- **THEN** the record references an existing Path Plan or records equivalent semantic label, scope, source, and relative path evidence before downstream state depends on the file

#### Scenario: Historical absolute paths remain readable
- **WHEN** validation or inspection reads a historical record that only stores an absolute path
- **THEN** the system keeps the record readable and reports any missing semantic evidence as a migration or compatibility diagnostic rather than deleting the record
