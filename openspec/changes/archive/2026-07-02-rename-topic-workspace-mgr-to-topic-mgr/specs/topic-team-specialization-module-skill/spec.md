## MODIFIED Requirements

### Requirement: Git-Backed Agent Workspace Delegation
The Topic Team Specialization module skill SHALL delegate Git-backed Agent Workspace repository, worktree, and `isomer-managed/` preparation to the appropriate topic setup owner instead of creating worktrees itself.

#### Scenario: Setup agent workspace delegates Git worktree setup
- **WHEN** `setup-agent-workspace` determines that the selected topic team needs Git-backed Agent Workspaces under resolved `agent.workspace` paths
- **THEN** it routes per-agent worktree creation and cwd verification through `isomer-srv-agent-env-setup` after Topic Main Development Repository predecessor evidence exists
- **AND** it does not create the worktrees itself

#### Scenario: Optional topology support routes to topic manager
- **WHEN** the operator asks for read-only topology inspection, branch helper operations, boundary summaries, stale topology repair, manual compatibility operations, or legacy diagnostics
- **THEN** the skill may route that bounded work to `isomer-admin-topic-mgr` storage or team commands
- **AND** it records that evidence separately from topic env materialization and agent env readiness evidence

#### Scenario: Static setup records delegated workspace refs
- **WHEN** delegated Git-backed workspace setup has completed
- **THEN** `setup-agent-workspace`, `validate-topic-team`, or `finalize-topic-team` may report the returned Agent Workspace paths, branch names, `isomer-managed/` paths, boundary docs, validation refs, blockers, and next actions as static setup evidence

#### Scenario: Delegation preserves static boundary
- **WHEN** Topic Team Specialization delegates Git-backed workspace setup, topology inspection, or environment verification
- **THEN** it still does not create Agent Instances, mutate Workspace Runtime records, launch agents, or invoke Execution Adapters

#### Scenario: Missing delegated setup blocks static readiness
- **WHEN** the specialized topic team requires Git-backed Agent Workspaces and no successful delegated setup or verification output exists
- **THEN** `validate-topic-team` reports an Agent Workspace setup blocker rather than claiming static material readiness

#### Scenario: Legacy support setup is not accepted as new readiness
- **WHEN** the only available workspace setup evidence names `.isomer-agent/` or top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` as the current standard layout
- **THEN** `validate-topic-team` reports stale workspace setup evidence and asks for `isomer-admin-topic-mgr team-validate-workspaces` or the appropriate service verification

#### Scenario: Topic-main setup is not topic-manager work in the canonical path
- **WHEN** the normal topic-team setup path needs `topic.repos.main`
- **THEN** `isomer-admin-topic-team-specialize` gets that evidence through `setup-topic-env` and `isomer-srv-topic-env-setup`
- **AND** it does not route canonical Topic Main Development Repository creation to `isomer-admin-topic-mgr`
