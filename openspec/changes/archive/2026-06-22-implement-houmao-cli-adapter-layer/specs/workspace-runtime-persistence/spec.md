## ADDED Requirements

### Requirement: Houmao CLI adapter command records
The system SHALL persist Houmao CLI adapter command runs and payload references as Workspace Runtime records linked to generic Isomer runtime records.

#### Scenario: Command run is persisted
- **WHEN** the Houmao adapter invokes `houmao-mgr --print-json`
- **THEN** Workspace Runtime records the command run id, Agent Team Instance ref when known, Agent Instance ref when known, Execution Adapter ref, operation kind, sanitized argv, cwd ref, payload refs, exit status, timestamp, diagnostics, and Provenance refs

#### Scenario: Raw command output is file-backed
- **WHEN** Houmao CLI output is safe to retain after redaction checks
- **THEN** the adapter stores the raw or normalized payload as a durable file-backed adapter payload ref instead of embedding rich command output inline in lifecycle records

#### Scenario: Command records survive restart
- **WHEN** Isomer restarts after a launch, inspect, prepare-only, or stop command
- **THEN** the Workspace Runtime can reconstruct the adapter command history and linked manifest refs for the Agent Team Instance from persisted records

### Requirement: Houmao launch attempt persistence
The system SHALL persist quick-launch and prepare-only adapter outcomes separately from generic Agent Team Instance identity.

#### Scenario: Launch attempt links generic and adapter refs
- **WHEN** a Houmao-backed quick launch starts
- **THEN** Workspace Runtime records a launch attempt with Agent Team Instance ref, selected Agent Instance refs, Execution Adapter ref, launch material refs, adapter manifest refs, per-agent command refs, status, diagnostics, timestamps, and Provenance refs

#### Scenario: Prepare-only outcome is not launched state
- **WHEN** launch material is prepared without running Houmao launch commands
- **THEN** Workspace Runtime records materialization and manifest refs without marking the Agent Team Instance or Agent Instances as launched or active

#### Scenario: Partial launch keeps known mappings
- **WHEN** a quick launch partially succeeds
- **THEN** Workspace Runtime stores known Agent Instance to Houmao adapter ref mappings, failed command diagnostics, manifest refs, and recovery status without deleting started-agent records

### Requirement: Houmao inspection and stop persistence
The system SHALL persist Houmao live inspection snapshots and stop outcomes as adapter-linked runtime records.

#### Scenario: Inspection snapshot is bounded
- **WHEN** live inspection returns Houmao state
- **THEN** Workspace Runtime records or returns a bounded inspection snapshot linked to Agent Team Instance refs, Agent Instance refs when known, adapter refs, manifest refs, timestamp, diagnostics, and Provenance refs

#### Scenario: Stop outcome is preserved
- **WHEN** a Houmao stop command completes
- **THEN** Workspace Runtime records stopped, failed, partial, or stale outcome state with target refs, command refs, remaining live refs when known, diagnostics, timestamp, and Provenance refs

#### Scenario: Generic records do not contain Houmao internals
- **WHEN** Workspace Runtime stores Houmao managed-agent ids, profile names, tmux session refs, mailbox refs, gateway refs, or project overlay refs
- **THEN** those values remain in opaque adapter refs, adapter payload refs, manifests, or adapter tables rather than generic Agent Team Instance, Agent Instance, Run, handoff, or Artifact core fields
