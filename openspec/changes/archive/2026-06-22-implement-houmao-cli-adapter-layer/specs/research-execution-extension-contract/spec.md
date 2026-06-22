## ADDED Requirements

### Requirement: Houmao adapter public backend boundary
The system SHALL route Houmao-backed live agent lifecycle operations through Execution Adapter Command Requests and Houmao’s public CLI JSON boundary rather than private Python internals.

#### Scenario: Agent launch request selects CLI-backed adapter
- **WHEN** the system prepares a Houmao-backed Agent Team Instance launch
- **THEN** it creates or validates an Execution Adapter Command Request with operation kind `agent_launch`, selected Execution Adapter ref, Agent Team Instance ref, Agent Instance refs, Agent Workspace refs, launch material refs, Gate policy refs, Provenance obligations, and an opaque adapter payload ref for Houmao CLI details

#### Scenario: Adapter uses public CLI JSON
- **WHEN** the Houmao adapter performs live launch, inspect, stop, or preflight behavior
- **THEN** it invokes `houmao-mgr --print-json` through the adapter runner and does not depend on private Houmao Python functions, Click callback internals, or in-process Houmao global state

#### Scenario: Future SDK requires accepted contract
- **WHEN** a future Houmao release exposes a stable Python SDK
- **THEN** Isomer may use it only after an accepted spec updates the Execution Adapter boundary and preserves equivalent recording, preflight, redaction, and manifest obligations

### Requirement: Houmao direct operation remains reconcilable
The system SHALL allow direct Houmao operation to coexist with Isomer quick launch by treating backend-native changes as observed adapter state until reconciliation or adoption records them.

#### Scenario: Direct launch does not bypass Isomer records
- **WHEN** a user invokes `houmao-mgr` directly from prepared material
- **THEN** Isomer does not treat the backend-native state as accepted Workspace Runtime launch state until reconciliation or adoption validates manifests, live observations, and Agent Instance mappings

#### Scenario: Backend observations are not generic completion
- **WHEN** the Houmao adapter observes live backend state during inspect-live, reconciliation, or stop
- **THEN** the observation remains an adapter inspection snapshot, Signal Observation, diagnostic Artifact, or adapter payload ref until accepted recording rules normalize it into generic lifecycle, handoff, Run, or research evidence records
