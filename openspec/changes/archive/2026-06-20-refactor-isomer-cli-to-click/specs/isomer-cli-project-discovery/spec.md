## ADDED Requirements

### Requirement: Click Command Registration
The system SHALL implement the Milestone 1 `isomer-cli` command surface with Click command groups while preserving the established Project discovery command behavior.

#### Scenario: Root command is Click backed
- **WHEN** the package exposes `isomer-cli` through `isomer_labs.cli:main`
- **THEN** the command dispatch uses a Click command group rather than an `argparse` parser tree

#### Scenario: Existing commands remain available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help still lists `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: Existing command outputs remain compatible
- **WHEN** a user runs `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, or `schemas list` with JSON output requested
- **THEN** the command emits the same versioned JSON contract shape used by the Milestone 1 project-discovery implementation

#### Scenario: Domain diagnostics remain Isomer diagnostics
- **WHEN** Project discovery, Project Manifest validation, Research Topic Config validation, Effective Topic Context resolution, or Workspace Path Resolution fails
- **THEN** the command reports stable Isomer diagnostics rather than replacing domain validation failures with Click parser errors
