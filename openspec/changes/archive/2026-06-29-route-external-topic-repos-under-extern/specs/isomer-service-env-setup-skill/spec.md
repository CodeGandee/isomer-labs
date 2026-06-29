## MODIFIED Requirements

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
- **AND** the derived gate may use inspected repo files to choose concrete Pixi install commands, Pixi run commands, scripts, imports, tools, and expected outputs
- **AND** any repo acquired from an inferred source is warning-labeled in the derived gate before readiness is reported

#### Scenario: Derived gate defines Pixi verification commands
- **WHEN** required repos are present or repo blockers are known
- **THEN** the skill instructs the agent to generate or update `isomer-env-gate.md` with Pixi install commands and Pixi run commands that verify the user-specified runnable target

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
