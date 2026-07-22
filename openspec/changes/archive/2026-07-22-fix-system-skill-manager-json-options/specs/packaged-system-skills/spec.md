## ADDED Requirements

### Requirement: Packaged System Skill CLI Examples Use Supported JSON Options
Packaged system-skill instructions SHALL place the global `--print-json` option immediately after `isomer-cli` when they request deterministic structured output, and repository validation SHALL reject `isomer-cli` command examples that use the unsupported command-local `--json` token.

#### Scenario: Structured-output example uses the global option
- **WHEN** a packaged system skill documents an Isomer CLI command that requests deterministic JSON output
- **THEN** the example uses `isomer-cli --print-json <command>`
- **AND** packaged skill validation accepts the option placement

#### Scenario: Command-local JSON option is rejected
- **WHEN** a packaged system skill contains an `isomer-cli <command> --json` example
- **THEN** packaged skill validation reports the file and line as unsupported command-local JSON syntax

#### Scenario: JSON-bearing command options remain valid
- **WHEN** a packaged system skill uses a supported option whose exact name is not `--json`, such as `--metadata-json`
- **THEN** packaged skill validation does not classify that option as command-local structured-output syntax
