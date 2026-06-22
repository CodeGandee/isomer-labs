## ADDED Requirements

### Requirement: UC-01 Adapter Boundary
The system SHALL run UC-01 through the Houmao Execution Adapter boundary or an adapter-simulated equivalent without exposing Houmao native fields in generic research records.

#### Scenario: UC-01 uses adapter refs
- **WHEN** the UC-01 runner launches, simulates, dispatches, observes, normalizes, inspects, or stops adapter-backed work
- **THEN** Houmao command outputs, message ids, gateway events, managed-agent ids, sessions, and project overlay refs are stored only in adapter payload refs, manifests, or adapter-scoped records

#### Scenario: Generic UC-01 records stay provider-neutral
- **WHEN** UC-01 Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, Research Inquiries, Research Tasks, Runs, or Provenance Records are inspected
- **THEN** they expose Isomer lifecycle and recording refs rather than fields named after Houmao mailboxes, gateways, specialists, managed agents, or launch dossiers

### Requirement: UC-01 Simulated Adapter Mode
The system SHALL provide an adapter-simulated mode for UC-01 that exercises the same Isomer-side recording flow as live Houmao.

#### Scenario: Simulated mode produces handoff observations
- **WHEN** UC-01 runs in simulated adapter mode
- **THEN** the adapter layer produces deterministic dispatch, observation, and normalization inputs for scouting and synthesis-review handoffs without invoking real Houmao live mutations

#### Scenario: Simulated mode preserves payload refs
- **WHEN** simulated adapter mode produces command-like outputs
- **THEN** the system records bounded adapter payload refs so runtime summaries and validation use the same ref patterns as live mode

### Requirement: UC-01 Live Houmao Cleanup
The system SHALL preserve cleanup and recovery state for UC-01 live Houmao runs.

#### Scenario: Live run records cleanup outcome
- **WHEN** UC-01 live mode launches or adopts Houmao-backed agents
- **THEN** the runner stops or reports cleanup state for the Agent Team Instance and records stopped, partial, failed, or skipped cleanup outcome with diagnostics

#### Scenario: Partial live run remains recoverable
- **WHEN** UC-01 live mode fails after some launch, handoff, observation, or recording work
- **THEN** Workspace Runtime preserves adapter command refs, payload refs, handoff refs, lifecycle refs, diagnostics, and recovery guidance without deleting started-agent or research records
