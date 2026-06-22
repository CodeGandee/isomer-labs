## MODIFIED Requirements

### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project-discovery commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `init`, `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show`

#### Scenario: CLI exposes template and profile commands
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script

### Requirement: Diagnostics and Output Formats
The system SHALL produce deterministic diagnostics and machine-readable output for Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile commands.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output for `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, `team-instances show`, `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, or `team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template registration, or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API

## ADDED Requirements

### Requirement: Runtime Command Side-effect Boundaries
The system SHALL make Workspace Runtime mutations explicit in CLI behavior while preserving the read-only guarantees of inspection and design-time commands.

#### Scenario: Runtime init is the runtime creation command
- **WHEN** a user runs `isomer-cli runtime init`
- **THEN** the command may create or reopen `state.sqlite` and the default Workspace Runtime directories for the selected Topic Workspace

#### Scenario: Runtime prepare is the readiness preparation command
- **WHEN** a user runs `isomer-cli runtime prepare`
- **THEN** the command may record selected topic Pixi environment use, readiness status, readiness diagnostics, and preparation provenance in the selected Workspace Runtime

#### Scenario: Runtime inspect is read-only
- **WHEN** a user runs `isomer-cli runtime inspect`
- **THEN** the command reads Workspace Runtime metadata and selected record counts without creating or mutating runtime state

#### Scenario: Runtime validate is read-only
- **WHEN** a user runs `isomer-cli runtime validate`
- **THEN** the command reports Workspace Runtime diagnostics without creating directories, changing statuses, or repairing records

#### Scenario: Team instance create is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances create`
- **THEN** the command may create Agent Team Instance, Agent Instance, Agent Workspace, path plan, Workflow Stage Cursor, and Provenance records for the selected Topic Workspace

#### Scenario: Team instance inspection is read-only
- **WHEN** a user runs `isomer-cli team-instances list` or `isomer-cli team-instances show`
- **THEN** the command reads Workspace Runtime records without creating Agent Team Instances, Agent Instances, Agent Workspaces, Runs, Houmao launch material, or adapter refs
