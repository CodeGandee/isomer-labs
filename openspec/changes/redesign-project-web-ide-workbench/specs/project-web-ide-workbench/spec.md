## ADDED Requirements

### Requirement: IDE-style Project Web Workbench
The Project Web GUI SHALL present an IDE-style workbench with a left Explorer pane and a right tab container.

#### Scenario: Semantic Project Explorer is the default navigation surface
- **WHEN** a user opens the local Project Web GUI for an Isomer Project
- **THEN** the left pane shows a semantic Project Explorer
- **AND** no filesystem or Files view is shown
- **AND** the right workbench opens only the selected or first Research Topic Overview tab when a topic is available
- **AND** Project Overview and Diagnostics open only when selected through semantic Explorer nodes or in-tab commands

#### Scenario: Right side owns all tabs
- **WHEN** the user opens a semantic item from the Explorer
- **THEN** the right side opens or focuses a Dockview tab for that item
- **AND** graph, record, runtime, diagnostics, file, repository, actor, and topic overview views are represented as right-side tabs rather than global page modes

#### Scenario: Graph scopes open as tabs
- **WHEN** the user opens `Idea Lineage`, `Artifact Overview`, `Experiment Records`, or `Paper Revisions` from the Project Explorer
- **THEN** the GUI opens a deterministic graph tab for the selected topic and graph scope
- **AND** changing graph scope does not remount unrelated workbench tabs

### Requirement: Headless Tree Explorer UI
The Project Web GUI SHALL use a tree interaction model suitable for semantic Project navigation.

#### Scenario: Tree rows use backend item metadata
- **WHEN** the Explorer renders Project tree rows
- **THEN** each row uses backend-provided id, parent id, label, item kind, icon hint, badge text, diagnostics count, openability state, and selected/expanded state inputs
- **AND** the frontend does not infer Isomer semantics from path strings alone

#### Scenario: Keyboard and search behavior are available
- **WHEN** the user focuses the Explorer
- **THEN** the tree supports keyboard navigation, selection, expansion, collapse, and search behavior through the Headless Tree integration

#### Scenario: Non-openable refs are summarized in the Explorer
- **WHEN** semantic refs are missing, stale, unresolved, outside accepted surfaces, or unsupported
- **THEN** the Explorer shows warning badges or diagnostic counts on the owning Project, Research Topic, or semantic group rows
- **AND** it does not add broken-looking leaf rows solely for those non-openable refs
- **AND** Diagnostics tabs expose the detailed refs and reasons

### Requirement: Openable Item Tab Routing
The Project Web GUI SHALL route all Explorer selections through a unified openable item command.

#### Scenario: Opening an item creates a deterministic tab
- **WHEN** the user opens an Explorer item with an `openable_item_id`
- **THEN** the GUI resolves the item descriptor and opens a tab with a deterministic `tab_id`
- **AND** opening the same item again focuses the existing tab instead of creating a duplicate

#### Scenario: Tab components lazy-load heavy content
- **WHEN** a tab opens for a graph, record, Markdown document, PDF, image, table, runtime view, repository view, or diagnostics view
- **THEN** only that tab starts the expensive fetching, rendering, graph layout, PDF loading, or subscription work needed for its content

#### Scenario: Closed tabs stop work
- **WHEN** the user closes a tab
- **THEN** the GUI stops tab-scoped polling, SSE-triggered refetches, graph layout, graph rendering, Markdown rendering, PDF loading, and future session attachment work for that tab

### Requirement: Responsive IDE Layout
The Project Web GUI SHALL keep the Explorer and Workbench usable across desktop and narrow browser sizes.

#### Scenario: Browser size changes
- **WHEN** the browser viewport changes size
- **THEN** the Explorer remains navigable, open tabs remain reachable, and active tab content remains usable without text overlap or hidden primary controls

#### Scenario: Narrow layout preserves navigation
- **WHEN** the viewport is too narrow for a fixed Explorer plus Workbench layout
- **THEN** the GUI provides a compact Explorer behavior that still allows users to browse semantic Project nodes and open tabs
