## ADDED Requirements

### Requirement: Use-Case Command Boundary
The public `isomer-cli` command surface SHALL expose reusable platform operations rather than named use-case acceptance runners unless a later accepted product spec explicitly promotes the command.

#### Scenario: UC-01 command group is absent
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface does not list `uc01`, `uc01 run`, or `uc01 inspect`

#### Scenario: Generic commands remain available
- **WHEN** a manual acceptance harness needs to validate a Project, prepare Workspace Runtime state, create or inspect Agent Team Instance records, dispatch or normalize handoffs, or validate runtime records
- **THEN** it can use generic command groups such as `validate`, `runtime`, `team-instances`, `handoffs`, `team-templates`, and `team-profiles`

#### Scenario: Root print-json remains global
- **WHEN** a manual acceptance harness invokes generic CLI commands for deterministic output
- **THEN** it uses root-level `--print-json` and no command-local `--json`, `--format json`, or `--format=json` options are introduced for use-case harness behavior

### Requirement: Manual Harness Entry Points Are Outside Product CLI
Named use-case acceptance runners SHALL be invoked through test or manual script entry points outside the installed `isomer-cli` command surface.

#### Scenario: UC-01 harness has script entry point
- **WHEN** a developer wants to run the pinned UC-01 headless acceptance path
- **THEN** they use a documented command such as `pixi run python tests/manual/uc01_headless_vertical_slice` or an equivalent manual script entry point

#### Scenario: Harness output is not product CLI schema
- **WHEN** the UC-01 harness prints a deterministic summary
- **THEN** the summary may include harness-specific fields, but core CLI commands still emit the versioned `isomer-cli-output.v1` wrapper only for generic platform commands

### Requirement: Product Promotion Requires Spec Update
A named use-case command SHALL require an accepted spec update before it appears in `isomer-cli`.

#### Scenario: Future use-case command is proposed
- **WHEN** a future milestone wants `isomer-cli uc07` or another named use-case command
- **THEN** the proposal identifies why the command is reusable product behavior, adds or modifies CLI requirements, and updates command-surface tests before implementation
