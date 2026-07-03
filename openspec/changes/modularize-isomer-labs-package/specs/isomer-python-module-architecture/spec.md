## ADDED Requirements

### Requirement: Root Package Uses Bounded Contexts
The system SHALL keep `src/isomer_labs` root implementation minimal by organizing domain behavior into accepted bounded-context packages instead of adding feature-sized modules directly under the package root.

#### Scenario: Root implementation files stay minimal
- **WHEN** repository architecture tests scan `src/isomer_labs`
- **THEN** they fail if root-level implementation modules outside an explicit transition allowlist exceed the accepted root-module size threshold

#### Scenario: New root domain modules are rejected
- **WHEN** a developer adds a new Python file directly under `src/isomer_labs`
- **THEN** architecture tests require it to be an accepted bootstrap, compatibility, or low-level package file rather than a feature-sized domain module

#### Scenario: Domain behavior moves into accepted packages
- **WHEN** Project, Topic Workspace, Team, Records, or shared Core behavior is refactored
- **THEN** the implementation lives under packages such as `project`, `workspace`, `teams`, `records`, or `core` with canonical internal imports

### Requirement: CLI App Is a Bootstrap Surface
The system SHALL keep `isomer_labs.cli.app` focused on Click app creation, shared bootstrap wiring, and registration instead of hosting command handler implementations.

#### Scenario: Command handlers live outside app bootstrap
- **WHEN** a public CLI command executes Project, Workspace, Team, Runtime, Records, or Houmao behavior
- **THEN** its command handler implementation is located in a focused CLI handler module rather than implemented directly in `cli/app.py`

#### Scenario: CLI entry point stays stable
- **WHEN** packaging invokes the project script entry point `isomer_labs.cli:main`
- **THEN** the import resolves and dispatches through the modular CLI package with the existing public command surface

#### Scenario: CLI app size is guarded
- **WHEN** repository architecture tests inspect `src/isomer_labs/cli/app.py`
- **THEN** they fail if the file grows beyond the accepted bootstrap-size threshold or contains command-handler clusters that belong in handler modules

### Requirement: Package Moves Preserve Behavior
The system SHALL treat the modularization as an internal organization change that preserves externally visible behavior.

#### Scenario: CLI output remains compatible
- **WHEN** existing unit tests invoke CLI commands with JSON or text output
- **THEN** command names, status behavior, output schema names, and documented JSON fields remain compatible unless another accepted spec changes them

#### Scenario: Runtime data formats remain compatible
- **WHEN** Project, Topic Workspace, Team Repository, Team Profile, Workspace Runtime, or Houmao adapter material is read after the refactor
- **THEN** existing persisted file formats and manifest schemas continue to parse with the same meanings

#### Scenario: Validation remains green
- **WHEN** implementation of the modularization is complete
- **THEN** `pixi run lint`, `pixi run typecheck`, and `pixi run test` pass without relying on broad architecture-test exemptions for the moved root modules
