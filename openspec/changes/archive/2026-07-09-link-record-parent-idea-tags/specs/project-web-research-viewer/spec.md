## MODIFIED Requirements

### Requirement: Record Detail Drill-down
The Project Web GUI SHALL let users inspect records and files from graph or table selections through openability-aware detail views.

#### Scenario: Selecting a node opens detail
- **WHEN** the user selects an idea, artifact, evidence, decision, experiment, paper revision, or file node
- **THEN** the GUI can open record detail, rendered Markdown, lineage, siblings, files, and facets using existing read APIs or the viewer descriptor API

#### Scenario: Parent idea tag opens idea detail
- **WHEN** a record or artifact detail page shows direct parent idea metadata with a stable idea id
- **THEN** the parent idea tag is clickable and opens the existing idea detail tab for that idea
- **AND** the GUI leaves the tag display-only when the parent idea metadata lacks a stable idea id
- **AND** stale or unresolvable parent idea links report a user-facing notification instead of crashing or silently clearing the current detail view

#### Scenario: File actions respect openability metadata
- **WHEN** a record or file facet points to a local or external file
- **THEN** the GUI offers file actions only when backend metadata says the file exists, is openable, and is within accepted Project or Topic Workspace surfaces

#### Scenario: Heavy content is lazy-loaded
- **WHEN** a record detail tab is not open
- **THEN** the GUI does not fetch full structured payload JSON, render Markdown, load PDF content, render Mermaid, render KaTeX, or start graph layout for that record
