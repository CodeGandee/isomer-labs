## ADDED Requirements

### Requirement: Approved Agent Workspace Ref Path Plans
Workspace Path Resolution SHALL allow approved role-binding `agent_workspace_ref` values to become recorded Agent Workspace path plans for the corresponding Agent Instance.

#### Scenario: Approved workspace ref becomes path plan
- **WHEN** Agent Team Instance creation processes an active role binding with a validated `agent_workspace_ref` under the selected Topic Workspace
- **THEN** the Agent Workspace path plan for the created Agent Instance uses that ref as the path

#### Scenario: Workspace ref source is recorded
- **WHEN** an Agent Workspace path plan is selected from `agent_workspace_ref`
- **THEN** the path plan records a source that identifies profile or packet material without storing unrelated profile contents inline

#### Scenario: Default path remains fallback
- **WHEN** an active role binding has no approved `agent_workspace_ref`
- **THEN** the resolver and runtime creation use the default Agent Workspace path under `<topic-workspace>/agents/<agent-instance-id>`

#### Scenario: Unsafe workspace ref is rejected
- **WHEN** an `agent_workspace_ref` points outside the Project root, outside the selected Topic Workspace, inside `.isomer-labs/`, or into another Agent Workspace where it would collide with an existing path plan
- **THEN** path validation rejects the ref before a dependent runtime record is written

### Requirement: Git-Backed Agent Workspace Subpaths
Workspace Path Resolution SHALL preserve the existing Agent Workspace subpath semantics when the Agent Workspace root comes from a Git-backed worktree path.

#### Scenario: Worktree root has agent subpaths
- **WHEN** an Agent Workspace root resolves to `<topic-workspace-dir>/agents/alice`
- **THEN** Agent Runtime, Agent Artifacts, Agent Scratch, and Agent Logs paths resolve under that root unless recorded path plans or supported environment overrides provide narrower subpaths

#### Scenario: Worktree path is not a separate Topic Workspace
- **WHEN** an Agent Workspace root resolves to a Git worktree under `<topic-workspace-dir>/agents/<agent-key>`
- **THEN** Workspace Path Resolution still treats it as an Agent Workspace inside the selected Topic Workspace, not as a Project or Topic Workspace
