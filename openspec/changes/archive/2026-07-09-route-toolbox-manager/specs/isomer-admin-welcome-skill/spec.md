## ADDED Requirements

### Requirement: Welcome Skill Exposes Toolbox Manager Owner Route
The `isomer-op-welcome` skill SHALL expose `isomer-op-toolbox-mgr` as an active owner workflow for project-local Toolbox business while preserving the welcome skill's read-only posture.

#### Scenario: Default options include Toolbox management
- **WHEN** the welcome skill prints its default options
- **THEN** it includes project-local Toolbox creation, conversion, installation, inspection, update, disable, uninstall, callback insertion, Runtime Param, and insertion-point work as supported actions
- **AND** it names `isomer-op-toolbox-mgr` as the owner skill
- **AND** it does not present Toolbox management as a first-class research-start usage path such as `start-research-manually` or `start-research-by-agent-team`

#### Scenario: Skill map includes Toolbox manager
- **WHEN** the welcome skill prints its direct skill map
- **THEN** it includes a Toolbox management intent row that routes to `isomer-op-toolbox-mgr`
- **AND** the direct invocation guidance uses `$isomer-op-toolbox-mgr`

#### Scenario: Path choice recognizes Toolbox tasks
- **WHEN** the user asks the welcome skill which path owns Toolbox authoring, Toolbox installation, callback insertion, callback insertion points, Runtime Params, or effective Toolbox state
- **THEN** it recommends `isomer-op-toolbox-mgr`
- **AND** it does not route the request to `isomer-misc-tool-packs`

#### Scenario: Welcome remains read-only for Toolbox work
- **WHEN** the welcome skill recommends `isomer-op-toolbox-mgr`
- **THEN** it does not author Toolbox source, install Toolboxes, mutate callback registries, or mutate Runtime Params itself
