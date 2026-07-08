## ADDED Requirements

### Requirement: Project Web Uses Documented Data Contracts
The Project Web backend and frontend SHALL treat documented UI contracts as the handoff surface for GUI-renderable topic data.

#### Scenario: Backend returns contract-compatible payloads
- **WHEN** a Project Web API returns a payload consumed directly by a GUI panel
- **THEN** the payload SHALL satisfy the required fields of the corresponding UI contract
- **AND** the payload MAY include additional fields for diagnostics, future viewers, or JSON inspection

#### Scenario: Frontend receives extra fields
- **WHEN** the TypeScript GUI receives a contract-compatible payload with extra fields
- **THEN** the GUI SHALL render from the documented required and optional fields it knows about
- **AND** it SHALL NOT fail solely because the payload contains additional fields

#### Scenario: Frontend receives missing required fields
- **WHEN** the TypeScript GUI or backend validation detects a payload missing required UI contract fields
- **THEN** the system SHALL report a diagnostic, validation error, or safe empty state instead of crashing the workbench

#### Scenario: Contract docs guide new views
- **WHEN** a new Project Web topic panel or viewer is added
- **THEN** the implementation SHALL add or update a `docs/ui/contracts/` page and schema coverage for the GUI-facing payload shape before relying on the new contract in the frontend
