## ADDED Requirements

### Requirement: Operator Skills Use Global Isomer CLI
Operator skills SHALL assume they are installed into agents outside the `isomer-labs` repository and SHALL invoke Isomer CLI commands through the globally installed `isomer-cli` executable.

#### Scenario: Operator skill examples avoid repo-local Pixi invocation
- **WHEN** validation scans files under `skillset/operator/`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** direct command examples use `isomer-cli ...` instead

#### Scenario: Developer skills are exempt
- **WHEN** validation scans files under `skillset/dev/`
- **THEN** repo-local examples may use `pixi run isomer-cli` because dev skills operate inside this repository

#### Scenario: Operator guidance can still mention Topic Workspace Pixi environments
- **WHEN** operator or service skills describe a Topic Workspace Pixi environment owned by the user's research workspace
- **THEN** they may mention Pixi environment setup or Pixi commands for that workspace
- **AND** they still must not invoke Isomer's own CLI as `pixi run isomer-cli`
