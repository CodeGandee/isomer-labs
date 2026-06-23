## ADDED Requirements

### Requirement: Operator-Agent Packet Profile Materialization
The system SHALL materialize authoritative Topic Agent Team Profiles from validated Operator Agent instantiation packets.

#### Scenario: Packet materializes profile
- **WHEN** an Operator Agent instantiation packet passes validation and approval
- **THEN** the system can write a Topic Agent Team Profile under the Project Config Directory using the packet's template ref, Research Topic ref, Topic Workspace ref, role bindings, policy refs, expected Artifacts, control mode, constraints, and provenance refs

#### Scenario: Profile records packet provenance
- **WHEN** a Topic Agent Team Profile is materialized from a packet
- **THEN** the profile or adjacent metadata records the packet ref, Operator Agent actor ref, approval ref, source template ref, and validation result

#### Scenario: Synthetic preview is not authoritative
- **WHEN** `team-profiles specialize` generates a profile without an Operator Agent packet
- **THEN** the output is treated as preview material and does not by itself satisfy launch-facing profile materialization requirements

### Requirement: Placeholder Reconciliation in Profiles
The system SHALL reject unresolved required placeholders in launch-facing Topic Agent Team Profiles unless the Operator Agent packet explicitly defers them with approval context.

#### Scenario: Required profile placeholders are resolved
- **WHEN** a Topic Agent Team Profile is validated for launch-facing use
- **THEN** validation confirms that Research Topic, Topic Workspace, Workspace Runtime, role binding, Agent Profile, Capability Binding, Skill Binding Projection, Agent Workspace, Coordination Policy, and Gate Policy placeholders are resolved or explicitly deferred in the linked packet

#### Scenario: Deferred placeholders block launch when needed
- **WHEN** an approved profile has deferred placeholders that affect Agent Team Instance creation or adapter launch
- **THEN** profile validation allows saving the profile but reports launch blockers until the deferrals are resolved

### Requirement: Agent-Mediated Profile Tests
The system SHALL prove profile materialization through deterministic Operator Agent packet fixtures before relying on live Houmao.

#### Scenario: Deterministic packet fixture materializes profile
- **WHEN** the test suite loads a deterministic Operator Agent packet fixture for `deepsci-mini`
- **THEN** profile materialization produces a valid Topic Agent Team Profile without hardcoded role substitution in product code

#### Scenario: Invalid packet is rejected
- **WHEN** a packet omits required role bindings, crosses topic refs, leaves required launch placeholders unresolved without deferral, or includes runtime truth in profile material
- **THEN** validation rejects the packet or resulting profile before Agent Team Instance creation
