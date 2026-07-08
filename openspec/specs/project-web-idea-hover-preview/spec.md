# project-web-idea-hover-preview Specification

## Purpose
TBD - created by archiving change fix-idea-lineage-hover-preview. Update Purpose after archive.
## Requirements
### Requirement: Idea Hover Preview Loads Full Markdown
The Project Web idea lineage graph SHALL show a hover popup for idea nodes that loads and renders the full idea Markdown preview through the same Markdown preview renderer used by the idea detail view.

#### Scenario: Hover starts async Markdown preview
- **WHEN** a user hovers over an idea lineage graph node long enough to trigger the preview
- **THEN** the system SHALL show a fixed-size hover popup immediately with a loading indicator while the idea Markdown preview loads

#### Scenario: Loaded preview preserves Markdown features
- **WHEN** the idea Markdown preview has loaded
- **THEN** the hover popup SHALL render the full Markdown content without shortening it and SHALL support the Markdown preview features available in the idea detail view

### Requirement: Idea Hover Preview Is Scrollable and Interactive
The hover popup SHALL be pointer-interactive, bounded to the viewport, and internally scrollable so users can inspect long Markdown previews without changing the popup size.

#### Scenario: Popup position locks after open
- **WHEN** the hover popup is visible and the user moves the pointer over the source node
- **THEN** the popup SHALL remain at its original screen position so the user can move into it predictably

#### Scenario: User scrolls inside popup
- **WHEN** a user moves the pointer from an idea node into the hover popup
- **THEN** the popup SHALL remain open and SHALL allow scrolling via mouse wheel or scrollbar without panning the graph

#### Scenario: User leaves popup
- **WHEN** a user moves the pointer out of the node and popup hover area
- **THEN** the system SHALL close the hover popup after the normal hover cleanup delay

### Requirement: Idea Hover Preview Supports Touch Long Press
The idea lineage graph SHALL provide a touch-compatible long-press gesture that opens the same Markdown-capable hover preview as mouse hover.

#### Scenario: Touch long press opens preview
- **WHEN** a user long-presses an idea lineage graph node on a touch interface
- **THEN** the system SHALL show the bounded hover popup for that node without requiring mouse hover

#### Scenario: Touch release before delay cancels preview
- **WHEN** a touch pointer leaves or releases before the long-press delay completes
- **THEN** the system SHALL cancel the pending hover popup

### Requirement: Idea Hover Preview Clears on Open
The idea lineage graph SHALL clear active hover previews before opening a node detail tab and SHALL NOT restore stale hover previews when the user returns to the graph.

#### Scenario: Double click opens node
- **WHEN** a user double-clicks an idea lineage graph node while its hover popup is visible or loading
- **THEN** the system SHALL clear the hover popup before opening the idea detail tab

#### Scenario: User returns from detail
- **WHEN** a user returns from an idea detail tab to the graph after opening a node
- **THEN** no previous hover popup SHALL remain visible unless the user starts a new hover interaction

