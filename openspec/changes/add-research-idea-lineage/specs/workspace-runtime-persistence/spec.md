## ADDED Requirements

### Requirement: Workspace Runtime Research Idea Store
The Workspace Runtime SHALL persist canonical Research Ideas, Idea Realizations, Idea Lineage Edges, and Idea Generation Groups inside the Topic Workspace runtime database.

#### Scenario: Research idea rows are stored
- **WHEN** canonical idea data is written for a Topic Workspace
- **THEN** the runtime stores topic-scoped rows for Research Ideas, Idea Realizations, Idea Lineage Edges, and Idea Generation Groups with stable semantic ids, alias metadata, timestamps, status, metadata JSON, and provenance refs when known

#### Scenario: Canonical idea id is unique per topic
- **WHEN** a Research Idea row is written
- **THEN** validation requires the canonical `idea_id` to be unique within the Research Topic and allows source alias reuse only as metadata

#### Scenario: Runtime reopen preserves idea data
- **WHEN** a Workspace Runtime is reopened after process restart
- **THEN** previously written Research Ideas, realizations, lineage edges, generation groups, statuses, and metadata are recoverable with the same ids and topic refs

### Requirement: Workspace Runtime Idea Validation
The Workspace Runtime SHALL validate Research Idea refs and lineage consistency without silently repairing canonical data.

#### Scenario: Missing idea ref is reported
- **WHEN** an Idea Realization, Idea Lineage Edge, or Idea Generation Group references a missing Research Idea
- **THEN** runtime validation reports the broken ref and identifies the referring row

#### Scenario: Missing realization record is reported
- **WHEN** an Idea Realization references a missing durable research record
- **THEN** runtime validation reports the missing record ref and keeps the realization row visible for repair

#### Scenario: Cross-topic idea leakage is reported
- **WHEN** Research Idea data in one Topic Workspace references another Topic Workspace's idea, record, generation group, or decision record
- **THEN** runtime validation reports cross-topic leakage and names both conflicting refs when available

#### Scenario: Idea lineage cycle is reported
- **WHEN** non-archived Idea Lineage Edges create a cycle
- **THEN** runtime validation reports the cycle and does not delete or rewrite any edge

### Requirement: Workspace Runtime Idea Store APIs
The Workspace Runtime SHALL expose Python store APIs used by CLI, record writers, query index rebuilds, and web graph reads for canonical idea data.

#### Scenario: Store upserts idea data
- **WHEN** CLI or record-write code upserts a Research Idea, realization, lineage edge, or generation group
- **THEN** it uses Workspace Runtime store APIs that validate topic scope and return deterministic diagnostics

#### Scenario: Read-only operations do not mutate ideas
- **WHEN** GUI, query, export, graph, or validation code opens Workspace Runtime in read-only mode
- **THEN** it can inspect Research Idea data without refreshing, repairing, or backfilling idea rows
