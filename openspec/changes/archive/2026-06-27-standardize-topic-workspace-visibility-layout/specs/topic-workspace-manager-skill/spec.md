## MODIFIED Requirements

### Requirement: Topic Workspace Git Layout
The topic workspace manager skill SHALL use `<topic-workspace-dir>/repos/topic-main` as the shared topic repository and `<topic-workspace-dir>/agents/<agent-name>` as each prepared Agent Workspace worktree.

#### Scenario: Workspace resolution uses Project Manifest
- **WHEN** `resolve-workspace` runs
- **THEN** it resolves Project root, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context instead of inferring a Topic Workspace by scanning directories

#### Scenario: Shared topic repo is placed under repos
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected repository path is `<topic-workspace-dir>/repos/topic-main`

#### Scenario: Topic owner branch is prepared
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** it reports the owner-managed branch, normally `topic-owner/main`, and does not treat worker branches as the owner checkout

#### Scenario: Agent worktrees are placed under agents
- **WHEN** `create-worktrees` creates an Agent Workspace for agent name `alice`
- **THEN** the expected worktree path is `<topic-workspace-dir>/agents/alice`

#### Scenario: Existing unsafe repo blocks preparation
- **WHEN** `<topic-workspace-dir>/repos/topic-main` exists but is not a usable Git repository for worktree creation
- **THEN** the skill reports a blocker and does not delete, replace, pull, or reinitialize the existing path without explicit user instruction

### Requirement: Agent Planning and Branch Names
The topic workspace manager skill SHALL normalize per-agent names, map them to role bindings, and use deterministic per-agent branch namespaces.

#### Scenario: Agent names are path safe
- **WHEN** `plan-agents` resolves requested agent names
- **THEN** it rejects empty names, unsafe path segments, reserved names, and normalized name collisions before creating worktrees or updating workspace refs

#### Scenario: Default per-agent branch is deterministic
- **WHEN** `plan-agents` plans an Agent Workspace for agent name `alice`
- **THEN** the default branch is `per-agent/alice/main`

#### Scenario: Future per-agent branches stay under prefix
- **WHEN** `create-agent-branch` creates branch `experiment-1` for agent name `alice`
- **THEN** the branch name is `per-agent/alice/experiment-1`

#### Scenario: Cross-agent branch prefix is rejected
- **WHEN** an agent branch request for agent name `alice` names a branch outside `per-agent/alice/`
- **THEN** the skill rejects the branch request before mutating Git state

### Requirement: Worktree Creation Safety
The topic workspace manager skill SHALL create Git worktrees idempotently and refuse ambiguous or unsafe workspace topology.

#### Scenario: Worktree creation uses topic-main
- **WHEN** `create-worktrees` prepares an Agent Workspace for agent name `alice`
- **THEN** it creates a Git worktree of `<topic-workspace-dir>/repos/topic-main` at `<topic-workspace-dir>/agents/alice` on `per-agent/alice/main`

#### Scenario: Existing matching worktree is ready
- **WHEN** `<topic-workspace-dir>/agents/alice` already exists as a worktree of `topic-main` on `per-agent/alice/main`
- **THEN** the skill reports the worktree as ready instead of creating another worktree

#### Scenario: Existing nonmatching path blocks creation
- **WHEN** `<topic-workspace-dir>/agents/alice` exists but is not the expected worktree
- **THEN** the skill reports a blocker and does not overwrite the path

#### Scenario: Duplicate branch checkout is rejected
- **WHEN** `per-agent/alice/main` is already checked out in another worktree of `topic-main`
- **THEN** the skill reports a blocker and does not create a second worktree for the same branch

#### Scenario: Agent local support directory is prepared
- **WHEN** a worktree is created or validated for agent name `alice`
- **THEN** the skill ensures the ignored support area `<topic-workspace-dir>/agents/alice/.isomer-agent/` exists or reports why it could not be prepared

### Requirement: Profile and Packet Workspace Ref Updates
The topic workspace manager skill SHALL write or validate planned agent-name workspace fields in Topic Team Instantiation Packet or Topic Agent Team Profile material when requested by the operator workflow, while treating `agent_workspace_ref` as derived compatibility material.

#### Scenario: Role binding receives agent name plan
- **WHEN** `plan-agents` maps an active role binding to agent name `alice`
- **THEN** the planned role binding receives or reports `agent_name = "alice"`, branch `per-agent/alice/main`, and Agent Workspace path `<topic-workspace-dir>/agents/alice`

#### Scenario: Compatibility workspace ref is derived
- **WHEN** the target packet or profile schema still requires `agent_workspace_ref`
- **THEN** the skill derives `agent_workspace_ref` from the validated agent-name plan and reports that the field is compatibility material

#### Scenario: Workspace plans are reported
- **WHEN** the skill completes planning or creation
- **THEN** its output reports role ids, agent names, Agent Workspace paths, branch names, derived refs, and any profile or packet files changed

#### Scenario: Cross-topic workspace ref is rejected
- **WHEN** a planned role binding points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** the skill reports a blocker and does not treat the workspace plan as ready

### Requirement: Workspace Boundary and Summary Material
The topic workspace manager skill SHALL record advisory Workspace Boundary and summary material for prepared Git-backed Agent Workspaces.

#### Scenario: Boundary docs are written
- **WHEN** `write-boundaries` runs after worktree planning
- **THEN** it writes or updates topic-level and per-agent boundary material that names write ownership, Peer Read Access, branch rules, `.isomer-agent/` support directories, optional symlinked shared links, and safe integration expectations

#### Scenario: Boundaries are advisory
- **WHEN** the boundary material describes Agent Workspace access
- **THEN** it states that Workspace Boundaries, Peer Read Access, and symlinked shared directories are advisory and are not filesystem-grade security isolation

#### Scenario: Summary is consumer neutral
- **WHEN** `summarize` runs
- **THEN** it reports the shared topic repository, owner branch, every agent name, worktree path, current branch, expected branch namespace, optional symlinked shared links, boundary material path, validation status, blockers, and next operator action

### Requirement: Topic Workspace Manager Validation
The topic workspace manager skill SHALL validate prepared Git-backed workspace topology without repairing it silently.

#### Scenario: Validation checks Git topology
- **WHEN** `validate-worktrees` runs
- **THEN** it checks `topic-main`, owner branch, expected worktree paths, expected current branches, duplicate branch checkouts, and branch namespace compliance

#### Scenario: Validation checks Isomer refs
- **WHEN** `validate-worktrees` has access to packet or profile material
- **THEN** it checks that active role binding agent names, branch names, and derived `agent_workspace_ref` values match prepared worktree paths for the selected Topic Workspace

#### Scenario: Validation checks visibility layout
- **WHEN** `validate-worktrees` runs against a prepared Topic Workspace
- **THEN** it reports legacy root worker collaboration directories, missing `records/*` directories, missing `.isomer-agent/` support directories, and unsafe symlink targets without deleting or moving files

#### Scenario: Validation does not launch
- **WHEN** validation succeeds
- **THEN** the skill reports readiness of the Git-backed workspace layout without creating Agent Instances, registering Workspace Runtime records, launching agents, or invoking Execution Adapters
