## ADDED Requirements

### Requirement: Idea Timeline View
Project Web SHALL provide an Idea Timeline view under the selected Research Topic's `Graphs` section.

#### Scenario: Timeline view appears under Graphs
- **WHEN** a user expands a Research Topic in the Project Explorer
- **THEN** the `Graphs` section includes an openable Idea Timeline view
- **AND** the Idea Timeline view is separate from the idea relationship graph view

#### Scenario: Timeline uses topic-scoped idea data
- **WHEN** the Idea Timeline view loads for a Research Topic
- **THEN** it derives rows from topic-scoped Research Idea graph/read-model data
- **AND** it does not read unscoped Project data or topic-specific fixture paths

#### Scenario: Timeline defaults to primary ideas
- **WHEN** the Idea Timeline view loads without user-selected expansion controls
- **THEN** it shows Primary Ideas by default
- **AND** supporting Research Ideas are not shown as peer rows until the user explicitly enables them

#### Scenario: User enables supporting records
- **WHEN** the user enables the Supporting Records control in Idea Timeline
- **THEN** the timeline may include supporting Research Ideas returned by the topic-scoped read model
- **AND** supporting rows remain visually distinguishable from Primary Ideas
- **AND** raw source records are not rendered as peer rows in the first Idea Timeline table

### Requirement: Idea Timeline Search and Filtering
The Idea Timeline view SHALL provide search and filtering controls comparable to the Idea Graph view.

#### Scenario: User searches timeline rows
- **WHEN** a user enters a search query in Idea Timeline
- **THEN** the visible rows are filtered by matching display key, idea title, aliases, one-liner, family, status, or parent display-key labels
- **AND** filtering does not change stored display keys, parent display-key references, or row-open identity

#### Scenario: User filters by status
- **WHEN** a user applies a status filter in Idea Timeline
- **THEN** the visible rows are limited to Research Ideas matching that status
- **AND** clearing the filter restores rows that are otherwise included by the current Supporting Records setting

#### Scenario: User filters by lineage relation
- **WHEN** a user applies a relation filter in Idea Timeline
- **THEN** the visible rows are limited by matching idea lineage edge kinds where relation data is available
- **AND** rows without interpretable relation data are either excluded or shown with diagnostics according to the filter state

#### Scenario: Supporting toggle participates in filtering
- **WHEN** the user changes the Supporting Records control while search or other filters are active
- **THEN** the timeline recomputes visible rows from the latest read model and all active filters
- **AND** hidden rows do not lose or change their persisted display keys

#### Scenario: Filtering remains read-only
- **WHEN** the user searches, filters, clears filters, or changes the Supporting Records control
- **THEN** Project Web does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows

### Requirement: Idea Timeline Row Category Styling
The Idea Timeline view SHALL provide configurable row category coloring.

#### Scenario: Category coloring defaults on
- **WHEN** the Idea Timeline view renders with default settings
- **THEN** Primary Idea rows use a light green background
- **AND** supporting idea rows use a light yellow background

#### Scenario: Category coloring can be disabled
- **WHEN** the user turns off Idea Timeline row category coloring in settings
- **THEN** the timeline renders rows without category background coloring
- **AND** row category remains available without relying only on color

#### Scenario: Category colors are configurable
- **WHEN** the user changes Idea Timeline category colors in settings
- **THEN** the timeline uses the configured colors for Primary Idea and supporting idea rows
- **AND** the setting defaults remain light green for Primary Ideas and light yellow for supporting ideas

### Requirement: Idea Timeline Table
The Idea Timeline view SHALL render Research Ideas as a chronological table with short display keys and parent display-key references.

#### Scenario: Timeline columns are visible
- **WHEN** the Idea Timeline view has idea rows
- **THEN** the table shows creation time, display key, idea title, and parent idea display keys

#### Scenario: User sorts by any visible column
- **WHEN** a user activates a visible Idea Timeline column header
- **THEN** the table sorts visible rows by that column
- **AND** every visible column supports ascending and descending sort direction
- **AND** equal values use a deterministic fallback order based on creation time, updated time, title, and idea id

#### Scenario: User sorts by parent column
- **WHEN** a user sorts by the parents column
- **THEN** the table sorts by the rendered parent display-key list
- **AND** parent idea ids are used as fallback sort values when parent display keys are unavailable

#### Scenario: User changes entries shown in the view
- **WHEN** a user changes the Idea Timeline entry-count control inside the timeline view
- **THEN** the table updates how many filtered and sorted rows are shown
- **AND** the user does not need to open the settings panel to change the count
- **AND** hidden rows do not lose or change their persisted display keys

#### Scenario: Display key comes from read model
- **WHEN** the Idea Timeline view receives graph or timeline data for the current revision
- **THEN** it uses each idea row's `display_key` as the short GUI handle
- **AND** it does not derive the handle from the current visible row position

#### Scenario: Hidden rows do not change display keys
- **WHEN** some ideas are hidden, filtered out, or excluded by the Supporting Records control
- **THEN** visible table rows keep their persisted display keys
- **AND** the timeline does not renumber or rewrite display keys solely to remove gaps

#### Scenario: Parent column uses display keys
- **WHEN** an idea row has parent ideas present in the current read model
- **THEN** the row's parent column shows the parent display keys

#### Scenario: Missing parent uses stable fallback and warning
- **WHEN** an idea row has a parent idea reference that is missing from the current read model
- **THEN** the row's parent column shows a stable fallback such as parent idea id instead of an invented display key
- **AND** the timeline reports a warning that lineage data is incomplete

#### Scenario: Missing timestamps do not break sorting
- **WHEN** one or more ideas are missing creation time
- **THEN** the table uses a deterministic fallback order based on updated time, title, and idea id
- **AND** rows with missing creation time remain visible

### Requirement: Timeline Live Update Handling
The Idea Timeline view SHALL tolerate research data changes while the GUI is open.

#### Scenario: New idea arrives during viewing
- **WHEN** Project Web receives refreshed idea data with one or more new ideas
- **THEN** the timeline shows each new idea using its assigned display key
- **AND** it preserves any selected row by `idea_id` when that idea still exists

#### Scenario: Selected idea is deleted during viewing
- **WHEN** refreshed idea data no longer contains the currently selected idea
- **THEN** the timeline clears that selection
- **AND** it shows a non-crashing warning or empty selection state

#### Scenario: Selected idea is filtered out during viewing
- **WHEN** the current search or filter settings exclude the selected idea from visible rows
- **THEN** the timeline clears or marks the visible selection without opening another row
- **AND** removing the filter can restore selection by `idea_id` if the selected idea still exists

#### Scenario: Selected idea moves due to sort or entry count
- **WHEN** the user changes sort order or the number of entries shown
- **THEN** the timeline preserves selection by `idea_id` when the selected idea remains visible
- **AND** it does not reinterpret the same row position as a different selected idea

#### Scenario: Lineage edge changes during viewing
- **WHEN** refreshed idea data changes parent-child lineage relationships
- **THEN** the timeline recomputes parent display-key references from the latest relationship data
- **AND** it does not keep stale parent references from earlier revisions

### Requirement: Timeline Data Integrity Guardrails
The Idea Timeline view SHALL degrade safely when idea or lineage data is malformed, missing, cyclic, or non-interpretable.

#### Scenario: Malformed row is skipped or degraded
- **WHEN** a timeline source row lacks required identity or title data
- **THEN** Project Web skips the row or renders a degraded row with diagnostics
- **AND** the workbench does not crash

#### Scenario: Malformed edge is ignored with warning
- **WHEN** a lineage edge references missing endpoints, duplicate nodes, or otherwise cannot be interpreted
- **THEN** Project Web excludes that edge from parent-index derivation
- **AND** it shows a warning or diagnostic for the affected timeline view

#### Scenario: Non-interpretable graph shows warning
- **WHEN** the idea data cannot be interpreted enough to render a safe timeline
- **THEN** Project Web shows a warning or empty state instead of crashing
- **AND** it provides access to recent backend errors for the affected topic when available

### Requirement: Timeline Row Opens Idea Detail
The Idea Timeline view SHALL open the existing idea detail page from row activation.

#### Scenario: Desktop row double-click opens idea
- **WHEN** a user double-clicks an idea row
- **THEN** Project Web opens or focuses the same idea detail tab used by opening that idea from the graph view

#### Scenario: Touch row double-tap opens idea
- **WHEN** a user double-taps an idea row on a touch interface
- **THEN** Project Web opens or focuses the same idea detail tab used by opening that idea from the graph view

#### Scenario: Single row selection does not open detail
- **WHEN** a user single-clicks or single-taps an idea row
- **THEN** Project Web MAY select or highlight the row
- **AND** it SHALL NOT open the idea detail page solely from that single action

### Requirement: Timeline Browsing Remains Read-only
The Idea Timeline view SHALL browse existing Research Idea data without mutating Workspace Runtime or query-index state.

#### Scenario: Timeline load is read-only
- **WHEN** the Idea Timeline view loads, refreshes, sorts, filters ideas, or changes the number of entries shown
- **THEN** backend responses report `mutated: false`
- **AND** the operation does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows
