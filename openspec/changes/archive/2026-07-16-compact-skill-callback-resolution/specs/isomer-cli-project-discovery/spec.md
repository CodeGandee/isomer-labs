## MODIFIED Requirements

### Requirement: Project Skill Callback Command Group
The system SHALL expose User Skill Callback management, compact execution resolution, detailed resolution explanation, and insertion-point discovery through the generic `isomer-cli project skill-callbacks` command group.

#### Scenario: Project group exposes skill-callbacks
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists the `skill-callbacks` command group alongside other Project-scoped command groups

#### Scenario: Skill-callbacks help lists commands
- **WHEN** a user runs `isomer-cli project skill-callbacks --help`
- **THEN** the command help lists `register`, `install`, `resolve`, `insertion-points`, `list`, `show`, `disable`, and `validate`

#### Scenario: Resolve help exposes detailed explanation
- **WHEN** a user runs `isomer-cli project skill-callbacks resolve --help`
- **THEN** the command documents compact execution output as the default
- **AND** it documents `--explain` as the detailed callback, registry, source, and Toolbox gating view

#### Scenario: Commands discover Project first
- **WHEN** a user runs a `project skill-callbacks` command
- **THEN** the command uses the standard Project discovery and explicit Project selector behavior before loading callback registries or Project-declared operator system extensions

#### Scenario: Topic-scoped commands resolve topic context
- **WHEN** a user runs a `project skill-callbacks` command that targets or reads topic-scoped callback registrations
- **THEN** the command uses standard topic selection precedence and Effective Topic Context validation before reading or mutating the topic-scoped registry

#### Scenario: JSON output is deterministic and purpose appropriate
- **WHEN** a user runs `isomer-cli --print-json project skill-callbacks <subcommand>`
- **THEN** the command returns deterministic machine-readable output and diagnostics
- **AND** ordinary `resolve` returns only ordered callback ids, source types, absolute instruction paths, and applicable external-source markers
- **AND** `resolve --explain`, `list`, `show`, `register`, `install`, `disable`, and `validate` return the management fields appropriate to their operation
- **AND** insertion-point metadata appears only when requested by the insertion-point surface

#### Scenario: Missing project is rejected
- **WHEN** no Project can be discovered for a `project skill-callbacks` command
- **THEN** the command fails with the standard missing-Project diagnostic and does not create callback registry files in the current directory
