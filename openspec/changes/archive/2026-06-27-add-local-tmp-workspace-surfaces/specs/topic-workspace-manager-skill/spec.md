## ADDED Requirements

### Requirement: Topic Workspace Manager Prepares Local Tmp Surfaces
The topic workspace manager skill SHALL prepare and validate local tmp labels for the resolved Topic Main Repository owner checkout and each Agent Workspace worktree.

#### Scenario: Ensure main repo prepares tmp ignore
- **WHEN** `ensure-main-repo` creates or validates resolved `topic.main_repo`
- **THEN** it prepares or validates resolved `topic.main_repo.tmp`
- **AND** it prepares or validates a root `.gitignore` rule that ignores tmp material

#### Scenario: Create worktrees prepares agent tmp
- **WHEN** `create-worktrees` prepares resolved `agent.workspace` for Agent Name `alice`
- **THEN** it prepares or validates resolved `agent.tmp` as an ignored local disposable directory
- **AND** it does not add tracked placeholder files under `agent.tmp`

#### Scenario: Validate worktrees checks tmp contract
- **WHEN** `validate-worktrees` checks prepared Git-backed workspace topology
- **THEN** it reports missing or ineffective tmp-label ignore policy, tracked tmp contents, or guidance that treats tmp material as shared or durable material

#### Scenario: Summaries do not present tmp as shared
- **WHEN** the topic workspace manager summarizes prepared Agent Workspaces
- **THEN** it may list `topic.main_repo.tmp` and `agent.tmp` as local disposable surfaces
- **AND** it does not include them in Peer Read Access, generated links, handoff paths, readiness evidence, or durable boundary material

## MODIFIED Requirements

### Requirement: Isomer-Managed Sharing Preparation
The topic workspace manager skill SHALL prepare and validate the standard `isomer-managed/` sharing layout for the topic owner checkout and each Agent Workspace worktree while keeping tmp surfaces outside sharing.

#### Scenario: Tmp is separate from isomer-managed sharing
- **WHEN** `ensure-main-repo` or `create-worktrees` prepares `isomer-managed/` layout
- **THEN** it keeps `topic.main_repo.tmp` and `agent.tmp` outside tracked Isomer material, agent-owned public shares, topic-owned projections, and generated links

### Requirement: Summary Uses Semantic Labels
The topic workspace manager skill SHALL summarize the workspace contract by semantic label first and default path second.

#### Scenario: Summary names tmp labels as local-only
- **WHEN** `summarize` reports tmp posture
- **THEN** it names semantic labels such as `topic.main_repo.tmp` and `agent.tmp`
- **AND** it identifies their default paths only as `isomer-default.v1` bindings
