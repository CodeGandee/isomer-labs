## ADDED Requirements

### Requirement: Standard Local Tmp Labels
The system SHALL define `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as standard local disposable semantic surfaces.

#### Scenario: Topic Workspace tmp label exists as local disposable material
- **WHEN** a Topic Workspace layout is described or prepared
- **THEN** `topic.tmp` is the standard topic-local disposable label
- **AND** under `isomer-default.v1` it binds to `<topic-workspace>/tmp/`

#### Scenario: Topic Main Repository tmp label exists as local disposable material
- **WHEN** the Topic Main Repository layout is described or prepared
- **THEN** `topic.main_repo.tmp` is the standard disposable label for the owner checkout of the resolved Topic Main Repository
- **AND** under `isomer-default.v1` it binds to `<resolved topic.main_repo>/tmp/`

#### Scenario: Agent Workspace tmp label exists as local disposable material
- **WHEN** an Agent Workspace for topic-local agent `alice` is described or prepared
- **THEN** `agent.tmp` is the standard disposable label for that agent worktree
- **AND** under `isomer-default.v1` it binds to `<resolved agent.workspace>/tmp/`

### Requirement: Tmp Surfaces Are Always Ignored
The system SHALL require each resolved standard tmp label to be ignored by the nearest relevant Git ignore policy.

#### Scenario: Topic Workspace root ignores tmp
- **WHEN** the Topic Workspace root `.gitignore` is prepared or validated
- **THEN** it contains an entry that ignores the default `topic.tmp` path

#### Scenario: Topic Main Repository root ignores tmp
- **WHEN** the Topic Main Repository root `.gitignore` is prepared or validated
- **THEN** it contains an entry that ignores the default `topic.main_repo.tmp` path

#### Scenario: Agent Workspace inherits topic-main tmp ignore
- **WHEN** an Agent Workspace is a Git worktree of the resolved `topic.main_repo`
- **THEN** its resolved `agent.tmp` path is ignored by the Topic Main Repository `.gitignore` rule for `tmp/`

### Requirement: Tmp Surfaces Are Not Shared
The system SHALL treat `tmp/` as local, disposable, and non-shared material that must not be used for Peer Read Access, handoffs, evidence, Provenance Records, Workspace Runtime dependencies, or durable path truth.

#### Scenario: Tmp is rejected as peer sharing
- **WHEN** a workflow attempts to expose material under a `tmp/` path as Peer Read Access
- **THEN** validation reports that `tmp/` is not a sharing surface and points to `isomer-managed/agent-owned/public/`, `isomer-managed/topic-owned/`, Git-tracked material, or owner-preserved records as appropriate

#### Scenario: Tmp is rejected as durable evidence
- **WHEN** a Workspace Runtime record, handoff, Provenance Record, Evidence Item, Decision Record, or downstream research claim depends on a file under a `tmp/` path
- **THEN** validation reports the dependency as non-durable and requires promotion before the record can be treated as ready

#### Scenario: Tmp is distinct from scratch
- **WHEN** documentation or validation distinguishes local surfaces
- **THEN** `tmp/` is described as sweepable disposable material and `isomer-managed/agent-owned/scratch/` is described as agent-owned draft support material that still requires promotion before downstream records depend on it
