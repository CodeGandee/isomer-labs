## ADDED Requirements

### Requirement: Idea Timeline Row Coloring Preference
Project Web settings SHALL provide browser-local controls for Idea Timeline row coloring, with coloring disabled by default.

#### Scenario: Coloring defaults off
- **WHEN** a browser has no stored Idea Timeline row coloring preference
- **THEN** Project Web initializes row coloring as disabled
- **AND** Idea Timeline rows render without primary/supporting category background colors

#### Scenario: Coloring preference persists
- **WHEN** the user enables or disables Idea Timeline row coloring in Project Settings
- **THEN** the GUI applies the preference immediately
- **AND** stores the preference as browser-local frontend state

#### Scenario: Configured colors remain available
- **WHEN** row coloring is enabled
- **THEN** Project Settings lets the user configure primary and supporting row colors
- **AND** those colors are stored as browser-local frontend state
