## ADDED Requirements

### Requirement: Idea Timeline Unified Fuzzy Search
The Idea Timeline view SHALL expose a single fuzzy text search bar for table entries, matching the Idea Graph search usage pattern.

#### Scenario: Search matches any table field
- **WHEN** the user types text into the Idea Timeline search bar
- **THEN** the timeline evaluates the query against display key, title, aliases, one-liner, family, status, idea id, parent display-key labels, parent titles, relation kinds, and other rendered table-entry fields
- **AND** matching is fuzzy enough to tolerate partial terms and normal text casing differences

#### Scenario: Search reaches supporting rows without changing visibility
- **WHEN** the search query matches a supporting Research Idea row
- **AND** the Supporting Records flag is off
- **THEN** the supporting row remains hidden
- **AND** enabling Supporting Records reveals matching supporting rows without changing the search text

#### Scenario: Timeline removes field-specific search controls
- **WHEN** the user opens Idea Timeline
- **THEN** the view presents one search bar instead of separate status, relation, or field-specific text inputs

### Requirement: Idea Timeline Display Key Labels
The Project Web GUI SHALL render Research Idea display keys in the `I-<index>` format wherever the Idea Timeline shows short idea identity.

#### Scenario: Timeline row shows hyphenated key
- **WHEN** a timeline row has `display_key: "I-7"`
- **THEN** the visible key column renders `I-7`
- **AND** the row identity remains keyed by canonical `idea_id`, not by row position

#### Scenario: Parent labels use hyphenated keys
- **WHEN** a timeline row renders parent references
- **THEN** parent references use parent `display_key` values such as `I-2` when available
- **AND** fall back to canonical parent `idea_id` only when the display key is missing

### Requirement: Idea Timeline Colorization Defaults Off
The Idea Timeline view SHALL render with row category colorization disabled by default while preserving opt-in row color support.

#### Scenario: Default table has no category background colors
- **WHEN** the user opens Idea Timeline with no stored row-color preference
- **THEN** primary and supporting rows do not use category background colors
- **AND** the table still exposes non-color cues for selection and row metadata

#### Scenario: User enables row colorization
- **WHEN** the user enables Idea Timeline row coloring in Project Settings
- **THEN** the timeline applies configured primary and supporting row colors to matching visible rows
