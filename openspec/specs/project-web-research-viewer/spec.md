# project-web-research-viewer Specification

## Purpose
TBD - created by archiving change add-topic-idea-iteration-map-gui. Update Purpose after archive.
## Requirements
### Requirement: Topic Idea Iteration Workbench
The Project Web GUI SHALL provide a topic-scoped workbench view for inspecting Research Topic idea evolution.

#### Scenario: User selects an existing topic
- **WHEN** a user opens the local Project Web GUI for a Project root and selects an existing Research Topic
- **THEN** the GUI opens an idea iteration view using project-discovered topics and topic-scoped APIs
- **AND** the GUI does not require topic-specific filenames, fixed record counts, or sample-topic-specific assumptions

#### Scenario: Idea nodes and rows show high-level meaning
- **WHEN** the idea iteration view displays proposed ideas
- **THEN** each idea is shown with stable id, concise title or one-liner, summary when available, status when available, source record id, producer or skill when available, and created or updated timestamps when available

#### Scenario: Relationship context is visible
- **WHEN** the source data provides predecessor, successor, sibling, selected, rejected, superseded, revised, follow-up, evidence, route, or decision relationships
- **THEN** the GUI shows those relationships through graph edges, grouped alternatives, list/table columns, or selected-node detail

#### Scenario: Partial lineage remains inspectable
- **WHEN** relationship metadata is missing, stale, unsupported, or ambiguous
- **THEN** the GUI shows affected ideas in an unconnected or partial-data group with diagnostics and maintenance hints
- **AND** it does not invent authoritative lineage from generated Markdown prose

### Requirement: Graph Renderer Selection
The Project Web GUI SHALL select graph renderers according to graph density and inspection depth.

#### Scenario: Sparse idea lineage uses React Flow
- **WHEN** the user opens an idea-lineage graph or selected reasoning path detail with bounded node count
- **THEN** the GUI renders the graph with React Flow and DAG layout suitable for readable idea, decision, and evidence cards

#### Scenario: Dense artifact maps use Sigma.js
- **WHEN** the user opens artifact overview, experiment records, paper revisions, or another dense graph scope
- **THEN** the GUI renders an overview with Sigma.js and Graphology and opens expanded details in separate tabs or panels when the user selects a node

#### Scenario: Large graph fallback is respected
- **WHEN** the backend reports `graph_too_large_for_renderer` or a `sigma-overview` renderer hint
- **THEN** the GUI does not force the graph into React Flow and offers the dense overview path instead

#### Scenario: List and table presentation remains available
- **WHEN** a graph is dense, incomplete, or difficult to scan
- **THEN** the GUI provides list or table presentation for ideas, records, evidence, diagnostics, and search results

### Requirement: Record Detail Drill-down
The Project Web GUI SHALL let users inspect records and files from graph or table selections through openability-aware detail views.

#### Scenario: Selecting a node opens detail
- **WHEN** the user selects an idea, artifact, evidence, decision, experiment, paper revision, or file node
- **THEN** the GUI can open record detail, rendered Markdown, lineage, siblings, files, and facets using existing read APIs or the viewer descriptor API

#### Scenario: File actions respect openability metadata
- **WHEN** a record or file facet points to a local or external file
- **THEN** the GUI offers file actions only when backend metadata says the file exists, is openable, and is within accepted Project or Topic Workspace surfaces

#### Scenario: Heavy content is lazy-loaded
- **WHEN** a record detail tab is not open
- **THEN** the GUI does not fetch full structured payload JSON, render Markdown, load PDF content, render Mermaid, render KaTeX, or start graph layout for that record

### Requirement: Open-tab Resource Policy
The Project Web GUI SHALL scope expensive data fetching and rendering to open relevant workbench tabs.

#### Scenario: Closed tabs stop expensive work
- **WHEN** a graph, Markdown, PDF, table, diagnostics, AG-UI, or future tmux tab is closed
- **THEN** the GUI stops polling, SSE-triggered refetches, graph layout work, graph rendering, Mermaid rendering, PDF rendering, and session attachment for that tab

#### Scenario: Live events invalidate relevant open views
- **WHEN** a topic change event arrives
- **THEN** the GUI invalidates only mounted queries whose topic id, graph scope, material kind, record id, or diagnostics interest intersects the event

#### Scenario: User context survives refresh
- **WHEN** the selected topic read model refreshes after terminal-side work creates or revises records
- **THEN** the GUI preserves topic selection, filters, layout mode, and selected detail when the selected record still exists

### Requirement: Read-only Browsing
The Project Web GUI SHALL keep ordinary research browsing separate from Workspace Runtime mutation and index maintenance.

#### Scenario: Browsing endpoints do not mutate
- **WHEN** the GUI lists topics, opens graphs, opens records, renders Markdown, reads lineage, reads siblings, reads files, reads facets, reads diagnostics, or refreshes runtime state
- **THEN** the backend response has `mutated: false`
- **AND** the operation does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows

#### Scenario: Maintenance remains explicit
- **WHEN** the GUI detects stale, missing, or partial query-index state
- **THEN** it shows diagnostics and maintenance hints
- **AND** any rebuild or cleanup operation remains an explicit user action through existing maintenance endpoints

### Requirement: Responsive Research Workbench
The Project Web GUI SHALL remain usable across desktop, tablet, and mobile browser sizes.

#### Scenario: Browser size changes
- **WHEN** the browser viewport changes size
- **THEN** the workbench layout, graph viewport, tables, detail panels, and diagnostics remain usable without text overlap or hidden primary controls

#### Scenario: Latest static assets are loaded
- **WHEN** the local web service serves the GUI shell, static assets, or API responses
- **THEN** cache headers prevent stale browser assets from hiding the latest local build during development and manual testing

