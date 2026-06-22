## ADDED Requirements

### Requirement: Houmao Manual Handoff Command Requests
The system SHALL route Houmao manual handoff dispatch, observation, and normalization through provider-neutral Execution Adapter Command Requests or equivalent command envelopes.

#### Scenario: Handoff request is provider neutral
- **WHEN** the Operator Agent dispatches a manual handoff through Houmao mail or gateway surfaces
- **THEN** the dispatch uses operation kind `manual_handoff` with Research Task or Run refs, source and target Agent Instance refs, selected Agent Team Instance ref, Completion Watcher Contract refs, expected output refs, Gate policy refs when present, and Provenance obligations

#### Scenario: Observation request is provider neutral
- **WHEN** the system ingests Houmao mail, gateway, file, or bounded inspection signals for a handoff
- **THEN** the observation uses operation kind `manual_handoff_observe` or an equivalent provider-neutral envelope with handoff refs, Run refs when known, source and target Agent Instance refs when known, adapter payload refs, and Provenance obligations

#### Scenario: Normalization request is provider neutral
- **WHEN** the Operator Agent accepts, rejects, blocks, supersedes, or routes repair for a handoff result
- **THEN** the normalization uses operation kind `manual_handoff_normalize` or an equivalent provider-neutral envelope with handoff refs, Signal Observation refs, output refs, rationale, and Provenance obligations

### Requirement: Houmao Handoff Preflight
The system SHALL complete handoff preflight before mutating Houmao communication surfaces or Workspace Runtime normalization state.

#### Scenario: Preflight checks Isomer prerequisites
- **WHEN** a Houmao handoff dispatch is requested
- **THEN** preflight verifies current Workspace Runtime schema, ready Topic Environment Readiness when required, selected Agent Team Instance, source and target Agent Instance records, handoff or Run refs, path plans, and required recording obligations

#### Scenario: Preflight checks adapter prerequisites
- **WHEN** a Houmao handoff dispatch or observation is requested
- **THEN** preflight verifies existing Houmao adapter refs, required mail or gateway capability, local Houmao checkout availability for live operations, and adapter compatibility before sending messages or ingesting live adapter signals

#### Scenario: Preflight blocks unresolved Gates
- **WHEN** handoff dispatch or normalization is governed by a Gate policy and the required Gate is unresolved
- **THEN** preflight blocks only the governed handoff operation and reports the Gate ref

#### Scenario: Failed preflight is non-mutating
- **WHEN** handoff preflight fails before adapter dispatch or normalization
- **THEN** the system does not send Houmao mail, call a gateway mutation, mark the handoff accepted, or mark the Run complete

### Requirement: Adapter Monitoring and Signal Observation
The system SHALL record adapter monitoring output as durable observations without making adapter signals authoritative lifecycle completion.

#### Scenario: Houmao mail becomes Signal Observation
- **WHEN** Houmao mail indicates a delegated Agent Instance has replied
- **THEN** the system records a Signal Observation linked to the handoff, Run, Agent Team Instance, Agent Instance, adapter refs, adapter payload refs, and Provenance refs

#### Scenario: Houmao gateway event becomes Signal Observation
- **WHEN** a Houmao gateway event indicates progress, failure, or candidate completion
- **THEN** the system records a Signal Observation linked to the relevant lifecycle refs and adapter payload refs

#### Scenario: Operator normalization controls lifecycle
- **WHEN** adapter observations suggest completion
- **THEN** handoff, Run, and Workflow Stage Cursor terminal state changes require Operator Agent normalization or an accepted future automatic-completion contract
