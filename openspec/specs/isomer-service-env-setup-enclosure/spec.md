# isomer-service-env-setup-enclosure Specification

## Purpose
Define the environment enclosure policy for Topic Workspace environment setup.
## Requirements
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

### Requirement: Dependency Enclosure Ladder
The service environment setup skill SHALL classify each dependency or runtime need through a fixed enclosure ladder before installation or verification.

#### Scenario: Pixi-managed dependency is preferred
- **WHEN** a dependency required by `topic.intent.topic_env_requirements` can be satisfied by PyPI through Pixi or by Pixi/Conda packages
- **THEN** the skill instructs the agent to install it through the selected Topic Workspace Pixi manifest
- **AND** the command uses `pixi add --manifest-path <manifest_path>` or `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`
- **AND** the dependency and selected source are recorded in `topic.env.topic_setup_target_spec`

#### Scenario: External runtime wiring is explicit
- **WHEN** a gate requires an external DLL, SO, SDK, compiler, CUDA runtime, package-config path, activation script, or similar runtime piece that cannot reasonably be installed through Pixi
- **THEN** the skill instructs the agent to route that runtime piece through an explicit Pixi-run command environment
- **AND** the derived gate records the external path, sourced script, environment variable, or activation command
- **AND** the derived gate records why Pixi-managed installation was not used

#### Scenario: Topic-local fallback is secondary
- **WHEN** Pixi-managed installation and Pixi-mediated external runtime wiring cannot satisfy the gate
- **THEN** the skill SHALL either instruct the agent to use a topic-local user-space fallback under `<topic-workspace-dir>/.isomer-user-env/` or report a blocker
- **AND** the fallback path is added to the Topic Workspace `.gitignore` when used
- **AND** the fallback command, installed path, and reason for fallback are recorded in `topic.env.topic_setup_target_spec`
- **AND** the final output reports the fallback as a lower-portability dependency

#### Scenario: Privileged or global mutation blocks setup
- **WHEN** a dependency or setup instruction requires sudo, system package manager mutation, global shell profile edits, global Python package installation, global Node package installation, `/etc` changes, `ldconfig`, daemon installation, kernel driver changes, or another privileged or machine-global action
- **THEN** the skill reports a blocker instead of running that action
- **AND** the blocker names the required action, why it is outside the service-safe boundary, and what user action or external preparation is needed

### Requirement: Derived Gate Records Enclosure Strategy
The service environment setup skill SHALL require `derive-env-gate` to record the enclosure strategy that later dependency installation and verification must follow.

#### Scenario: Dependency plan includes enclosure choices
- **WHEN** `derive-env-gate` writes or updates `topic.env.topic_setup_target_spec`
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
- **WHEN** `install-topic-deps` reads `topic.env.topic_setup_target_spec`
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
- **WHEN** `verify-env-gate` runs a command from `topic.env.topic_setup_target_spec`
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
- **AND** the final output warns that those pieces can require repair or reinstall if the Topic Workspace moves or the host runtime changes

### Requirement: Package Source Resolution Is Delegated When It Becomes a Decision
The service environment setup enclosure workflow SHALL keep dependency installation Pixi-scoped while routing package repository, mirror, registry, or channel choice to the package repository resolver when source selection is uncertain or policy-relevant.

#### Scenario: Reachability uncertainty invokes package resolver guidance
- **WHEN** topic env setup must choose among official package sources, configured mirrors, private registries, or fallback channels before dependency mutation
- **THEN** the skill text names `isomer-srv-resolve-pkg-repo` as the package source resolution surface
- **AND** the topic env setup output records the selected source, source evidence, and any reachability or fallback warning rather than embedding an untraceable source decision

#### Scenario: Fixed gate or manifest source does not require extra resolution
- **WHEN** the environment gate, Pixi manifest, lockfile, or Service Request already fixes the package source and there is no reachability concern
- **THEN** topic env setup may use that fixed source without invoking package repository resolution
- **AND** it records the source as fixed by existing evidence

### Requirement: CUDA Compile and NVIDIA Environment Policy Are Routed to Misc Skills
The service environment setup enclosure workflow SHALL route CUDA compile bounding decisions to `isomer-misc-bounded-run-tips` and CUDA/C++ Pixi environment decisions to `isomer-misc-nvidia-tools` instead of expanding topic env setup into a general CUDA guide.

#### Scenario: CUDA compile decisions use bounded run skill
- **WHEN** topic env setup encounters CUDA architecture targets, `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `nvcc` build flags, CUDA/C++ Pixi build environments, or CUDA build parallelism decisions
- **THEN** the skill text points to `isomer-misc-bounded-run-tips` for CUDA architecture targets, `nvcc` build flags, and CUDA build parallelism
- **AND** the skill text points to `isomer-misc-nvidia-tools` for CUDA/C++ Pixi build environment preferences and NVIDIA package/runtime wiring
- **AND** topic env setup records only the setup decisions needed for the selected Topic Workspace Pixi environment and derived gate

#### Scenario: NVIDIA channel choice remains auditable
- **WHEN** an NVIDIA tool or runtime package must be installed through Pixi channels
- **THEN** the final setup evidence records the selected channel and reason
- **AND** if channel reachability or mirror selection is uncertain, the package repository resolver provides the source decision before topic env setup mutates the Pixi manifest

### Requirement: Explicit Target Specs Need Enclosure Validation
The service environment setup skill SHALL validate enclosure strategy in any explicit derived topic env target spec before mutating Topic Workspace environment files or running setup commands.

#### Scenario: Explicit target spec contains enclosure strategy
- **WHEN** `isomer-srv-topic-env-setup` receives an explicit derived gate file, target-spec prompt, or target-spec context from a manual invocation
- **AND** the target spec contains dependency or runtime setup requirements
- **THEN** the service validates that each requirement has a Pixi-managed, Pixi-mediated external runtime wiring, topic-local fallback, or blocked enclosure strategy before materialization

#### Scenario: Explicit target spec lacks enclosure strategy
- **WHEN** an explicit derived topic env target spec lacks enclosure strategy for a dependency or runtime need
- **THEN** the service either derives the missing enclosure strategy into the target spec before mutation or reports a blocker
- **AND** it does not install or verify that dependency from ambient shell state alone

### Requirement: Heavy Operation Resource Strategy Routes Through Bounded Run Tips First
The service environment setup enclosure workflow SHALL treat bounded-run tips as the first routing surface for resource-heavy setup and verification planning across topic env and agent env gates.

#### Scenario: Heavy-operation policy is shared
- **WHEN** topic env setup or agent env setup generates an operational env gate with a resource-heavy setup or verification item
- **THEN** the service guidance routes the item to `isomer-misc-bounded-run-tips` before using local generic resource judgment
- **AND** the generated gate records the bounded-run guidance source in its `Resource Check Plan`
- **AND** the gate records generic best-effort judgment only when no specific bounded-run guidance applies

#### Scenario: Bounded run guidance does not replace dependency policy
- **WHEN** a heavy operation also needs package installation, CUDA/C++ Pixi environment setup, NVIDIA runtime wiring, package repository resolution, or package-specific caveat handling
- **THEN** bounded-run tips provide only the resource-safe execution strategy
- **AND** package installation, runtime wiring, and repository source choices remain routed to their existing package-specific, NVIDIA, repository-resolution, and enclosure policy surfaces

#### Scenario: Readiness still requires real-path evidence
- **WHEN** a generated env gate includes a heavy source-intent path
- **THEN** readiness requires passing evidence from the bounded real-path command or a named blocker with resource evidence
- **AND** a smoke test that misses the critical build, inference, dataset, benchmark, or cwd command path does not satisfy the checklist item unless the user explicitly downgraded the gate
