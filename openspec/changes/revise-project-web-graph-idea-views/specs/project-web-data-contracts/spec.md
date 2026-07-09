## ADDED Requirements

### Requirement: Idea Timeline Contract Coverage
The Project Web UI contract set SHALL document and validate the payload shape consumed by the Idea Timeline view.

#### Scenario: Timeline contract is documented
- **WHEN** a developer or agent needs to implement or review the Idea Timeline view
- **THEN** `docs/ui/contracts/` contains contract documentation for the timeline payload or an updated topic graph contract that explicitly covers timeline use
- **AND** the documentation identifies required fields, optional useful fields, extra-field handling, and a concrete example

#### Scenario: Timeline payload validates required fields
- **WHEN** tests validate a representative Idea Timeline payload
- **THEN** validation passes when required topic identity, idea identity, title, timestamp or fallback ordering fields, parent relationship identity, diagnostics, and mutation state are present

#### Scenario: Timeline payload rejects unsafe omissions
- **WHEN** tests validate a representative Idea Timeline payload missing fields required for safe table rendering or row opening
- **THEN** validation fails with a deterministic error or the GUI reports a safe empty/diagnostic state

### Requirement: Graph View Metadata Contract Coverage
The Project Web UI contract set SHALL document metadata needed to distinguish idea graph and idea timeline views.

#### Scenario: View metadata is documented
- **WHEN** a graph-section openable descriptor or graph payload identifies an idea view
- **THEN** the contract documentation describes the field or identifier that separates relationship graph presentation from timeline/table presentation

#### Scenario: Extra graph fields remain accepted
- **WHEN** graph or timeline payloads include additional metadata for future timeline growth
- **THEN** contract validation accepts those extra fields as long as required GUI fields are present
