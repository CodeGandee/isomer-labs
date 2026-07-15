## MODIFIED Requirements

### Requirement: Topic Workspace Repo Materialization
The service environment setup skill SHALL use semantic `topic.repos.*` targets for independent repositories required by the Topic Workspace task or environment gate, SHALL execute repository commands through the acting agent outside Isomer APIs, and SHALL register a missing repository only after external acquisition and verification succeed.

#### Scenario: Required repos are rooted under the Topic Workspace
- **WHEN** the gate or task requires an independent repository
- **THEN** the skill instructs the agent to resolve an existing non-main `topic.repos.*` binding or query its non-mutating default target before external acquisition
- **AND** the skill treats `repos/extern/...` as the default non-main repository namespace under `isomer-default.v1`
- **AND** the skill does not place task repositories in the Project root, Agent Workspace, `.pixi/`, or another ad hoc location

#### Scenario: Derived gate records repo requirements
- **WHEN** the source gate implies that runnable repository code is needed
- **THEN** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` lists the required repository names
- **AND** it lists each expected semantic `topic.repos.*` label and registered or candidate repository path
- **AND** it records the requested and resolved acquisition source when known, the externally selected acquisition method, and the verification requirements
- **AND** it records commands, scripts, imports, or equivalent checks that verify each repo is usable

#### Scenario: User supplies repository commands
- **WHEN** the user supplies exact commands or a custom source-control procedure for a required repository
- **THEN** the skill instructs the acting agent to run those commands outside `isomer-cli` under the applicable Gate and resource constraints
- **AND** it does not replace them with a fixed clone depth, checkout, fetch, provider, staging, retry, or cleanup strategy

#### Scenario: Missing repo is acquired when enough source information exists
- **WHEN** a required repository has no verified checkout at its registered or candidate non-main `topic.repos.*` path
- **AND** the gate or task provides enough source information to acquire it safely
- **THEN** the skill instructs the acting agent to select and execute the applicable repository commands directly at the candidate path
- **AND** after success it requires source-identity verification and `project repos register` before treating a new checkout as canonical
- **AND** it records evidence from the registered repository before reporting readiness

#### Scenario: Missing repo source may be inferred
- **WHEN** a required repository has no verified checkout at its registered or candidate non-main `topic.repos.*` path
- **AND** the gate or task implies runnable repository code is needed without naming an explicit source
- **THEN** the skill may instruct the agent to infer and search for a likely source, then select and run external acquisition commands only after the candidate is sufficiently supported
- **AND** the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` includes a visible warning in `Inferred Source Warnings` that the repository source was inferred rather than explicitly provided by the user
- **AND** the warning names the repo, semantic label, candidate path, inferred source, reason for choosing it, acquisition method, and any uncertainty or review needed
- **AND** the final skill output reports the same warning

#### Scenario: Missing repo blocks readiness when source remains ambiguous
- **WHEN** a required repository is absent from its registered or candidate non-main `topic.repos.*` path
- **AND** the gate, task, and agent source inference do not identify a likely source that can be verified against the desired command
- **THEN** the skill reports a blocker instead of executing speculative acquisition commands or claiming the Topic Workspace environment is ready
- **AND** the blocker names the missing repo requirement, semantic label, candidate path, and required clarification

#### Scenario: External acquisition or verification fails
- **WHEN** a repository command fails, leaves partial content, or produces an identity that does not match the accepted source
- **THEN** the skill records sanitized commands, the observed filesystem posture, impact, and a safe resume condition
- **AND** it does not create a successful semantic binding or ask an Isomer API to clean up the result

#### Scenario: Repo checks drive readiness
- **WHEN** the derived gate requires one or more repositories
- **THEN** readiness requires each repository to have a valid `topic.repos.*` binding, an existing canonical path, verified source identity, and passing checks from the derived gate
- **AND** missing registration, failed verification, and failed checks are explicit blockers

#### Scenario: Repo materialization keeps Pixi root stable
- **WHEN** a required repo has its own project files, install commands, or run commands
- **THEN** the Topic Workspace remains the standalone Pixi environment root
- **AND** repo-specific commands may run from the resolved repository path only as acquisition, verification, checks, or setup steps defined by the derived gate and applicable authorization

#### Scenario: External topic repos are not primary worktree sources
- **WHEN** topic environment setup registers or verifies a non-main repository under `repos/extern/...`
- **THEN** the skill treats that repository as supporting topic-local code rather than the primary Topic Main Repository used for Agent Workspace worktrees
- **AND** the skill may inspect or modify it only when the gate or user authorizes that action

#### Scenario: External repo projection is materialized
- **WHEN** the target spec says a Canonical External Repository must be visible from topic-main
- **THEN** the service creates or validates a projection under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`
- **AND** it records projection metadata in `topic.repos.main.projections.manifest`
