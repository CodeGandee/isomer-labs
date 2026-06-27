## MODIFIED Requirements

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL delegate Git-backed Agent Workspace repository, worktree, and `isomer-managed/` preparation to `isomer-admin-topic-workspace-mgr` when a specialized topic team needs the `repos/topic-main` layout.

#### Scenario: Setup agent workspace delegates Git worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under `<topic-workspace-dir>/agents/<agent-name>`
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` rather than creating the worktrees itself

#### Scenario: Setup agent workspace delegates Isomer-managed setup
- **WHEN** `setup-agent-workspace` determines that per-agent worker-facing support paths, peer-readable large artifact paths, generated links, or boundary material are needed
- **THEN** it routes or instructs the operator to use `isomer-admin-topic-workspace-mgr` for `isomer-managed/` preparation rather than creating `.isomer-agent/` or top-level `topic-main` collaboration directories itself

#### Scenario: Static setup records delegated workspace refs
- **WHEN** delegated Git-backed workspace setup has completed
- **THEN** `setup-agent-workspace`, `validate-topic-team`, or `finalize-topic-team` may report the returned Agent Workspace paths, branch names, `isomer-managed/` paths, boundary docs, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Delegation preserves static boundary
- **WHEN** Topic Team Specialization delegates Git-backed workspace setup
- **THEN** it still does not create Agent Instances, mutate Workspace Runtime records, launch agents, or invoke Execution Adapters

#### Scenario: Missing delegated setup blocks static readiness
- **WHEN** the specialized topic team requires Git-backed Agent Workspaces and no successful topic workspace manager output exists
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker rather than claiming static material readiness

#### Scenario: Legacy support setup is not accepted as new readiness
- **WHEN** the only available workspace setup evidence names `.isomer-agent/` or top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` as the current standard layout
- **THEN** `validate-topic-team` reports stale workspace setup evidence and asks for `isomer-admin-topic-workspace-mgr` validation of the `isomer-managed/` layout
