## MODIFIED Requirements

### Requirement: Project Manager Topic Workspace Visibility Guidance
The project manager skill SHALL explain the standard Topic Workspace visibility layout when it initializes, checks, or prepares Workspace Runtime state.

#### Scenario: Runtime guidance reports standard layout
- **WHEN** the user asks the project manager skill to initialize or inspect Workspace Runtime for a Topic Workspace
- **THEN** it explains that `repos/topic-main` and `agents/<agent-name>` are worker-facing Git surfaces, `records/*` is owner-preserved topic record material, and `runtime/` plus `state.sqlite` are runtime-internal surfaces

#### Scenario: Runtime guidance avoids legacy collaboration roots
- **WHEN** project-manager runtime-boundary guidance describes directories created by `isomer-cli project runtime init`
- **THEN** it does not present root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` as normal worker-visible outputs

#### Scenario: Legacy layout is repair guidance
- **WHEN** project-manager diagnostics see legacy root collaboration directories in a Topic Workspace
- **THEN** the skill reports migration guidance and directs repair through explicit operator action instead of telling the user to delete the directories by hand

#### Scenario: Topic manager handoff is named
- **WHEN** the user asks the project manager skill to prepare per-agent worktrees, validate worker visibility boundaries, or inspect initialized-topic storage topology
- **THEN** it hands off to `isomer-admin-topic-mgr` rather than duplicating Topic Workspace or Agent Workspace setup instructions

### Requirement: Project Manager Routes Human-Orchestrated Research Preparation
The Project Manager skill SHALL route manual or human-orchestrated Research Topic preparation to `isomer-admin-topic-creator` without implying topic team specialization.

#### Scenario: Human-orchestrated research request is handed off
- **WHEN** the user asks the Project Manager skill to prepare, start, create, or set up a Research Topic for manual research, multiple manually controlled agents, or human-orchestrated work
- **THEN** the Project Manager skill hands off to `isomer-admin-topic-creator` with the selected Project, Research Topic, requested actor context, and any known Project lifecycle state
- **AND** Topic Actor CRUD or Topic Actor Workspace materialization requests are still routed by the creator or direct advanced users to `isomer-admin-topic-mgr` actor commands
- **AND** it does not route the request to `isomer-admin-topic-team-specialize fast-forward` unless the user explicitly asks for Topic Agent Team specialization

#### Scenario: Project manager help distinguishes actor and team paths
- **WHEN** the Project Manager skill lists topic-oriented operations
- **THEN** it names `isomer-admin-topic-creator` as the front door for topic creation and manual-research readiness
- **AND** it distinguishes `isomer-admin-topic-mgr` actor management, deprecated compatibility preparation/session skills, and Topic Agent Team specialization while keeping runtime initialization or preparation as explicit prerequisites or delegated steps
