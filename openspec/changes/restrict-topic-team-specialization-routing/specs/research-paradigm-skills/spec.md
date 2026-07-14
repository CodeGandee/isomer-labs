## ADDED Requirements

### Requirement: Formal Team Recovery Is Conditional on Selected Team Topology
Research-paradigm workspace and readiness skills SHALL route missing formal-team material to Topic Team Specialization only when the selected research topology includes a formal Agent Team layer.

#### Scenario: Selected formal team lacks its summary
- **WHEN** authoritative context selects formal team material and its required `isomer-topic-summary.md` is missing, blocked, stale, or not checked
- **THEN** the research workspace manager routes recovery to `isomer-op-topic-team-specialize` or the applicable formal-team setup service
- **AND** it names the selected template, profile, packet, Agent Team Instance, or other formal-team evidence

#### Scenario: Human-orchestrated topology lacks a team summary
- **WHEN** the selected topology uses Topic Actors or other non-team preparation and does not select a formal Agent Team layer
- **THEN** absence of `isomer-topic-summary.md` is not a Topic Team Specialization blocker
- **AND** the workspace manager evaluates Topic Creator, Topic Manager, runtime, actor, environment, and research-bootstrap evidence without requiring formal team material

#### Scenario: Missing Agent Workspace does not create team intent
- **WHEN** Agent Workspace or worker-access evidence is missing but no formal Agent Team target is established
- **THEN** the research workspace manager routes to the owner of the selected actor or workspace topology or reports the missing selection
- **AND** it does not infer Topic Team Specialization from the missing workspace evidence alone
