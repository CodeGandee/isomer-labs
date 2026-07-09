## MODIFIED Requirements

### Requirement: Project Skill Callback Command Group
The system SHALL expose User Skill Callback management, resolution, and insertion-point discovery through the generic `isomer-cli project skill-callbacks` command group.

#### Scenario: Project group exposes skill-callbacks
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists the `skill-callbacks` command group alongside other Project-scoped command groups

#### Scenario: Skill-callbacks help lists commands
- **WHEN** a user runs `isomer-cli project skill-callbacks --help`
- **THEN** the command help lists `register`, `install`, `resolve`, `insertion-points`, `list`, `show`, `disable`, and `validate`

#### Scenario: Commands discover Project first
- **WHEN** a user runs a `project skill-callbacks` command
- **THEN** the command uses the standard Project discovery and explicit Project selector behavior before loading callback registries or Project-declared operator system extensions

#### Scenario: Topic-scoped commands resolve topic context
- **WHEN** a user runs a `project skill-callbacks` command that targets or reads topic-scoped callback registrations
- **THEN** the command uses standard topic selection precedence and Effective Topic Context validation before reading or mutating the topic-scoped registry

#### Scenario: JSON output is deterministic
- **WHEN** a user runs `isomer-cli --print-json project skill-callbacks <subcommand>`
- **THEN** the command returns deterministic machine-readable output with callback ids, target system skill names, stages, scopes, statuses, priorities, source summaries, callback insertion-point metadata when requested, and diagnostics

#### Scenario: Missing project is rejected
- **WHEN** no Project can be discovered for a `project skill-callbacks` command
- **THEN** the command fails with the standard missing-Project diagnostic and does not create callback registry files in the current directory

## ADDED Requirements

### Requirement: Project System Extensions Command Group
The system SHALL expose Project operator system-extension memory through the generic `isomer-cli project system-extensions` command group.

#### Scenario: Project group exposes system-extensions
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists the `system-extensions` command group alongside other Project-scoped command groups

#### Scenario: System-extensions help lists commands
- **WHEN** a user runs `isomer-cli project system-extensions --help`
- **THEN** the command help lists `list`, `remember`, and `forget`

#### Scenario: Commands use Project discovery
- **WHEN** a user runs a `project system-extensions` command
- **THEN** the command uses the standard Project discovery and explicit Project selector behavior before reading or mutating the Project Manifest

#### Scenario: JSON output is deterministic
- **WHEN** a user runs `isomer-cli --print-json project system-extensions <subcommand>`
- **THEN** the command returns deterministic machine-readable output with catalog extension ids, Project declaration state, mutation status, and diagnostics

#### Scenario: Missing project is rejected
- **WHEN** no Project can be discovered for a `project system-extensions` command
- **THEN** the command fails with the standard missing-Project diagnostic and does not create a Project Manifest in the current directory
