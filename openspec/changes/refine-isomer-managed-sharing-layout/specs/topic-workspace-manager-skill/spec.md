## MODIFIED Requirements

### Requirement: Topic Workspace Git Layout
The topic workspace manager skill SHALL use `<topic-workspace-dir>/repos/topic-main` as the shared topic repository and `<topic-workspace-dir>/agents/<agent-name>` as each prepared Agent Workspace worktree.

#### Scenario: Workspace resolution uses Project Manifest
- **WHEN** `resolve-workspace` runs
- **THEN** it resolves Project root, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context instead of inferring a Topic Workspace by scanning directories

#### Scenario: Shared topic repo is placed under repos
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected repository path is `<topic-workspace-dir>/repos/topic-main`

#### Scenario: Isomer-managed namespace is placed inside topic-main
- **WHEN** `ensure-main-repo` creates or validates the shared topic repository
- **THEN** the expected Isomer worker-facing namespace is `<topic-workspace-dir>/repos/topic-main/isomer-managed`

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

#### Scenario: Agent Isomer-managed support directory is prepared
- **WHEN** a worktree is created or validated for agent name `alice`
- **THEN** the skill ensures the ignored support area `<topic-workspace-dir>/agents/alice/isomer-managed/` exists with the expected tracked, agent-owned, topic-owned, and link subpaths or reports why it could not be prepared

### Requirement: Profile and Packet Workspace Ref Updates
The topic workspace manager skill SHALL write or validate planned Agent Workspace refs in Topic Team Instantiation Packet or Topic Agent Team Profile material when requested by the operator workflow.

#### Scenario: Role binding receives workspace ref
- **WHEN** `plan-agents` maps an active role binding to agent name `alice`
- **THEN** the planned role binding `agent_workspace_ref` is `<topic-workspace-dir>/agents/alice` or an equivalent project-relative ref under the selected Topic Workspace

#### Scenario: Role binding receives agent name and branch plan
- **WHEN** `plan-agents` maps an active role binding to agent name `alice`
- **THEN** the skill reports or writes the topic-local agent name, branch `per-agent/alice/main`, and `isomer-managed/` support path as static setup evidence when the target material has fields for them

#### Scenario: Workspace refs are reported
- **WHEN** the skill completes planning or creation
- **THEN** its output reports role ids, agent names, Agent Workspace paths, branch names, `isomer-managed/` paths, and any profile or packet files changed

#### Scenario: Cross-topic workspace ref is rejected
- **WHEN** a planned role binding points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** the skill reports a blocker and does not treat the workspace plan as ready

### Requirement: Workspace Boundary and Summary Material
The topic workspace manager skill SHALL record advisory Workspace Boundary and summary material for prepared Git-backed Agent Workspaces.

#### Scenario: Boundary docs are written
- **WHEN** `write-boundaries` runs after worktree planning
- **THEN** it writes or updates topic-level and per-agent boundary material that names write ownership, Peer Read Access, branch rules, `isomer-managed/` tracked and untracked directories, generated links, and safe integration expectations

#### Scenario: Boundaries are advisory
- **WHEN** the boundary material describes Agent Workspace access
- **THEN** it states that Workspace Boundaries, Peer Read Access, owner/reader split, and generated links are advisory and are not filesystem-grade security isolation

#### Scenario: Summary is consumer neutral
- **WHEN** `summarize` runs
- **THEN** it reports the shared topic repository, every agent name, worktree path, current branch, expected branch namespace, `isomer-managed/` path status, boundary material path, validation status, blockers, and next operator action

### Requirement: Topic Workspace Manager Validation
The topic workspace manager skill SHALL validate prepared Git-backed workspace topology without repairing it silently.

#### Scenario: Validation checks Git topology
- **WHEN** `validate-worktrees` runs
- **THEN** it checks `topic-main`, expected worktree paths, expected current branches, duplicate branch checkouts, and branch namespace compliance

#### Scenario: Validation checks Isomer refs
- **WHEN** `validate-worktrees` has access to packet or profile material
- **THEN** it checks that active role binding `agent_workspace_ref`, agent name, branch name, and `isomer-managed/` support refs match prepared worktree paths for the selected Topic Workspace

#### Scenario: Validation checks Isomer-managed layout
- **WHEN** `validate-worktrees` runs against a prepared Topic Workspace
- **THEN** it reports missing `isomer-managed/.gitignore`, missing tracked subdirectories, missing agent-owned support directories, missing topic-owned projection directories, unsafe generated links, legacy `.isomer-agent/` paths, and legacy top-level worker collaboration directories without deleting or moving files

#### Scenario: Validation does not launch
- **WHEN** validation succeeds
- **THEN** the skill reports readiness of the Git-backed workspace layout without creating Agent Instances, registering Workspace Runtime records, launching agents, or invoking Execution Adapters

## ADDED Requirements

### Requirement: Isomer-Managed Sharing Preparation
The topic workspace manager skill SHALL prepare and validate the standard `isomer-managed/` sharing layout for the topic owner checkout and each Agent Workspace worktree.

#### Scenario: Tracked Isomer layout is prepared
- **WHEN** `ensure-main-repo` or `create-worktrees` prepares the Topic Main Repository layout
- **THEN** it creates or validates `isomer-managed/.gitignore` and `isomer-managed/tracked/{shared,artifacts,tasks,runs,views,tools,boundaries,manifests}/` without creating top-level Isomer collaboration directories in `topic-main`

#### Scenario: Agent-owned untracked layout is prepared
- **WHEN** `create-worktrees` prepares an Agent Workspace for agent name `alice`
- **THEN** it creates or validates `isomer-managed/agent-owned/{runtime,scratch,logs,artifacts,public,inbox}/` as ignored agent-owned material

#### Scenario: Topic-owned projection layout is prepared
- **WHEN** topic-owned non-Git material is configured for worker visibility
- **THEN** the skill creates or validates `isomer-managed/topic-owned/readonly/`, `isomer-managed/topic-owned/writable/`, and corresponding boundary policy before reporting the projection as ready

#### Scenario: Peer links are generated only when requested or configured
- **WHEN** the operator requests peer-readable convenience links or the workspace plan declares them
- **THEN** the skill creates links under `isomer-managed/links/peers/` to peer `isomer-managed/agent-owned/public/` paths and reports each link target

#### Scenario: Link creation is safe
- **WHEN** a requested generated link would point outside the selected Topic Workspace or into a forbidden owner-preserved root without an explicit projection policy
- **THEN** the skill reports a blocker and does not create the link

### Requirement: Isomer-Managed Conflict Diagnostics
The topic workspace manager skill SHALL report risky tracked Isomer material and untracked share ownership problems without trying to resolve them automatically.

#### Scenario: Tracked conflict markers are reported
- **WHEN** validation finds unresolved Git conflict markers under `isomer-managed/tracked/`
- **THEN** it reports the affected paths and does not mark the workspace layout ready

#### Scenario: Agent-owned reader writes are reported
- **WHEN** validation can determine that a peer wrote into another agent's `isomer-managed/agent-owned/public/` without an allowed policy
- **THEN** it reports an owner/reader split diagnostic and names the owning agent, reader agent, and affected path when known

#### Scenario: Topic-owned writable policy is required
- **WHEN** `isomer-managed/topic-owned/writable/` exists or is linked but boundary material does not state a write policy
- **THEN** validation reports a missing topic-owned writable policy diagnostic
