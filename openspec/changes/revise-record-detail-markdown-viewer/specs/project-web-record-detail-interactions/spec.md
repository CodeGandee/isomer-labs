## ADDED Requirements

### Requirement: Record detail uses Markdown-first inspection
The Project Web GUI SHALL render record detail tabs as Markdown-first inspection pages with raw JSON available through a secondary dialog.

#### Scenario: Record detail opens with Markdown preview
- **WHEN** a user opens a record from the Records table, graph, idea detail, or another openable record link
- **THEN** the record detail tab shows the record title and a Markdown preview as the primary content when rendered Markdown is available
- **AND** the tab does not show raw canonical/detail JSON as always-visible primary columns

#### Scenario: Toolbar mirrors idea detail controls
- **WHEN** a user opens a record detail tab
- **THEN** the toolbar shows `View JSON`, `Copy Markdown`, `Refresh`, and `Copy Filepath`
- **AND** `Copy Markdown` is disabled when no Markdown content is available
- **AND** `Copy Filepath` is disabled when no absolute artifact filepath is available

#### Scenario: Metadata appears under title
- **WHEN** record detail metadata includes a Topic Workspace-relative path
- **THEN** the detail header shows that relative path under the title
- **AND** it does not require the user to open the JSON dialog to inspect the path

#### Scenario: Direct parent idea appears when known
- **WHEN** structured record metadata identifies a direct parent idea for the record
- **THEN** the detail header shows the parent idea using the best available short label, title, or id
- **AND** the full relationship payload remains available in `View JSON`

#### Scenario: View JSON contains raw supporting payloads
- **WHEN** a user chooses `View JSON` on a record detail tab
- **THEN** the GUI opens a tabbed JSON dialog containing raw descriptor/detail JSON, rendered response data, lineage, siblings, files, facets, and diagnostics that have been loaded for that record
- **AND** the dialog provides JSON copy behavior for the selected tab

#### Scenario: Clipboard actions report state
- **WHEN** a user chooses `Copy Markdown` or `Copy Filepath`
- **THEN** the GUI writes the corresponding Markdown text or absolute filepath to the clipboard when available
- **AND** it shows a visible success or failure state without mutating Workspace Runtime, query-index rows, or source files

#### Scenario: Refresh keeps browsing read-only
- **WHEN** a user chooses `Refresh` on a record detail tab
- **THEN** the GUI refetches the mounted record detail queries
- **AND** the backend responses remain `mutated: false`
- **AND** refresh does not rebuild, repair, migrate, backfill, or cleanup Workspace Runtime or query-index state
