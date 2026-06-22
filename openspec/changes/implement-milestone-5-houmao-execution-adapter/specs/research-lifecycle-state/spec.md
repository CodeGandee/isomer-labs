## ADDED Requirements

### Requirement: Houmao-backed Agent Team Instance Lifecycle
The system SHALL represent Houmao-backed launch, inspection, stop, failure, and stale states through generic Agent Team Instance lifecycle transitions and adapter-linked records.

#### Scenario: Launch transition records actor and adapter ref
- **WHEN** a Houmao-backed Agent Team Instance moves from pre-launch planned state to launched or active state
- **THEN** the lifecycle transition records actor, timestamp, previous status, next status, rationale, Execution Adapter ref, launch attempt ref, and Provenance refs

#### Scenario: Failed launch remains visible
- **WHEN** Houmao launch fails before all Agent Instances are active
- **THEN** the Agent Team Instance and any created Agent Instance mappings remain visible with failed or blocked status and adapter diagnostics

#### Scenario: Stop transition preserves audit
- **WHEN** a launched Houmao-backed Agent Team Instance is stopped
- **THEN** the system records the stop transition and keeps Agent Team Instance, Agent Instance, Run, handoff, adapter, and Provenance refs visible for audit or recovery

#### Scenario: Stale launch is reported
- **WHEN** live Houmao inspection cannot reach expected managed actors or communication surfaces
- **THEN** validation can report the Agent Team Instance or Agent Instance as stale without deleting the adapter mapping

### Requirement: Manual Handoff Lifecycle Normalization
The system SHALL separate manual handoff dispatch, adapter observation, candidate completion, and accepted completion in lifecycle state.

#### Scenario: Dispatch sets handoff observing
- **WHEN** the Operator Agent dispatches a manual handoff through Houmao
- **THEN** the handoff records source actor, target actor, Run or Research Task ref, Agent Team Instance ref, status, Completion Watcher Contract refs, and adapter dispatch refs

#### Scenario: Adapter reply is candidate completion
- **WHEN** Houmao mail or gateway surfaces return a specialist result
- **THEN** the system records candidate completion as a Signal Observation or candidate handoff state without marking the handoff accepted

#### Scenario: Operator normalization accepts completion
- **WHEN** the Operator Agent reviews and accepts the candidate result
- **THEN** the system records accepted handoff state, Run updates, output Artifact refs, and Provenance refs

#### Scenario: Rejected result remains linked
- **WHEN** the Operator Agent rejects or requests repair for a candidate result
- **THEN** the system keeps the observation and produced refs visible and records rejected, blocked, or superseded handoff state with rationale
