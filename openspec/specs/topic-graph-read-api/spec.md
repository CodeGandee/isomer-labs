# topic-graph-read-api Specification

## Purpose
TBD - created by archiving change add-topic-idea-iteration-map-gui. Update Purpose after archive.
## Requirements

### Requirement: Topic Graph View API
The system SHALL expose topic-scoped, renderer-neutral graph view APIs that return coherent read models for supported Research Topic graph scopes and report whether the returned topology is complete.

#### Scenario: Valid idea-lineage graph request
- **WHEN** a GUI calls `GET /api/topics/{topic_id}/graphs/idea-lineage` for a Research Topic resolved through the Project Manifest and Effective Topic Context
- **THEN** the response includes `ok`, `mutated: false`, `topic_id`, `topic_workspace_id`, `graph_scope: "idea-lineage"`, compatibility `renderer_hint`, `index_revision`, `generated_at`, `nodes`, `edges`, `groups`, `facets`, topology completeness metadata, optional paging or projection metadata, and `diagnostics`
- **AND** the response is derived from Workspace Runtime and query-index read models without rebuilding, repairing, cleaning up, migrating, or writing index rows

#### Scenario: Unsupported graph scope is rejected
- **WHEN** a GUI requests an unknown or removed graph scope
- **THEN** the response reports `unsupported_graph_scope`
- **AND** the operation does not mutate Workspace Runtime or query-index state

#### Scenario: React Flow is requested for hundreds of Idea Graph nodes
- **WHEN** a GUI requests `renderer=react-flow` for `idea-lineage` and the graph exceeds the former sparse renderer bound
- **THEN** the API does not reject the request solely because React Flow was requested
- **AND** it does not require or return a Sigma.js fallback as the only usable result

#### Scenario: Graph exceeds a renderer-independent transfer bound
- **WHEN** the complete Idea Graph exceeds a configured response safety bound
- **THEN** the API returns explicit incomplete-topology metadata, total counts, and diagnostics or a requested coherent neighborhood projection
- **AND** the safety decision does not select a frontend renderer

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

### Requirement: Topic Graph Responses Report Topology Completeness
The Topic Graph read API SHALL report whether a response contains every node and Idea Lineage Edge required to calculate traversal over its declared source scope.

#### Scenario: Response contains complete topology
- **WHEN** the returned graph contains every node and eligible edge in the requested source scope
- **THEN** the response reports `topology_complete: true`, total node count, and total edge count
- **AND** every returned edge references returned source and target nodes

#### Scenario: Response is truncated or paged
- **WHEN** a transfer bound, cursor, or other read limit omits source-scope nodes or cross-boundary edges
- **THEN** the response reports `topology_complete: false`, total node count, total edge count, and truncation diagnostics
- **AND** clients do not need to infer completeness from node count or renderer hints

#### Scenario: Response metadata changes without topology changes
- **WHEN** only generation time, transport metadata, or another non-topology field changes
- **THEN** the topology completeness value and topology identity remain stable for the same effective index revision and graph scope

### Requirement: Topic Graph API Supports Read-only N-hop Projection
The Topic Graph read API SHALL support a bounded, read-only multi-source N-hop projection when the frontend cannot obtain complete source topology safely.

#### Scenario: Client requests multi-source neighborhood
- **WHEN** a client supplies valid selected Research Idea node ids, a nonnegative hop radius, traversal direction, and optional Idea Lineage Edge-kind filters
- **THEN** the API returns the union of nodes whose shortest eligible path from any selected seed is at most the requested radius
- **AND** every selected seed has distance zero

#### Scenario: Projection requests incoming traversal
- **WHEN** projection direction is Incoming
- **THEN** the backend traverses each eligible Idea Lineage Edge from target to source

#### Scenario: Projection requests outgoing traversal
- **WHEN** projection direction is Outgoing
- **THEN** the backend traverses each eligible Idea Lineage Edge from source to target

#### Scenario: Projection requests both directions
- **WHEN** projection direction is Both
- **THEN** the backend traverses each eligible Idea Lineage Edge in either direction without changing its stored or returned direction

#### Scenario: Projection returns induced edges
- **WHEN** the projection has resolved its visible node set
- **THEN** the response includes every eligible Idea Lineage Edge whose source and target both belong to that visible set unless the request explicitly chooses traversal edges only

#### Scenario: Requested seed is unknown
- **WHEN** one or more requested seed ids do not identify Research Ideas in the current source graph
- **THEN** the response reports unresolved-seed diagnostics
- **AND** computes a projection from any remaining valid seeds without inventing graph nodes

#### Scenario: Neighborhood exceeds its safety bound
- **WHEN** the requested N-hop projection exceeds configured node, edge, seed-count, or radius bounds
- **THEN** the response reports that the projection is incomplete or rejected with actionable diagnostics
- **AND** it does not silently drop arbitrary nodes while reporting a complete projection

#### Scenario: Neighborhood request completes
- **WHEN** the API returns a full requested N-hop projection
- **THEN** projection metadata records resolved seed ids, hop radius, direction, edge-kind filters, total visible counts, source total counts, source index revision, and `topology_complete: true` for the projected scope

#### Scenario: Neighborhood projection is evaluated
- **WHEN** the backend calculates or returns an N-hop projection
- **THEN** it does not write selected seeds, focus settings, layout algorithms, layout parameters, Graph Layout Presets, or calculated positions to Workspace Runtime or query-index state

### Requirement: Backend Does Not Persist React Flow Layout State
The Topic Graph API SHALL remain renderer-neutral and SHALL NOT treat React Flow positions or browser-local Graph Layout Presets as canonical research data.

#### Scenario: Client applies a layout preset
- **WHEN** Project Web previews or applies a Graph Layout Preset
- **THEN** graph read requests continue to exchange nodes, edges, topology, projection parameters, and diagnostics without uploading the preset or calculated positions

#### Scenario: Graph read model is generated
- **WHEN** the backend returns an Idea Graph response
- **THEN** it does not read or write browser-local layout presets, panel selection, viewport state, or calculated React Flow coordinates
