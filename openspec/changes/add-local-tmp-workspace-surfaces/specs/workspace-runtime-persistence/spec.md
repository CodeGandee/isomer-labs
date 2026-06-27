## ADDED Requirements

### Requirement: Runtime Setup Handles Local Tmp Surfaces
The Workspace Runtime setup flow SHALL prepare or validate resolved standard tmp-label directories and ignore policies without making tmp material a durable dependency surface.

#### Scenario: Runtime init prepares Topic Workspace tmp
- **WHEN** Workspace Runtime initialization creates or verifies the selected Topic Workspace layout
- **THEN** it prepares or validates resolved `topic.tmp` and the owning Topic Workspace root ignore rule

#### Scenario: Agent Workspace setup prepares Agent tmp
- **WHEN** Agent Team Instance creation prepares an Agent Workspace directory for topic-local agent `alice`
- **THEN** it prepares or validates resolved `agent.tmp` and the Topic Main Repository ignore rule that keeps tmp material untracked

#### Scenario: Runtime validation reports durable tmp dependencies
- **WHEN** Workspace Runtime validation finds a runtime record, handoff, Artifact locator, Provenance Record, Evidence Item, or Decision Record that depends on a `tmp/` path
- **THEN** it reports a non-durable temporary path diagnostic and does not treat the referring record as ready until the material is promoted

#### Scenario: Runtime validation does not delete tmp
- **WHEN** Workspace Runtime validation finds files under a standard `tmp/` path
- **THEN** it does not delete, move, archive, or promote those files automatically
