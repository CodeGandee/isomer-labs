## MODIFIED Requirements

### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with Project discovery, doctor diagnostics, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project-discovery commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `init`, `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: CLI exposes template and profile commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script

### Requirement: Diagnostics and Output Formats
The system SHALL produce deterministic diagnostics and machine-readable output for Project discovery, doctor diagnostics, template inspection, and Topic Agent Team Profile commands.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output for `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, or `team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for doctor diagnostics, template registration, or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API
