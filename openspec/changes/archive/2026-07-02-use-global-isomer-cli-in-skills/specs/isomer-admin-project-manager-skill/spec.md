## ADDED Requirements

### Requirement: Project Manager Uses Global Isomer CLI Invocation
The Project Manager skill SHALL present `isomer-cli` as a globally installed executable, not as a repo-local Pixi task.

#### Scenario: Project Manager command examples omit pixi prefix
- **WHEN** Project Manager skill text or local references list Project command examples
- **THEN** examples use command shapes such as `isomer-cli project init`, `isomer-cli --print-json project validate`, `isomer-cli project runtime init`, and `isomer-cli project cleanup --dry-run`
- **AND** they do not use `pixi run isomer-cli`

#### Scenario: Project Manager still preserves project namespace
- **WHEN** the Pixi prefix is removed from examples
- **THEN** the command still preserves the canonical `isomer-cli project ...` namespace and existing flags
