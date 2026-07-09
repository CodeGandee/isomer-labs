## MODIFIED Requirements

### Requirement: IDE-style Project Web Workbench
The Project Web GUI SHALL present an IDE-style workbench with a left Explorer pane and a right tab container.

#### Scenario: Semantic Project Explorer is the default navigation surface
- **WHEN** a user opens the local Project Web GUI for an Isomer Project
- **THEN** the left pane shows a semantic Project Explorer focused on topic overview, graphs, records, and diagnostics
- **AND** no filesystem or Files view is shown
- **AND** topic-level `Workspace Runtime`, `Topic Actors`, and `Repositories` rows are not shown in the Explorer
- **AND** the right workbench opens only the selected or first Research Topic Overview tab when a topic is available
- **AND** Project Overview and Diagnostics open only when selected through semantic Explorer nodes or in-tab commands

#### Scenario: Right side owns Explorer-opened tabs
- **WHEN** the user opens a semantic item from the Explorer
- **THEN** the right side opens or focuses a Dockview tab for that item
- **AND** graph, record, diagnostics, file, and topic overview views are represented as right-side tabs rather than global page modes
- **AND** hidden runtime, actor, or repository implementation surfaces are not advertised as Explorer-opened topic tabs

#### Scenario: Graph scopes open as tabs
- **WHEN** the user opens `Idea Lineage`, `Artifact Overview`, `Experiment Records`, or `Paper Revisions` from the Project Explorer
- **THEN** the GUI opens a deterministic graph tab for the selected topic and graph scope
- **AND** changing graph scope does not remount unrelated workbench tabs
