## MODIFIED Requirements

### Requirement: Record Detail Drill-down
The Project Web GUI SHALL let users inspect records and files from graph or table selections through openability-aware, Markdown-first detail views.

#### Scenario: Selecting a node opens detail
- **WHEN** the user selects an idea, artifact, evidence, decision, experiment, paper revision, or file node
- **THEN** the GUI can open record detail, rendered Markdown, lineage, siblings, files, and facets using existing read APIs or the viewer descriptor API

#### Scenario: Record detail prioritizes readable content
- **WHEN** the GUI opens a record detail tab for a record that can render Markdown
- **THEN** the record detail tab shows rendered Markdown as the primary content
- **AND** raw canonical/detail JSON, lineage, siblings, files, and facets are available through `View JSON` rather than always-visible primary columns

#### Scenario: File actions respect openability metadata
- **WHEN** a record or file facet points to a local or external file
- **THEN** the GUI offers file actions only when backend metadata says the file exists, is openable, and is within accepted Project or Topic Workspace surfaces

#### Scenario: Heavy content is lazy-loaded
- **WHEN** a record detail tab is not open
- **THEN** the GUI does not fetch full structured payload JSON, render Markdown, load PDF content, render Mermaid, render KaTeX, or start graph layout for that record
