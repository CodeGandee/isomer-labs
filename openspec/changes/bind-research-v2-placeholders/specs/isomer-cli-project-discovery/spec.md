## ADDED Requirements

### Requirement: Research Extension Command Surface
The system SHALL expose `isomer-cli ext research records` commands as part of the installed CLI command surface.

#### Scenario: Root help lists research record extension
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface includes `ext research records create`, `ext research records show`, `ext research records list`, `ext research records update`, and `ext research records delete`

#### Scenario: Extension help lists records group
- **WHEN** a user runs `isomer-cli ext research --help`
- **THEN** the CLI lists the `records` command group

#### Scenario: Records help lists CRUD commands
- **WHEN** a user runs `isomer-cli ext research records --help`
- **THEN** the CLI lists `create`, `show`, `list`, `update`, and `delete`

#### Scenario: Research record commands require topic context
- **WHEN** a user invokes a mutating or reading research record command without a resolvable Topic Workspace
- **THEN** the command returns a deterministic error rather than creating implicit Project or Topic Workspace state
