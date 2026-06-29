## MODIFIED Requirements

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
- **AND** Procedural Subcommands include `resolve-topic-workspace`, `read-env-gate`, `derive-env-gate`, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, and `verify-env-gate`
- **AND** Misc Subcommands include `help` and `setup-topic-env`
- **AND** Helper Subcommands may explicitly state that no helper subcommands are currently exposed
- **AND** each subcommand name is short kebab-case

#### Scenario: Topic environment setup orchestrates the full workflow
- **WHEN** the `setup-topic-env` subcommand runs
- **THEN** it orchestrates target spec resolution or derivation before materialization
- **AND** it materializes the Topic Main Development Repository, canonical external repos, external repo projections, Pixi dependencies, and verification commands from the derived topic env target spec
- **AND** it reports the combined result through the parent skill output contract

#### Scenario: Setup mode is selected from prompt
- **WHEN** the `setup-topic-env` subcommand is invoked
- **THEN** the skill selects `fast-forward` mode when the prompt asks for `fast-forward`, `fast-foward`, `auto`, `automatic`, or equivalent direct execution
- **AND** the skill selects `step-by-step` mode when the prompt asks for `step-by-step`, `manual`, `interactive`, confirmation, or equivalent user-controlled execution
- **AND** if the prompt gives a concrete setup task but no mode, the skill defaults to `fast-forward` mode unless the prompt asks to inspect, decide, or proceed carefully

#### Scenario: Fast-forward mode runs the ordered setup chain
- **WHEN** `setup-topic-env` runs in `fast-forward` mode
- **THEN** it executes `resolve-topic-workspace`, `read-env-gate` when direct derivation is needed, `derive-env-gate` or target-spec validation, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, and `verify-env-gate` in order without pausing for optional user consent
- **AND** it still stops for blockers, missing required inputs, unsafe ambiguity, or out-of-scope requests

#### Scenario: Step-by-step mode asks consent before each step
- **WHEN** `setup-topic-env` runs in `step-by-step` mode
- **THEN** before each required workflow step it explains what is about to happen and why
- **AND** it presents choices in a table with columns for `Option`, `Explain`, and `Pros and Cons`
- **AND** it states the recommended option outside the table with the option name, reason, and why that option is recommended
- **AND** it waits for the user to choose an option before executing that step
- **AND** after executing the chosen action, it reports the result before offering the next step

#### Scenario: Step subcommands are directly callable
- **WHEN** a user or agent invokes a direct procedural subcommand
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

### Requirement: Topic Workspace Repo Materialization
The service environment setup skill SHALL use resolved semantic `topic.repos.*` paths for canonical external repositories and SHALL expose those repositories inside Topic Main Development Repository only through Isomer-managed projections.

#### Scenario: Required repos are rooted under the Topic Workspace
- **WHEN** the derived topic env target spec requires an independent repository
- **THEN** the skill resolves or registers a non-main `topic.repos.*` label and finds an existing repository or places a missing repository at that resolved path
- **AND** the skill treats `repos/extern/...` as the default non-main repository namespace under `isomer-default.v1`
- **AND** the skill does not place task repositories in the Project root, Agent Workspace, `.pixi/`, `repos/topic-main/extern/`, or another ad hoc location

#### Scenario: Derived gate records repo requirements
- **WHEN** the topic env target spec names runnable repository code
- **THEN** it lists each required repository name, expected semantic `topic.repos.*` label, canonical resolved repository path, projection access intent when needed, and acquisition source when known
- **AND** it records commands, scripts, imports, or equivalent checks that verify each repo is usable

#### Scenario: Missing repo is acquired when enough source information exists
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the target spec, prompt, or accepted source context provides enough source information to acquire it through service-safe operations
- **THEN** the skill downloads or materializes the repository at the resolved semantic path
- **AND** it records evidence from the repository at that expected path before reporting readiness

#### Scenario: Missing repo source may be inferred
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the target spec or source intent implies runnable repository code is needed without naming an explicit source
- **THEN** the skill may infer, search for, and acquire a likely repository source at the resolved semantic path
- **AND** the derived topic env target spec includes a visible warning in `Inferred Source Warnings`
- **AND** the final skill output reports the same warning

#### Scenario: External repo projection is materialized
- **WHEN** the target spec says a canonical external repository must be visible from topic-main
- **THEN** the service creates or validates a projection under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`
- **AND** it records projection metadata in `topic.repos.main.projections.manifest`

#### Scenario: Missing repo blocks readiness when source remains ambiguous
- **WHEN** a required repository is missing from its resolved non-main `topic.repos.*` path
- **AND** the target spec, task, and service-safe source inference do not identify a likely source that can be verified against the desired command
- **THEN** the skill reports a blocker instead of claiming Topic Workspace environment readiness
- **AND** the blocker names the missing repo requirement, semantic label, expected resolved path, and projection requirement when present

#### Scenario: Repo checks drive readiness
- **WHEN** the derived target spec requires one or more repositories or projections
- **THEN** readiness requires each expected canonical repo and projection path to exist or be explicitly blocked
- **AND** readiness requires the repo and projection checks from the derived gate to pass or be reported as blockers

#### Scenario: External topic repos are not primary worktree sources
- **WHEN** topic environment setup acquires, verifies, or projects a non-main topic repository under `repos/extern/...`
- **THEN** the skill treats that repository as supporting topic-local code rather than the Topic Main Development Repository used for Agent Workspace worktrees
- **AND** the skill may inspect or modify it only when the target spec or user authorizes that action

### Requirement: Direct Topic Workspace Environment Mutation
The service environment setup skill SHALL allow direct, auditable mutation of the selected Topic Workspace Pixi environment, Topic Main Development Repository setup surfaces, missing required external repositories, and Isomer-managed external repo projections after the selected Topic Workspace and effective Pixi binding are confirmed.

#### Scenario: Direct mutation is allowed after confirmation
- **WHEN** the user invokes `isomer-srv-topic-env-setup` for Topic Workspace environment setup
- **AND** the Project Manifest-declared Topic Workspace and effective Topic Workspace Pixi binding have been confirmed
- **THEN** the skill may add dependencies, update `pixi.toml`, refresh `pixi.lock`, install packages, create or validate `topic.repos.main`, create or validate Isomer-managed projection roots, acquire missing required external repos, create projections, and run gate commands for that Topic Workspace
- **AND** it does not require a separate Service Request before performing those service-safe mutations

#### Scenario: Direct mutation remains scoped
- **WHEN** the skill performs direct setup mutation
- **THEN** the mutation scope is limited to the selected Topic Workspace Pixi environment, the resolved Topic Main Development Repository Isomer-managed namespace, missing required repositories at resolved non-main `topic.repos.*` paths, and projection paths under `isomer-managed/topic-owned/{readonly,writable}/extern/`

#### Scenario: Existing external repos are not mutated by ensure-topic-repos
- **WHEN** `ensure-topic-repos` sees that a required repo path already exists at the resolved non-main `topic.repos.*` path
- **THEN** it inspects the existing repo as read-only evidence by default
- **AND** it does not run `git pull`, switch branches, copy files into the repo, delete files from the repo, install packages into it, regenerate files in it, or otherwise mutate it unless the target spec explicitly authorizes that repository mutation
- **AND** if the existing repo is unsuitable for the gate, it reports a blocker instead of repairing the repo without explicit authorization

#### Scenario: Mutation output remains auditable in the response
- **WHEN** direct setup mutation changes files or runs commands
- **THEN** the skill reports changed environment files, Topic Main Development Repository files, projection metadata, commands run, readiness status, and blockers through the parent skill output contract
- **AND** changed files include `.gitignore` or `extern-projections.toml` when those files are added or refreshed
- **AND** it does not hide dependency, lockfile, repository, or projection changes behind generic readiness language

## ADDED Requirements

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
