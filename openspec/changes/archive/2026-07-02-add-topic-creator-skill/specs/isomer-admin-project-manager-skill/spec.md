## MODIFIED Requirements

### Requirement: Project Manager Routes Human-Orchestrated Research Preparation
The Project Manager skill SHALL route manual or human-orchestrated Research Topic preparation to `isomer-admin-topic-creator` without implying topic team specialization.

#### Scenario: Human-orchestrated research request is handed off
- **WHEN** the user asks the Project Manager skill to prepare, start, create, or set up a Research Topic for manual research, multiple manually controlled agents, or human-orchestrated work
- **THEN** the Project Manager skill hands off to `isomer-admin-topic-creator` with the selected Project, Research Topic, requested actor context, and any known Project lifecycle state
- **AND** Topic Actor CRUD or Topic Actor Workspace materialization requests are still routed by the creator or direct advanced users to the Topic Workspace Manager actor-management workflow
- **AND** it does not route the request to `isomer-admin-topic-team-specialize fast-forward` unless the user explicitly asks for Topic Agent Team specialization

#### Scenario: Project manager help distinguishes actor and team paths
- **WHEN** the Project Manager skill lists topic-oriented operations
- **THEN** it names `isomer-admin-topic-creator` as the front door for topic creation and manual-research readiness
- **AND** it distinguishes Topic Workspace Manager actor management, deprecated compatibility preparation/session skills, and Topic Agent Team specialization while keeping runtime initialization or preparation as explicit prerequisites or delegated steps
