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
The service environment setup skill SHALL read `<topic-workspace-dir>/user-intent/src/env-gate.md`, generate `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`, and use the derived gate as the operational verification gate for Topic Workspace environment readiness.

#### Scenario: Gate file is required for readiness verification
- **WHEN** an agent uses `isomer-srv-topic-env-setup` for a Topic Workspace environment
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
- **WHEN** either gate file names checks that imply live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, research decision authority, or Topic Agent Team Profile materialization
- **THEN** the skill reports those parts as out-of-scope blockers or deferrals
- **AND** it verifies only the service-safe Topic Workspace environment setup portion

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
- **THEN** it first checks the prompt, `env-gate.md`, derived gate content, and inspected repo evidence for Python version constraints
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
- **AND** the command results determine whether `env-gate.md` has passed

#### Scenario: Dependency blockers are explicit
- **WHEN** the agent cannot infer or install a dependency needed for the gate to pass
- **THEN** the skill reports a blocker instead of claiming readiness
- **AND** the blocker names the missing dependency, why it is needed, and what information or manual action is required

### Requirement: Direct Topic Workspace Environment Mutation
The service environment setup skill SHALL allow direct service-safe mutation of the selected Topic Workspace Pixi environment during an explicit setup invocation, without requiring a separate Service Request boundary.

#### Scenario: Setup invocation authorizes Topic Workspace Pixi mutation
- **WHEN** the user invokes `isomer-srv-topic-env-setup` for Topic Workspace environment setup
- **AND** the Project Manifest-declared Topic Workspace and effective Topic Workspace Pixi binding have been confirmed
- **THEN** the skill may instruct the agent to add dependencies, update `pixi.toml`, refresh `pixi.lock`, install packages, and run gate commands for that Topic Workspace
- **AND** it does not require a separate Service Request before performing those service-safe mutations

#### Scenario: Direct mutation remains scoped
- **WHEN** the skill performs direct setup mutation
- **THEN** the mutation scope is limited to the selected Topic Workspace Pixi environment and missing required repos under `<topic-workspace-dir>/repos/<repo-name>`

#### Scenario: Existing topic repos are not mutated by ensure-topic-repos
- **GIVEN** a required repo path already exists under `<topic-workspace-dir>/repos/<repo-name>`
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
- **THEN** `isomer-srv-topic-env-setup` MAY report those diagnostics as unrelated or downstream context
- **AND** it MUST NOT treat those diagnostics as blockers unless they also prevent Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification

#### Scenario: Single-agent runnable target is the setup model
- **WHEN** `isomer-srv-topic-env-setup` interprets `env-gate.md`
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

#### Scenario: Custom repo root is accepted
- **WHEN** the Topic Workspace Manifest binds setup repositories to a safe project-local path that differs from `<topic-workspace>/repos/<repo-name>`
- **THEN** the service uses that binding for repository checks and setup evidence

#### Scenario: Custom gate root is accepted
- **WHEN** the Topic Workspace Manifest binds user intent gate surfaces to safe project-local paths
- **THEN** the service reads, derives, writes, and reports gate material through those bindings

#### Scenario: Unsafe custom binding blocks setup
- **WHEN** a required semantic binding resolves outside the Project root, inside `.isomer-labs/`, or into another Topic Workspace without an accepted policy
- **THEN** the service reports a blocker and does not mutate setup files at that path

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
- **THEN** it does not read or create `user-intent/src/agent-env-gate.md`
- **AND** it does not create Agent Workspace Git worktrees, per-agent branches, Agent Workspace boundary material, or `isomer-agent-env-gate.md`

#### Scenario: Topic setup output can be consumed downstream
- **WHEN** topic env setup reports readiness
- **THEN** its output and `user-intent/derived/isomer-env-gate.md` are suitable predecessor evidence for `isomer-srv-agent-env-setup`

#### Scenario: Agent cwd failures route to downstream service
- **WHEN** the Topic Workspace env passes from the Topic Workspace root but a user asks whether it passes from every Agent Workspace cwd
- **THEN** the topic env setup skill routes or points to `isomer-srv-agent-env-setup` instead of claiming per-agent cwd readiness itself

### Requirement: Topic Env Gate Supports Agent-Cwd Consumption
The Topic Workspace environment setup service SHALL keep its derived env gate replayable enough for downstream per-agent cwd verification.

#### Scenario: Derived gate records replayable commands
- **WHEN** `derive-env-gate` writes `user-intent/derived/isomer-env-gate.md`
- **THEN** verification commands use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`
- **AND** external runtime wiring is recorded explicitly rather than relying on ambient shell state

#### Scenario: Derived gate distinguishes cwd assumptions
- **WHEN** a verification command must run from the Topic Workspace root or a repo-specific cwd
- **THEN** the derived gate records that cwd assumption so downstream agent env setup can detect agent-cwd incompatibility instead of silently reusing the command

#### Scenario: Topic setup does not claim per-agent Pixi readiness
- **WHEN** topic setup reports `ready`
- **THEN** it claims only the selected Topic Workspace Pixi environment readiness for the topic-level gate
- **AND** it does not claim that every Agent Workspace cwd has passed unless separate `isomer-srv-agent-env-setup` evidence exists

