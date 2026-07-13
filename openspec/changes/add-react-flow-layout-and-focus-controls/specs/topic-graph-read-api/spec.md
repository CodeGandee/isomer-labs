## MODIFIED Requirements

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

## ADDED Requirements

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
