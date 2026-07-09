## ADDED Requirements

### Requirement: Idea Timeline Read Model
The Topic Graph read API SHALL provide or support a timeline-friendly read model for Research Ideas without introducing a separate canonical timeline store.

#### Scenario: Timeline read model includes idea rows
- **WHEN** Project Web requests data for the Idea Timeline view of a valid Research Topic
- **THEN** the response includes topic identity, index revision when available, generated timestamp, idea nodes or rows with display keys, idea lineage edges or parent refs, diagnostics, and `mutated: false`

#### Scenario: Timeline can render parent display keys
- **WHEN** the timeline response includes parent-child idea relationships
- **THEN** the frontend has enough stable source and target idea identity to render parent display-key references from the current read model

#### Scenario: Timeline can apply graph-like filters
- **WHEN** Project Web requests or derives filtered Idea Timeline rows
- **THEN** the read model includes enough idea status, searchable text, visibility/supporting metadata, and lineage relation-kind data to support search, status filtering, relation filtering, and the Supporting Records toggle
- **AND** filter application remains bounded and reports `mutated: false`

#### Scenario: Timeline can sort and limit entries
- **WHEN** Project Web requests or derives sorted Idea Timeline rows
- **THEN** the read model includes enough creation time, updated time, display key, title, parent display-key or parent-id fallback, and idea identity data to sort every visible timeline column deterministically
- **AND** entry-count limiting is bounded and reports `mutated: false`

#### Scenario: Timeline read model uses existing idea semantics
- **WHEN** the backend builds the timeline read model
- **THEN** it uses canonical Research Ideas, Idea Realizations, and Idea Lineage Edges when available
- **AND** it preserves existing legacy fallback diagnostics when canonical Research Ideas are absent

#### Scenario: Timeline request is read-only
- **WHEN** Project Web requests the Idea Timeline read model
- **THEN** the backend does not rebuild, repair, cleanup, migrate, backfill, or write Workspace Runtime records or query-index rows

#### Scenario: Timeline read model reports interpretation problems
- **WHEN** the backend detects missing idea refs, malformed edges, invalid timestamps, duplicate ids, cycles, or other non-interpretable timeline data
- **THEN** the response includes diagnostics describing the issue
- **AND** the response remains bounded and read-only

#### Scenario: Missing display key is diagnostic
- **WHEN** a Research Idea lacks a display key required by the timeline read model
- **THEN** the response includes a diagnostic for the missing display key
- **AND** the response does not invent a persistent key during read-only browsing

### Requirement: Visible Graph Scope Metadata Favors Idea Views
The Topic Graph read API SHALL expose enough graph/view metadata for Project Web to distinguish the visible Idea Graph and Idea Timeline views.

#### Scenario: Idea graph metadata is available
- **WHEN** Project Web opens the Idea Graph view
- **THEN** the read model identifies the relationship graph view and preserves the `idea-lineage` semantics used by existing graph rendering

#### Scenario: Idea timeline metadata is available
- **WHEN** Project Web opens the Idea Timeline view
- **THEN** the read model or openable descriptor identifies the timeline/table presentation separately from the relationship graph presentation

### Requirement: Removed Dense Graph Scopes Are Unsupported
The Topic Graph read API SHALL reject removed dense graph scopes instead of preserving compatibility renderers for them.

#### Scenario: Artifact overview scope is rejected
- **WHEN** a caller requests `artifact-overview`
- **THEN** the response reports `unsupported_graph_scope`
- **AND** the operation does not mutate Workspace Runtime or query-index state

#### Scenario: Experiment records scope is rejected
- **WHEN** a caller requests `experiment-records`
- **THEN** the response reports `unsupported_graph_scope`
- **AND** the operation does not mutate Workspace Runtime or query-index state

#### Scenario: Paper revisions scope is rejected
- **WHEN** a caller requests `paper-revisions`
- **THEN** the response reports `unsupported_graph_scope`
- **AND** the operation does not mutate Workspace Runtime or query-index state
