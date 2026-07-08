## ADDED Requirements

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
- **THEN** documented contracts and Python schemas SHALL cover the fields required to choose a viewer, open canonical detail, display file openability, and report diagnostics

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
