## ADDED Requirements

### Requirement: Idea Lineage Overview Shows User-facing Ideas
The Project Web GUI SHALL show only user-facing idea nodes in the default Idea Lineage overview.

#### Scenario: Default graph excludes secondary material
- **WHEN** a user opens the Idea Lineage graph for a Research Topic
- **THEN** the graph request does not include secondary material by default
- **AND** the rendered first-level graph contains only nodes whose graph read model `material_kind` is `idea`
- **AND** route decisions, claims, evidence records, files, metrics, and other supporting details are not rendered as peer idea nodes

#### Scenario: Idea labels use idea-facing text
- **WHEN** the Idea Lineage overview renders an idea node
- **THEN** the node label uses the idea row one-liner, title, or equivalent idea-facing text
- **AND** labels such as "Route decision" or extracted claim titles are not shown as first-level idea labels unless the source node is itself an idea

#### Scenario: Topic-specific assumptions are avoided
- **WHEN** the GUI opens Idea Lineage for any Project-discovered Research Topic
- **THEN** the overview derives idea nodes from topic-scoped graph read models and query-index idea rows
- **AND** it does not rely on Flash Attention-specific filenames, record ids, fixed counts, or source JSON paths

### Requirement: Collapsed Idea Edges Preserve Overview Lineage
The Topic Graph API SHALL support an idea-only overview that can show meaningful idea-to-idea lineage without rendering secondary records as nodes.

#### Scenario: Backend projects idea-to-idea edges
- **WHEN** an idea-lineage graph request excludes secondary material
- **THEN** the backend returns only idea nodes
- **AND** it returns direct or collapsed edges between idea nodes when accepted canonical lineage, query-index relationships, or secondary paths can be projected without ambiguity
- **AND** each projected edge identifies its relation kind, whether it is collapsed, source relationship refs, source record refs, and source classification when available

#### Scenario: Overview prioritizes idea lineage relation kinds
- **WHEN** the backend projects the default idea-lineage overview
- **THEN** it preserves accepted stable relation kinds in the API response
- **AND** the default overview prioritizes `derived_from`, `revision_of`, `selected_from`, `follow_up_to`, `alternative_to`, and `supersedes` as idea-lineage relations
- **AND** `supports` and `contradicts` appear as overview edges only when both endpoints are real idea nodes

#### Scenario: Ambiguous projections remain diagnostic
- **WHEN** secondary relationships cannot be projected into an unambiguous idea-to-idea edge
- **THEN** the backend does not invent an authoritative edge
- **AND** it reports diagnostics or groups that explain partial, unconnected, or ambiguous lineage

#### Scenario: Markdown prose is not authoritative lineage
- **WHEN** the backend derives collapsed idea edges
- **THEN** it uses payload-backed fields, authored metadata, canonical lineage, accepted query-index edges, or record relationship metadata
- **AND** it does not parse generated Markdown prose as an authoritative source for idea relationships

### Requirement: Selected Idea Drill-down Shows Details
The Project Web GUI SHALL expose supporting details for a selected idea through drill-down rather than the first-level overview.

#### Scenario: Selecting an idea opens detail context
- **WHEN** a user selects an idea node in the Idea Lineage overview
- **THEN** the GUI opens or focuses a Dockview record-detail tab for that idea's source record
- **AND** the detail surface can load the source record, rendered content, lineage, siblings, files, facets, diagnostics, and supporting secondary material for that idea

#### Scenario: Details are lazy-loaded
- **WHEN** no selected-idea detail surface is open
- **THEN** the GUI does not fetch full structured payload JSON, rendered Markdown, file content, secondary-neighborhood graph data, Mermaid, KaTeX, PDF content, or expensive detail layout for that idea

#### Scenario: Secondary material is labeled as detail
- **WHEN** the selected-idea detail surface shows route decisions, claims, evidence, metrics, files, or supporting records
- **THEN** the GUI labels them as supporting details, evidence, claims, decisions, or files
- **AND** it does not present them as peer user-facing ideas

#### Scenario: Common idea statuses are normalized conservatively
- **WHEN** the selected idea detail or overview displays idea status
- **THEN** the GUI recognizes `candidate`, `selected`, `rejected`, `superseded`, `deferred`, `unresolved`, and `stale`
- **AND** unknown source status values remain visible as raw values or diagnostics rather than being silently remapped

### Requirement: Secondary Material Is Explicit
The Project Web GUI SHALL make secondary material opt-in for Idea Lineage.

#### Scenario: User enables secondary material
- **WHEN** the user explicitly enables secondary material for Idea Lineage
- **THEN** the graph may request and display decisions, claims, evidence, files, or other supporting nodes
- **AND** the UI labels the control and resulting view as **Supporting Records** rather than presenting them as peer ideas

#### Scenario: Secondary toggle does not affect other graph scopes
- **WHEN** the user changes the Idea Lineage secondary material setting
- **THEN** Artifact Overview, Experiment Records, Paper Revisions, and unrelated open tabs keep their own renderer and filter state

### Requirement: Browsing Remains Read-only
Idea Lineage overview and selected-idea drill-down SHALL remain read-only browsing operations.

#### Scenario: Overview does not mutate records or index
- **WHEN** the GUI opens, refreshes, filters, or lays out the Idea Lineage overview
- **THEN** backend responses report `mutated: false`
- **AND** browsing does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows

#### Scenario: Drill-down does not mutate records or index
- **WHEN** the GUI opens selected-idea details, record detail, rendered Markdown, lineage, siblings, files, facets, or secondary-neighborhood data
- **THEN** backend responses report `mutated: false`
- **AND** drill-down does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows
