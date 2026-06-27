## ADDED Requirements

### Requirement: Local Tmp Path Labels
The system SHALL resolve standard local tmp labels through Workspace Path Resolution without treating them as durable runtime path truth.

#### Scenario: Topic Workspace tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for a selected Topic Workspace
- **THEN** the output includes `topic.tmp`
- **AND** under `isomer-default.v1` it resolves to `<topic-workspace>/tmp/`

#### Scenario: Topic Main Repository tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for the selected Topic Workspace's Topic Main Repository
- **THEN** the output includes `topic.main_repo.tmp`
- **AND** under `isomer-default.v1` it resolves under the resolved `topic.main_repo` path

#### Scenario: Agent Workspace tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for topic-local agent `alice`
- **THEN** the output includes `agent.tmp`
- **AND** under `isomer-default.v1` it resolves under the resolved `agent.workspace` path

#### Scenario: Tmp preview is not durable dependency approval
- **WHEN** a tmp label or path appears in Workspace Path Resolution output
- **THEN** downstream runtime records still must not depend on that path as durable state, evidence, handoff material, or Peer Read Access
