## ADDED Requirements

### Requirement: Lineage-aware Research Record Writes
The research recording API and CLI SHALL accept canonical artifact lineage inputs separately from optional query-index relationship hints.

#### Scenario: Create supplies parents
- **WHEN** a caller creates a research record with parent record refs, lineage kind, parent roles, generation id, or decision record id
- **THEN** the recording API validates and stores those refs as canonical artifact lineage rather than only as query-index relationship metadata

#### Scenario: Create supplies relationship hints
- **WHEN** a caller creates a research record with non-canonical relationship hints such as evidence, citation, file, summary, support, or GUI relationship metadata
- **THEN** the recording API preserves those hints for query-index extraction without treating them as canonical artifact lineage

#### Scenario: Lineage and relationship hints coexist
- **WHEN** a record creation request includes both canonical lineage inputs and optional relationship hints
- **THEN** the recording API stores canonical lineage and query-index hints through separate fields and reports diagnostics for each surface independently

### Requirement: Research Record Revision Command
The research recording CLI SHALL provide a revision path that creates a new descendant record for content-changing revisions.

#### Scenario: Revise creates descendant
- **WHEN** a caller revises an accepted structured record with a new payload
- **THEN** the CLI creates a new record, stores the new payload, and creates a canonical `revision_of` lineage edge from the revised record to the new record

#### Scenario: Revise preserves semantic identity
- **WHEN** a caller revises a record with a placeholder, semantic id, or latest-for semantic id
- **THEN** the new record preserves the semantic identity needed for latest-view resolution while retaining a distinct record id

#### Scenario: Update remains non-revision
- **WHEN** a caller updates status, actor metadata, file hints, query hints, or repair metadata without changing accepted content
- **THEN** the operation MAY update the existing record without creating a revision edge

### Requirement: Research Record Lineage Maintenance CLI
The research recording CLI SHALL expose explicit maintenance commands for canonical lineage.

#### Scenario: Lineage edge is added explicitly
- **WHEN** an operator runs a lineage maintenance command to add a parent-child edge
- **THEN** the CLI validates topic scope, record existence, acyclicity, and lineage kind before mutating canonical lineage

#### Scenario: Lineage DAG is validated
- **WHEN** an operator runs lineage validation for a Topic Workspace
- **THEN** the CLI reports missing records, cross-topic refs, cycles, invalid revision chains, missing generation groups, and unsupported lineage kinds

#### Scenario: Lineage maintenance avoids payload inference
- **WHEN** lineage maintenance inspects existing records
- **THEN** it uses explicit payload fields, metadata, and existing canonical refs and does not infer authoritative lineage from generated Markdown prose
