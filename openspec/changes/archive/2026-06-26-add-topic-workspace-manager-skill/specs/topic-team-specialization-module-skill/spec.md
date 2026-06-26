## ADDED Requirements

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL delegate Git-backed Agent Workspace repository and worktree preparation to `isomer-admin-topic-workspace-mgr` when a specialized topic team needs the `repos/topic-main` layout.

#### Scenario: Setup agent workspace delegates Git worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under `<topic-workspace-dir>/agents/<agent-key>`
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` rather than creating the worktrees itself

#### Scenario: Static setup records delegated workspace refs
- **WHEN** delegated Git-backed workspace setup has completed
- **THEN** `setup-agent-workspace`, `validate-topic-team`, or `finalize-topic-team` may report the returned Agent Workspace paths, branch names, boundary docs, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Delegation preserves static boundary
- **WHEN** Topic Team Specialization delegates Git-backed workspace setup
- **THEN** it still does not create Agent Instances, mutate Workspace Runtime records, launch agents, or invoke Execution Adapters

#### Scenario: Missing delegated setup blocks static readiness
- **WHEN** the specialized topic team requires Git-backed Agent Workspaces and no successful topic workspace manager output exists
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker rather than claiming static material readiness
