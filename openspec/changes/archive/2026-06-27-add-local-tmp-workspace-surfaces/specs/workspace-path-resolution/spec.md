## ADDED Requirements

### Requirement: Local Tmp Path Labels
Workspace Path Resolution SHALL resolve standard local tmp labels through the Topic Workspace Manifest/default-profile path model without treating them as durable runtime dependency approval.

#### Scenario: Topic Workspace tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for a selected Topic Workspace
- **THEN** the output includes `topic.tmp`
- **AND** under `isomer-default.v1` it resolves to `<topic-workspace>/tmp/`
- **AND** the output classifies the surface as disposable and non-shared

#### Scenario: Topic Main Repository tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for the selected Topic Workspace's Topic Main Repository
- **THEN** the output includes `topic.main_repo.tmp`
- **AND** under `isomer-default.v1` it resolves under the resolved `topic.main_repo` path
- **AND** the output classifies the surface as disposable and non-shared

#### Scenario: Agent Workspace tmp is previewed
- **WHEN** Workspace Path Resolution previews paths for topic-local Agent Name `alice`
- **THEN** the output includes `agent.tmp`
- **AND** under `isomer-default.v1` it resolves under the resolved `agent.workspace` path
- **AND** the output classifies the surface as disposable and non-shared

#### Scenario: Tmp preview is not durable dependency approval
- **WHEN** a tmp label or path appears in Workspace Path Resolution output
- **THEN** downstream runtime records, handoffs, Evidence Items, Decision Records, Provenance Records, profile material, and readiness reports still must not depend on that path as durable state, evidence, handoff material, or Peer Read Access

## MODIFIED Requirements

### Requirement: Compatibility Surface Mapping
Workspace Path Resolution SHALL preserve compatibility for existing internal path surface ids while presenting semantic labels as the public contract.

#### Scenario: Tmp compatibility ids map to semantic labels
- **WHEN** code requests compatibility ids such as `topic_tmp`, `topic_main_tmp`, or `agent_tmp`
- **THEN** the resolver maps those ids to `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp`
- **AND** it preserves disposable, non-shared classification in the returned path evidence

### Requirement: Manifest-backed Path Safety
Workspace Path Resolution SHALL apply the same canonicalization and safety checks to manifest-backed semantic paths as it applies to default and environment-derived paths.

#### Scenario: Unsafe tmp binding is rejected
- **WHEN** a manifest-backed tmp label resolves outside the Project root, inside `.isomer-labs/`, or into another Topic Workspace without an accepted policy
- **THEN** the resolver reports a validation diagnostic and does not return the tmp path as usable for dependent setup
