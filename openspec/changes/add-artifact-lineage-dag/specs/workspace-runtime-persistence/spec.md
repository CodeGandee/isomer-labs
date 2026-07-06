## ADDED Requirements

### Requirement: Workspace Runtime Artifact Lineage Storage
Workspace Runtime SHALL persist canonical artifact lineage edges and generation groups in topic-scoped SQLite tables.

#### Scenario: Runtime initializes lineage tables
- **WHEN** Workspace Runtime initializes or migrates `state.sqlite`
- **THEN** it creates or preserves tables for canonical artifact lineage edges and generation groups with indexes for topic, parent record, child record, lineage kind, and generation group

#### Scenario: Runtime stores lineage with records
- **WHEN** the recording API creates a record with lineage parents or generation metadata
- **THEN** Workspace Runtime stores the lifecycle record and structured payload first, then stores validated canonical lineage edges in the same Topic Workspace

#### Scenario: Runtime reset preserves schema support
- **WHEN** a Topic Workspace is reset or bootstrapped
- **THEN** the reset path prepares the artifact lineage schema without requiring any lineage rows to exist

### Requirement: Workspace Runtime Lineage Validation
Workspace Runtime SHALL validate canonical artifact lineage before accepting it.

#### Scenario: Missing parent is reported
- **WHEN** a lineage edge references a missing parent record
- **THEN** Workspace Runtime rejects the edge or reports a validation diagnostic according to the operation mode

#### Scenario: Missing child is reported
- **WHEN** a lineage edge references a missing child record
- **THEN** Workspace Runtime rejects the edge or reports a validation diagnostic according to the operation mode

#### Scenario: Cycle check is topic scoped
- **WHEN** Workspace Runtime checks whether a lineage edge creates a cycle
- **THEN** the check is scoped to the active Topic Workspace and does not traverse records from other topics

### Requirement: Workspace Runtime Latest Artifact Views
Workspace Runtime SHALL derive current/latest artifact views from explicit latest metadata and canonical revision lineage without mutating historical records.

#### Scenario: Latest semantic record is resolved
- **WHEN** several records share a semantic id or placeholder and one is the newest accepted revision
- **THEN** Workspace Runtime can resolve the latest record without deleting or rewriting prior records

#### Scenario: Historical record remains inspectable
- **WHEN** a record is no longer latest because a descendant revision exists
- **THEN** Workspace Runtime keeps the historical record, payload, lineage edges, and provenance inspectable
