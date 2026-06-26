## ADDED Requirements

### Requirement: Command-Style Subcommand Structure
The service environment setup skill SHALL be structured as a single command-style skill with short kebab-case subcommands, a lean top-level router, and linked executable reference pages.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-srv-env-setup`
- **THEN** the top-level `SKILL.md` instructs the agent to select one subcommand from a grouped `Subcommands` section
- **AND** the top-level workflow loads the selected subcommand's reference page and executes that page's `## Workflow`
- **AND** if no subcommand is given, the skill defaults to `topic-workspace`

#### Scenario: Subcommands are grouped for complex skill use
- **WHEN** the skill lists subcommands
- **THEN** it divides them into Procedural Subcommands, Helper Subcommands, and Misc Subcommands
- **AND** Procedural Subcommands include `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate`
- **AND** Misc Subcommands include `help` and `topic-workspace`
- **AND** Helper Subcommands may explicitly state that no helper subcommands are currently exposed
- **AND** each subcommand name is short kebab-case

#### Scenario: Topic workspace orchestrates the full workflow
- **WHEN** the `topic-workspace` subcommand runs
- **THEN** it orchestrates `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate` in order
- **AND** it reports the combined result through the parent skill output contract

#### Scenario: Step subcommands are directly callable
- **WHEN** a user or agent invokes `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, or `verify-gate` directly
- **THEN** the skill executes only that subcommand's workflow
- **AND** it refuses or blocks when predecessor artifacts required by that subcommand are missing

#### Scenario: Executable subcommand pages follow the style format
- **WHEN** a reference page acts as an executable subcommand page
- **THEN** it has a `## Workflow` section near the top
- **AND** the workflow is written as numbered steps
- **AND** the workflow ends with a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Workspace Pixi Layout
The service environment setup skill SHALL define Topic Workspace environment setup as materializing a standalone Pixi workspace directly under the selected Topic Workspace directory.

#### Scenario: Topic Workspace is the environment root
- **WHEN** an agent uses `isomer-srv-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to resolve the Project Manifest-declared Topic Workspace directory as the environment root
- **AND** the skill does not treat the Project root or an Agent Workspace as the Topic Workspace Pixi environment root

#### Scenario: Successful setup leaves Pixi files in the Topic Workspace
- **WHEN** Topic Workspace environment setup completes successfully
- **THEN** `<topic-workspace-dir>/pixi.toml` exists
- **AND** `<topic-workspace-dir>/pixi.lock` exists
- **AND** `<topic-workspace-dir>/.pixi/` exists

#### Scenario: Setup result is validated before readiness is reported
- **WHEN** the skill reports a Topic Workspace environment as ready
- **THEN** it has checked for `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/`
- **AND** it reports blockers instead of readiness when any of those paths is missing

#### Scenario: Manifest binding remains authoritative
- **WHEN** the skill resolves Topic Workspace Pixi paths
- **THEN** it uses the Project Manifest and active `topic_standalone_pixi_bindings` entry to identify the selected Topic Workspace and expected Pixi manifest
- **AND** it refuses to infer the binding solely from directory names

### Requirement: Environment Gate Verification
The service environment setup skill SHALL read `<topic-workspace-dir>/user-intent/src/env-gate.md`, generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`, and use the derived gate as the operational verification gate for Topic Workspace environment readiness.

#### Scenario: Gate file is required for readiness verification
- **WHEN** an agent uses `isomer-srv-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to look for `<topic-workspace-dir>/user-intent/src/env-gate.md`
- **AND** the skill treats the file as the source of user intent for what must be able to run after setup

#### Scenario: Missing gate file blocks readiness
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` is missing or unreadable
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** it asks for the gate file to be created or repaired before final readiness verification

#### Scenario: Derived gate is generated from source intent
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` is present and readable
- **THEN** the skill instructs the agent to generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **AND** the generated gate preserves the source gate's user intent while converting it into operational environment-readiness checks based on the user requirement and any required repo contents

#### Scenario: Derived gate uses fixed Markdown sections
- **WHEN** the skill generates `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **THEN** the generated file includes top-level sections named `Source Intent`, `Runnable Target`, `Repo Requirements`, `Inferred Source Warnings`, `Dependency Plan`, `Pixi Install Commands`, `Verification Commands`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Vague source gate is made operational
- **WHEN** the source gate is vague about what must run after environment setup
- **THEN** the generated `isomer-env-gate.md` includes concrete required-to-succeed dependencies, Pixi install commands, Pixi run commands, scripts, imports, tools, expected outputs, or equivalent pass/fail checks
- **AND** it establishes success criteria that another agent can execute or inspect without reinterpreting the vague source wording

#### Scenario: Derived gate contents drive post-setup checks
- **WHEN** the gate file describes commands, scripts, imports, tools, or other runnable checks expected after setup
- **THEN** the skill uses the derived `isomer-env-gate.md` expectations to select or report dependency installation commands and verification commands after Pixi setup
- **AND** readiness is reported only when the gate expectations are satisfied or explicitly deferred with blockers

#### Scenario: Gate verification remains service-safe
- **WHEN** either gate file names checks that imply live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, or research decision authority
- **THEN** the skill reports those parts as out-of-scope blockers or deferrals
- **AND** it verifies only the service-safe environment setup portion

### Requirement: Topic Workspace Repo Materialization
The service environment setup skill SHALL use `<topic-workspace-dir>/repos/<repo-name>` as the location for independent repositories required by the Topic Workspace task or environment gate.

#### Scenario: Required repos are rooted under the Topic Workspace
- **WHEN** the gate or task requires an independent repository
- **THEN** the skill instructs the agent to find an existing repository or place a missing repository under `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the skill does not place task repositories in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location

#### Scenario: Derived gate records repo requirements
- **WHEN** the source gate implies that runnable repository code is needed
- **THEN** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` lists the required repository names
- **AND** it lists each expected `<topic-workspace-dir>/repos/<repo-name>` path
- **AND** it records the acquisition source when the source is known
- **AND** it records commands, scripts, imports, or equivalent checks that verify each repo is usable

#### Scenario: Missing repo is acquired when enough source information exists
- **WHEN** a required repository is missing from `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the gate or task provides enough source information to acquire it through service-safe operations
- **THEN** the skill instructs the agent to download or materialize the repository under `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the skill records evidence from the repository at that expected path before reporting readiness

#### Scenario: Missing repo source may be inferred
- **WHEN** a required repository is missing from `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the gate or task implies runnable repository code is needed without naming an explicit source
- **THEN** the skill may instruct the agent to infer, search for, and acquire a likely repository source under `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` includes a visible warning in `Inferred Source Warnings` that the repository source was inferred rather than explicitly provided by the user
- **AND** the warning names the repo, expected path, inferred source, reason for choosing it, and any uncertainty or review needed
- **AND** the final skill output reports the same warning

#### Scenario: Missing repo blocks readiness when source remains ambiguous
- **WHEN** a required repository is missing from `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the gate, task, and agent source inference do not identify a likely source that can be verified against the desired command
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** the blocker names the missing repo requirement and the expected `<topic-workspace-dir>/repos/<repo-name>` location

#### Scenario: Repo checks drive readiness
- **WHEN** the derived gate requires one or more repositories
- **THEN** readiness requires each expected repo path to exist
- **AND** readiness requires the repo checks from the derived gate to pass or be reported as explicit blockers

#### Scenario: Repo materialization keeps Pixi root stable
- **WHEN** a required repo has its own project files, install commands, or run commands
- **THEN** the Topic Workspace remains the standalone Pixi environment root
- **AND** repo-specific commands may run from `<topic-workspace-dir>/repos/<repo-name>` only as checks or setup steps defined by the derived gate

### Requirement: Dependency Inference and Pixi Execution
The service environment setup skill SHALL instruct the agent to infer the dependencies needed for `env-gate.md` to pass, install those dependencies with Pixi, and run the desired command through the Topic Workspace Pixi environment.

#### Scenario: Dependencies are inferred from source gate and repo contents
- **WHEN** the source gate and any required repos are available
- **THEN** the skill instructs the agent to infer the language runtimes, libraries, tools, package-manager requirements, editable repo installs, and command-line programs needed for the gate to pass
- **AND** the inferred dependencies are recorded in `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`

#### Scenario: Python packages prefer PyPI
- **WHEN** the inferred dependency is a Python package
- **AND** the package can satisfy the gate through PyPI
- **THEN** the skill instructs the agent to prefer a PyPI dependency over a Pixi/Conda package
- **AND** the selected package source is recorded in `isomer-env-gate.md`

#### Scenario: Pixi or Conda packages are used when needed
- **WHEN** a dependency is a non-Python tool, command-line program, binary or system-level runtime dependency, Python package unavailable or unsuitable on PyPI, or setup requirement that cannot satisfy the gate through PyPI
- **THEN** the skill instructs the agent to use Pixi/Conda dependency mechanisms for that dependency
- **AND** if the dependency is a Python package, `isomer-env-gate.md` records why PyPI was not used

#### Scenario: NVIDIA packages prefer the NVIDIA channel
- **WHEN** the inferred dependency is an NVIDIA tool or runtime package installed through Pixi channels
- **THEN** the skill instructs the agent to prefer the `nvidia` channel over `conda-forge`
- **AND** `isomer-env-gate.md` records the selected channel and any fallback channel used

#### Scenario: Python is always available as the glue language
- **WHEN** the skill prepares a Topic Workspace root environment
- **THEN** the skill instructs the agent to include Python as the glue and orchestration language
- **AND** this remains true when the user-specified runnable target uses C++, TypeScript, CUDA, Rust, shell, or another non-Python language
- **AND** the Python baseline is recorded in `isomer-env-gate.md`

#### Scenario: Native target tooling is still installed
- **WHEN** the user-specified runnable target requires a non-Python language, toolchain, package manager, runtime, or command-line tool
- **THEN** the skill instructs the agent to install and verify those native dependencies in addition to the Python glue baseline
- **AND** Python does not replace the native tools required for the gate to pass

#### Scenario: Pixi installs inferred dependencies
- **WHEN** the derived gate lists dependencies needed for the user-specified runnable target
- **THEN** the skill instructs the agent to use Pixi from the Topic Workspace root to add or install those dependencies into the Topic Workspace environment
- **AND** the skill does not treat dependency inference as complete until the needed Pixi manifest and lockfile changes are present or blockers are reported

#### Scenario: Desired command runs through Pixi
- **WHEN** Pixi dependency installation has completed
- **THEN** the skill instructs the agent to run the desired command or commands through the Topic Workspace Pixi environment
- **AND** the command results determine whether `env-gate.md` has passed

#### Scenario: Dependency blockers are explicit
- **WHEN** the agent cannot infer or install a dependency needed for the gate to pass
- **THEN** the skill reports a blocker instead of claiming readiness
- **AND** the blocker names the missing dependency, why it is needed, and what information or manual action is required

### Requirement: Direct Topic Workspace Environment Mutation
The service environment setup skill SHALL allow direct service-safe mutation of the selected Topic Workspace Pixi environment during an explicit setup invocation, without requiring a separate Service Request boundary.

#### Scenario: Setup invocation authorizes Topic Workspace Pixi mutation
- **WHEN** the user invokes `isomer-srv-env-setup` for Topic Workspace environment setup
- **AND** the Project Manifest-declared Topic Workspace and active `topic_standalone_pixi_bindings` entry have been confirmed
- **THEN** the skill may instruct the agent to add dependencies, update `pixi.toml`, refresh `pixi.lock`, install packages, and run gate commands for that Topic Workspace
- **AND** it does not require a separate Service Request before performing those service-safe mutations

#### Scenario: Direct mutation remains scoped
- **WHEN** the skill performs direct setup mutation
- **THEN** the mutation scope is limited to the selected Topic Workspace Pixi environment and missing required repos under `<topic-workspace-dir>/repos/<repo-name>`

#### Scenario: Existing topic repos are not mutated by ensure-repos
- **GIVEN** a required repo path already exists under `<topic-workspace-dir>/repos/<repo-name>`
- **WHEN** `ensure-repos` runs
- **THEN** it inspects the existing repo as read-only evidence
- **AND** it does not run `git pull`, switch branches, copy files into the repo, delete files from the repo, install packages into the repo, regenerate files in the repo, or otherwise mutate the repo
- **AND** if the existing repo is unsuitable for the gate, it reports a blocker instead of repairing the repo without explicit user authorization
- **AND** the skill does not mutate the Project-root Pixi environment, an Agent Workspace-specific environment, unrelated Workspace Runtime records, agent launch material, GUI state, or research decision artifacts

#### Scenario: Mutation output remains auditable in the response
- **WHEN** direct setup mutation changes files or runs commands
- **THEN** the skill reports changed environment files, commands run, readiness status, and blockers through the parent skill output contract
- **AND** it does not hide dependency or lockfile changes behind generic readiness language

### Requirement: Setup Workflow Ordering
The service environment setup skill SHALL present the Topic Workspace setup workflow as source-gate analysis, repo acquisition or verification, dependency inference, derived-gate generation, Pixi installation, desired-command execution, and readiness verification in that order.

#### Scenario: Source gate is read before repo or Pixi decisions
- **WHEN** an agent starts Topic Workspace environment setup
- **THEN** the skill instructs the agent to read `<topic-workspace-dir>/user-intent/src/env-gate.md` before choosing repos, dependencies, Pixi install commands, setup commands, or verification commands
- **AND** the agent identifies what the user says must be runnable after setup

#### Scenario: Repos and dependencies are resolved before derived gate generation
- **WHEN** the source gate indicates that runnable repo code is needed
- **THEN** the skill resolves required repos under `<topic-workspace-dir>/repos/<repo-name>` before finalizing `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **AND** the skill infers dependencies from inspected repo files before finalizing the derived gate
- **AND** the derived gate may use inspected repo files to choose concrete Pixi install commands, Pixi run commands, scripts, imports, tools, and expected outputs
- **AND** any repo acquired from an inferred source is warning-labeled in the derived gate before readiness is reported

#### Scenario: Derived gate defines Pixi verification commands
- **WHEN** required repos are present or repo blockers are known
- **THEN** the skill instructs the agent to generate or update `isomer-env-gate.md` with Pixi install commands and Pixi run commands that verify the user-specified runnable target
- **AND** those Pixi commands are specific enough to run or inspect without reinterpreting the source gate

#### Scenario: Pixi readiness follows user-specified runnable target
- **WHEN** Pixi setup commands have completed
- **THEN** the skill verifies readiness using the Pixi commands and checks from `isomer-env-gate.md`
- **AND** readiness means the user-specified runnable target works, not merely that Pixi files exist
