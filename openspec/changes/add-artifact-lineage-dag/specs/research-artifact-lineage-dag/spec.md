## ADDED Requirements

### Requirement: Canonical Artifact Lineage DAG
The system SHALL represent durable research artifact parent-child relationships as a canonical Topic Workspace DAG.

#### Scenario: Child record is linked to one parent
- **WHEN** a durable research record is created from one prior durable record
- **THEN** Workspace Runtime stores a canonical lineage edge with parent record id, child record id, lineage kind, status, timestamps, rationale when supplied, and metadata

#### Scenario: Child record is linked to many parents
- **WHEN** a durable research record combines or is selected from several prior durable records
- **THEN** Workspace Runtime stores one canonical lineage edge per parent-child relationship without forcing a single parent

#### Scenario: Non-lineage refs remain outside the DAG
- **WHEN** a record cites evidence, materializes files, supports a claim, summarizes another record, or carries GUI facet metadata
- **THEN** the system MAY index those refs as query relationships without treating them as canonical artifact lineage

### Requirement: Artifact Lineage Acyclicity
The system SHALL prevent canonical artifact lineage edges from creating cycles within a Topic Workspace.

#### Scenario: Acyclic edge is accepted
- **WHEN** a lineage edge from parent record A to child record B would not create a path from B back to A
- **THEN** the system accepts the lineage edge

#### Scenario: Cyclic edge is rejected
- **WHEN** a lineage edge from parent record A to child record B would create a path from B back to A
- **THEN** the system rejects the edge and reports a lineage cycle diagnostic without mutating the canonical lineage DAG

#### Scenario: Cross-topic parent is rejected
- **WHEN** a lineage edge references a parent or child outside the active Topic Workspace
- **THEN** the system rejects the edge and reports a cross-topic lineage diagnostic

### Requirement: Artifact Revision Chains
The system SHALL represent content-changing revisions as new descendant records in a linear revision chain.

#### Scenario: Record is revised
- **WHEN** an accepted structured research record receives a content-changing revision
- **THEN** the system creates a new durable record and stores a `revision_of` lineage edge from the prior record to the new record

#### Scenario: Revision parent is unique
- **WHEN** a new record is created as a revision
- **THEN** the system allows exactly one immediate `revision_of` parent for that record

#### Scenario: Historical revision remains visible
- **WHEN** a record is superseded by a revision
- **THEN** the prior record remains queryable as historical state and the latest view resolves through explicit latest metadata or lineage-derived state

### Requirement: Artifact Generation Groups
The system SHALL represent sibling exploration paths through generation groups.

#### Scenario: Sibling candidates are generated together
- **WHEN** several durable records are generated from the same parent set as alternatives in one exploration pass
- **THEN** the system stores a generation group and associates each child lineage edge with that generation group

#### Scenario: Siblings are queried
- **WHEN** a caller asks for siblings of a record
- **THEN** the system returns other records in the same generation group with the same parent set and excludes the selected record itself

#### Scenario: Pairwise sibling edges are unnecessary
- **WHEN** sibling records share a generation group
- **THEN** the system does not require pairwise `sibling_of` edges to preserve sibling semantics

### Requirement: Artifact Lineage Query
The system SHALL expose topic-scoped lineage queries over the canonical artifact DAG.

#### Scenario: Ancestors are queried
- **WHEN** a caller queries ancestors for a record
- **THEN** the system returns upstream canonical lineage edges and node summaries in deterministic order

#### Scenario: Descendants are queried
- **WHEN** a caller queries descendants for a record
- **THEN** the system returns downstream canonical lineage edges and node summaries in deterministic order

#### Scenario: DAG diagnostics are reported
- **WHEN** canonical lineage data is missing, stale, invalid, cyclic, or references missing records
- **THEN** lineage query and validation commands report diagnostics rather than inferring hidden parents from generated prose
