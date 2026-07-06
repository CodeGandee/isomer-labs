## ADDED Requirements

### Requirement: Query-index Freshness Metadata
The research record query index SHALL expose read-only freshness metadata that GUI consumers can use for cache invalidation and graph refresh.

#### Scenario: Export includes freshness token
- **WHEN** a GUI or operator runs a topic-scoped query export
- **THEN** the response includes a deterministic freshness token such as `index_revision` or an equivalent change token derived from query-index state
- **AND** the export still returns `mutated: false`

#### Scenario: Freshness metadata survives partial index state
- **WHEN** query-index tables are stale, incomplete, or missing some derived rows
- **THEN** the response reports diagnostics and exposes the best available freshness metadata for the read model that was actually served
- **AND** it does not create, refresh, repair, or backfill query-index rows

#### Scenario: GUI invalidation can compare revisions
- **WHEN** the Project Web GUI receives a topic change event, polls a graph view, or refreshes a query export
- **THEN** it can compare the returned freshness token with its cached value to decide whether relevant open views need refetching

### Requirement: Graph-ready Query Export Data
The research record query index SHALL expose enough relationship, facet, and file metadata for GUI graph read models without requiring Markdown parsing.

#### Scenario: Idea graph export data is complete enough for projection
- **WHEN** a GUI or backend graph read model consumes query export data for idea lineage
- **THEN** the export provides record summaries, typed edges, idea facets, route decisions, claims, metrics, facts, file refs, source JSON paths when known, source classifications, selected flags when known, statuses when known, producer or skill hints when known, and diagnostics

#### Scenario: File metadata supports safe GUI actions
- **WHEN** query export or file detail returns a file ref
- **THEN** the row includes existence or openability metadata sufficient for the GUI to avoid offering actions for missing, external, unresolved, or outside-project files

#### Scenario: Markdown is not an authoritative graph source
- **WHEN** the graph read model derives idea relationships, evidence links, claims, metrics, route status, or file refs
- **THEN** it uses payload-backed fields, authored metadata, canonical lineage, accepted query-index edges, or file metadata rather than generated Markdown body parsing as the authoritative source

### Requirement: Query-index Read-only GUI Consumption
The research record query index SHALL support Project Web GUI graph and detail browsing through read-only access paths.

#### Scenario: Graph read model opens runtime read-only
- **WHEN** the Project Web API composes a topic graph from query-index export, lineage, siblings, files, or facets
- **THEN** it opens Workspace Runtime and query-index tables in read-only mode
- **AND** it reports stale or missing index data as diagnostics or maintenance hints

#### Scenario: Explicit maintenance owns repair
- **WHEN** graph or viewer APIs find stale rows, missing rows, broken edges, missing files, unsupported relation kinds, or extractor failures
- **THEN** they do not repair the index during browsing
- **AND** explicit rebuild, validation, and cleanup commands remain the only query-index maintenance paths
