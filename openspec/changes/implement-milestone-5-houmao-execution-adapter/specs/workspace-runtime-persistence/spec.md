## ADDED Requirements

### Requirement: Adapter Launch State Persistence
The system SHALL persist Houmao adapter launch state in Workspace Runtime through opaque adapter refs linked to generic Agent Team Instance, Agent Instance, Run, handoff, path plan, Artifact, and Provenance records.

#### Scenario: Launch attempt is recorded
- **WHEN** a Houmao-backed Agent Team Instance launch starts
- **THEN** Workspace Runtime records a launch attempt with Agent Team Instance ref, Execution Adapter ref, launch material refs, status, timestamps, diagnostics, and Provenance refs

#### Scenario: Launch material refs are durable
- **WHEN** Workspace Runtime stores launch material refs for a Houmao launch attempt
- **THEN** those refs identify durable file-backed Artifacts or adapter payload refs and are not recorded as disposable cache refs

#### Scenario: Adapter refs are opaque
- **WHEN** Workspace Runtime records Houmao-specific launch, mailbox, gateway, notifier, or managed-agent ids
- **THEN** it stores them as opaque adapter refs or adapter payload refs rather than generic Agent Team Instance or Agent Instance fields

#### Scenario: Agent mapping is recoverable
- **WHEN** a Houmao-backed Agent Team Instance is reopened after process restart
- **THEN** Workspace Runtime can reconstruct the mapping between generic Agent Instance ids and opaque Houmao adapter refs

#### Scenario: Launch state is topic scoped
- **WHEN** adapter launch state is written
- **THEN** validation requires every linked Agent Team Instance, Agent Instance, Agent Workspace, Run, path plan, and Artifact ref to belong to the selected Topic Workspace

### Requirement: Adapter Inspection Snapshot Persistence
The system SHALL persist or return Houmao inspection snapshots without overwriting authoritative lifecycle records.

#### Scenario: Inspection snapshot is linked
- **WHEN** live adapter inspection returns Houmao state
- **THEN** the system records or returns an inspection snapshot linked to the Agent Team Instance, Agent Instance refs when known, adapter refs, timestamp, and Provenance refs

#### Scenario: Inspection does not silently change lifecycle
- **WHEN** inspection shows a Houmao-managed agent as stopped, failed, stale, or unreachable
- **THEN** the system reports the observation and records diagnostics or Signal Observations without silently changing generic lifecycle state unless a stop, recovery, or normalization operation accepts the change

#### Scenario: Inspection payload is bounded
- **WHEN** inspection returns large logs, transcripts, command output, or mailbox content
- **THEN** Workspace Runtime stores refs to Artifacts, logs, or adapter payload files rather than embedding rich content inline

### Requirement: Adapter Stop and Recovery State
The system SHALL preserve stop and recovery outcomes for Houmao-backed Agent Team Instances.

#### Scenario: Stop outcome is durable
- **WHEN** a stop command completes
- **THEN** Workspace Runtime records stopped, failed, partial, or stale stop outcome state with adapter refs, diagnostics, timestamp, and Provenance refs

#### Scenario: Partial cleanup remains visible
- **WHEN** some Houmao-managed actors remain reachable after stop
- **THEN** the runtime keeps the launch and adapter refs visible and reports cleanup diagnostics instead of deleting records

#### Scenario: Recovery summarizes adapter state
- **WHEN** a launched Agent Team Instance is inspected after process restart
- **THEN** the system reconstructs generic runtime summaries and adapter state summaries from persisted Workspace Runtime records and live Houmao inspection when available
