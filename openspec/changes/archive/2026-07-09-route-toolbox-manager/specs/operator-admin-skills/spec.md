## ADDED Requirements

### Requirement: Operator Inventory Routes Toolbox Manager
The operator skillset documentation SHALL list `isomer-op-toolbox-mgr` as an active operator owner skill and SHALL keep welcome and entrypoint guidance consistent with that inventory.

#### Scenario: Operator docs list Toolbox manager as active
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-op-toolbox-mgr`
- **AND** it describes the skill as the owner for project-local Toolbox source authoring, conversion, callback insertion, Runtime Params, install, mutation, and inspection through existing CLI-backed surfaces

#### Scenario: Welcome and entrypoint use inventory consistently
- **WHEN** active operator guidance is inspected
- **THEN** `isomer-op-welcome` can recommend `isomer-op-toolbox-mgr` as an active owner workflow
- **AND** `isomer-op-entrypoint` can select `isomer-op-toolbox-mgr` as the route-and-proceed owner for concrete Toolbox tasks
