## ADDED Requirements

### Requirement: Idea Timeline Contract Coverage
The Project Web UI contract set SHALL document and validate the payload shape consumed by the Idea Timeline view.

#### Scenario: Timeline contract is documented
- **WHEN** a developer or agent needs to implement or review the Idea Timeline view
- **THEN** `docs/ui/contracts/` contains contract documentation for the timeline payload or an updated topic graph contract that explicitly covers timeline use
- **AND** the documentation identifies required fields, optional useful fields, extra-field handling, and a concrete example

#### Scenario: Timeline payload validates required fields
- **WHEN** tests validate a representative Idea Timeline payload
- **THEN** validation passes when required topic identity, idea identity, display key, title, timestamp or fallback ordering fields, parent relationship identity, visibility or supporting-row metadata, diagnostics, and mutation state are present

#### Scenario: Timeline filter contract validates required fields
- **WHEN** tests validate Idea Timeline search or filter state and payloads
- **THEN** validation covers search text, status filter, relation filter, Supporting Records state, and enough row metadata to apply those filters safely

#### Scenario: Timeline sort and entry-count contract validates required fields
- **WHEN** tests validate Idea Timeline sort state, entry-count state, and payloads
- **THEN** validation covers active sort column, sort direction, entry-count limit, and enough row metadata to sort each visible column deterministically

#### Scenario: Timeline settings contract covers row coloring
- **WHEN** tests validate Project Web settings used by Idea Timeline
- **THEN** validation covers whether row category coloring is enabled and the configured Primary Idea and supporting idea row colors

#### Scenario: Timeline payload rejects unsafe omissions
- **WHEN** tests validate a representative Idea Timeline payload missing fields required for safe table rendering or row opening
- **THEN** validation fails with a deterministic error or the GUI reports a safe empty/diagnostic state

#### Scenario: Display key uniqueness is database-backed
- **WHEN** backend contract tests exercise Research Idea persistence
- **THEN** they verify topic-scoped `display_key` uniqueness is enforced by Workspace Runtime database constraints

### Requirement: Graph View Metadata Contract Coverage
The Project Web UI contract set SHALL document metadata needed to distinguish idea graph and idea timeline views.

#### Scenario: View metadata is documented
- **WHEN** a graph-section openable descriptor or graph payload identifies an idea view
- **THEN** the contract documentation describes the field or identifier that separates relationship graph presentation from timeline/table presentation

#### Scenario: Extra graph fields remain accepted
- **WHEN** graph or timeline payloads include additional metadata for future timeline growth
- **THEN** contract validation accepts those extra fields as long as required GUI fields are present

### Requirement: Recent Errors Contract Coverage
The Project Web UI contract set SHALL document and validate the recent-errors response used by graph and timeline warning surfaces.

#### Scenario: Recent errors contract is documented
- **WHEN** a developer or agent needs to implement or review the recent-errors query
- **THEN** `docs/ui/contracts/` contains contract documentation for recent errors or an updated diagnostics contract that explicitly covers recent read-model errors

#### Scenario: Recent errors payload validates required fields
- **WHEN** tests validate a representative recent-errors payload
- **THEN** validation passes when bounded list metadata, timestamp, severity, code, message, source view or operation, diagnostics, and `mutated: false` are present
