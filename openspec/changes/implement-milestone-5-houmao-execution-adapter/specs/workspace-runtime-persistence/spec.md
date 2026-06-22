## ADDED Requirements

### Requirement: Adapter Handoff Dispatch Persistence
The system SHALL persist Houmao-backed manual handoff dispatch state through provider-neutral handoff records linked to opaque adapter refs and payload refs.

#### Scenario: Dispatch record is persisted
- **WHEN** a Houmao-backed manual handoff is dispatched
- **THEN** Workspace Runtime records the handoff ref, Agent Team Instance ref, source Agent Instance ref, target Agent Instance ref, Run or Research Task ref, Execution Adapter ref, dispatch status, expected output refs, Completion Watcher Contract refs, timestamps, diagnostics, adapter payload refs, and Provenance refs

#### Scenario: Dispatch refs are opaque
- **WHEN** Workspace Runtime records Houmao-specific message ids, mailbox ids, gateway event ids, managed-agent ids, session refs, or command payload ids for a handoff
- **THEN** it stores them as opaque adapter refs, adapter payload refs, or adapter command refs rather than generic handoff, Run, Agent Team Instance, or Agent Instance fields

#### Scenario: Dispatch state is topic scoped
- **WHEN** handoff dispatch state is written
- **THEN** validation requires every linked Agent Team Instance, Agent Instance, Run, Research Task, path plan, Artifact, and adapter payload ref to belong to the selected Topic Workspace

### Requirement: Signal Observation Persistence
The system SHALL persist Houmao mail, gateway, file, command, and bounded inspection signals as Signal Observations linked to runtime lifecycle refs.

#### Scenario: Observation is persisted
- **WHEN** Houmao mail, gateway events, files, command output, or inspection snapshots indicate handoff progress, failure, or candidate completion
- **THEN** Workspace Runtime records a Signal Observation with handoff ref, Run ref when known, Agent Team Instance ref, Agent Instance refs when known, adapter refs, adapter payload refs, timestamp, diagnostics, and Provenance refs

#### Scenario: Observation does not silently change lifecycle
- **WHEN** a Signal Observation suggests candidate completion or failure
- **THEN** Workspace Runtime keeps the observation visible without silently changing handoff, Run, Agent Team Instance, or Workflow Stage Cursor terminal state

#### Scenario: Observation payload is bounded
- **WHEN** an observation includes rich reply text, logs, transcripts, command output, mailbox content, or generated files
- **THEN** Workspace Runtime stores refs to Artifacts, logs, or adapter payload files rather than embedding rich content inline in lifecycle records

### Requirement: Handoff Normalization Persistence
The system SHALL persist accepted, rejected, blocked, superseded, and repair-routed handoff normalization outcomes.

#### Scenario: Accepted normalization is durable
- **WHEN** the Operator Agent accepts a Houmao-observed handoff result
- **THEN** Workspace Runtime records accepted handoff state, Run updates, output Artifact refs, normalization rationale, actor ref, timestamp, and Provenance refs

#### Scenario: Rejected or repair-routed normalization is durable
- **WHEN** the Operator Agent rejects a candidate result, blocks it, supersedes it, or routes repair
- **THEN** Workspace Runtime records the outcome status, rationale, affected Signal Observation refs, produced refs when retained, corrective Service Request or follow-up handoff refs when present, actor ref, timestamp, and Provenance refs

#### Scenario: Normalization state survives restart
- **WHEN** Isomer restarts after a handoff dispatch, observation, or normalization
- **THEN** Workspace Runtime can reconstruct the handoff state, linked Signal Observations, output refs, adapter payload refs, and Provenance refs from persisted records
