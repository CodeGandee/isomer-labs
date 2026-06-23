## ADDED Requirements

### Requirement: Packet-Backed Profile Bundle Materialization
The system SHALL materialize authoritative Topic Agent Team Profiles as the selected Research Topic's single Topic Agent Team Profile Bundle from validated instantiation packets approved by a Project Operator Session or Operator Agent.

#### Scenario: Packet materializes profile bundle
- **WHEN** an instantiation packet passes validation and approval
- **THEN** the system can write the Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/` using the packet's template ref, Research Topic ref, Topic Workspace ref, role bindings, policy refs, expected Artifacts, control mode, constraints, copied template material plan, and provenance refs

#### Scenario: Project config keeps only profile bundle refs
- **WHEN** a Topic Agent Team Profile Bundle is materialized
- **THEN** the Project Manifest can register the bundle's `profile.toml` path for discovery while the profile body, copied template material, packet, validation, and provenance files remain inside the owning Topic Workspace

#### Scenario: Second active profile bundle for the same topic is rejected
- **WHEN** a materialization request or Project Manifest registration would create a second active Topic Agent Team Profile Bundle for a Research Topic
- **THEN** validation rejects the request and reports that each Research Topic has one authoritative topic team

#### Scenario: Bundle contains copied specialized material
- **WHEN** a Domain Agent Team Template such as `deepsci-mini` requires deep topic specialization
- **THEN** materialization copies editable template material such as `execplan/` into the Topic Agent Team Profile Bundle, applies approved topic-specific changes there, and leaves the source Domain Agent Team Template unchanged

#### Scenario: Cross-topic profile bundle placement is rejected
- **WHEN** a materialization request attempts to write or register a Topic Agent Team Profile Bundle outside the selected Topic Workspace or inside another Research Topic's Topic Workspace
- **THEN** validation rejects the request and reports a Topic Agent Team Profile isolation diagnostic

#### Scenario: Profile records packet provenance
- **WHEN** a Topic Agent Team Profile is materialized from a packet
- **THEN** `profile.toml` or adjacent bundle metadata records the packet ref, project operator actor or session ref, Topic Service Agent refs when used, approval ref, source template ref, copied material refs, and validation result

#### Scenario: Synthetic preview is not authoritative
- **WHEN** `team-profiles specialize` generates a profile without an approved instantiation packet
- **THEN** the output is treated as preview material and does not by itself satisfy launch-facing profile bundle materialization requirements

### Requirement: Placeholder Reconciliation in Profiles
The system SHALL reject unresolved required placeholders in launch-facing Topic Agent Team Profiles unless the approved instantiation packet explicitly defers them with approval context.

#### Scenario: Required profile placeholders are resolved
- **WHEN** a Topic Agent Team Profile Bundle is validated for launch-facing use
- **THEN** validation confirms that Research Topic, Topic Workspace, Workspace Runtime, role binding, Agent Profile, Capability Binding, Skill Binding Projection, Agent Workspace, Coordination Policy, and Gate Policy placeholders are resolved or explicitly deferred in the linked packet

#### Scenario: Deferred placeholders block launch when needed
- **WHEN** an approved profile has deferred placeholders that affect Agent Team Instance creation or adapter launch
- **THEN** profile validation allows saving the profile but reports launch blockers until the deferrals are resolved

### Requirement: Agent-Mediated Profile Bundle Tests
The system SHALL prove profile bundle materialization through deterministic project-operator and Topic Service Agent packet fixtures before relying on live Houmao.

#### Scenario: Deterministic packet fixture materializes profile
- **WHEN** the test suite loads a deterministic instantiation packet fixture for `deepsci-mini`
- **THEN** profile bundle materialization produces a valid Topic Agent Team Profile Bundle with copied specialized template material and without hardcoded role substitution in product code

#### Scenario: Invalid packet is rejected
- **WHEN** a packet omits required role bindings, crosses topic refs, leaves required launch placeholders unresolved without deferral, or includes runtime truth in profile material
- **THEN** validation rejects the packet or resulting profile before Agent Team Instance creation
