# topic-graph-read-api Specification

## Purpose
TBD - created by archiving change add-topic-idea-iteration-map-gui. Update Purpose after archive.
## Requirements
### Requirement: Topic Graph View API
The system SHALL expose topic-scoped graph view APIs that return renderer-neutral read models for Research Topic artifact relationships.

#### Scenario: Valid idea-lineage graph request
- **WHEN** a GUI calls `GET /api/topics/{topic_id}/graphs/idea-lineage` for a Research Topic resolved through the Project Manifest and Effective Topic Context
- **THEN** the response includes `ok`, `mutated: false`, `topic_id`, `topic_workspace_id`, `graph_scope: "idea-lineage"`, `renderer_hint`, `index_revision`, `generated_at`, `nodes`, `edges`, `groups`, `facets`, optional `paging`, and `diagnostics`
- **AND** the response is derived from Workspace Runtime and query-index read models without rebuilding, repairing, cleaning up, migrating, or writing index rows

#### Scenario: Dense graph scopes are supported
- **WHEN** a GUI requests `artifact-overview`, `experiment-records`, or `paper-revisions`
- **THEN** the response uses the same graph view model and returns a `sigma-overview` renderer hint unless the request filters produce a bounded sparse graph

#### Scenario: Unsupported graph scope is rejected
- **WHEN** a GUI requests an unknown graph scope
- **THEN** the response reports `unsupported_graph_scope`
- **AND** the operation does not mutate Workspace Runtime or query-index state

#### Scenario: Renderer is unsuitable for graph size
- **WHEN** a GUI requests `renderer=react-flow` for a graph that exceeds the configured sparse graph bound
- **THEN** the response reports `graph_too_large_for_renderer` with a Sigma.js fallback hint
- **AND** the response does not return an unbounded React Flow detail graph

### Requirement: Renderer-neutral Graph Model
The topic graph API SHALL describe graph nodes, edges, groups, facets, and diagnostics without exposing renderer-specific state as canonical research data.

#### Scenario: Nodes carry inspection metadata
- **WHEN** the graph API returns a node
- **THEN** the node includes stable `id`, `record_id`, `material_kind`, `density_class`, title or one-liner text, status when known, producer or skill when known, created or updated timestamps when known, source refs, detail refs, and renderer hints

#### Scenario: Edges carry relationship metadata
- **WHEN** the graph API returns an edge
- **THEN** the edge includes stable `id`, `source`, `target`, `relation_kind`, canonical flag, optional lineage kind, optional generation id, optional status, optional rationale, optional confidence, and source classification

#### Scenario: Relationship labels map to accepted vocabularies
- **WHEN** graph relationships are derived
- **THEN** relation kinds map to query-index relation kinds, canonical lineage kinds, or accepted Research Inquiry Relationship vocabulary
- **AND** generated Markdown prose is not used as an authoritative lineage source

#### Scenario: Groups represent generation and partial-data structure
- **WHEN** generation groups, sibling sets, unconnected ideas, or artifact clusters are present
- **THEN** the graph API returns group entries with `group_kind`, title, optional purpose, optional parent-set digest, node ids, and diagnostics

### Requirement: Record Viewer Descriptor API
The system SHALL expose lightweight record viewer descriptors so GUI tabs can choose a viewer before loading heavy content.

#### Scenario: Descriptor selects viewer kind
- **WHEN** a GUI calls `GET /api/topics/{topic_id}/viewer/records/{record_id}` for an indexed record
- **THEN** the response includes `ok`, `mutated: false`, topic id, record id, title, viewer kind, optional primary content URL, detail URL, optional render URL, optional files URL, optional facets URL, media type when known, existence state, and diagnostics

#### Scenario: Descriptor avoids heavy payloads
- **WHEN** the descriptor response is produced
- **THEN** it does not include full structured payload JSON, rendered Markdown content, PDF bytes, image bytes, terminal output, credentials, or local file contents

#### Scenario: Missing record is reported
- **WHEN** the requested record no longer exists in the selected topic read model
- **THEN** the response reports `record_not_found`
- **AND** the operation does not mutate Workspace Runtime or query-index state

### Requirement: Topic Change Event Stream
The system SHALL expose topic-scoped live update hints for GUI read-model invalidation.

#### Scenario: Topic event stream emits invalidation hints
- **WHEN** a GUI opens `GET /api/events?topic_id={topic_id}` for a valid Research Topic
- **THEN** the service emits events such as `topic.index.changed`, `topic.records.changed`, `topic.diagnostics.changed`, or `topic.runtime.changed` with event id, topic id, optional topic workspace id, optional index revision, optional changed record ids, optional changed material kinds, optional graph scopes, diagnostic count, and timestamp

#### Scenario: Events do not carry sensitive or heavy content
- **WHEN** a topic change event is emitted
- **THEN** it does not include raw payload bodies, rendered Markdown bodies, file contents, terminal input, terminal output, credentials, or authorization headers

#### Scenario: Polling fallback remains valid
- **WHEN** SSE is unavailable or disconnected
- **THEN** the GUI can fall back to bounded polling of topic graph, record, runtime, and diagnostics endpoints without requiring a backend write or maintenance action

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

### Requirement: Idea Graph Display Key Payloads
The topic graph read API SHALL include Research Idea display keys in graph node payloads using the `I-<index>` format.

#### Scenario: Idea node includes display key
- **WHEN** the graph API returns a node for a canonical Research Idea with a display key
- **THEN** the node includes `display_key` in the `I-<index>` format
- **AND** the value matches the corresponding Workspace Runtime Research Idea row

#### Scenario: Missing display key is diagnostic data
- **WHEN** a graph node represents an old Research Idea without a display key
- **THEN** the graph API keeps returning a safe graph payload
- **AND** diagnostics or recent-errors data can report that explicit display-key repair is needed

### Requirement: Idea Graph Visible Labels Use Display Keys
The Project Web Idea Graph SHALL use display keys as the leading short identity in visible node labels when display keys are available.

#### Scenario: React Flow node label includes key
- **WHEN** an Idea Graph node has `display_key: "I-3"` and title `Precision model`
- **THEN** the visible node label begins with `I-3`
- **AND** the title remains visible in the same label

#### Scenario: Graph label falls back safely
- **WHEN** an Idea Graph node has no display key
- **THEN** the visible label falls back to the existing title or idea id behavior
- **AND** the graph does not crash

