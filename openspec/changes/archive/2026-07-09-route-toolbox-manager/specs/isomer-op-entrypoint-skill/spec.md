## ADDED Requirements

### Requirement: Entrypoint Routes Toolbox Tasks
The `isomer-op-entrypoint` skill SHALL route concrete project-local Toolbox tasks to `isomer-op-toolbox-mgr` while preserving owner boundaries for misc helper skills and direct CLI requests.

#### Scenario: System skill index includes Toolbox manager
- **WHEN** the entrypoint system skill index is inspected
- **THEN** it lists `isomer-op-toolbox-mgr` as the active operator owner for creating, converting, installing, inspecting, updating, disabling, uninstalling, and explaining project-local Toolboxes
- **AND** it includes Toolbox callback declarations, callback insertion points, Runtime Params, and effective-state inspection in that owner boundary

#### Scenario: Concrete Toolbox task routes to owner skill
- **WHEN** the user gives a concrete task to create a Toolbox, convert a skill into Toolbox material, insert a Toolbox callback, list callback insertion points, manage Toolbox Runtime Params, or inspect Toolbox effective state
- **THEN** the entrypoint selects `isomer-op-toolbox-mgr` as the owner skill
- **AND** it proceeds through that owner route or reports the blocker that prevents safe execution

#### Scenario: Toolbox route is distinct from tool packs
- **WHEN** the user asks for project-local Toolbox callback or Runtime Param management
- **THEN** the entrypoint does not route the task to `isomer-misc-tool-packs`
- **AND** package or installable toolset requests still use the existing misc helper boundary only when explicitly requested

### Requirement: Entrypoint Indexes Toolbox CLI Families
The `isomer-op-entrypoint` skill SHALL include concise CLI routing guidance for existing Toolbox command families.

#### Scenario: Toolbox CLI families are named
- **WHEN** entrypoint CLI guidance is inspected
- **THEN** it names `isomer-cli project toolboxes ...`, `isomer-cli project skill-callbacks ...`, and `isomer-cli project toolbox-params ...` as Toolbox-related CLI command families
- **AND** it describes `toolboxes` as full Toolbox registration, validation, install, enable, disable, update-source, uninstall, show, list, or explain work
- **AND** it describes `skill-callbacks` as callback insertion-point, registry, resolve, validation, and callback install or refresh work
- **AND** it describes `toolbox-params` as Runtime Param set, unset, import, get, explain, and validate work

#### Scenario: Explicit CLI request may use CLI route
- **WHEN** the user explicitly asks for a Toolbox CLI command family
- **THEN** the entrypoint may route to the matching CLI family, inspect CLI help when flags are needed, and preserve read-only or mutation posture in its output
