# local-tmp-workspace-surfaces Specification

## Purpose
TBD - created by archiving change add-local-tmp-workspace-surfaces. Update Purpose after archive.
## Requirements
### Requirement: Standard Local Tmp Labels
The system SHALL define `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as standard local disposable semantic surfaces.

#### Scenario: Topic Workspace tmp label exists as local disposable material
- **WHEN** a Topic Workspace layout is described, resolved, or prepared
- **THEN** `topic.tmp` is the standard topic-local disposable label
- **AND** under `isomer-default.v1` it binds to `<topic-workspace>/tmp/`

#### Scenario: Topic Main Repository tmp label exists as local disposable material
- **WHEN** the Topic Main Repository layout is described, resolved, or prepared
- **THEN** `topic.main_repo.tmp` is the standard disposable label for the owner checkout of the resolved Topic Main Repository
- **AND** under `isomer-default.v1` it binds to `<resolved topic.main_repo>/tmp/`

#### Scenario: Agent Workspace tmp label exists as local disposable material
- **WHEN** an Agent Workspace for topic-local Agent Name `alice` is described, resolved, or prepared
- **THEN** `agent.tmp` is the standard disposable label for that agent worktree
- **AND** under `isomer-default.v1` it binds to `<resolved agent.workspace>/tmp/`

### Requirement: Tmp Surfaces Are Always Ignored
The system SHALL require each resolved standard tmp label to be ignored by the nearest relevant Git ignore policy before a setup flow reports the related root as ready.

#### Scenario: Topic Workspace root ignores tmp
- **WHEN** the Topic Workspace root `.gitignore` is prepared or validated for `topic.tmp`
- **THEN** it contains an entry that ignores the resolved default `topic.tmp` path

#### Scenario: Topic Main Repository root ignores tmp
- **WHEN** the Topic Main Repository root `.gitignore` is prepared or validated for `topic.main_repo.tmp`
- **THEN** it contains an entry that ignores the resolved default `topic.main_repo.tmp` path

#### Scenario: Agent Workspace inherits topic-main tmp ignore
- **WHEN** an Agent Workspace is a Git worktree of the resolved `topic.main_repo`
- **THEN** its resolved `agent.tmp` path is ignored by the Topic Main Repository `.gitignore` rule for `tmp/`

#### Scenario: Tmp directories stay untracked
- **WHEN** a setup flow prepares a missing tmp directory
- **THEN** it does not add `.gitkeep`, tracked sentinels, or tracked placeholder files under the tmp path

### Requirement: Tmp Surfaces Are Not Shared
The system SHALL treat tmp surfaces as local, disposable, and non-shared material that must not be used for Peer Read Access, handoffs, evidence, Provenance Records, Workspace Runtime dependencies, profile material, or durable path truth.

#### Scenario: Tmp is rejected as peer sharing
- **WHEN** a workflow attempts to expose material under a resolved tmp path as Peer Read Access
- **THEN** validation reports that tmp is not a sharing surface and points to `agent.public_share`, approved `agent.topic_readonly` or `agent.topic_writable` projections, Git-tracked material, or owner-preserved records as appropriate

#### Scenario: Tmp is rejected as durable evidence
- **WHEN** a Workspace Runtime record, handoff, Provenance Record, Evidence Item, Decision Record, or downstream research claim depends on a file under a resolved tmp path
- **THEN** validation reports the dependency as non-durable and requires promotion before the record can be treated as ready

#### Scenario: Tmp is distinct from scratch
- **WHEN** documentation, CLI output, skill output, or validation distinguishes local surfaces
- **THEN** tmp is described as sweepable disposable material
- **AND** `agent.scratch` is described as agent-owned draft support material that still requires promotion before downstream records depend on it

