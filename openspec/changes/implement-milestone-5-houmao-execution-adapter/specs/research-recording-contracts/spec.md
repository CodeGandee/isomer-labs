## ADDED Requirements

### Requirement: Adapter Launch Provenance
The system SHALL record Provenance Records for Houmao adapter launch, inspection, stop, handoff dispatch, observation, and normalization operations.

#### Scenario: Launch provenance names source refs
- **WHEN** a Houmao-backed Agent Team Instance launch is attempted
- **THEN** Provenance Records name the actor, Project, Research Topic, Topic Workspace, Agent Team Instance, Topic Agent Team Profile, Domain Agent Team Template, launch material refs, Execution Adapter ref, and readiness record ref

#### Scenario: Inspection provenance names adapter snapshot
- **WHEN** live adapter inspection records a snapshot or Artifact
- **THEN** Provenance Records link the snapshot to the inspected Agent Team Instance or Agent Instance refs and opaque adapter refs

#### Scenario: Stop provenance records cleanup
- **WHEN** a stop or cleanup request runs
- **THEN** Provenance Records capture requested targets, adapter response summary, remaining live refs when known, diagnostics, and actor ref

### Requirement: Adapter Signal Observation Recording
The system SHALL record Houmao mail, gateway, file, and inspection signals as Signal Observations linked to runtime lifecycle refs.

#### Scenario: Mail observation is recorded
- **WHEN** Houmao mail returns a delegated agent reply
- **THEN** the system records a Signal Observation with handoff ref, Run ref when known, source Agent Instance ref, adapter payload ref, timestamp, and Provenance refs

#### Scenario: Gateway observation is recorded
- **WHEN** Houmao gateway state reports progress, failure, or candidate completion
- **THEN** the system records a Signal Observation linked to relevant Agent Team Instance, Agent Instance, Run, handoff, and adapter refs

#### Scenario: Observation content remains file-backed
- **WHEN** an observation includes rich reply text, logs, transcripts, generated files, or tool output
- **THEN** the system records or links that content as Artifacts, logs, or adapter payload refs instead of embedding it in lifecycle records

### Requirement: Handoff Result Normalization Recording
The system SHALL convert accepted manual handoff results into durable Run, Artifact, Decision Record, Evidence Item, Finding, or Provenance refs according to research recording contracts.

#### Scenario: Accepted result records outputs
- **WHEN** the Operator Agent accepts a Houmao-observed handoff result
- **THEN** the system records output Artifact refs, Run status updates, handoff accepted state, and Provenance Records

#### Scenario: Result is not automatically evidence
- **WHEN** a Houmao-backed specialist returns a claim, measurement, literature summary, or analysis note
- **THEN** the result is not treated as Evidence Item support for a Research Claim until normalized into accepted Evidence Item or Finding records

#### Scenario: Rejected result records rationale
- **WHEN** the Operator Agent rejects a candidate handoff result
- **THEN** the system records rejection rationale, affected refs, any corrective Service Request or follow-up handoff refs, and Provenance Records
