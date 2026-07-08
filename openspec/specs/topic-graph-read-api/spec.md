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

