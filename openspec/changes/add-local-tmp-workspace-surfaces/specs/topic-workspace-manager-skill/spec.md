## ADDED Requirements

### Requirement: Topic Workspace Manager Prepares Local Tmp Surfaces
The topic workspace manager skill SHALL prepare and validate local tmp labels for the resolved Topic Main Repository owner checkout and each Agent Workspace worktree.

#### Scenario: Ensure main repo prepares tmp ignore
- **WHEN** `ensure-main-repo` creates or validates resolved `topic.main_repo`
- **THEN** it prepares or validates resolved `topic.main_repo.tmp` and a root `.gitignore` rule that ignores tmp material

#### Scenario: Create worktrees prepares agent tmp
- **WHEN** `create-worktrees` prepares resolved `agent.workspace` for `alice`
- **THEN** it prepares or validates resolved `agent.tmp` as an ignored local disposable directory

#### Scenario: Validate worktrees checks tmp contract
- **WHEN** `validate-worktrees` checks prepared Git-backed workspace topology
- **THEN** it reports missing tmp-label ignore policy, tracked tmp contents, or guidance that treats tmp material as shared material

#### Scenario: Summaries do not present tmp as shared
- **WHEN** the topic workspace manager summarizes prepared Agent Workspaces
- **THEN** it may list `topic.main_repo.tmp` and `agent.tmp` as local disposable surfaces but does not include them in Peer Read Access, generated links, handoff paths, or durable boundary material
