## ADDED Requirements

### Requirement: Idea graph separates preview, selection, and opening
The Project Web GUI SHALL keep idea graph hover preview, single-click selection, and double-click opening as distinct interactions.

#### Scenario: Hover previews an idea without opening it
- **WHEN** a user hovers over an idea graph node long enough for the hover delay to pass
- **THEN** the GUI shows a size-limited Markdown tooltip near the pointer using the node title, one-liner, summary, status, and record references available in the graph payload
- **AND** the GUI does not open a workbench tab or fetch full record detail solely because of hover

#### Scenario: Single click selects an idea node
- **WHEN** a user single-clicks an idea graph node
- **THEN** the GUI highlights or selects that node
- **AND** the GUI does not open the idea detail tab because of that single click

#### Scenario: Double click opens an idea node
- **WHEN** a user double-clicks an idea graph node
- **THEN** the GUI opens the existing idea detail tab for that node
- **AND** the selected-node highlight may remain on the opened node

### Requirement: Idea detail JSON is grouped inside View JSON
The Project Web GUI SHALL keep the idea detail page focused on Markdown content and move raw idea-related JSON into a tabbed `View JSON` dialog.

#### Scenario: Detail toolbar omits top-level JSON copy
- **WHEN** a user opens an idea detail page
- **THEN** the toolbar shows `View JSON`, `Copy Markdown`, and refresh controls
- **AND** the toolbar does not show a top-level `Copy JSON` control

#### Scenario: View JSON opens tabbed idea data
- **WHEN** a user chooses `View JSON` on an idea detail page
- **THEN** the GUI opens a modal dialog with `Main Record`, `Lineage`, `Realizations`, and `Diagnostics` tabs
- **AND** `Main Record` is selected by default

#### Scenario: JSON copy applies to the selected tab
- **WHEN** a user opens the idea JSON dialog and selects one of its JSON tabs
- **THEN** the dialog provides a JSON copy action for the currently selected tab
