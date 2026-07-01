## ADDED Requirements

### Requirement: Service Skills Use Global Isomer CLI for Isomer Operations
Non-dev service skills SHALL use direct `isomer-cli` command examples for Isomer Project, Topic Workspace, path, runtime, and record operations.

#### Scenario: Service skill Isomer CLI examples omit pixi prefix
- **WHEN** validation scans `skillset/service/**`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** examples use `isomer-cli ...` directly

#### Scenario: Topic Workspace Pixi setup remains allowed
- **WHEN** a service skill describes installing or verifying a Topic Workspace Pixi environment
- **THEN** it may keep Pixi environment commands for the user's workspace
- **AND** it still must call Isomer control-plane operations through global `isomer-cli`
