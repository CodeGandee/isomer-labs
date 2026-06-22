## ADDED Requirements

### Requirement: Manual Handoff Lifecycle Normalization
The system SHALL separate manual handoff dispatch, adapter observation, candidate completion, accepted completion, rejection, repair, and stale states in lifecycle state.

#### Scenario: Dispatch sets handoff observing
- **WHEN** the Operator Agent dispatches a manual handoff through Houmao
- **THEN** the handoff records source actor, target actor, Run or Research Task ref, Agent Team Instance ref, status, Completion Watcher Contract refs, adapter dispatch refs, and Provenance refs

#### Scenario: Adapter reply is candidate completion
- **WHEN** Houmao mail, gateway, file, or bounded inspection surfaces return a specialist result
- **THEN** the system records candidate completion as a Signal Observation or candidate handoff state without marking the handoff accepted

#### Scenario: Operator normalization accepts completion
- **WHEN** the Operator Agent reviews and accepts the candidate result
- **THEN** the system records accepted handoff state, Run updates, output Artifact refs, normalization rationale, and Provenance refs

#### Scenario: Rejected result remains linked
- **WHEN** the Operator Agent rejects or requests repair for a candidate result
- **THEN** the system keeps the observation and produced refs visible and records rejected, blocked, superseded, corrective Service Request, or follow-up handoff state with rationale

#### Scenario: Stale handoff remains recoverable
- **WHEN** a Houmao-backed handoff remains open beyond its staleness threshold or expected observation window
- **THEN** validation reports the stale handoff without deleting dispatch records, Signal Observations, adapter refs, Run refs, or produced Artifact refs

### Requirement: Handoff Lifecycle Respects Adapter Boundary
The system SHALL use existing Agent Team Instance lifecycle records as context for handoff behavior without letting adapter observations rewrite unrelated lifecycle state.

#### Scenario: Handoff requires active or adopted target context
- **WHEN** a Houmao-backed handoff targets an Agent Team Instance
- **THEN** dispatch verifies that the target has a valid launched, adopted, or otherwise accepted adapter context before sending the handoff

#### Scenario: Observation does not rewrite team lifecycle
- **WHEN** a handoff observation reports a specialist reply, failure, or unreachable actor
- **THEN** the system records handoff or Signal Observation state and does not silently change Agent Team Instance or Agent Instance terminal lifecycle state without an explicit stop, recovery, or normalization operation
