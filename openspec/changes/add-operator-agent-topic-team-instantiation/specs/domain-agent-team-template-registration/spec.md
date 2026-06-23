## ADDED Requirements

### Requirement: Template Instantiation Metadata Inspection
The system SHALL expose instantiation metadata for Domain Agent Team Templates without treating the template as a concrete topic team.

#### Scenario: Placeholder catalog is reported
- **WHEN** a user, Project Operator Session, Operator Agent, or Topic Service Agent inspects a Domain Agent Team Template
- **THEN** the output includes declared placeholder names, required status, source files, expected replacement layer, and whether unresolved values block profile save or only launch

#### Scenario: Role binding slots are reported
- **WHEN** a user, Project Operator Session, Operator Agent, or Topic Service Agent inspects a Domain Agent Team Template
- **THEN** the output includes role ids, required or optional status, Agent Profile slots, Capability Binding slots, Skill Binding Projection slots, Agent Workspace placeholder refs, and Workflow Stage ownership

#### Scenario: Instantiation schema is discoverable
- **WHEN** a template package includes an instantiation schema or placeholder parameter catalog
- **THEN** template validation and inspection expose that schema path and validate that it does not contain concrete Research Topic, Topic Workspace, Agent Team Instance, launch, credential, or Run truth

### Requirement: Template Boundary for Agent-Mediated Instantiation
The system SHALL preserve the reusable template boundary when instantiation metadata is added for Project Operator Session, Operator Agent, or Topic Service Agent workflows.

#### Scenario: Template may require topic instantiation
- **WHEN** a Domain Agent Team Template declares `topic_instantiation_required`
- **THEN** the system accepts the declaration and reports that the template must go through Topic Team Specialization before Agent Team Instance creation

#### Scenario: Template validation rejects concrete packet output
- **WHEN** a Domain Agent Team Template source file contains an approved instantiation packet, concrete Topic Agent Team Profile, concrete Agent Workspace path, live adapter ref, user approval decision, or Topic Service Agent runtime ref
- **THEN** template validation rejects the file as crossing from template material into topic, service, or runtime material

#### Scenario: Template source is copied before topic edits
- **WHEN** a Project Operator Session, Operator Agent, or Topic Service Agent needs to rewrite prompts, skills, workflow contracts, or execplan material for a topic
- **THEN** the system copies the required template material into the Topic Agent Team Profile Bundle and applies topic edits there rather than editing the Domain Agent Team Template source
