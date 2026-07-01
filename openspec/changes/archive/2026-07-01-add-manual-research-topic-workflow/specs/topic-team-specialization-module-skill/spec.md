## ADDED Requirements

### Requirement: Team Specialization Consumes Prepared Topic and Actor Context
The Topic Team Specialization skill SHALL treat reusable topic preparation and existing Topic Actor bindings as predecessor context that can coexist with team-specific material.

#### Scenario: Prepared topic satisfies reusable prerequisites
- **WHEN** Topic Team Specialization starts with valid prepared-topic evidence for the selected Research Topic
- **THEN** it consumes the Research Topic ref, Topic Workspace ref, topic overview, topic environment readiness, Topic Main Development Repository readiness, runtime readiness, storage bootstrap refs, current Topic Actor roster, and Topic Actor Workspace refs
- **AND** it proceeds to team template adaptation, Topic Agent Team Profile material, agent environment gate resolution, formal Agent Workspace setup, validation, and team summary work without recreating the common topic preparation artifacts

#### Scenario: Full team fast-forward delegates common preparation
- **WHEN** the user asks for full Topic Team Specialization and the selected topic is not prepared
- **THEN** the specialization flow runs or delegates common topic preparation before team-specific steps
- **AND** the final team summary records which common preparation refs and Topic Actor refs were used or preserved

### Requirement: Team Specialization Preserves Topic Actors
The Topic Team Specialization skill SHALL keep Topic Actor bindings and formal team material separate.

#### Scenario: Existing actors are not removed by team specialization
- **WHEN** Topic Team Specialization runs in a Topic Workspace with active Topic Actor bindings
- **THEN** the flow preserves those bindings and Topic Actor Workspace refs unless the user explicitly asks to remove or archive them through the Topic Workspace Manager actor-management workflow

#### Scenario: Actor preparation does not create team material
- **WHEN** common topic preparation or human-orchestrated actor preparation runs
- **THEN** Topic Team Specialization requirements for Domain Agent Team Template adaptation, Topic Agent Team Profile Bundle materialization, formal per-Agent Workspace setup, and launch approval remain unsatisfied until the team specialization workflow runs
