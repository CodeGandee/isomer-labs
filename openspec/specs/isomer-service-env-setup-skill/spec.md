# isomer-service-env-setup-skill Specification

## Purpose
Define the service skill that prepares Topic Workspace Pixi environments from user intent gates.
## Requirements
### Requirement: Command-Style Subcommand Structure
The service environment setup skill SHALL be structured as a single command-style skill with short kebab-case subcommands, a lean top-level router, and linked executable reference pages.

#### Scenario: Entrypoint routes by subcommand
- **WHEN** an agent invokes `isomer-srv-topic-env-setup`
- **THEN** the top-level `SKILL.md` instructs the agent to select one subcommand from a grouped `Subcommands` section
- **AND** the top-level workflow loads the selected subcommand's reference page and executes that page's `## Workflow`
- **AND** if no prompt is given, the skill defaults to `help`
- **AND** if a concrete setup task is given without a subcommand, the skill defaults to `setup-topic-env`

#### Scenario: Subcommands are grouped for complex skill use
- **WHEN** the skill lists subcommands
- **THEN** it divides them into Procedural Subcommands, Helper Subcommands, and Misc Subcommands
- **AND** Procedural Subcommands include `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate`
- **AND** Misc Subcommands include `help` and `setup-topic-env`
- **AND** Helper Subcommands may explicitly state that no helper subcommands are currently exposed
- **AND** each subcommand name is short kebab-case

#### Scenario: Topic environment setup orchestrates the full workflow
- **WHEN** the `setup-topic-env` subcommand runs
- **THEN** it orchestrates `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` in order
- **AND** it reports the combined result through the parent skill output contract

#### Scenario: Setup mode is selected from prompt
- **WHEN** the `setup-topic-env` subcommand is invoked
- **THEN** the skill selects `fast-forward` mode when the prompt asks for `fast-forward`, `fast-foward`, `auto`, `automatic`, or equivalent direct execution
- **AND** the skill selects `step-by-step` mode when the prompt asks for `step-by-step`, `manual`, `interactive`, confirmation, or equivalent user-controlled execution
- **AND** if the prompt gives a concrete setup task but no mode, the skill defaults to `fast-forward` mode unless the prompt asks to inspect, decide, or proceed carefully

#### Scenario: Fast-forward mode runs the ordered setup chain
- **WHEN** `setup-topic-env` runs in `fast-forward` mode
- **THEN** it executes `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` in order without pausing for optional user consent
- **AND** it still stops for blockers, missing required inputs, unsafe ambiguity, or out-of-scope requests

#### Scenario: Step-by-step mode asks consent before each step
- **WHEN** `setup-topic-env` runs in `step-by-step` mode
- **THEN** before each required workflow step it explains what is about to happen and why
- **AND** it presents choices in a table with columns for `Option`, `Explain`, and `Pros and Cons`
- **AND** it states the recommended option outside the table with the option name, reason, and why that option is recommended
- **AND** it waits for the user to choose an option before executing that step
- **AND** after executing the chosen action, it reports the result before offering the next step

#### Scenario: Step subcommands are directly callable
- **WHEN** a user or agent invokes `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, or `verify-env-gate` directly
- **THEN** the skill executes only that subcommand's workflow
- **AND** it refuses or blocks when predecessor artifacts required by that subcommand are missing

#### Scenario: Executable subcommand pages follow the style format
- **WHEN** a reference page acts as an executable subcommand page
- **THEN** it has a `## Required Inputs` section before its `## Workflow`
- **AND** the `## Required Inputs` section names the prompt inputs, predecessor artifacts, default paths, and refusal conditions needed by that subcommand
- **AND** direct callers can resolve that subcommand's inputs from that page without reading a central parent required-inputs table
- **AND** the top-level `SKILL.md` does not keep a central `## Required Inputs` table for executable setup behavior
- **AND** it has a `## Workflow` section near the top
- **AND** the workflow is written as numbered steps
- **AND** the workflow ends with a freeform fallback for tasks that do not map cleanly to the default steps

### Requirement: Topic Workspace Pixi Layout
The service skill SHALL prepare the selected Topic Workspace Pixi layout and baseline VCS ignores needed for topic-scoped environment setup.

#### Scenario: Topic Workspace VCS ignores preserve topic tmp posture
- **WHEN** Topic Workspace environment setup mutates the selected Topic Workspace
- **THEN** the owning Topic Workspace `.gitignore` ignores the default `topic.tmp` path
- **AND** it still preserves unrelated existing ignore entries

### Requirement: Environment Gate Verification
The service environment setup skill SHALL use a derived topic env target spec as the operational verification gate for Topic Workspace environment readiness. The target spec can come from `topic.env.topic_setup_target_spec`, derivation from `topic.intent.topic_env_requirements`, or explicit manual input.

#### Scenario: Source gate can derive target spec
- **WHEN** an agent uses `isomer-srv-topic-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to resolve `topic.intent.topic_env_requirements`
- **AND** the skill treats the resolved file as the source of user intent for deriving `topic.env.topic_setup_target_spec` when no explicit target spec is supplied

#### Scenario: Missing gate file blocks readiness only when no target spec is supplied
- **WHEN** `topic.intent.topic_env_requirements` is missing or unreadable
- **AND** no explicit derived topic env target spec is supplied
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** it asks for `resolve-topic-env-gate` to create or repair the source gate, or for the caller to provide an explicit target spec, before final readiness verification

#### Scenario: Legacy source gate path is not canonical
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` exists but `<topic-workspace-dir>/intent/src/topic-env-gate.md` is missing
- **THEN** the skill reports a legacy-path blocker naming `topic.intent.topic_env_requirements` and its default-layout path
- **AND** it does not silently treat the legacy file as the canonical source gate

#### Scenario: Derived gate is generated from source intent
- **WHEN** `topic.intent.topic_env_requirements` is present and readable
- **AND** no explicit derived topic env target spec is supplied
- **THEN** the skill instructs the agent to generate `topic.env.topic_setup_target_spec`
- **AND** the generated gate preserves the source gate's user intent while converting it into operational environment-readiness checks based on the user requirement and any required repo contents

#### Scenario: Target spec uses fixed Markdown sections
- **WHEN** the skill generates or accepts a derived topic env target spec
- **THEN** the target spec includes top-level sections named `Source Intent`, `Runnable Target`, `Repo Requirements`, `Inferred Source Warnings`, `Dependency Plan`, `Pixi Install Commands`, `Verification Commands`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Vague source gate is made operational
- **WHEN** the source gate is vague but understandable about what must be available or runnable after environment setup
- **THEN** the generated `isomer-env-gate.md` includes concrete required-to-succeed dependencies, Pixi install commands, Pixi run commands, scripts, imports, tools, expected outputs, or equivalent pass/fail checks
- **AND** it establishes success criteria that another agent can execute or inspect without reinterpreting the vague source wording

#### Scenario: Target spec contents drive post-setup checks
- **WHEN** the target spec describes tools, libraries, repos, datasets, commands, scripts, imports, or other runnable checks expected after setup
- **THEN** the skill uses the derived `isomer-env-gate.md` expectations to select or report dependency installation commands and verification commands after Pixi setup
- **AND** readiness is reported only when the gate expectations are satisfied or explicitly deferred with blockers

#### Scenario: Gate verification remains service-safe
- **WHEN** either gate file names checks that imply live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, research decision authority, or Topic Agent Team Profile materialization
- **THEN** the skill reports those parts as out-of-scope blockers or deferrals
- **AND** it verifies only the service-safe Topic Workspace environment setup portion

#### Scenario: Gate checklist records required readiness work
- **WHEN** the skill generates `topic.env.topic_setup_target_spec`
- **THEN** every required setup, repo, projection, dependency, resource, verification, expected-result, and blocker-resolution item needed for readiness is represented as a Markdown checkbox under `Gate Checklist`
- **AND** optional diagnostics or supporting smoke checks that are not required for readiness are recorded outside `Gate Checklist`

#### Scenario: Unchecked checklist item blocks readiness
- **WHEN** any required item under `Gate Checklist` remains unchecked after setup or verification
- **THEN** the skill does not report the Topic Workspace environment as ready
- **AND** it reports `blocked` when the item could not be run, `failed` when it ran and missed its expected result, or `not checked` only when verification was explicitly not requested
- **AND** it names the exact checklist item, reason, and next safe action in `Blockers`, `Execution Log`, or the final output

#### Scenario: Bounded real-path evidence can complete heavy checklist item
- **WHEN** a required checklist item names heavy work such as compilation, model inference, dataset processing, benchmark execution, large archive extraction, or a broad test suite
- **THEN** the skill may check the item only after a bounded real-path command exercises the same critical path named by the item and passes its expected result
- **AND** bounded real-path evidence may use reduced parallelism, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, or short benchmark cases

#### Scenario: Unrelated smoke test cannot complete critical checklist item
- **WHEN** a required checklist item names a critical build, inference, dataset, benchmark, or repo-specific runtime path
- **THEN** the skill does not mark that item checked merely because a weaker smoke test passed
- **AND** generic import success, device visibility, Pixi install success, repository inspection, or path existence counts only for a checklist item that specifically asks for that smoke evidence

#### Scenario: User downgrade is explicit evidence
- **WHEN** the user explicitly instructs the agent to accept a weaker check instead of the original critical-path checklist item
- **THEN** the skill records the user instruction, original checklist item, weaker evidence, and resulting limitation in the execution log or blocker record
- **AND** it does not silently present the weaker check as proof that the original critical path passed

### Requirement: Topic Workspace Repo Materialization
The service environment setup skill SHALL use resolved semantic `topic.repos.*` paths for independent repositories required by the Topic Workspace task or environment gate, defaulting non-main helper-created repositories under `<topic-workspace-dir>/repos/extern/<repo-label-path>`.

#### Scenario: Required repos are rooted under the Topic Workspace
- **WHEN** the gate or task requires an independent repository
- **THEN** the skill instructs the agent to resolve or register a non-main `topic.repos.*` label and find an existing repository or place a missing repository at that resolved path
- **AND** the skill treats `repos/extern/...` as the default non-main repository namespace under `isomer-default.v1`
- **AND** the skill does not place task repositories in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location

#### Scenario: Derived gate records repo requirements
- **WHEN** the source gate implies that runnable repository code is needed
- **THEN** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` lists the required repository names
- **AND** it lists each expected semantic `topic.repos.*` label and resolved repository path
- **AND** it records the acquisition source when the source is known
- **AND** it records commands, scripts, imports, or equivalent checks that verify each repo is usable

#### Scenario: Missing repo is acquired when enough source information exists
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the gate or task provides enough source information to acquire it through service-safe operations
- **THEN** the skill instructs the agent to download or materialize the repository at the resolved semantic path
- **AND** the skill records evidence from the repository at that expected path before reporting readiness

#### Scenario: Missing repo source may be inferred
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the gate or task implies runnable repository code is needed without naming an explicit source
- **THEN** the skill may instruct the agent to infer, search for, and acquire a likely repository source at the resolved semantic path
- **AND** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` includes a visible warning in `Inferred Source Warnings` that the repository source was inferred rather than explicitly provided by the user
- **AND** the warning names the repo, semantic label, expected path, inferred source, reason for choosing it, and any uncertainty or review needed
- **AND** the final skill output reports the same warning

#### Scenario: Missing repo blocks readiness when source remains ambiguous
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the gate, task, and agent source inference do not identify a likely source that can be verified against the desired command
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** the blocker names the missing repo requirement, semantic label, and expected resolved path

#### Scenario: Repo checks drive readiness
- **WHEN** the derived gate requires one or more repositories
- **THEN** readiness requires each expected repo path to exist
- **AND** readiness requires the repo checks from the derived gate to pass or be reported as explicit blockers

#### Scenario: Repo materialization keeps Pixi root stable
- **WHEN** a required repo has its own project files, install commands, or run commands
- **THEN** the Topic Workspace remains the standalone Pixi environment root
- **AND** repo-specific commands may run from the resolved repository path only as checks or setup steps defined by the derived gate

#### Scenario: External topic repos are not primary worktree sources
- **WHEN** topic environment setup acquires or verifies a non-main topic repository under `repos/extern/...`
- **THEN** the skill treats that repository as supporting topic-local code rather than the primary Topic Main Repository used for Agent Workspace worktrees
- **AND** the skill may inspect or modify it only when the gate or user authorizes that action

#### Scenario: External repo projection is materialized
- **WHEN** the target spec says a canonical external repository must be visible from topic-main
- **THEN** the service creates or validates a projection under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`
- **AND** it records projection metadata in `topic.repos.main.projections.manifest`

### Requirement: Dependency Inference and Pixi Execution
The service environment setup skill SHALL instruct the agent to infer the dependencies needed for `topic.intent.topic_env_requirements` to pass, install those dependencies with Pixi, and run the desired command through the Topic Workspace Pixi environment.

#### Scenario: Dependencies are inferred from source gate and repo contents
- **WHEN** the source gate and any required repos are available
- **THEN** the skill instructs the agent to infer the language runtimes, libraries, tools, package-manager requirements, editable repo installs, and command-line programs needed for the gate to pass
- **AND** the inferred dependencies are recorded in `topic.env.topic_setup_target_spec`

#### Scenario: Python packages prefer PyPI
- **WHEN** the inferred dependency is a Python package
- **AND** the package can satisfy the gate through PyPI
- **THEN** the skill instructs the agent to prefer a PyPI dependency over a Pixi/Conda package
- **AND** the selected package source is recorded in `isomer-env-gate.md`

#### Scenario: Starter Python dependencies are included
- **WHEN** the skill prepares a Topic Workspace root environment
- **THEN** it includes starter Python dependencies `scipy`, `mdutils`, `ruff`, `mkdocs-material`, `mypy`, `attrs`, `omegaconf`, `imageio`, `matplotlib`, `jsonschema`, and `jinja2` through PyPI unless existing compatible constraints already provide them
- **AND** the starter dependencies and install command are recorded in `isomer-env-gate.md`
- **AND** inability to install a starter dependency is reported as a blocker

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

#### Scenario: Python version is recovered before fallback
- **WHEN** the skill selects the Topic Workspace Python runtime version
- **THEN** it first checks the prompt, `topic.intent.topic_env_requirements`, derived gate content, and inspected repo evidence for Python version constraints
- **AND** repo evidence includes Python metadata, requirement markers, runtime files, CI files, Dockerfiles, lockfiles, and setup notes when present
- **AND** the selected version and evidence are recorded in `isomer-env-gate.md`

#### Scenario: Unspecified Python version defaults to previous stable minor
- **WHEN** no Python version can be recovered from prompt, gate, or repo context
- **THEN** the skill instructs the agent to select the previous stable Python minor release relative to the latest stable Python release at execution time
- **AND** the skill does not hard-code a specific fallback Python version
- **AND** the selected fallback version is recorded in `isomer-env-gate.md`

#### Scenario: Conflicting Python version sources choose the highest target
- **WHEN** multiple prompt, gate, or repo sources provide conflicting Python version constraints
- **THEN** the skill instructs the agent to choose the highest Python minor version mentioned or required by those sources as the target
- **AND** it adapts environment-level requirements toward that target through compatible package releases, service-safe constraint changes, compatibility shims, or setup-command changes
- **AND** it does not mutate existing repo source files merely to force compatibility
- **AND** if service-safe adaptation is impossible, it reports a blocker naming the conflicting sources and attempted target version

### Requirement: Topic Env Gate Delegates Operation Classification
The service environment setup skill SHALL delegate setup and verification operation classification to `isomer-misc-bounded-run-tips` before deciding whether a topic env gate item needs a resource check plan.

#### Scenario: Derivation records classification evidence
- **WHEN** `derive-env-gate` converts source intent or an explicit target spec into `topic.env.topic_setup_target_spec`
- **THEN** it asks `isomer-misc-bounded-run-tips` to classify each setup or verification operation whose resource cost affects readiness planning
- **AND** the generated gate records classification source, classification result, reason, resource dimensions, and whether bounded guidance is required

#### Scenario: Heavy and unknown-risk classifications require bounded plan
- **WHEN** bounded-run tips classifies a topic env operation as `heavy` or `unknown-risk`
- **THEN** `derive-env-gate` includes a `Resource Check Plan` entry with bounded-run guidance, a bounded real-path command, expected result, and blocker condition
- **AND** the gate does not replace the source-intent operation with an unrelated smoke test

#### Scenario: Specific bounded run guidance is applied when available
- **WHEN** an operation classified as `heavy` or `unknown-risk` matches a bounded-run tips subcommand such as `cuda-compile`
- **THEN** `derive-env-gate` applies that subcommand's relevant guidance in the generated `Resource Check Plan`, `Verification Commands`, `Expected Results`, and `Gate Checklist`
- **AND** the gate records the matched skill and subcommand name as evidence for the resource decision
- **AND** the gate does not duplicate the full reference guide when only the selected probes, limits, and command are needed

#### Scenario: Generic best-effort plan is explicit when no recipe exists
- **WHEN** a topic env operation classified as `heavy` or `unknown-risk` has no matching `isomer-misc-bounded-run-tips` subcommand
- **THEN** `derive-env-gate` creates a generic bounded real-path plan that balances system resource utilization and crash prevention
- **AND** the gate records that the source is generic best-effort judgment
- **AND** the plan still exercises the source-intent build, inference, dataset, benchmark, or test path with bounded scope rather than replacing it with an unrelated smoke test

#### Scenario: Light classification can skip resource plan
- **WHEN** bounded-run tips classifies a topic env operation as `light`
- **THEN** `derive-env-gate` may record that no resource check plan is required for that operation
- **AND** the gate preserves the classification evidence and reason

#### Scenario: Topic env setup does not own heavy-operation list
- **WHEN** topic env setup documentation mentions examples of operations that may be resource-heavy
- **THEN** the documentation states that bounded-run tips owns the classification decision
- **AND** it does not make the example list the normative definition of heavy operation

#### Scenario: Install and verify enforce the derived bounded plan
- **WHEN** `install-topic-deps` or `verify-env-gate` encounters a command classified as `heavy` or `unknown-risk` in `topic.env.topic_setup_target_spec`
- **THEN** it uses the generated `Resource Check Plan` and matching checklist item as the execution contract
- **AND** it reports a blocker when classification evidence or the bounded-run plan is missing, ambiguous, unsafe, or cannot exercise the required path
- **AND** it does not mark readiness ready from an unrelated smoke test or an unrecorded full-scale command

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
- **AND** the command form is `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`
- **AND** the skill does not rely on activated shells or ambient Python environments
- **AND** the command results determine whether the derived topic env target spec has passed

#### Scenario: Dependency blockers are explicit
- **WHEN** the agent cannot infer or install a dependency needed for the gate to pass
- **THEN** the skill reports a blocker instead of claiming readiness
- **AND** the blocker names the missing dependency, why it is needed, and what information or manual action is required

### Requirement: Direct Topic Workspace Environment Mutation
The service environment setup skill SHALL allow direct, auditable mutation of the selected Topic Workspace Pixi environment and missing required topic repositories after the selected Topic Workspace and its effective Pixi binding are confirmed.

#### Scenario: Direct mutation is allowed after confirmation
- **WHEN** the user invokes `isomer-srv-topic-env-setup` for Topic Workspace environment setup
- **AND** the Project Manifest-declared Topic Workspace and effective Topic Workspace Pixi binding have been confirmed
- **THEN** the skill may instruct the agent to add dependencies, update `pixi.toml`, refresh `pixi.lock`, install packages, and run gate commands for that Topic Workspace
- **AND** it does not require a separate Service Request before performing those service-safe mutations

#### Scenario: Direct mutation remains scoped
- **WHEN** the skill performs direct setup mutation
- **THEN** the mutation scope is limited to the selected Topic Workspace Pixi environment and missing required repositories at resolved non-main `topic.repos.*` paths

#### Scenario: Existing topic repos are not mutated by ensure-topic-repos
- **GIVEN** a required repo path already exists at the resolved non-main `topic.repos.*` path
- **WHEN** `ensure-topic-repos` runs
- **THEN** it inspects the existing repo as read-only evidence
- **AND** it does not run `git pull`, switch branches, copy files into the repo, delete files from the repo, install packages into the repo, regenerate files in the repo, or otherwise mutate the repo
- **AND** if the existing repo is unsuitable for the gate, it reports a blocker instead of repairing the repo without explicit user authorization
- **AND** the skill does not mutate the Project-root Pixi environment, an Agent Workspace-specific environment, unrelated Workspace Runtime records, team-profile material, agent launch material, GUI state, or research decision artifacts

#### Scenario: Mutation output remains auditable in the response
- **WHEN** direct setup mutation changes files or runs commands
- **THEN** the skill reports changed environment files, commands run, readiness status, and blockers through the parent skill output contract
- **AND** changed environment files include `.gitignore` when the VCS ignore rules are added or refreshed
- **AND** it does not hide dependency or lockfile changes behind generic readiness language

#### Scenario: Existing external repos are not mutated by ensure-topic-repos
- **WHEN** `ensure-topic-repos` sees that a required repo path already exists at the resolved non-main `topic.repos.*` path
- **THEN** it inspects the existing repo as read-only evidence by default
- **AND** it does not run `git pull`, switch branches, copy files into the repo, delete files from the repo, install packages into it, regenerate files in it, or otherwise mutate it unless the target spec explicitly authorizes that repository mutation
- **AND** if the existing repo is unsuitable for the gate, it reports a blocker instead of repairing the repo without explicit authorization

### Requirement: Setup Workflow Ordering
The service environment setup skill SHALL present the Topic Workspace setup workflow as source-gate analysis, repo acquisition or verification, dependency inference, derived-gate generation, Pixi installation, desired-command execution, and readiness verification in that order.

#### Scenario: Source gate is read before repo or Pixi decisions
- **WHEN** an agent starts Topic Workspace environment setup
- **THEN** the skill instructs the agent to read `<topic-workspace-dir>/user-intent/src/env-gate.md` before choosing repos, dependencies, Pixi install commands, setup commands, or verification commands
- **AND** the agent identifies what the user says must be runnable after setup

#### Scenario: Repos and dependencies are resolved before derived gate generation
- **WHEN** the source gate indicates that runnable repo code is needed
- **THEN** the skill resolves required repositories through semantic non-main `topic.repos.*` labels before finalizing `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`
- **AND** the skill infers dependencies from inspected repo files before finalizing the derived gate

### Requirement: Service Routes Ad Hoc Environment Requests to Topic Manager
The service environment setup skill SHALL route ad hoc package mutation and package verification requests to `isomer-admin-topic-mgr` while preserving full gate-driven setup in the service.

#### Scenario: Ad hoc package install routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to add or repair packages for a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-admin-topic-mgr env-install-packages`
- **AND** it does not treat `install-topic-deps` as a competing public package-add entrypoint

#### Scenario: Ad hoc package update routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to update packages for a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-admin-topic-mgr env-update-packages`

#### Scenario: Ad hoc package removal routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to remove packages from a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-admin-topic-mgr env-remove-packages`

#### Scenario: Topic environment verification remains service compatible
- **WHEN** `isomer-admin-topic-mgr env-verify-topic` routes full gate-driven verification to this service
- **THEN** the service accepts the selected Research Topic, Topic Workspace, topic env target spec, semantic path expectations, and verification intent as ordinary setup or verification context
- **AND** it returns command evidence, changed paths, blockers, and next action without claiming actor, formal agent, or runtime launch readiness

#### Scenario: Full setup still uses install-topic-deps
- **WHEN** the service is executing the complete topic env setup workflow from source gate through derived gate verification
- **THEN** it may still run `install-topic-deps` as an internal procedural step
- **AND** it records Pixi install commands, Pixi run commands, setup evidence, verification evidence, skipped heavy checks, blockers, and next action as service output
- **AND** the derived gate may use inspected repo files to choose concrete Pixi install commands, Pixi run commands, scripts, imports, tools, and expected outputs
- **AND** any repo acquired from an inferred source is warning-labeled in the derived gate before readiness is reported

#### Scenario: Derived gate defines Pixi verification commands
- **WHEN** required repos are present or repo blockers are known
- **THEN** the skill instructs the agent to generate or update `isomer-env-gate.md` with Pixi install commands and Pixi run commands that verify the user-specified runnable target

#### Scenario: Temporary setup files stay local
- **WHEN** environment setup needs disposable intermediate files
- **THEN** the skill uses resolved `topic.tmp` or another explicitly temporary path
- **AND** it reports that the material is local, ignored, disposable, not shared, and not durable evidence

### Requirement: Topic Workspace Environment Setup Independence
The service environment setup skill SHALL treat Topic Workspace development environment readiness as independent from Topic Agent Team Profile material, Agent Team Instance records, agent roles, and agent count.

#### Scenario: Missing team profile does not block environment setup
- **WHEN** `isomer-srv-topic-env-setup` runs for a Project Manifest-backed Research Topic and Topic Workspace
- **AND** `<topic-workspace-dir>/team-profile/` is missing, incomplete, unapproved, or not materialized
- **THEN** the skill continues environment setup when the Topic Workspace, Pixi binding, source gate, repos, dependencies, and verification commands can be resolved
- **AND** it does not report missing team-profile material as an environment setup blocker

#### Scenario: Agent team structure is not requested as input
- **WHEN** `isomer-srv-topic-env-setup` resolves setup context
- **THEN** it does not ask for Domain Agent Team Template selection, Topic Agent Team Profile fields, Topic Team Instantiation Packet contents, Agent Team Instance ids, Agent Instance ids, Agent Workspace plans, agent roles, or number of agents
- **AND** readiness is based on the Topic Workspace environment gate rather than team structure

#### Scenario: Project diagnostics are classified by environment relevance
- **WHEN** a read-only Project validation or doctor command reports diagnostics that mention missing Topic Agent Team Profile material, missing Agent Team Instances, missing Agent Workspaces, roles, or launch readiness
- **THEN** `isomer-srv-topic-env-setup` reports those diagnostics as unrelated or downstream context
- **AND** it does not treat those diagnostics as blockers unless they also prevent Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification

#### Scenario: Single-agent runnable target is the setup model
- **WHEN** `isomer-srv-topic-env-setup` interprets `topic.intent.topic_env_requirements`
- **THEN** it frames readiness as whether one agent or operator can run the commands needed to conduct the research inside the selected Topic Workspace
- **AND** it does not require proof that a multi-agent team can be launched or coordinated

### Requirement: Service Setup Resolves Semantic Topic Surfaces
The service environment setup skill SHALL resolve semantic Topic Workspace surfaces before setup and report their labels, sources, and blockers.

#### Scenario: Service setup reports topic tmp label when available
- **WHEN** `topic.tmp` is available through Workspace Path Resolution
- **THEN** the service output includes `topic.tmp` as local ignored disposable setup posture
- **AND** it does not treat files under `topic.tmp` as durable changed files, readiness evidence, dependency plan inputs, verification logs, or blockers unless the content has been promoted to an approved durable path

#### Scenario: Temporary setup files stay local
- **WHEN** environment setup needs disposable intermediate files
- **THEN** the skill uses resolved `topic.tmp` or another explicitly temporary path
- **AND** it reports that the material is local, ignored, disposable, not shared, and not durable evidence

### Requirement: Service Setup Preserves Custom Topic Layouts
The service environment setup skill SHALL accept safe manifest-backed Topic Workspace layout bindings that differ from the default layout.

#### Scenario: Custom repo path is accepted
- **WHEN** the Topic Workspace Manifest binds setup repositories to safe project-local `topic.repos.*` paths that differ from `<topic-workspace>/repos/extern/<repo-label-path>`
- **THEN** the service uses those bindings for repository checks and setup evidence

#### Scenario: Custom gate root is accepted
- **WHEN** the Topic Workspace Manifest binds user intent gate surfaces to safe project-local paths
- **THEN** the service reads, derives, writes, and reports gate material through those bindings

### Requirement: Service Output Reports Semantic Evidence
The service environment setup skill SHALL report semantic path evidence in its output.

#### Scenario: Tmp is not durable service evidence
- **WHEN** the service reports changed files, setup commands, verification results, enclosure warnings, or next actions
- **THEN** files under resolved tmp labels are omitted from durable evidence unless they have been promoted to an approved durable path

### Requirement: Agent Workspace Environment Targets Require Explicit Scope
The service environment setup skill SHALL avoid implicit Agent Workspace setup unless the requested setup target includes explicit or inferred Effective Agent Context.

#### Scenario: Topic setup does not infer agent
- **WHEN** the service is preparing the Topic Workspace environment
- **THEN** it does not treat cwd inside an Agent Workspace as permission to mutate agent-specific environment files unless the requested setup target is agent-scoped

#### Scenario: Agent-scoped setup can use cwd inference
- **WHEN** a future accepted agent-scoped setup workflow requests an agent surface and cwd is inside a known Agent Workspace
- **THEN** the service may use Effective Agent Context inference to resolve agent-scoped semantic labels

#### Scenario: Cross-agent setup requires explicit selector
- **WHEN** service setup targets another agent's workspace surface
- **THEN** it requires an explicit Agent Name or Agent Instance selector rather than relying on the caller's cwd

### Requirement: Topic Env Setup Remains Topic Scoped
The Topic Workspace environment setup service SHALL remain responsible for Topic Workspace Pixi dependency readiness and SHALL NOT become the per-agent worktree setup workflow.

#### Scenario: Topic setup does not create agent worktrees
- **WHEN** `isomer-srv-topic-env-setup setup-topic-env` runs
- **THEN** it does not read or create `topic.intent.agent_env_requirements`
- **AND** it does not create Agent Workspace Git worktrees, per-agent branches, Agent Workspace boundary material, or `isomer-agent-env-gate.md`

#### Scenario: Topic setup output can be consumed downstream
- **WHEN** topic env setup reports readiness
- **THEN** its output and `topic.env.topic_setup_target_spec` are suitable predecessor evidence for `isomer-srv-agent-env-setup`

#### Scenario: Agent cwd failures route to downstream service
- **WHEN** the Topic Workspace env passes from the Topic Workspace root but a user asks whether it passes from every Agent Workspace cwd
- **THEN** the topic env setup skill routes or points to `isomer-srv-agent-env-setup` instead of claiming per-agent cwd readiness itself

### Requirement: Topic Env Gate Supports Agent-Cwd Consumption
The Topic Workspace environment setup service SHALL keep its derived env gate replayable enough for downstream per-agent cwd verification.

#### Scenario: Derived gate records replayable commands
- **WHEN** `derive-env-gate` writes `topic.env.topic_setup_target_spec`
- **THEN** verification commands use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`
- **AND** external runtime wiring is recorded explicitly rather than relying on ambient shell state

#### Scenario: Derived gate distinguishes cwd assumptions
- **WHEN** a verification command must run from the Topic Workspace root or a repo-specific cwd
- **THEN** the derived gate records that cwd assumption so downstream agent env setup can detect agent-cwd incompatibility instead of silently reusing the command

#### Scenario: Topic setup does not claim per-agent Pixi readiness
- **WHEN** topic setup reports `ready`
- **THEN** it claims only the selected Topic Workspace Pixi environment readiness for the topic-level gate
- **AND** it does not claim that every Agent Workspace cwd has passed unless separate `isomer-srv-agent-env-setup` evidence exists

### Requirement: Topic Env Setup Consumes Storage Contract
The service environment setup skill SHALL resolve setup file surfaces through Workspace Path Resolution before reading, writing, or reporting them.

#### Scenario: Topic env intent and target labels are resolved
- **WHEN** topic environment setup needs source intent or a derived target spec in the normal operator flow
- **THEN** it resolves `topic.intent.topic_env_requirements` and `topic.env.topic_setup_target_spec` through Workspace Path Resolution
- **AND** it reports the semantic labels, resolved paths, storage profiles, sources, source details, and diagnostics in service output

#### Scenario: Setup repo uses resolved semantic label
- **WHEN** topic environment setup checks or mutates the setup repository surface
- **THEN** it uses the resolved semantic label for that surface, reports source metadata, and does not assume `repos/topic-main` or another default physical path

#### Scenario: Custom setup surface is accepted
- **WHEN** `topic.intent.topic_env_requirements`, setup notes, or operator input names a valid `custom.*` semantic label for setup material
- **THEN** the service resolves that label, validates safety and storage-profile-derived traits, and uses the resolved path for the dependent setup step

#### Scenario: Unknown setup label blocks mutation
- **WHEN** setup material names a semantic label that Workspace Path Resolution cannot resolve
- **THEN** the service reports a setup blocker and does not create a guessed path

### Requirement: Topic Env Setup Reports Durable and Disposable Surfaces Separately
The service environment setup skill SHALL use storage-profile-derived lifecycle traits to distinguish durable setup evidence from disposable local material.

#### Scenario: Disposable custom label is not durable evidence
- **WHEN** a custom semantic label uses a `storage_profile` with disposable lifecycle
- **THEN** the service omits files under that label from durable readiness evidence unless they are promoted to an accepted durable semantic surface

#### Scenario: Durable custom label may carry setup evidence
- **WHEN** a custom semantic label uses a `storage_profile` with durable lifecycle and passes safety validation
- **THEN** the service may report files under that label as changed files or setup evidence with semantic label and source metadata

### Requirement: Topic Env Setup Stops at Topic Workspace Readiness
The service environment setup skill SHALL treat Topic Workspace Pixi readiness as its final readiness boundary and SHALL NOT own Agent Workspace cwd readiness.

#### Scenario: Topic setup reports predecessor evidence
- **WHEN** `isomer-srv-topic-env-setup` completes `setup-topic-env` or `verify-env-gate`
- **THEN** it reports Topic Workspace predecessor evidence including the resolved Topic Workspace, Topic Workspace Pixi binding, source `env-gate.md`, derived `isomer-env-gate.md`, dependency and enclosure records, topic-root verification status, commands run, changed files, blockers, and next action
- **AND** it does not report `overall_readiness_status`, `readiness_by_agent`, Agent Names, Agent Workspace paths, or `isomer-agent-env-gate.md` evidence

#### Scenario: Agent gate files are outside topic setup
- **WHEN** `isomer-srv-topic-env-setup` is invoked for Topic Workspace setup or verification
- **THEN** it does not read `user-intent/src/agent-env-gate.md`
- **AND** it does not create or update `user-intent/derived/isomer-agent-env-gate.md`
- **AND** it does not verify commands from any resolved `agent.workspace` cwd

#### Scenario: Per-agent readiness is a follow-up, not a topic setup call
- **WHEN** topic setup output needs to mention per-Agent Workspace readiness
- **THEN** it states that per-agent readiness is not checked by `isomer-srv-topic-env-setup`
- **AND** it may name `isomer-srv-agent-env-setup` as an operator follow-up only when the caller requested per-agent proof or launch-facing Agent Workspace readiness
- **AND** it does not present the follow-up as a topic env setup subcommand, delegated call, or readiness dependency

### Requirement: Topic Env Process Graph Does Not Show Downstream Agent Readiness Ownership
The service environment setup skill SHALL be represented in process graphs as producing Topic Workspace predecessor evidence, not as calling Agent Workspace readiness setup.

#### Scenario: Topic env to agent env edge is absent
- **WHEN** the Topic Team Specialization process documentation describes top-level skill-to-skill call paths
- **THEN** it does not include a normal call path from `isomer-srv-topic-env-setup` to `isomer-srv-agent-env-setup`
- **AND** any note about per-agent readiness describes it as a caller or operator decision outside topic env setup

#### Scenario: Repair edge remains agent-owned
- **WHEN** a process graph includes the relationship between `isomer-srv-agent-env-setup` and `isomer-srv-topic-env-setup`
- **THEN** it represents the repair route as `isomer-srv-agent-env-setup` requiring or routing missing or stale Topic Workspace environment predecessor evidence back to `isomer-srv-topic-env-setup`

### Requirement: Topic Env Source Intent is High Level
The service environment setup skill SHALL treat `topic.intent.topic_env_requirements` as high-level user-editable source intent and SHALL place operational setup detail in `topic.env.topic_setup_target_spec`. In the normal operator flow those surfaces are resolved through Workspace Path Resolution; manual service invocation can supply an explicit target spec file, prompt, or context.

#### Scenario: High-level tool requirement is valid source intent
- **WHEN** `topic.intent.topic_env_requirements` says that a tool, library, repository, dataset, runtime, or capability must be available for the topic
- **THEN** the service treats that statement as sufficient source intent for deriving operational checks when the requirement is understandable
- **AND** it does not require the source file to name exact commands

#### Scenario: Commands belong in the derived gate
- **WHEN** the service derives Pixi install commands, verification commands, expected outputs, package-source choices, repo acquisition steps, or execution logs
- **THEN** it resolves `topic.env.topic_setup_target_spec` and writes those details to the resolved path
- **AND** it does not rewrite `topic.intent.topic_env_requirements` with generated implementation detail

### Requirement: Topic Env Target Spec Precedes Materialization
The service environment setup skill SHALL require a derived topic env target spec before it materializes Topic Workspace environment changes.

#### Scenario: Derived topic env target spec is the materialization input
- **WHEN** `setup-topic-env` runs from `topic.intent.topic_env_requirements`
- **THEN** it creates or updates `topic.env.topic_setup_target_spec` before installing dependencies, acquiring repositories, applying Pixi mutations, or running verification commands
- **AND** those materialization actions use the derived target spec as their execution contract

#### Scenario: Explicit topic env target spec is accepted
- **WHEN** `isomer-srv-topic-env-setup` is invoked manually with an explicit derived gate file, target-spec prompt, or target-spec context
- **THEN** it treats that input as the topic env target spec after checking that it is operational enough to drive service-safe materialization
- **AND** it records the target spec source in output
- **AND** it does not require `topic.intent.topic_env_requirements` solely because the invocation is manual

#### Scenario: Materialization blocks when target spec is missing
- **WHEN** the service cannot create, load, or validate a usable derived topic env target spec
- **THEN** it reports a blocker
- **AND** it does not materialize Topic Workspace environment changes from the high-level source intent alone

### Requirement: Topic Env Setup Uses Essential and Complete Output
The topic environment setup service skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential topic env output reports user-facing readiness
- **WHEN** `isomer-srv-topic-env-setup` reports a result without a complete-output request
- **THEN** it reports the selected topic, Topic Workspace, Pixi binding summary, readiness status, Topic Main Development Repository status, external repo projection summary, critical gate checklist result, important changed files, blockers, and next action
- **AND** it reports `per_agent_readiness_status: not checked` when Agent Workspace cwd readiness is relevant to the caller

#### Scenario: Complete topic env output preserves handoff detail
- **WHEN** complete output is requested from `isomer-srv-topic-env-setup`
- **THEN** it reports semantic paths, source and target spec labels and paths, path diagnostics, repo source details, dependency plan, enclosure records, operation classification evidence, resource probes, commands run, changed files, warnings, blockers, and next action

#### Scenario: Reference pages use parent output mode
- **WHEN** a topic env setup reference page reports through the parent output contract
- **THEN** it follows the parent skill's Essential Output by default and Complete Output on request

### Requirement: Topic Main Development Repository Setup
The Topic Workspace environment setup service SHALL create, configure, and verify the Topic Main Development Repository before downstream Agent Workspace setup consumes it.

#### Scenario: Missing main repository is initialized
- **WHEN** `topic.repos.main` resolves to a missing safe path, empty directory, or empty normal Git repository
- **THEN** topic env setup initializes or validates a normal non-bare Git repository
- **AND** it creates a topic-owner branch posture accepted by the target spec
- **AND** it prepares `topic.repos.main.isomer_managed` and the projection labels required by the target spec

#### Scenario: Existing main repository is reused
- **WHEN** `topic.repos.main` resolves to an existing normal non-bare Git repository
- **THEN** topic env setup reuses it without deleting, resetting, cleaning, recloning, pulling, or rewriting history
- **AND** it places Isomer-created material only under the resolved `topic.repos.main.isomer_managed` namespace unless the user explicitly authorizes another path

#### Scenario: Main repository readiness is predecessor evidence
- **WHEN** topic env setup reports ready or blocked status
- **THEN** its output includes Topic Main Development Repository readiness as predecessor evidence for Agent Workspace setup
- **AND** it does not claim per-Agent Workspace cwd readiness

### Requirement: Topic Env Gate Heavy Operations Use Bounded Run Tips First
The service environment setup skill SHALL require topic env gate derivation to consult `isomer-misc-bounded-run-tips` before inventing resource plans for heavy setup or verification work.

#### Scenario: Derivation routes heavy topic commands to bounded run tips first
- **WHEN** `derive-env-gate` converts source intent or an explicit target spec into `topic.env.topic_setup_target_spec`
- **AND** a setup or verification item involves compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, large GPU jobs, benchmark execution, or another resource-heavy operation
- **THEN** the generated `Resource Check Plan` identifies the operation as heavy
- **AND** the derivation first checks `isomer-misc-bounded-run-tips` for an applicable subcommand or recipe
- **AND** the generated gate records the selected bounded-run guidance source, probes, capacity signals, bounded command, expected result, and blocker condition

#### Scenario: Specific bounded run guidance is applied when available
- **WHEN** a heavy topic env operation matches a bounded-run tips subcommand such as `cuda-compile`
- **THEN** `derive-env-gate` applies that subcommand's relevant guidance in the generated `Resource Check Plan`, `Verification Commands`, `Expected Results`, and `Gate Checklist`
- **AND** the gate records the matched skill and subcommand name as evidence for the resource decision
- **AND** the gate does not duplicate the full reference guide when only the selected probes, limits, and command are needed

#### Scenario: Generic best-effort plan is explicit when no recipe exists
- **WHEN** a heavy topic env operation has no matching `isomer-misc-bounded-run-tips` subcommand
- **THEN** `derive-env-gate` creates a generic bounded real-path plan that balances system resource utilization and crash prevention
- **AND** the gate records that the source is generic best-effort judgment
- **AND** the plan still exercises the source-intent build, inference, dataset, benchmark, or test path with bounded scope rather than replacing it with an unrelated smoke test

#### Scenario: Install and verify enforce the derived bounded plan
- **WHEN** `install-topic-deps` or `verify-env-gate` encounters a required heavy command from `topic.env.topic_setup_target_spec`
- **THEN** it uses the generated `Resource Check Plan` and matching checklist item as the execution contract
- **AND** it reports a blocker when the bounded-run plan is missing, ambiguous, unsafe, or cannot exercise the required path
- **AND** it does not mark readiness ready from an unrelated smoke test or an unrecorded full-scale command

### Requirement: Service Skills Use Global Isomer CLI for Isomer Operations
Non-dev service skills SHALL use direct `isomer-cli` command examples for Isomer Project, Topic Workspace, path, runtime, and record operations.

#### Scenario: Service skill Isomer CLI examples omit pixi prefix
- **WHEN** validation scans `skillset/service/**`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** examples use `isomer-cli ...` directly

#### Scenario: Topic Workspace Pixi setup remains allowed
- **WHEN** a service skill describes installing or verifying a Topic Workspace Pixi environment
- **THEN** it may keep Pixi environment commands for the user's workspace
- **AND** it still must call Isomer control-plane operations through global `isomer-cli`
