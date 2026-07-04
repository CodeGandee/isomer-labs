# research-record-query-index Specification

## Purpose
TBD - created by archiving change add-research-record-graph-index. Update Purpose after archive.
## Requirements
### Requirement: Topic-scoped Research Record Query Index
The system SHALL maintain a topic-scoped SQL query index over Workspace Runtime research records for GUI, CLI, and operator inspection.

#### Scenario: Record metadata is indexed
- **WHEN** a Topic Workspace has lifecycle records with structured payload rows or rendered record bodies
- **THEN** the query index exposes each indexed record with record id, record kind, status, topic/workspace refs, format profile refs when known, title, summary, producer or consumer hints when known, content path, rendered Markdown path when known, timestamps, and validation/render status

#### Scenario: Canonical storage remains authoritative
- **WHEN** query index rows disagree with `lifecycle_records`, `structured_research_payloads`, or rendered record locators
- **THEN** validation reports stale or inconsistent index rows and treats the canonical runtime records and payload rows as the source of truth

#### Scenario: Index rows are rebuildable
- **WHEN** an operator rebuilds the query index for a Topic Workspace
- **THEN** the system recreates derived index rows from canonical records, structured payloads, rendered Markdown locators, and accepted operation-set files without requiring Markdown body parsing as an authoritative source

### Requirement: Query-index Write Ownership
The Workspace Runtime record store and query-index service SHALL be responsible for writing query-index tables.

#### Scenario: Producers write through the recording API
- **WHEN** a Producer Agent, Topic Actor, Project Operator, or GUI-approved action creates or updates research content
- **THEN** it writes the canonical record through the research recording API or CLI and does not write query-index SQL tables directly

#### Scenario: Runtime refreshes affected index rows
- **WHEN** the recording API creates or updates a lifecycle record, structured payload, rendered locator, relationship hint, file hint, or index hint
- **THEN** Workspace Runtime writes the canonical data first and then refreshes affected query-index rows or marks them stale for rebuild

#### Scenario: Explicit archive refreshes index state
- **WHEN** the recording API archives or otherwise explicitly mutates a research record status
- **THEN** Workspace Runtime updates the canonical lifecycle record and refreshes or marks stale affected query-index rows

#### Scenario: Read operations do not mutate index rows
- **WHEN** an agent, operator, or GUI runs record list, show, validate, render, export, or another read-only inspection operation
- **THEN** the operation does not create, refresh, repair, or backfill query-index rows in `state.sqlite`
- **AND** stale or missing index data is reported as a diagnostic or rebuild recommendation

#### Scenario: Rebuild owns backfill
- **WHEN** existing topic records need query-index rows
- **THEN** an explicit Workspace Runtime rebuild operation backfills derived rows from canonical records, structured payloads, rendered locators, and accepted operation-set files

### Requirement: Research Record Relationship Index
The system SHALL index typed relationships between research records as graph edges without making the graph the only research record view.

#### Scenario: Edge source is classified
- **WHEN** an edge is written or rebuilt
- **THEN** the edge records source and target record ids, relation kind, optional role, source field or JSON path when known, source classification, confidence when known, status, rationale when known, and metadata

#### Scenario: Relation vocabulary supports research flows
- **WHEN** an edge relation kind is validated
- **THEN** the system accepts known relation kinds such as `uses_input`, `evidence_basis`, `routes_to`, `supports_claim`, `derived_from`, `supersedes`, `produces`, `materializes_file`, `blocks`, `cites`, and `summarizes`
- **AND** it accepts `custom.*` relation kinds as explicit extensions

#### Scenario: Low-confidence body inference is marked
- **WHEN** the system creates an edge from Markdown body inference rather than explicit metadata or structured payload fields
- **THEN** the edge is marked as inferred from body content and is not treated as authoritative support for claims unless later confirmed by authored metadata or accepted payload fields

### Requirement: Research Record File Index
The system SHALL index files attached to, produced by, or materialized from research records without requiring every file to become a lifecycle record.

#### Scenario: Attached files are indexed
- **WHEN** a research record references, renders, produces, or accepts a project-local file
- **THEN** the query index records the owning record id, file path or locator, file role, semantic label when known, operation-set id when known, digest when available, size when available, media type when known, existence status, and metadata

#### Scenario: Operation-set outputs can be indexed
- **WHEN** a Topic Workspace contains accepted worker output files associated with a record, run, or artifact manifest
- **THEN** the query index can expose those files as indexed attachments while preserving Artifact lifecycle records only for accepted durable artifacts

### Requirement: Research Record Facet Extraction
The system SHALL extract normalized GUI facets from structured research payloads using profile-aware extractors.

#### Scenario: Common DeepSci facets are extracted
- **WHEN** a structured payload matches a supported DeepSci record profile
- **THEN** the index extracts applicable ideas, route decisions, metrics, claims, artifact/file references, and generic scalar facts with source JSON paths or source file locators

#### Scenario: Unsupported profile still indexes the record
- **WHEN** a structured payload uses an unknown or unsupported profile
- **THEN** the system indexes the record metadata and records a non-fatal facet extraction diagnostic instead of rejecting the record

#### Scenario: Generic facts preserve useful scalar data
- **WHEN** a supported payload contains scalar fields that are useful for inspection but do not match a dedicated facet table
- **THEN** the system can record those fields as generic JSON facts with record id, JSON path, value type, value, and extractor metadata

### Requirement: Research Record Query Export
The system SHALL provide deterministic query/export behavior for GUI and operator views of indexed research records.

#### Scenario: Query list reads indexed records
- **WHEN** an operator or GUI runs `isomer-cli ext research records query list` with topic-scoped filters such as record kind, status, profile, facet, or limit
- **THEN** the command reads query-index tables through a read-only runtime connection and returns deterministic JSON with indexed record summaries and diagnostics

#### Scenario: Topic export includes graph and facets
- **WHEN** a GUI or operator runs `isomer-cli ext research records query export` for a Topic Workspace
- **THEN** the system returns topic-scoped nodes, edges, files, ideas, routes, metrics, claims, generic facts, diagnostics, and detail locators in deterministic JSON

#### Scenario: Topic export supports named views
- **WHEN** a GUI or operator requests an export view
- **THEN** the command supports `graph`, `dashboard`, `timeline`, `ideas`, `experiments`, and `claims` view names without mutating Workspace Runtime state

#### Scenario: Lineage query reads edges
- **WHEN** an operator or GUI runs `isomer-cli ext research records query lineage <record-id>`
- **THEN** the command returns upstream, downstream, or bidirectional indexed edges and node summaries for the selected record without repairing missing edges

#### Scenario: Files query reads attachments
- **WHEN** an operator or GUI runs `isomer-cli ext research records query files <record-id>`
- **THEN** the command returns indexed file attachments, roles, locators, existence status, and diagnostics for the selected record without touching the files

#### Scenario: Facets query reads normalized facets
- **WHEN** an operator or GUI runs `isomer-cli ext research records query facets <record-id>`
- **THEN** the command returns indexed ideas, routes, metrics, claims, or generic facts for the selected record according to the requested facet filter

#### Scenario: Detail views can reopen canonical content
- **WHEN** a GUI receives an indexed record or facet from export output
- **THEN** it can use the returned record id, payload locator, rendered Markdown path, or attached file locator to open the canonical detail source

### Requirement: Research Record Index Maintenance CLI
The system SHALL expose explicit index maintenance commands for rebuild, validation, and cleanup.

#### Scenario: Rebuild command refreshes derived rows
- **WHEN** an operator runs `isomer-cli ext research records index rebuild` for a Topic Workspace or selected record id
- **THEN** the command refreshes derived query-index rows from canonical runtime records, structured payloads, rendered locators, and accepted operation-set files

#### Scenario: Validate command is read-only
- **WHEN** an operator runs `isomer-cli ext research records index validate`
- **THEN** the command reports missing indexed records, stale derived rows, broken edges, missing files, unsupported relation kinds, extractor failures, and cross-topic refs without mutating `state.sqlite`

#### Scenario: Cleanup previews by default
- **WHEN** an operator runs `isomer-cli ext research records index cleanup` without `--apply`
- **THEN** the command returns a deterministic cleanup plan and does not delete, update, refresh, or backfill query-index rows

#### Scenario: Cleanup apply only touches index rows
- **WHEN** an operator runs `isomer-cli ext research records index cleanup --apply` with cleanup selectors such as `--stale-derived`, `--orphaned`, or `--missing-files`
- **THEN** the command removes or marks only selected query-index rows and does not delete lifecycle records, structured payloads, rendered Markdown, operation-set files, accepted artifacts, or canonical record bodies
