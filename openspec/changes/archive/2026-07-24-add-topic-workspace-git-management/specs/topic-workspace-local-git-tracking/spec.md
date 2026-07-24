## ADDED Requirements

### Requirement: Local Mutations Require Workspace Runtime
The local tracking layer SHALL require an existing valid Workspace Runtime for init, ignore, and commit mutations while keeping status and plan inspection read-only.

#### Scenario: Local mutation is requested before runtime
- **WHEN** the Research Topic and Topic Workspace are registered but Workspace Runtime is unavailable
- **THEN** local status and planning may report the prerequisite
- **AND** local init, ignore, and commit perform no mutation

#### Scenario: Topic Git does not initialize runtime
- **WHEN** local mutation is blocked by missing Workspace Runtime
- **THEN** the skill reports the owning runtime initialization workflow
- **AND** it does not run an Isomer CLI runtime mutation command itself

### Requirement: Local Tracking Requires Explicit Initialization
The local layer SHALL initialize a Git repository at the Source Topic Workspace root only after explicit user intent and an approved mutation plan.

#### Scenario: Local init creates the root repository
- **WHEN** the user approves `local init` for a Source Topic Workspace that is not already a Git top level
- **THEN** the workflow initializes that root repository, applies the approved managed ignore block, and reports changed paths and Git state
- **AND** it does not add, configure, fetch, or push a remote

#### Scenario: Existing root repository is reused
- **WHEN** the Source Topic Workspace is already a valid Git top level
- **THEN** local init reports it as enabled and preserves its history, branches, index, remotes, and user configuration

#### Scenario: Unsafe existing Git state blocks initialization
- **WHEN** `.git` exists but is corrupt, points outside the accepted root, or conflicts with another worktree
- **THEN** local init reports a blocker and does not reinitialize, move, delete, or repair it implicitly

### Requirement: Local Initialization Requires Ignored Ancestor State
The local layer SHALL require the Source Topic Workspace to be untracked and effectively ignored by every ancestor Git repository before initialization.

#### Scenario: Ancestor repository safely ignores the workspace
- **WHEN** every ancestor Git repository reports that the Source Topic Workspace is absent from its index and effectively ignored
- **THEN** the ancestor-state prerequisite is satisfied

#### Scenario: Ancestor repository tracks topic content
- **WHEN** any Source Topic Workspace path is tracked in an ancestor Git repository
- **THEN** local init reports a blocker and does not initialize the nested repository or remove ancestor index entries

#### Scenario: Ancestor repository sees unignored topic content
- **WHEN** the Source Topic Workspace is untracked but is not effectively ignored by an ancestor Git repository
- **THEN** local init reports a blocker and does not edit the ancestor `.gitignore`

#### Scenario: No ancestor Git repository exists
- **WHEN** the Source Topic Workspace has no ancestor Git repository
- **THEN** the ancestor-state prerequisite is satisfied without an ignore requirement

### Requirement: Local Tracking Preserves Nested Workspace Topology
The local root repository SHALL leave Topic Main, canonical external repositories, Topic Actor Workspaces, and Agent Workspaces in their existing Git topology.

#### Scenario: Nested Git workspaces are excluded
- **WHEN** local ignore policy is prepared
- **THEN** it excludes the resolved Topic Main, canonical external repository, Topic Actor Workspace, and Agent Workspace roots from root-repository staging
- **AND** it does not add unconfigured gitlinks or `.gitmodules` entries

#### Scenario: Nested Git metadata is untouched
- **WHEN** local status, plan, ignore, or commit runs
- **THEN** it does not copy, absorb, reparent, initialize, clean, reset, or rewrite nested repository or worktree metadata

#### Scenario: Local version manifest records pointers only
- **WHEN** the operator approves a `topic-workspace-local-version.toml` update
- **THEN** it may record relative semantic labels, branch names, commit SHAs, and dirty-state booleans for nested workspaces
- **AND** it states that uncommitted nested content is not preserved by the root commit

### Requirement: Local Plans Select Exact Root Files
The local `plan` operation SHALL classify root-owned candidate paths and produce an exact whole-file local commit plan.

#### Scenario: Local plan is read-only
- **WHEN** local plan runs
- **THEN** it reports candidate root paths, tracked and ignored state, proposed ignore changes, exact files to stage, warnings, blockers, and proposed commit grouping
- **AND** it does not stage or modify files

#### Scenario: Known local-only surfaces default to ignore
- **WHEN** planning encounters Workspace Runtime, `state.sqlite`, local environments, caches, logs, tmp, credentials, nested workspaces, or canonical external repositories
- **THEN** it proposes exclusion unless the path has a narrower explicitly approved local use

#### Scenario: Secret-like local content is warned
- **WHEN** an exact local candidate contains secret-like material
- **THEN** planning reports the risk and requires explicit approval before local staging
- **AND** it does not expose the detected value in output or persisted state

### Requirement: Local Ignore Updates Preserve User Rules
The local `ignore` operation SHALL update only the approved Isomer-managed block in the Source Topic Workspace root `.gitignore`.

#### Scenario: Managed local ignore block is updated
- **WHEN** an approved current local plan contains ignore changes
- **THEN** the operation applies them idempotently and preserves user-authored content outside the managed block

#### Scenario: Tracked path is not hidden by ignore
- **WHEN** a proposed ignored path is already tracked
- **THEN** the operation reports that ignore rules do not remove tracked content
- **AND** it does not run `git rm --cached` or rewrite history implicitly

### Requirement: Local Commit Never Performs Remote Operations
The local `commit` operation SHALL stage and commit only exact approved root files and SHALL never contact a remote.

#### Scenario: Exact local commit succeeds
- **WHEN** the local plan is current, the index equals the approved scope, and no blocker remains
- **THEN** the operation creates the approved local commit and reports its SHA
- **AND** it performs no remote discovery, fetch, pull, push, or remote configuration

#### Scenario: Unexpected staged content blocks commit
- **WHEN** the index contains a path outside the approved local plan
- **THEN** local commit reports the unexpected staged content
- **AND** it does not commit, unstage, or discard it

#### Scenario: Publication state is irrelevant
- **WHEN** remote publication is disabled, blocked, stale, or copy-missing
- **THEN** a valid local commit remains allowed

### Requirement: Local Mutations Reject Stale Local Plans
Each local mutation SHALL recalculate root repository state and reject a local plan whose approved assumptions no longer match.

#### Scenario: Root state changed after local approval
- **WHEN** local HEAD, index, approved working-tree content, repository identity, or ignore file changes after plan approval
- **THEN** local ignore or commit reports the plan as stale and performs no further mutation

#### Scenario: Publication changed independently
- **WHEN** only the Topic Publication Copy or remote changes after local approval
- **THEN** the local plan remains current when its own Source Topic Workspace root state still matches
