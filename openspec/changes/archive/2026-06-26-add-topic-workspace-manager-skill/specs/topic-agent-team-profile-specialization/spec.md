## ADDED Requirements

### Requirement: Git-Backed Agent Workspace Refs
Topic Agent Team Profile and Topic Team Instantiation Packet validation SHALL accept and validate role-binding `agent_workspace_ref` values that identify prepared Git-backed Agent Workspaces under the selected Topic Workspace.

#### Scenario: Agent workspace ref may point to prepared worktree
- **WHEN** a role binding uses `agent_workspace_ref = "<topic-workspace-dir>/agents/alice"` or an equivalent project-relative ref under the selected Topic Workspace
- **THEN** profile and packet validation treat that ref as the planned Agent Workspace path for the role binding

#### Scenario: Agent workspace ref must be topic scoped
- **WHEN** a role binding `agent_workspace_ref` points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** profile or packet validation rejects the ref with a Topic Agent Team Profile isolation diagnostic

#### Scenario: Active role binding can carry agent key path
- **WHEN** an active role binding maps to a topic-local agent key such as `alice`
- **THEN** the profile or packet may carry the path under `<topic-workspace-dir>/agents/alice` without requiring the future Agent Instance id to equal `alice`

#### Scenario: Workspace ref remains design-time material
- **WHEN** a Topic Agent Team Profile or packet contains `agent_workspace_ref`
- **THEN** validation does not create the Agent Workspace, create Agent Instances, create Workspace Runtime records, launch agents, or treat the workspace ref as live runtime state

### Requirement: Git-Backed Workspace Ref Completion
Launch-facing profile bundle validation SHALL report unresolved or mismatched Git-backed Agent Workspace refs before Agent Team Instance creation.

#### Scenario: Required workspace refs are resolved for launch-facing profile
- **WHEN** a launch-facing Topic Agent Team Profile Bundle requires Git-backed Agent Workspaces
- **THEN** validation confirms each active role binding has a resolved topic-scoped `agent_workspace_ref` or reports a launch blocker

#### Scenario: Mismatched prepared workspace is diagnostic
- **WHEN** profile or packet material names `<topic-workspace-dir>/agents/alice` but topic workspace manager validation reports that path missing or bound to the wrong branch
- **THEN** launch-facing validation reports a blocker instead of treating the profile as ready for Agent Team Instance creation
