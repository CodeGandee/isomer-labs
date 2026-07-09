## MODIFIED Requirements

### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with a global command surface for doctor diagnostics and a `project` command group for Project discovery, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `project` and global Project-independent commands such as `schemas`

#### Scenario: Top-level empty invocation shows command overview
- **WHEN** a user runs `isomer-cli` without arguments
- **THEN** the process exits successfully
- **AND** the output lists the top-level subcommands `doctor`, `project`, `ext`, `schemas`, and `system-skills`
- **AND** the output explains the purpose of each top-level subcommand

#### Scenario: Top-level help links to project resources
- **WHEN** a user runs `isomer-cli` or `isomer-cli --help`
- **THEN** the output includes the GitHub repository URL `https://github.com/CodeGandee/isomer-labs`
- **AND** the output includes the documentation URL `https://codegandee.github.io/isomer-labs/`

#### Scenario: CLI reports installed version
- **WHEN** a user runs `isomer-cli --version`
- **THEN** the process exits successfully
- **AND** the output reports the installed `isomer-labs` package version

#### Scenario: Empty group invocation shows group help
- **WHEN** a user runs a command group without a child subcommand, such as `isomer-cli project`, `isomer-cli project topics`, `isomer-cli ext research`, or `isomer-cli system-skills`
- **THEN** the process exits successfully
- **AND** the output lists the subcommands available at that command level
- **AND** the output is not wrapped in an `ISOCLI001` invocation-error diagnostic

#### Scenario: Project group exposes project-discovery command groups
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists immediate Project subcommands and command groups such as `init`, `validate`, `topics`, `workspaces`, `context`, `paths`, `runtime`, and `team-instances`
- **AND** the command help does not list `doctor`

#### Scenario: Project group exposes template and profile commands
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script
