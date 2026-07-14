## ADDED Requirements

### Requirement: Welcome Recommendations Require a Formal Team Target
The welcome skill SHALL recommend Topic Team Specialization only for an explicit specialization route or a prompt or authoritative context that establishes an Agent Team target.

#### Scenario: Manual topic preparation remains manual
- **WHEN** the user asks to prepare a Research Topic, Topic Workspace, Topic Actor workflow, runtime, or other launch-facing surface without formal Agent Team intent
- **THEN** the welcome skill recommends Topic Creator, Topic Manager, Project Manager, Topic Service Agent support, GUI Manager, or another applicable owner
- **AND** it does not infer Topic Team Specialization

#### Scenario: Agent Team launch recommendation is qualified
- **WHEN** the user asks for launch-facing help and the prompt or authoritative context identifies a Domain Agent Team Template, Topic Agent Team Profile, Topic Team Instantiation Packet, Agent Team Instance, or selected formal team
- **THEN** the welcome skill may recommend `isomer-op-topic-team-specialize`
- **AND** it explains the formal-team evidence that made the route applicable
