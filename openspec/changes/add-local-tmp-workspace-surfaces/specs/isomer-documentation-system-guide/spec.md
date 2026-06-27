## ADDED Requirements

### Requirement: Documentation Defines Local Tmp Surfaces
The documentation system SHALL describe standard tmp semantic labels, their default bindings, and the rule that they are local, ignored, disposable, and not shared.

#### Scenario: Topic Workspace definition lists tmp labels
- **WHEN** a reader opens the Topic Workspace definition
- **THEN** it lists `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` with local disposable meanings
- **AND** default directories are described only as `isomer-default.v1` bindings

#### Scenario: Documentation distinguishes tmp from sharing
- **WHEN** documentation explains worker visibility and collaboration paths
- **THEN** it states that `tmp/` is not Peer Read Access, not a generated link target, not owner-preserved records, and not Git-tracked collaboration material

#### Scenario: Documentation distinguishes tmp from scratch
- **WHEN** documentation explains `isomer-managed/agent-owned/scratch/`
- **THEN** it distinguishes agent-owned draft support from root `tmp/` disposable material
