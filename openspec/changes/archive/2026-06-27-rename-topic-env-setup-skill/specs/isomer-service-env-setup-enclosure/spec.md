## MODIFIED Requirements

### Requirement: Environment Enclosure Policy
The service environment setup skill SHALL define environment enclosure as Pixi-first, auditable Topic Workspace setup that avoids privileged or machine-global host mutation.

#### Scenario: Enclosure policy is visible from the parent skill
- **WHEN** an agent reads `skillset/service/isomer-srv-topic-env-setup/SKILL.md`
- **THEN** the skill describes the environment enclosure policy for Topic Workspace setup
- **AND** the policy prioritizes Pixi-managed dependency installation
- **AND** the policy allows explicitly recorded runtime wiring through Pixi-run commands when Pixi cannot fully provide the needed runtime pieces
- **AND** the policy allows topic-local user-space fallback only as a secondary option
- **AND** the policy requires blockers for privileged or global host mutation

#### Scenario: Enclosure policy is carried through setup output
- **WHEN** the skill reports dependency setup results
- **THEN** the output contract includes enough information to identify Pixi-managed installs, external runtime wiring, topic-local user-space fallback installs, and blockers
- **AND** the output does not hide non-Pixi runtime dependencies behind generic readiness wording

### Requirement: Derived Gate Records Enclosure Strategy
The service environment setup skill SHALL require `derive-env-gate` to record the enclosure strategy that later dependency installation and verification must follow.

#### Scenario: Dependency plan includes enclosure choices
- **WHEN** `derive-env-gate` writes or updates `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **THEN** the `Dependency Plan` section records the enclosure strategy for each dependency or runtime need
- **AND** each entry identifies whether it is Pixi-managed, Pixi-mediated external runtime wiring, topic-local user-space fallback, or blocked
- **AND** non-Pixi choices include reasons

#### Scenario: Pixi install commands remain Pixi-scoped
- **WHEN** `derive-env-gate` writes `Pixi Install Commands`
- **THEN** dependency mutation commands use `pixi add --manifest-path <manifest_path>` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`
- **AND** setup commands that need runtime environment wiring use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`
- **AND** the commands do not rely on an unspecified activated shell

#### Scenario: Blocked global setup is visible
- **WHEN** the source gate or repo instructions mention privileged or global setup
- **THEN** `derive-env-gate` records the service-safe portion of setup when possible
- **AND** the derived gate records the privileged or global portion as a blocker or external prerequisite
- **AND** the derived gate does not convert the privileged or global action into an executable setup command

### Requirement: Install Dependencies Enforces Enclosure
The service environment setup skill SHALL require `install-topic-deps` to enforce the enclosure strategy before mutating Topic Workspace environment files or running setup commands.

#### Scenario: Install step refuses unclassified dependencies
- **WHEN** `install-topic-deps` reads `isomer-env-gate.md`
- **AND** a required dependency or runtime need lacks an enclosure strategy
- **THEN** the subcommand reports a blocker instead of installing or verifying the dependency
- **AND** the blocker tells the agent to update the derived gate before mutation

#### Scenario: Install step uses Pixi first
- **WHEN** a dependency is classified as Pixi-managed
- **THEN** `install-topic-deps` uses Pixi dependency commands against the selected Topic Workspace manifest
- **AND** it does not install the dependency into the Project-root environment, global Python, global Node, a user home package manager, or an Agent Workspace environment

#### Scenario: Install step records explicit runtime wiring
- **WHEN** a dependency uses Pixi-mediated external runtime wiring
- **THEN** `install-topic-deps` records the exact environment variables, source commands, runtime paths, and setup commands in the derived gate execution log
- **AND** those setup commands run through `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`

#### Scenario: Install step keeps fallback topic-local
- **WHEN** a dependency uses topic-local user-space fallback
- **THEN** `install-topic-deps` places the fallback under `<topic-workspace-dir>/.isomer-user-env/`
- **AND** it updates `<topic-workspace-dir>/.gitignore` to ignore `.isomer-user-env/`
- **AND** it records the fallback commands and changed files

### Requirement: Verification Requires Recorded Enclosure
The service environment setup skill SHALL require `verify-env-gate` to judge readiness from recorded Pixi-scoped commands and recorded runtime wiring, not from ambient shell state.

#### Scenario: Verification command is replayable
- **WHEN** `verify-env-gate` runs a command from `isomer-env-gate.md`
- **THEN** the command uses `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`
- **AND** any required runtime variables, sourced scripts, or external runtime paths are recorded in the derived gate before the command runs
- **AND** the execution log records the exact command form used

#### Scenario: Ambient shell success is not readiness
- **WHEN** a verification command passes only because the ambient shell has an unrecorded active environment, PATH entry, library path, global package, or sourced script
- **THEN** the skill does not report `ready`
- **AND** it reports `blocked` or `failed` with the missing enclosure record or missing Pixi-scoped command

#### Scenario: Readiness includes enclosure warnings
- **WHEN** the final readiness status is `ready`
- **AND** the setup uses external runtime wiring or topic-local user-space fallback
- **THEN** the final output reports the relevant paths, scripts, variables, or fallback prefix
- **AND** the final output warns that those pieces may need repair or reinstall if the Topic Workspace moves or the host runtime changes
