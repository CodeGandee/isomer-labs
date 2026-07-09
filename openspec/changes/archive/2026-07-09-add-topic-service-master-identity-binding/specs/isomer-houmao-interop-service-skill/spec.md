## ADDED Requirements

### Requirement: Houmao Interop Uses Isomer Topic Service Master Identity
Houmao interop service guidance SHALL use Isomer-provided Topic Service Master names and bindings when routing to Houmao-owned procedures.

#### Scenario: Preparation passes suggested names
- **WHEN** `isomer-srv-houmao-interop` or `isomer-srv-topic-service-agent-support` routes to Houmao-owned preparation procedure
- **THEN** it passes the Isomer-provided specialist name, launch profile name, and managed agent name as context
- **AND** it does not ask the agent to invent those names

#### Scenario: Later lifecycle routes use binding
- **WHEN** launch, inspect, stop, or repair routes operate on a Topic Service Master
- **THEN** they first inspect the Topic Workspace Manifest binding or skill-context binding payload
- **AND** they use the recorded specialist, launch profile, and managed agent names when present

#### Scenario: Drift is reported in Isomer terms
- **WHEN** Houmao observations differ from the Topic Workspace Manifest binding
- **THEN** the service reports drift against the Topic Workspace and Topic Service Master identity
- **AND** it routes repair through `repair-topic-service-master` rather than silently choosing new Houmao names
