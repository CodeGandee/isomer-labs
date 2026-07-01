## ADDED Requirements

### Requirement: Project Manager Routes Human-Orchestrated Research Preparation
The Project Manager skill SHALL route manual or human-orchestrated Research Topic preparation to common topic preparation, Topic Workspace Manager actor management, and the human-orchestrated research session without implying topic team specialization.

#### Scenario: Human-orchestrated research request is handed off
- **WHEN** the user asks the Project Manager skill to prepare, start, or set up a Research Topic for manual research, multiple manually controlled agents, or human-orchestrated work
- **THEN** the Project Manager skill hands off to common topic preparation and the human-orchestrated research workflow with the selected Project, Research Topic, and requested actor context
- **AND** Topic Actor CRUD or Topic Actor Workspace materialization requests are routed to the Topic Workspace Manager actor-management workflow
- **AND** it does not route the request to `isomer-admin-topic-team-specialize fast-forward` unless the user explicitly asks for Topic Agent Team specialization

#### Scenario: Project manager help distinguishes actor and team paths
- **WHEN** the Project Manager skill lists topic-oriented operations
- **THEN** it distinguishes common topic preparation, Topic Workspace Manager actor management, human-orchestrated research sessions, and Topic Agent Team specialization while keeping runtime initialization or preparation as explicit prerequisites or delegated steps
