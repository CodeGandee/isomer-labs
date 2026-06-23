## ADDED Requirements

### Requirement: Houmao Handoff Adapter Extension
The system SHALL extend the existing CLI-backed Houmao adapter layer with manual handoff dispatch, observation, and normalization behavior without rebuilding the existing launch, inspect-live, stop, reconciliation, or adoption foundation.

#### Scenario: Existing lifecycle adapter is reused
- **WHEN** a Houmao-backed handoff command targets an Agent Team Instance
- **THEN** the system uses the existing adapter refs, manifest refs, launch attempts, inspection snapshots, reconciliation records, or adoption records to establish target state rather than re-materializing launch material or relaunching agents

#### Scenario: Handoff consumes provider-neutral runtime refs
- **WHEN** the Houmao adapter prepares a manual handoff dispatch
- **THEN** it consumes Workspace Runtime refs for the Agent Team Instance, source Agent Instance, target Agent Instance, Run or Research Task, expected outputs, Completion Watcher Contract refs, and Provenance obligations

#### Scenario: Houmao handoff details remain adapter scoped
- **WHEN** the adapter records Houmao mailbox refs, gateway refs, message ids, managed-agent refs, session refs, command payloads, or live process refs for a handoff
- **THEN** those details are stored as opaque adapter refs, adapter payload refs, or adapter-specific records linked to generic Workspace Runtime records

#### Scenario: Generic schema excludes Houmao fields
- **WHEN** an Agent Team Instance, Agent Instance, Run, handoff, Signal Observation, Artifact, or Provenance Record is inspected through generic Isomer APIs
- **THEN** the record does not expose Houmao-specific field names as core schema fields

### Requirement: Houmao Manual Handoff Dispatch
The system SHALL support one manual handoff round from an Operator Agent-controlled `deepsci-org` Agent Team Instance to a selected specialist Agent Instance.

#### Scenario: Manual handoff dispatches through adapter
- **WHEN** the Operator Agent delegates a Research Task or Run step from `deepsci-org-master` to a specialist Agent Instance
- **THEN** the adapter dispatches the handoff through Houmao mail or gateway surfaces and records the handoff, Run linkage, adapter dispatch refs, expected output refs, Completion Watcher Contract refs, and Provenance refs

#### Scenario: Dispatch preflight is non-mutating on failure
- **WHEN** handoff dispatch preflight fails because the runtime schema, Agent Team Instance, Agent Instance mapping, readiness state, adapter refs, Gate policy, or Houmao capability is invalid
- **THEN** the system does not send Houmao mail, call a gateway mutation, create accepted handoff state, or mark the Run complete

#### Scenario: Dispatch may create a Run when requested
- **WHEN** the dispatch command is given enough Research Task and actor refs but no existing Run ref
- **THEN** the system may create or select a provider-neutral Run record before dispatch and link the handoff to that Run

### Requirement: Houmao Signal Observation Ingestion
The system SHALL ingest Houmao mail, gateway, file, and bounded inspection signals as Signal Observations rather than authoritative handoff completion.

#### Scenario: Mail reply becomes Signal Observation
- **WHEN** Houmao mail indicates a delegated Agent Instance has replied
- **THEN** the system records a Signal Observation linked to the handoff, Run, Agent Team Instance, Agent Instance, adapter refs, payload refs, timestamp, and Provenance refs

#### Scenario: Gateway event becomes Signal Observation
- **WHEN** a Houmao gateway event indicates progress, failure, or candidate completion
- **THEN** the system records a Signal Observation linked to the relevant lifecycle refs and adapter payload refs

#### Scenario: Observation is not completion
- **WHEN** Houmao mail, gateway events, files, command output, or inspection snapshots indicate candidate completion
- **THEN** the adapter records Signal Observations without marking the handoff accepted, promoting produced content into Evidence Items, or changing Run terminal state

### Requirement: Houmao Handoff Normalization
The system SHALL require Operator Agent normalization before a Houmao-observed handoff result becomes accepted Workspace Runtime state.

#### Scenario: Normalization accepts result
- **WHEN** the Operator Agent accepts an observed handoff result
- **THEN** Workspace Runtime records accepted handoff state, Run updates, produced Artifact refs when present, normalization rationale, and Provenance Records

#### Scenario: Normalization rejects or routes repair
- **WHEN** the Operator Agent rejects a candidate result or routes repair
- **THEN** Workspace Runtime keeps the Signal Observation and produced refs visible and records rejected, blocked, superseded, corrective Service Request, or follow-up handoff refs with rationale

#### Scenario: Normalization preserves research evidence boundary
- **WHEN** a Houmao-backed specialist returns a claim, measurement, literature summary, or analysis note
- **THEN** the result is not treated as Evidence Item support for a Research Claim until normalization creates accepted Evidence Item, Finding, Artifact, Decision Record, or Provenance refs under the relevant recording contract

### Requirement: Houmao Live Validation Boundary
The system SHALL keep live Houmao handoff validation capability-gated and separate from the default unit test suite.

#### Scenario: Live handoff validation checks capability first
- **WHEN** a live-gated handoff integration or manual test is requested
- **THEN** the system reports the resolved `extern/orphan/houmao` checkout or override, read-only capability-gate status, and skipped or unavailable status before any launch, handoff, observe, normalize, or stop mutation runs

#### Scenario: Houmao defects remain repository-local
- **WHEN** the handoff adapter discovers a Houmao defect or missing capability
- **THEN** the required fix is made and validated in the Houmao checkout before Isomer records the handoff adapter capability as available
