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

### Requirement: Idea Timeline Table
The Idea Timeline view SHALL render Research Ideas as a chronological table with display indexes and parent indexes.

#### Scenario: Timeline columns are visible
- **WHEN** the Idea Timeline view has idea rows
- **THEN** the table shows creation time, display index, idea title, and parent idea indexes

#### Scenario: Display indexes are re-indexed for the current view
- **WHEN** the Idea Timeline view sorts or filters visible ideas
- **THEN** it assigns display indexes from `1` to the number of visible rows
- **AND** display indexes are presentation labels, not persisted Research Idea identity

#### Scenario: Parent indexes use the same visible index map
- **WHEN** an idea row has parent ideas that are visible in the current table
- **THEN** the row's parent column shows the parent display indexes from the same visible table view

#### Scenario: Hidden parent uses stable fallback
- **WHEN** an idea row has a parent idea outside the current visible table set
- **THEN** the row's parent column shows a stable fallback such as parent title or parent idea id instead of an invented display index

#### Scenario: Missing timestamps do not break sorting
- **WHEN** one or more ideas are missing creation time
- **THEN** the table uses a deterministic fallback order based on updated time, title, and idea id
- **AND** rows with missing creation time remain visible

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
- **WHEN** the Idea Timeline view loads, refreshes, sorts, or filters ideas
- **THEN** backend responses report `mutated: false`
- **AND** the operation does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows
