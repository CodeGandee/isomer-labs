## ADDED Requirements

### Requirement: Houmao Adapter Command Requests
The system SHALL route Houmao launch, inspection, stop, and handoff operations through Execution Adapter Command Requests with provider-neutral identity, operation, policy, and recording fields.

#### Scenario: Agent launch request is provider neutral
- **WHEN** the system prepares a Houmao-backed Agent Team Instance launch
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `agent_launch`, selected Execution Adapter ref, Agent Team Instance ref, Agent Instance refs, Agent Workspace refs, expected launch material refs, Gate policy refs, and Provenance obligations

#### Scenario: Inspect request is provider neutral
- **WHEN** the system requests live Houmao inspection
- **THEN** it uses an adapter command request or equivalent provider-neutral envelope with operation kind `agent_inspect` and selected Agent Team Instance or Agent Instance refs

#### Scenario: Stop request is provider neutral
- **WHEN** the system requests Houmao stop behavior
- **THEN** it uses an adapter command request or equivalent provider-neutral envelope with operation kind `agent_stop`, target Agent Team Instance or Agent Instance refs, cleanup expectations, and Provenance obligations

#### Scenario: Handoff request is provider neutral
- **WHEN** the Operator Agent dispatches a manual handoff through Houmao mail or gateway surfaces
- **THEN** the dispatch uses operation kind `manual_handoff` with Research Task or Run refs, source and target Agent Instance refs, Completion Watcher Contract refs, expected output refs, and Provenance obligations

### Requirement: Houmao Launch Preflight
The system SHALL complete launch preflight before mutating Houmao runtime state.

#### Scenario: Preflight checks Isomer prerequisites
- **WHEN** a Houmao launch is requested
- **THEN** preflight verifies current Workspace Runtime schema, ready Topic Environment Readiness, validated Topic Agent Team Profile, Agent Team Instance records, Agent Workspace directories, path plans, and required recording obligations

#### Scenario: Preflight checks adapter prerequisites
- **WHEN** a Houmao launch is requested
- **THEN** preflight verifies the local Houmao checkout, required Houmao command or API availability, generated launch material, and adapter compatibility before starting agents

#### Scenario: Preflight blocks unresolved Gates
- **WHEN** launch or handoff dispatch is governed by a Gate policy and the required Gate is unresolved
- **THEN** preflight blocks only the governed launch or handoff operation and reports the Gate ref

#### Scenario: Failed preflight is non-mutating
- **WHEN** launch preflight fails before adapter dispatch
- **THEN** the system does not start Houmao agents, send handoffs, or mark launch state active

### Requirement: Adapter Monitoring and Signal Observation
The system SHALL record adapter monitoring output as durable observations without making adapter signals authoritative lifecycle completion.

#### Scenario: Houmao mail becomes Signal Observation
- **WHEN** Houmao mail indicates a delegated Agent Instance has replied
- **THEN** the system records a Signal Observation linked to the handoff, Run, Agent Instance, adapter refs, and Provenance refs

#### Scenario: Houmao gateway event becomes Signal Observation
- **WHEN** a Houmao gateway event indicates progress, failure, or candidate completion
- **THEN** the system records a Signal Observation linked to the relevant lifecycle refs and adapter payload refs

#### Scenario: Operator normalization controls lifecycle
- **WHEN** adapter observations suggest completion
- **THEN** handoff, Run, and Workflow Stage Cursor terminal state changes require Operator Agent normalization or an accepted future automatic-completion contract
