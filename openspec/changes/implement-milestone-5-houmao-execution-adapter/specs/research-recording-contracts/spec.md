## ADDED Requirements

### Requirement: Handoff Adapter Provenance
The system SHALL record Provenance Records for Houmao-backed handoff dispatch, observation, and normalization operations.

#### Scenario: Dispatch provenance names source refs
- **WHEN** a Houmao-backed handoff dispatch is attempted
- **THEN** Provenance Records name the actor, Project, Research Topic, Topic Workspace, Agent Team Instance, source Agent Instance, target Agent Instance, Run or Research Task refs, expected output refs, Completion Watcher Contract refs, Execution Adapter ref, adapter payload refs, and readiness or Gate refs when relevant

#### Scenario: Observation provenance names adapter payload
- **WHEN** adapter observation records a Signal Observation, snapshot, or Artifact
- **THEN** Provenance Records link the observation to the handoff, Run, Agent Team Instance, Agent Instance refs when known, opaque adapter refs, adapter payload refs, and observation source

#### Scenario: Normalization provenance records decision
- **WHEN** a normalization request accepts, rejects, blocks, supersedes, or routes repair for a candidate handoff result
- **THEN** Provenance Records capture the Operator Agent actor, reviewed Signal Observation refs, decision rationale, output refs, corrective refs when present, and affected lifecycle refs

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
