## MODIFIED Requirements

### Requirement: Git-Backed Agent Workspace Refs
Topic Agent Team Profile and Topic Team Instantiation Packet validation SHALL accept topic-local agent-name workspace plans as the primary representation of prepared Git-backed Agent Workspaces under the selected Topic Workspace, while treating `agent_workspace_ref` as derived compatibility material when present.

#### Scenario: Agent name identifies prepared worktree
- **WHEN** a role binding uses `agent_name = "alice"` with branch `per-agent/alice/main`
- **THEN** profile and packet validation treat `<topic-workspace-dir>/agents/alice` as the planned Agent Workspace path for the role binding

#### Scenario: Compatibility workspace ref may point to prepared worktree
- **WHEN** a role binding uses `agent_workspace_ref = "<topic-workspace-dir>/agents/alice"` or an equivalent project-relative ref under the selected Topic Workspace
- **THEN** profile and packet validation may accept it only after deriving the matching topic-local agent name and branch namespace

#### Scenario: Agent workspace ref must be topic scoped
- **WHEN** a role binding `agent_workspace_ref` points outside the selected Topic Workspace or into another Research Topic's Topic Workspace
- **THEN** profile or packet validation rejects the ref with a Topic Agent Team Profile isolation diagnostic

#### Scenario: Active role binding carries agent name path
- **WHEN** an active role binding maps to a topic-local agent name such as `alice`
- **THEN** the profile or packet may carry the path under `<topic-workspace-dir>/agents/alice` without requiring the future Agent Instance id to equal `alice`

#### Scenario: Workspace plan remains design-time material
- **WHEN** a Topic Agent Team Profile or packet contains agent-name workspace planning fields or compatibility `agent_workspace_ref`
- **THEN** validation does not create the Agent Workspace, create Agent Instances, create Workspace Runtime records, launch agents, or treat the workspace plan as live runtime state

### Requirement: Git-Backed Workspace Ref Completion
Launch-facing profile bundle validation SHALL report unresolved or mismatched Git-backed Agent Workspace plans before Agent Team Instance creation.

#### Scenario: Required workspace plans are resolved for launch-facing profile
- **WHEN** a launch-facing Topic Agent Team Profile Bundle requires Git-backed Agent Workspaces
- **THEN** validation confirms each active role binding has a resolved topic-scoped agent name, expected branch namespace, and Agent Workspace path or reports a launch blocker

#### Scenario: Mismatched prepared workspace is diagnostic
- **WHEN** profile or packet material names `agent_name = "alice"` but topic workspace manager validation reports that `<topic-workspace-dir>/agents/alice` is missing or bound to the wrong branch
- **THEN** launch-facing validation reports a blocker instead of treating the profile as ready for Agent Team Instance creation

#### Scenario: Legacy workspace ref without agent name is diagnostic
- **WHEN** profile or packet material only names `agent_workspace_ref` and validation cannot derive a safe topic-local agent name from it
- **THEN** launch-facing validation reports a workspace planning blocker instead of accepting the ref as complete
