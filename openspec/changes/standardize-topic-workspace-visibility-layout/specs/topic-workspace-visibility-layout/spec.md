## ADDED Requirements

### Requirement: Canonical Topic Workspace Visibility Layout
The system SHALL define a standard Topic Workspace layout that separates worker-visible Git collaboration surfaces, topic-owner preserved records, and runtime-internal material.

#### Scenario: Standard root layout is present
- **WHEN** a Topic Workspace is prepared with the standard layout
- **THEN** it contains `repos/topic-main`, `agents/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, `runtime/`, and `state.sqlite` as distinct semantic surfaces

#### Scenario: Worker collaboration lives in topic-main
- **WHEN** a file surface is intended to be visible to worker agents as normal collaboration material
- **THEN** that surface belongs inside `repos/topic-main` or one of its per-agent worktrees rather than as a root Topic Workspace directory

#### Scenario: Root records are owner preserved
- **WHEN** the topic owner, Operator Agent, Service Agent, runtime, or adapter preserves normalized Artifacts, task records, Run records, View Manifests, or logs outside the shared Git workflow
- **THEN** those files are written under `records/*` and are not treated as normal worker input

#### Scenario: Runtime internals are not worker collaboration
- **WHEN** Workspace Runtime, adapter payloads, launch material, inspection snapshots, or repair state are persisted for the topic
- **THEN** those files are stored through `state.sqlite`, `runtime/`, `records/*`, or recorded path plans without publishing them into worker-visible Git surfaces unless an explicit workflow promotes them

### Requirement: Agent Workspace Worktree Layout
The system SHALL use topic-local agent names to prepare per-agent Agent Workspaces as Git worktrees of `repos/topic-main`.

#### Scenario: Agent workspace path uses agent name
- **WHEN** an Agent Workspace is prepared for agent name `alice`
- **THEN** the standard path is `<topic-workspace>/agents/alice`

#### Scenario: Agent workspace is launch cwd
- **WHEN** an Execution Adapter launches or prepares a worker agent with a recorded Agent Workspace
- **THEN** the adapter uses the corresponding `agents/<agent-name>` worktree as the worker agent's current working directory

#### Scenario: Agent-local support is inside ignored support area
- **WHEN** agent-local runtime, scratch, temporary logs, symlink metadata, or recovery files are needed inside an Agent Workspace worktree
- **THEN** they are placed under an ignored `.isomer-agent/` support area unless a later accepted contract defines a different agent-local support root

#### Scenario: Agent instance id remains runtime identity
- **WHEN** Workspace Runtime creates or inspects an Agent Instance linked to an Agent Workspace
- **THEN** the Agent Instance id remains the globally unique runtime identity and does not need to match the topic-local agent name

### Requirement: Topic Workspace Branch Semantics
The system SHALL define deterministic branch namespaces for the topic-owner checkout and per-agent worktrees.

#### Scenario: Topic owner branch is named
- **WHEN** `repos/topic-main` is prepared as the owner-managed checkout
- **THEN** the expected owner branch is `topic-owner/main` unless the operator records an explicit alternative

#### Scenario: Default agent branch is named
- **WHEN** the standard Agent Workspace is prepared for agent name `alice`
- **THEN** the default branch is `per-agent/alice/main`

#### Scenario: Future agent branches stay under namespace
- **WHEN** an operator or agent creates a future branch named `experiment-1` for agent name `alice`
- **THEN** the branch name is `per-agent/alice/experiment-1`

#### Scenario: Cross-agent branch namespace is invalid
- **WHEN** a prepared Agent Workspace for agent name `alice` is checked out on a branch outside `per-agent/alice/`
- **THEN** validation reports a branch namespace diagnostic before treating the worktree as ready

### Requirement: Topic Collaboration Channels
The system SHALL define Git, approved symlinks, and topic-owned Pixi tasks as the supported worker collaboration channels.

#### Scenario: Git is primary communication
- **WHEN** worker agents need to share durable topic material with each other
- **THEN** the primary mechanism is Git operations across `repos/topic-main` and per-agent branches

#### Scenario: Symlinked shared dirs are secondary
- **WHEN** the topic owner provides symlinked shared directories inside an Agent Workspace
- **THEN** those symlinks live under `.isomer-agent/links/`, point to approved paths under `repos/topic-main`, and are reported as advisory convenience links

#### Scenario: Pixi tasks are tool mediated communication
- **WHEN** a worker agent needs topic-owned tools, scripts, or APIs that may read owner-preserved root state
- **THEN** the agent invokes an approved topic-owned Pixi task or wrapper rather than browsing root `records/`, `runtime/`, or `state.sqlite` directly

#### Scenario: Root browsing is not normal worker workflow
- **WHEN** worker-facing instructions, skills, or docs describe ordinary worker agent behavior
- **THEN** they keep the worker agent's normal operating surface inside its `agents/<agent-name>` worktree and its approved channels

### Requirement: Legacy Layout Diagnostics
The system SHALL detect old root collaboration surfaces and report migration guidance without deleting user files.

#### Scenario: Legacy root collaboration directories are reported
- **WHEN** validation finds root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` directories in a Topic Workspace
- **THEN** it reports them as legacy surfaces and explains whether their content should move to `repos/topic-main` or `records/*`

#### Scenario: Legacy agent workspace refs are reported
- **WHEN** profile, packet, runtime, or fixture material uses `agent-workspaces/`, `agents/<agent-instance-id>`, or arbitrary `agent_workspace_ref` paths as primary planning inputs
- **THEN** validation reports migration guidance toward topic-local agent names and `agents/<agent-name>` worktrees

#### Scenario: Validation is non-destructive
- **WHEN** legacy layout diagnostics are emitted
- **THEN** the system does not delete, move, reset, or rewrite the referenced files without explicit operator instruction
