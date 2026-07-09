## ADDED Requirements

### Requirement: Hyphenated Display Key Contract
Project Web data contracts SHALL document and validate Research Idea display keys as GUI-visible labels in the `I-<index>` format.

#### Scenario: Graph node contract carries display key
- **WHEN** a topic graph node represents a canonical Research Idea with a display key
- **THEN** the graph payload exposes `display_key` using the `I-<index>` format
- **AND** UI contract schemas accept the field without requiring consumers to parse canonical `idea_id`

#### Scenario: Timeline contract uses display key as visible identity
- **WHEN** the Idea Timeline derives rows from graph data
- **THEN** the timeline contract identifies `display_key` as the short visible key
- **AND** it states that `idea_id` remains the stable row identity

### Requirement: Timeline Fuzzy Search Contract
Project Web data contracts SHALL document the Idea Timeline fuzzy search state and matching surface.

#### Scenario: Search state is one text value
- **WHEN** the Idea Timeline view stores or restores search state
- **THEN** the contract represents search as one text query value
- **AND** it does not require separate status, relation, or field-specific query values

#### Scenario: Search surface includes supporting rows
- **WHEN** the contract describes timeline search behavior
- **THEN** it states that search can match primary and supporting Research Idea row fields
- **AND** it states that the Supporting Records flag controls whether supporting rows are visible
