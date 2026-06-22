## ADDED Requirements

### Requirement: Adapter Launch Material Path Plans
The system SHALL resolve and record path plans for Houmao adapter launch material before generated files or Houmao launch behavior depend on those paths.

#### Scenario: Launch material root is topic scoped
- **WHEN** the Houmao adapter generates launch material for an Agent Team Instance
- **THEN** the launch material root resolves under the selected Topic Workspace or an accepted Topic Workspace path plan

#### Scenario: Agent launch material is agent scoped
- **WHEN** the adapter generates per-agent launch material
- **THEN** the generated files resolve under the corresponding Agent Workspace or a recorded Agent Workspace path plan

#### Scenario: Path plans precede generated files
- **WHEN** the adapter writes project-profile launch files, notifier prompts, communication templates, mailbox metadata, gateway metadata, or adapter logs
- **THEN** Workspace Runtime records the semantic path plan and source before those files are written

#### Scenario: Launch material is not cache-like
- **WHEN** adapter launch material is written for a launch attempt
- **THEN** the path plan or Artifact locator marks it as durable launch evidence rather than cache-like generated material

#### Scenario: Adapter paths preserve source detail
- **WHEN** adapter paths come from supported `ISOMER_*` path overrides or Project Manifest defaults
- **THEN** the stored path plans preserve source and source detail without storing unrelated environment values

#### Scenario: External launch material is rejected by default
- **WHEN** a launch-material path resolves outside the Project root or selected Topic Workspace without an accepted external-root contract
- **THEN** validation rejects the path before adapter launch material is written

### Requirement: Adapter Observation and Log Paths
The system SHALL keep Houmao adapter observations, inspection snapshots, and logs under recorded Workspace Runtime path plans.

#### Scenario: Inspection snapshot path is planned
- **WHEN** live adapter inspection persists a snapshot
- **THEN** the snapshot path is recorded as a path plan or Artifact locator before the snapshot is referenced by Workspace Runtime

#### Scenario: Adapter log path is planned
- **WHEN** the Houmao adapter writes launch, inspect, stop, mailbox, gateway, or handoff logs
- **THEN** the log path is recorded through Workspace Path Resolution before downstream diagnostics depend on it

#### Scenario: Missing adapter files remain visible
- **WHEN** an adapter launch material, snapshot, or log path no longer exists
- **THEN** runtime validation reports the missing durable path without deleting the adapter, Artifact, or Provenance refs
