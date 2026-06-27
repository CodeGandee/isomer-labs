## ADDED Requirements

### Requirement: Semantic Workspace Manager Inputs
The topic workspace manager skill SHALL plan and report Topic Workspace Git layout through semantic labels and Topic Workspace Manifest bindings.

#### Scenario: Resolve workspace reports semantic labels
- **WHEN** `resolve-workspace` resolves the selected Topic Workspace
- **THEN** it reports semantic labels for Topic Main Repository, Agent Workspace root, Isomer-managed support namespace, records root, and runtime support root along with their resolved paths and sources

#### Scenario: Existing custom binding is honored
- **WHEN** the Topic Workspace Manifest binds `topic.main_repo` or `agent.workspace` to safe project-local paths that differ from the default layout
- **THEN** the skill uses those bindings for planning and validation instead of assuming the default paths

#### Scenario: Missing manifest uses default profile for planning
- **WHEN** the Topic Workspace Manifest is missing and the operator has not requested a custom layout
- **THEN** the skill plans against the built-in `isomer-default.v1` labels and reports that the paths come from the default profile

### Requirement: Default Layout Materialization
The topic workspace manager skill SHALL materialize default semantic workspace directories only when the operator asks for default creation.

#### Scenario: Default main repo is explicitly created
- **WHEN** the operator asks the skill to create default Topic Main Repository material
- **THEN** the skill creates or validates the `topic.main_repo` default binding and directory through the Topic Workspace Manifest contract

#### Scenario: Default agent worktrees are explicitly created
- **WHEN** the operator asks the skill to create Agent Workspace worktrees at default locations
- **THEN** the skill creates or validates `agent.workspace` default bindings for the planned Agent Names before creating the worktrees

#### Scenario: Read-only planning does not create manifest
- **WHEN** the skill runs `resolve-workspace`, `plan-agents`, `validate-worktrees`, or `summarize` without creation intent
- **THEN** it does not create or rewrite `topic-workspace.toml`, directories, branches, or worktrees

### Requirement: Semantic Agent Planning
The topic workspace manager skill SHALL plan Agent Names, branches, worktrees, and compatibility refs from semantic `agent.workspace` resolution.

#### Scenario: Planned agent path comes from semantic label
- **WHEN** `plan-agents` plans Agent Name `alice`
- **THEN** the planned Agent Workspace path is the resolved `agent.workspace` path for `alice`

#### Scenario: Compatibility workspace ref is derived from semantic path
- **WHEN** older packet or profile material still needs `agent_workspace_ref`
- **THEN** the skill derives the compatibility ref from the resolved `agent.workspace` path rather than assembling a default path directly

#### Scenario: Branch namespace remains agent scoped
- **WHEN** a semantic Agent Workspace path differs from the default layout
- **THEN** the planned branch still stays under `per-agent/<agent-name>/` unless a later accepted contract changes branch namespace semantics

#### Scenario: Cwd-friendly query guidance is included
- **WHEN** the skill writes Workspace Boundary or summary material for an Agent Workspace
- **THEN** it tells agents to use semantic path queries for their own agent-scoped surfaces from inside their Agent Workspace without requiring an Agent Name selector

### Requirement: Semantic Workspace Validation
The topic workspace manager skill SHALL validate Git-backed workspace topology against manifest-backed semantic labels.

#### Scenario: Validation checks manifest binding
- **WHEN** `validate-worktrees` checks a prepared Topic Main Repository or Agent Workspace
- **THEN** it verifies that the actual Git repository or worktree matches the resolved semantic binding for the selected Topic Workspace and Agent Name

#### Scenario: Custom path collision is a blocker
- **WHEN** a manifest binding points to an existing path that is not the expected repository or worktree for the requested semantic label
- **THEN** the skill reports a blocker and does not overwrite, reinitialize, delete, reset, or move the path

#### Scenario: Validation reports labels and paths
- **WHEN** validation completes
- **THEN** the output reports each checked semantic label, resolved path, source, readiness, blockers, and next operator action

### Requirement: Summary Uses Semantic Labels
The topic workspace manager skill SHALL summarize the workspace contract by semantic label first and default path second.

#### Scenario: Summary is label-first
- **WHEN** `summarize` runs
- **THEN** it reports semantic labels such as `topic.main_repo`, `agent.workspace`, `agent.private_artifacts`, and `agent.public_share` before showing concrete paths

#### Scenario: Default path is identified as default
- **WHEN** a path comes from `isomer-default.v1`
- **THEN** the summary identifies it as the default layout rather than presenting it as the only valid path
