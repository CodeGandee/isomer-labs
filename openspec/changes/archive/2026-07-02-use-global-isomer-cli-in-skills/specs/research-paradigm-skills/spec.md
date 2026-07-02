## ADDED Requirements

### Requirement: Research Skills Use Global Isomer CLI
Non-dev research paradigm skills SHALL call Isomer CLI surfaces through direct `isomer-cli` commands.

#### Scenario: Research skill CLI examples omit pixi prefix
- **WHEN** validation scans `skillset/research-paradigm/**`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** accepted Isomer extension calls use direct shapes such as `isomer-cli ext deepsci call ...` and `isomer-cli ext research records ...`

#### Scenario: Research environment commands remain separate
- **WHEN** a research skill describes commands to run inside a user Topic Workspace environment
- **THEN** it may describe that environment's own package or task runner when relevant
- **AND** it still must not use that runner to invoke Isomer's global CLI
