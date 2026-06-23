## ADDED Requirements

### Requirement: Adapter Handoff Path Plans
The system SHALL resolve and record path plans for Houmao handoff payloads, observations, normalization artifacts, and logs before Workspace Runtime records depend on those files.

#### Scenario: Handoff payload root is topic scoped
- **WHEN** the Houmao adapter writes handoff dispatch payloads, mailbox payload copies, gateway payload copies, or command payloads
- **THEN** the payload root resolves under the selected Topic Workspace or an accepted Topic Workspace path plan

#### Scenario: Agent-scoped handoff files are agent scoped
- **WHEN** the adapter writes per-Agent Instance handoff payloads or observation files
- **THEN** the generated files resolve under the corresponding Agent Workspace or a recorded Agent Workspace path plan

#### Scenario: Path plans precede handoff files
- **WHEN** the adapter writes dispatch payloads, observation snapshots, normalization artifacts, mailbox metadata, gateway metadata, or adapter logs
- **THEN** Workspace Runtime records the semantic path plan and source before those files are referenced by handoff, Signal Observation, Artifact, or Provenance records

#### Scenario: Handoff payloads are not cache-like
- **WHEN** adapter handoff payloads, observations, normalization artifacts, or logs are written for a handoff round
- **THEN** the path plan or Artifact locator marks them as durable handoff evidence rather than cache-like generated material

#### Scenario: Adapter paths preserve source detail
- **WHEN** adapter paths come from supported `ISOMER_*` path overrides, Project Manifest defaults, Topic Workspace plans, or Agent Workspace plans
- **THEN** the stored path plans preserve source and source detail without storing unrelated environment values

#### Scenario: External handoff material is rejected by default
- **WHEN** a handoff payload, observation, normalization artifact, or log path resolves outside the Project root or selected Topic Workspace without an accepted external-root contract
- **THEN** validation rejects the path before downstream records depend on it

### Requirement: Adapter Observation and Log Paths
The system SHALL keep Houmao adapter observations, mailbox or gateway snapshots, normalization artifacts, and logs under recorded Workspace Runtime path plans.

#### Scenario: Observation snapshot path is planned
- **WHEN** adapter observation persists a mailbox, gateway, file, command, or inspection snapshot
- **THEN** the snapshot path is recorded as a path plan or Artifact locator before the snapshot is referenced by Workspace Runtime

#### Scenario: Normalization artifact path is planned
- **WHEN** Operator Agent normalization creates or retains an output Artifact, rejection rationale, repair payload, or follow-up handoff payload
- **THEN** the file path is recorded through Workspace Path Resolution before downstream diagnostics or research records depend on it

#### Scenario: Adapter log path is planned
- **WHEN** the Houmao adapter writes handoff dispatch, observe, normalize, mailbox, gateway, or diagnostic logs
- **THEN** the log path is recorded through Workspace Path Resolution before downstream diagnostics depend on it

#### Scenario: Missing adapter files remain visible
- **WHEN** an adapter handoff payload, observation snapshot, normalization artifact, or log path no longer exists
- **THEN** runtime validation reports the missing durable path without deleting the adapter, Artifact, Signal Observation, handoff, or Provenance refs
