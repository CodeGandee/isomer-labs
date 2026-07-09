# project-web-data-contracts Specification

## Purpose
Define GUI-usable Project Web data contracts and permissive validation rules for read payloads rendered by the Isomer Labs GUI.
## Requirements
### Requirement: UI Contract Documentation
The system SHALL document GUI-usable data contracts under `docs/ui/contracts/` as separate pages organized by Project Web view or shared payload shape.

#### Scenario: Contract pages exist
- **WHEN** a developer or agent needs to understand the data required by a Project Web view
- **THEN** `docs/ui/contracts/` SHALL contain an index page and focused contract pages for the relevant GUI payloads
- **AND** each page SHALL describe required fields, optional useful fields, extra-field handling, and a concrete example

#### Scenario: Contract docs distinguish storage from viewing
- **WHEN** a contract page describes a GUI payload
- **THEN** it SHALL state that the payload is a UI read contract unless it is explicitly documenting an existing canonical storage contract
- **AND** it SHALL NOT imply that extra agent-authored metadata must be removed from Workspace Runtime records

### Requirement: Permissive Python GUI Schemas
The system SHALL provide Python schemas for GUI-facing read models that validate required Project Web fields while allowing additional fields.

#### Scenario: Required fields are present
- **WHEN** backend code, tests, or fixture checks validate a GUI payload with all required fields and additional unknown fields
- **THEN** schema validation SHALL pass
- **AND** the caller SHALL be able to preserve or ignore unknown fields according to its use case

#### Scenario: Required fields are missing
- **WHEN** a GUI payload omits fields required for the corresponding Project Web view to render safely
- **THEN** schema validation SHALL fail with a deterministic validation error that identifies the missing or invalid field

#### Scenario: Nested payloads contain richer agent metadata
- **WHEN** a payload includes nested metadata that is not required by the GUI contract
- **THEN** schema validation SHALL NOT reject the payload solely because of those extra fields

### Requirement: Initial Contract Coverage
The initial GUI contract set SHALL cover the read models currently needed by Project Web topic inspection flows.

#### Scenario: Topic overview contract is covered
- **WHEN** the topic overview panel consumes a topic overview response
- **THEN** a documented contract and Python schema SHALL cover `ok`, `mutated`, topic identity, overview source metadata, Markdown content availability, supporting JSON payloads, and diagnostics

#### Scenario: Graph view contract is covered
- **WHEN** the idea lineage or artifact graph panels consume a graph response
- **THEN** a documented contract and Python schema SHALL cover graph identity fields, nodes, edges, groups, facets, paging, diagnostics, and renderer hints needed by Project Web

#### Scenario: Idea detail contract is covered
- **WHEN** the idea detail panel consumes an idea detail response
- **THEN** a documented contract and Python schema SHALL cover idea identity, canonical idea metadata, realizations, source provenance, source JSON availability, lineage edges, generation groups, diagnostics, and optional exact source JSON

#### Scenario: Record inspection contracts are covered
- **WHEN** record tabs consume viewer descriptors, rendered record payloads, file lists, lineage, siblings, or facets
- **THEN** documented contracts and Python schemas SHALL cover the fields required to choose a viewer, open canonical detail, display rendered Markdown, display file openability, group raw JSON modal payloads, report diagnostics, and copy an absolute artifact filepath when available
- **AND** record detail contracts SHALL cover optional Topic Workspace-relative path, absolute artifact filepath, and direct parent idea metadata when those values can be derived from structured read-model data

### Requirement: Contract Validation Tests
The system SHALL include tests that exercise GUI contract schema validation with representative Project Web payloads.

#### Scenario: Extra fields are accepted in tests
- **WHEN** a test validates a representative GUI payload that includes unknown top-level and nested fields
- **THEN** the test SHALL pass if all required GUI fields are present

#### Scenario: Missing required fields are rejected in tests
- **WHEN** a test validates a representative GUI payload with a required field removed
- **THEN** the test SHALL assert that validation fails

#### Scenario: Current backend payloads remain compatible
- **WHEN** tests build representative payloads from current Project Web read-model shapes
- **THEN** those payloads SHALL validate without requiring database migration or removal of extra metadata

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

### Requirement: Project Web Display Contracts Use Summary
Project Web graph, timeline, hover, detail, and record read contracts SHALL expose `summary` as the brief display field and SHALL NOT require `one_liner`.

#### Scenario: Graph node uses summary
- **WHEN** the Project Web idea graph consumes a graph response
- **THEN** each graph node exposes `title`, `summary`, material kind, status, refs, and diagnostics needed for rendering
- **AND** canonical Research Idea nodes also expose `display_key`, visibility, and parent refs
- **AND** the node contract does not expose `one_liner`

#### Scenario: Timeline row uses summary
- **WHEN** the Project Web idea timeline consumes a timeline row response
- **THEN** the row exposes creation time, display index, display key, title, summary, parent display keys or indexes, visibility, status, and diagnostics needed for table rendering
- **AND** the row contract does not expose `one_liner`

#### Scenario: Hover and detail use summary
- **WHEN** the Project Web hover preview or idea detail panel opens a Research Idea
- **THEN** the read payload exposes canonical idea `title` and `summary` and exact source-fragment `title` and `summary` when available
- **AND** source aliases remain separate from display fields

#### Scenario: Fuzzy search includes summary
- **WHEN** a GUI user performs fuzzy text search in idea graph or timeline views
- **THEN** search matching includes `summary` and the other visible/searchable row or node fields
- **AND** visibility flags still control whether supporting or hidden ideas are shown in results

### Requirement: Project Web Display Diagnostics Are Non-fatal
Project Web read contracts SHALL carry display-contract diagnostics so damaged data does not crash the GUI.

#### Scenario: Missing summary reaches GUI as diagnostic
- **WHEN** a backend graph, timeline, hover, or detail response encounters an idea without a usable `summary`
- **THEN** the response includes a diagnostic naming the affected idea and missing field
- **AND** the GUI can render the remaining interpretable data without reading `one_liner`

#### Scenario: Recent errors include display issues
- **WHEN** Project Web records display-contract warnings or errors while building read models
- **THEN** the recent-errors read contract exposes those issues for operator inspection
- **AND** the recent-errors contract remains a process-local recent diagnostic query rather than durable Workspace Runtime storage for this change

