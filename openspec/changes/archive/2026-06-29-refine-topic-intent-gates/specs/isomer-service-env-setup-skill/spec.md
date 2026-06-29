## ADDED Requirements

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

## MODIFIED Requirements

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

### Requirement: Topic Workspace Repo Materialization
The service environment setup skill SHALL use `<topic-workspace-dir>/repos/<repo-name>` as the location for independent repositories required by the Topic Workspace task or topic environment gate.

#### Scenario: Required repos are rooted under the Topic Workspace
- **WHEN** the gate or task requires an independent repository
- **THEN** the skill instructs the agent to find an existing repository or place a missing repository under `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the skill does not place task repositories in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location

#### Scenario: Derived gate records repo requirements
- **WHEN** the source gate implies that runnable repository code is needed
- **THEN** the generated `topic.env.topic_setup_target_spec` lists the required repository names
- **AND** it lists each expected `<topic-workspace-dir>/repos/<repo-name>` path
- **AND** it records the acquisition source when the source is known
- **AND** it records commands, scripts, imports, or equivalent checks that verify each repo is usable

#### Scenario: Missing repo is acquired when enough source information exists
- **WHEN** a required repository is missing from `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the gate or task provides enough source information to acquire it through service-safe operations
- **THEN** the skill instructs the agent to download or materialize the repository under `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the skill records evidence from the repository at that expected path before reporting readiness

#### Scenario: Missing repo source can be inferred
- **WHEN** a required repository is missing from `<topic-workspace-dir>/repos/<repo-name>`
- **AND** the gate or task implies runnable repository code is needed without naming an explicit source
- **THEN** the skill SHALL either instruct the agent to infer, search for, and acquire a likely repository source under `<topic-workspace-dir>/repos/<repo-name>` or report an uncertainty blocker
- **AND** the generated `topic.env.topic_setup_target_spec` includes a visible warning in `Inferred Source Warnings` that the repository source was inferred rather than explicitly provided by the user
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
- **AND** repo-specific commands are allowed to run from `<topic-workspace-dir>/repos/<repo-name>` only as checks or setup steps defined by the derived gate

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

### Requirement: Setup Workflow Ordering
The service environment setup skill SHALL present the Topic Workspace setup workflow as target-spec resolution, repo acquisition or verification, dependency inference or validation, Pixi installation, desired-command execution, and readiness verification in that order.

#### Scenario: Target spec is resolved before repo or Pixi decisions
- **WHEN** an agent starts Topic Workspace environment setup
- **THEN** the skill instructs the agent to resolve a derived topic env target spec before choosing repos, dependencies, Pixi install commands, setup commands, or verification commands
- **AND** that target spec comes from `topic.env.topic_setup_target_spec`, source-gate derivation, or explicit manual input

#### Scenario: Repos and dependencies are resolved before derived gate generation
- **WHEN** the source gate indicates that runnable repo code is needed
- **THEN** the skill resolves required repos under `<topic-workspace-dir>/repos/<repo-name>` before finalizing `topic.env.topic_setup_target_spec`
- **AND** the skill infers dependencies from inspected repo files before finalizing the derived gate
- **AND** the derived gate can use inspected repo files to choose concrete Pixi install commands, Pixi run commands, scripts, imports, tools, and expected outputs
- **AND** any repo acquired from an inferred source is warning-labeled in the derived gate before readiness is reported

#### Scenario: Target spec defines Pixi verification commands
- **WHEN** required repos are present, repo blockers are known, or an explicit target spec has already supplied repo decisions
- **THEN** the skill instructs the agent to use or update `isomer-env-gate.md` with Pixi install commands and Pixi run commands that verify the user-specified runnable target
- **AND** those Pixi commands are specific enough to run or inspect without reinterpreting the source gate

#### Scenario: Pixi readiness follows user-specified runnable target
- **WHEN** Pixi setup commands have completed
- **THEN** the skill verifies readiness using the Pixi commands and checks from `isomer-env-gate.md`
- **AND** readiness means the user-specified runnable target works, not merely that Pixi files exist

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
