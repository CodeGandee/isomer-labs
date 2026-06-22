## MODIFIED Requirements

### Requirement: Doctor Output Contract
The system SHALL emit deterministic text and versioned JSON output for `doctor` suitable for CI, unit tests, and future Operator Agent consumption.

#### Scenario: JSON output is wrapped
- **WHEN** a user runs `isomer-cli --print-json doctor`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, `mode`, `mutated`, `checks`, and `diagnostics`

#### Scenario: Mutated flag is false
- **WHEN** a user runs `isomer-cli --print-json doctor`
- **THEN** the JSON payload reports `mutated` as false

#### Scenario: Checks have stable shape
- **WHEN** `doctor` emits JSON checks
- **THEN** each check includes a stable id, scope, status, concept, summary, and optional source path or source detail

#### Scenario: Text output groups checks
- **WHEN** a user runs `isomer-cli doctor` without JSON output
- **THEN** the text output groups checks by host, Project, and topic scope and uses Isomer concept names in diagnostic lines

#### Scenario: Secret values are not printed
- **WHEN** Project or topic config contains secret-like fields or values
- **THEN** `doctor` reports the offending field or path without printing the secret value
