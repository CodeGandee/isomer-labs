## MODIFIED Requirements

### Requirement: Topic environment setup is explicit
The module skill SHALL route topic environment setup through `isomer-srv-env-setup` and SHALL treat the setup as durable static preparation. The skill SHALL NOT block environment setup solely because the Project Manifest lacks an explicit `topic_standalone_pixi_bindings` entry when Pixi can resolve the registered Topic Workspace directory as the default Topic Workspace Pixi binding target.

#### Scenario: Setup delegates to environment service
- **WHEN** the specialized topic team needs a development environment before work can start
- **THEN** the skill routes to `setup-topic-env`, prepares or reuses the source gate at `<topic-workspace>/user-intent/src/env-gate.md`, and delegates heavy environment setup to `isomer-srv-env-setup`

#### Scenario: Default binding removes explicit binding blocker
- **WHEN** `setup-topic-env` runs for a registered Topic Workspace
- **AND** the Project Manifest has no active `topic_standalone_pixi_bindings` entry for the Research Topic
- **AND** Pixi can resolve the registered Topic Workspace directory as a confined Topic Workspace Pixi binding target
- **THEN** the skill delegates environment setup to `isomer-srv-env-setup` instead of reporting a missing binding blocker

#### Scenario: Missing default Pixi workspace still blocks
- **WHEN** `setup-topic-env` runs for a registered Topic Workspace
- **AND** the Project Manifest has no active `topic_standalone_pixi_bindings` entry for the Research Topic
- **AND** Pixi cannot resolve the registered Topic Workspace directory as a Topic Workspace Pixi binding target
- **THEN** the skill records a blocker that names the Topic Workspace directory as the default binding target and the option to add an explicit binding

#### Scenario: Setup records environment status
- **WHEN** `setup-topic-env` completes or stops on a blocker
- **THEN** it records environment setup status, commands run, changed files, validation refs, and blockers as durable static preparation evidence
