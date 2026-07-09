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

### Requirement: Payload-file Query Index Rebuild
The research record query index SHALL derive record summaries, relationships, facets, and file refs from managed payload files and runtime metadata.

#### Scenario: Rebuild reads payload files
- **WHEN** an operator rebuilds the research record query index
- **THEN** the system reads each managed payload JSON file, verifies its digest, and derives indexed rows from the file content and lifecycle metadata

#### Scenario: Missing payload blocks derived rows
- **WHEN** a payload file is missing, invalid, or digest-mismatched during index rebuild
- **THEN** the system reports diagnostics and does not create fresh derived rows from stale SQLite cache content

#### Scenario: Query results locate payload files
- **WHEN** query list, export, lineage, files, facets, or detail commands return a structured research record
- **THEN** the result includes record id, structured payload id, payload locator, payload digest, format profile ref, schema ref, current/latest relationship hints when known, and generated artifact locators when any explicit exports exist

#### Scenario: Markdown is not queried as source
- **WHEN** the query index extracts title, summary, claims, metrics, ideas, routes, relationships, or file refs
- **THEN** extraction uses payload files and authored metadata rather than generated Markdown bodies

### Requirement: Latest and Historical Record Views
The query index SHALL distinguish historical records from current/latest views without relying on fixed generated Markdown files.

#### Scenario: Historical events remain append-only
- **WHEN** multiple rounds produce experiment results, evidence items, decisions, or attempts
- **THEN** the query index exposes them as distinct records with chronological and relationship metadata

#### Scenario: Latest view is derived
- **WHEN** a caller asks for the current candidate board, frontier, latest context, resume packet, or similar current-state concept
- **THEN** the query layer resolves the latest payload-backed snapshot or derives a view from related records without requiring a mutable Markdown file

#### Scenario: Cleanup preserves payload files
- **WHEN** index cleanup removes stale derived query rows or generated-export references
- **THEN** it does not delete managed payload JSON files unless an explicit record deletion or archival policy names those files

### Requirement: Web GUI Query-index Read Model
The research record query index SHALL provide enough read-only data for the local Project web GUI to browse Topic Workspace records without parsing Markdown.

#### Scenario: GUI reads indexed summaries
- **WHEN** the web GUI lists records, exports a dashboard view, or opens lineage, file, facet, idea, experiment, or claim views
- **THEN** it reads query-index rows through the existing query APIs or equivalent Python API calls
- **AND** it does not treat generated Markdown as an authoritative data source

#### Scenario: GUI opens canonical detail
- **WHEN** the web GUI opens a record detail view
- **THEN** it uses returned record ids, payload locators, rendered Markdown locators, file locators, and structured payload metadata to reopen canonical detail sources

#### Scenario: GUI reports stale index state
- **WHEN** query-index validation reports missing, stale, orphaned, or inconsistent rows
- **THEN** the web GUI exposes those diagnostics and offers explicit maintenance actions instead of repairing the index during read operations

### Requirement: Concrete File Locator Extraction
The query index SHALL only create `research_record_files` rows for concrete file attachments, generated exports, structured payload files, rendered Markdown files, explicit query-index file hints, or payload objects with enough locator evidence to resolve them as files.

#### Scenario: Bare payload path stays unresolved
- **WHEN** a structured payload contains a bare relative path value such as an artifact name without semantic label, file role, operation-set id, locator kind, digest, media type, or accepted base path evidence
- **THEN** query-index rebuild does not create a `research_record_files` row for that value
- **AND** validation does not emit `query_index_file_missing` for that value

#### Scenario: Explicit file hint remains indexed
- **WHEN** lifecycle metadata or payload metadata explicitly declares a file attachment with file role and a resolvable project-local or external locator
- **THEN** query-index rebuild creates a file-index row with role, locator, existence status, and source metadata

#### Scenario: Semantic inventory does not become attachment
- **WHEN** a record payload contains semantic path inventory, readiness evidence, checkpoint paths, or expected workspace surfaces
- **THEN** those entries are not indexed as concrete file attachments unless a separate explicit file hint marks them as attachments

### Requirement: Query-index File Openability
The query index read APIs SHALL expose conservative file openability metadata for indexed file rows so GUI consumers can render actions without guessing filesystem state.

#### Scenario: Existing local file is openable
- **WHEN** a file-index row resolves to an existing project-local file inside an accepted Project or Topic Workspace surface
- **THEN** the read API marks the row as existing and openable and returns enough derived metadata for the GUI to display an open or preview affordance

#### Scenario: Missing or unresolved file is not openable
- **WHEN** a file-index row cannot be resolved locally or resolves to a missing path
- **THEN** the read API marks the row as not openable and includes a deterministic reason
- **AND** the GUI does not try to open the missing or unresolved file

### Requirement: GUI-safe Query Diagnostics
The query-index export API SHALL support generic GUI rendering by summarizing diagnostics while preserving detailed diagnostics.

#### Scenario: Export includes diagnostic summary
- **WHEN** a GUI or operator exports a query-index view for any Research Topic
- **THEN** the response includes full diagnostics and a grouped diagnostic summary by severity and diagnostic code

#### Scenario: GUI renders diagnostics dynamically
- **WHEN** the frontend receives query-index diagnostics for any selected Project root or Research Topic
- **THEN** it renders counts and expandable details from the returned diagnostic data
- **AND** it does not special-case topic ids, known file names, or repository-local paths

### Requirement: Canonical Lineage Projection
The research record query index SHALL project canonical artifact lineage into graph and lineage read models.

#### Scenario: Rebuild projects lineage edges
- **WHEN** query-index rebuild runs for a Topic Workspace
- **THEN** it reads canonical artifact lineage edges and projects them into exported graph and lineage views with source classification that identifies canonical lineage

#### Scenario: Query export distinguishes lineage
- **WHEN** query export returns graph edges
- **THEN** each edge identifies whether it came from canonical artifact lineage, authored relationship metadata, payload-derived refs, file-derived refs, or body inference

#### Scenario: Missing canonical lineage is diagnostic
- **WHEN** an artifact profile normally expects canonical lineage but no canonical lineage exists
- **THEN** query export reports a diagnostic or missing-lineage hint instead of fabricating parents from prose

### Requirement: Query Lineage Uses Canonical DAG
The record lineage query SHALL prefer canonical artifact lineage for ancestor, descendant, and sibling traversal.

#### Scenario: Ancestor traversal uses lineage table
- **WHEN** a caller runs a lineage query for ancestors
- **THEN** the command traverses canonical parent-child lineage before adding non-canonical relationship context

#### Scenario: Descendant traversal uses lineage table
- **WHEN** a caller runs a lineage query for descendants
- **THEN** the command traverses canonical child relationships before adding non-canonical relationship context

#### Scenario: Sibling traversal uses generation groups
- **WHEN** a caller runs a sibling or idea-iteration query
- **THEN** the command derives siblings from generation groups and parent-set identity rather than pairwise inferred sibling edges

### Requirement: Lineage Relation Vocabulary
The query index SHALL expose canonical lineage kinds in a stable vocabulary.

#### Scenario: Canonical lineage kinds are exported
- **WHEN** query export or lineage query returns canonical artifact lineage
- **THEN** it can expose `derived_from`, `revision_of`, `selected_from`, `merged_from`, and `follow_up_to` as lineage kinds or relation kinds

#### Scenario: Custom relationship extensions remain supported
- **WHEN** a non-canonical relationship uses a `custom.*` relation kind
- **THEN** the query index accepts it as an extension without confusing it with canonical artifact lineage

### Requirement: Idea Iteration Fixture Export Integrity
The research record query index SHALL expose repaired fixture data for idea iteration views without requiring read-time repair or topic-specific GUI filtering.

#### Scenario: Repaired topic idea export is diagnostic-clean
- **WHEN** a caller exports the repaired Flash Attention topic with the `ideas` view
- **THEN** the export returns topic-scoped nodes, canonical-lineage edges, idea facets, route rows, metrics, claims, facts, and files with no missing-record, stale-index, unsupported-relation, or missing-file integrity diagnostics

#### Scenario: Repaired idea facets are stable enough for GUI grouping
- **WHEN** the export contains raw idea facets, serious candidate records, selected hypothesis records, and follow-up hypothesis records
- **THEN** each idea-like item has enough stable fields for the GUI read model to group by source record, idea id or hypothesis id, family, one-liner or title, status, and lineage role

#### Scenario: Historical extractor duplicates are not authoritative siblings
- **WHEN** an array-valued historical payload causes duplicate raw idea facet rows
- **THEN** the query data still includes stable ids and source JSON paths that allow the backend read model to deduplicate presentation nodes without treating duplicate rows as sibling alternatives

### Requirement: Fixture Relationship Projection
The query index SHALL project repaired canonical lineage and authored relationship metadata so the idea iteration map can distinguish relationship meaning.

#### Scenario: Canonical lineage is projected
- **WHEN** repaired records have canonical lineage edges or generation groups
- **THEN** query export and lineage queries expose relation kind, relation role, source and target record ids, rationale when known, source classification, and canonical edge ids

#### Scenario: Route and evidence context remain queryable
- **WHEN** a repaired idea node is connected to route decisions, experiment results, analysis summaries, claims, or metrics
- **THEN** facets and export output include the relevant route rows, evidence links, claims, metrics, and scalar facts needed for the GUI detail panel

#### Scenario: Test and archived records do not pollute fixture diagnostics
- **WHEN** historical test or archived records remain in the topic runtime
- **THEN** they are either indexed consistently as archived records or excluded by explicit status/facet filtering without producing query-index integrity diagnostics

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

### Requirement: Canonical Research Idea Query Export
The research record query index SHALL export canonical Research Idea data for GUI, CLI, and operator graph views.

#### Scenario: Topic export includes ideas
- **WHEN** a GUI or operator exports a Topic Workspace query view
- **THEN** the payload includes canonical Research Ideas, Idea Realizations, Idea Lineage Edges, Idea Generation Groups, diagnostics, and detail locators when canonical idea data exists

#### Scenario: Canonical idea rows are rebuildable
- **WHEN** an operator rebuilds the query index
- **THEN** canonical idea export rows are derived from Workspace Runtime Research Idea tables and not from generated Markdown prose

#### Scenario: Idea query is read-only
- **WHEN** a caller queries idea graph, idea detail, idea siblings, or idea realizations
- **THEN** the query reads Workspace Runtime or query-index rows without creating, repairing, or backfilling canonical idea data

#### Scenario: Stale status is diagnostic
- **WHEN** indexed experiment, analysis, claim, or decision records suggest that a Research Idea status may be stale
- **THEN** the query or graph response may include a diagnostic or suggested status change without mutating the canonical Research Idea

### Requirement: Extracted Idea Facets Are Fallback Metadata
The query index SHALL keep extracted `research_record_ideas` facets available for legacy inspection while preferring canonical Research Idea rows for idea-lineage graphs.

#### Scenario: Canonical ideas suppress duplicate facets in graph
- **WHEN** canonical Research Idea rows exist for a Topic Workspace
- **THEN** the idea-lineage graph uses canonical idea nodes and does not create duplicate primary nodes from extracted record idea facets with the same idea id or source phrase

#### Scenario: Legacy facets remain queryable
- **WHEN** a caller requests record facets for an individual record
- **THEN** extracted ideas, route decisions, metrics, claims, and facts remain available as record facets even if canonical Research Idea rows also exist

#### Scenario: Heuristic graph is diagnosed
- **WHEN** the graph backend falls back to extracted idea facets because canonical Research Idea rows are absent
- **THEN** the response includes diagnostics that the graph is heuristic and may lack authoritative idea lineage

### Requirement: Primary Idea Graph Projection
The topic graph read model SHALL project canonical primary Research Ideas and their canonical idea edges for the default `idea-lineage` view.

#### Scenario: Default graph shows primary ideas
- **WHEN** the GUI requests the default `idea-lineage` graph for a Topic Workspace with canonical idea data
- **THEN** the backend returns only primary Research Ideas, including raw time-parent ideas when marked primary, and canonical idea-level edges unless the request includes supporting or secondary material

#### Scenario: Expanded graph includes realizations
- **WHEN** the GUI requests supporting material or opens an idea detail tab
- **THEN** the backend can return supporting ideas, realization records, route decisions, claims, files, and record-lineage refs linked to the selected idea

### Requirement: Canonical Idea Detail Read Model
The topic-scoped web read model SHALL expose canonical Research Idea detail data needed by GUI idea inspection without mutating Workspace Runtime.

#### Scenario: Idea detail resolves canonical idea
- **WHEN** the GUI requests detail for a topic-scoped canonical Research Idea id
- **THEN** the backend returns the Research Idea metadata, realization history, latest realization when known, generation group context when known, and incoming or outgoing idea lineage refs when available
- **AND** the response includes diagnostics instead of mutating runtime state when some related data is missing

#### Scenario: Idea detail resolves source JSON
- **WHEN** the selected Research Idea or latest realization points to a managed structured payload JSON source
- **THEN** the backend returns exact source JSON content or the exact source JSON fragment, source locator metadata, payload digest when known, and source record refs
- **AND** the response is read from canonical runtime records or managed payload files rather than generated Markdown prose

#### Scenario: Source JSON precedence is deterministic
- **WHEN** multiple possible JSON sources exist for one Research Idea
- **THEN** the backend chooses the latest Idea Realization `source_json_path` first, the latest realization record payload second, and Research Idea source metadata third
- **AND** the response identifies the selected source so the frontend can show realization history separately from the preview source

#### Scenario: Large source JSON is capped by default
- **WHEN** the selected source JSON serializes above the default 1 MiB response cap and the caller has not explicitly requested full source JSON
- **THEN** the backend returns source metadata, omits the full JSON body, and emits a non-fatal `source_json_truncated` diagnostic
- **AND** an explicit full-source request can fetch the exact JSON for the modal or copy action without mutating Workspace Runtime

#### Scenario: Missing source JSON is diagnostic
- **WHEN** the selected Research Idea has no resolvable source JSON payload
- **THEN** the backend returns the available idea metadata and realization records with a non-fatal diagnostic explaining why exact JSON is unavailable
- **AND** the read operation does not create, rebuild, repair, or backfill query-index rows

### Requirement: Idea Openable Descriptor
The semantic openable item resolver SHALL support canonical Research Idea items as workbench-openable resources.

#### Scenario: Idea openable descriptor resolves
- **WHEN** the frontend requests an openable descriptor for `idea:<topic_id>:<idea_id>`
- **THEN** the backend returns a descriptor for an `ideaDetail` workbench tab with topic id, idea id, title, stable tab id, and idea detail URL

#### Scenario: Unknown idea descriptor reports error
- **WHEN** the frontend requests an openable descriptor for an unknown or cross-topic idea id
- **THEN** the backend returns an error descriptor with diagnostics and does not fall back to a record tab for the wrong object

### Requirement: Query Index Exposes Idea Source Fragment Status
The research record query index SHALL expose exact idea source-fragment status for canonical Research Ideas and Idea Realizations.

#### Scenario: Canonical idea export includes source status
- **WHEN** `isomer-cli ext research records query export` returns canonical ideas or idea graph data
- **THEN** each idea or realization summary includes source record id, source JSON path, source fragment status, source classification, payload digest when known, and diagnostics when the source fragment is missing, unresolved, broad, or non-object
- **AND** `source_fragment_status` uses `exact`, `missing_payload`, `missing_path`, `unresolved_path`, `broad_path`, `non_object`, or `legacy_fallback`
- **AND** `source_classification` uses `canonical_idea_source`, `record_context`, or `legacy_heuristic`

#### Scenario: Query index does not promote context notes
- **WHEN** a structured payload contains idea entries and context sections such as filter notes, rejection notes, route notes, or slate summaries
- **THEN** query-index facet extraction maps idea facets only from declared idea-bearing sections
- **AND** it does not expose context-only sections as canonical Primary Idea nodes

#### Scenario: Rebuild preserves canonical source truth
- **WHEN** the query index is rebuilt
- **THEN** it derives idea source status from canonical Workspace Runtime idea rows, Idea Realizations, managed payload files, and profile-aware mappings
- **AND** it does not infer authoritative idea source paths from generated Markdown bodies

### Requirement: Idea Graph Detail Refs Prefer Exact Idea Content
The topic graph read model SHALL route Primary Idea nodes to exact idea detail refs while keeping record refs as provenance.

#### Scenario: Primary idea node detail refs
- **WHEN** the backend returns an `idea-lineage` graph node for a canonical Primary Idea
- **THEN** the node includes an idea detail ref for the exact idea content read model
- **AND** source record refs remain available as latest record detail, rendered Markdown, or provenance refs

#### Scenario: Legacy fallback is diagnostic
- **WHEN** a topic has record idea facets but lacks canonical exact source-fragment metadata
- **THEN** the graph may return a legacy heuristic view
- **AND** it includes diagnostics that the idea source data requires import or repair before the GUI can show authoritative Primary Idea content

### Requirement: Query Index Uses Canonical Summary
The research record query index SHALL derive record summaries, idea facet summaries, and graph node summaries from canonical `summary` fields rather than from `one_liner` or generated Markdown.

#### Scenario: Record summary is indexed
- **WHEN** query-index rebuild processes a structured Research Record payload
- **THEN** the indexed record row stores `title` from the payload root `title`
- **AND** it stores `summary` from the payload root `summary`

#### Scenario: Idea facet summary is indexed
- **WHEN** query-index extraction processes an idea-bearing payload section
- **THEN** each extracted idea facet stores the idea entry's `title` and `summary`
- **AND** it does not create or expose a first-class `one_liner` facet field

#### Scenario: Rebuild reports missing summary
- **WHEN** query-index rebuild encounters a record or idea entry without a required `summary`
- **THEN** it records a deterministic diagnostic and skips or marks only the affected derived field or row
- **AND** it does not synthesize a summary from arbitrary text during ordinary rebuild

#### Scenario: Export omits one-liner display field
- **WHEN** query list, export, lineage, facets, graph, or timeline responses include record or idea summaries
- **THEN** they expose `summary` as the brief display field
- **AND** they do not require GUI consumers to read `one_liner`

#### Scenario: Graph node summaries use summary across material kinds
- **WHEN** query-index or Project Web graph export builds nodes for ideas, records, routes, claims, files, or other material kinds
- **THEN** each node uses `summary` for its brief display text when such text is available
- **AND** it does not expose `one_liner` as the generic node subtitle field

### Requirement: Query Index Display Diagnostics
The query-index export API SHALL include display-contract diagnostics in GUI-safe diagnostic summaries.

#### Scenario: Export includes display diagnostics
- **WHEN** a GUI or operator exports a query-index view for a Topic Workspace with missing, duplicated, stale, or legacy display fields
- **THEN** the response includes full diagnostics and a grouped summary by severity and diagnostic code
- **AND** the response preserves safely interpretable nodes, rows, and detail locators

