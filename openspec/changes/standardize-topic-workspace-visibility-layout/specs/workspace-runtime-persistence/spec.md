## MODIFIED Requirements

### Requirement: Workspace Runtime Creation and Reopening
The system SHALL create and reopen a Workspace Runtime for a selected Topic Workspace through explicit runtime commands or APIs, with schema metadata and standard Topic Workspace visibility directories.

#### Scenario: Runtime init creates state and directories
- **WHEN** a user runs the explicit Workspace Runtime initialization command for a valid Research Topic and Topic Workspace
- **THEN** the system creates `state.sqlite`, `repos/`, `agents/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, and `runtime/` under the Topic Workspace

#### Scenario: Runtime init does not create legacy root collaboration directories
- **WHEN** Workspace Runtime initialization creates the standard directories
- **THEN** it does not create root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` as worker-visible collaboration surfaces

#### Scenario: Runtime init records schema metadata
- **WHEN** the Workspace Runtime is initialized
- **THEN** the system records the runtime schema version, Project ref, Research Topic ref, Topic Workspace ref, creation timestamp, and source Project Manifest schema versions in `state.sqlite`

#### Scenario: Runtime init is idempotent for current schema
- **WHEN** a Workspace Runtime already exists with the current supported runtime schema version
- **THEN** initialization reopens it, verifies required directories, and reports that the runtime already exists without replacing records

#### Scenario: Runtime mutation blocks unsupported schema
- **WHEN** a Workspace Runtime exists with an unsupported older or newer schema version
- **THEN** mutating commands fail with a schema-version diagnostic and do not alter runtime records or directories

#### Scenario: Runtime is not created by read-only commands
- **WHEN** a user runs `project doctor`, `project validate`, `project context show`, `project paths preview`, `project team-templates`, or `project team-profiles validate`
- **THEN** the system does not create `state.sqlite` or Workspace Runtime directories

### Requirement: Agent Team Instance Record Instantiation
The system SHALL instantiate Agent Team Instance records from validated Topic Agent Team Profiles without launching agents or creating adapter-specific launch material, and SHALL bind each active role to a validated topic-local agent name and Agent Workspace worktree plan.

#### Scenario: Team instance create consumes a profile
- **WHEN** a user creates an Agent Team Instance record from a Topic Agent Team Profile
- **THEN** the system validates the selected Effective Topic Context, Project Manifest registration, Topic Agent Team Profile, source Domain Agent Team Template, and topic-local agent-name workspace plans before writing runtime records

#### Scenario: Active roles create agent records
- **WHEN** the selected Topic Agent Team Profile has active Agent Role bindings with validated agent-name workspace plans
- **THEN** the system creates Agent Instance records and Agent Workspace records for those active role bindings under the same Agent Team Instance

#### Scenario: Agent-name workspace plans create path plans
- **WHEN** an active Agent Role binding has validated agent name `alice`, expected branch `per-agent/alice/main`, and workspace path `<topic-workspace>/agents/alice`
- **THEN** Agent Team Instance creation records the Agent Workspace path plan from that agent-name plan before creating the Agent Workspace directory and Agent Workspace record

#### Scenario: Compatibility workspace refs are derived inputs
- **WHEN** legacy profile or packet material still carries `agent_workspace_ref` for an active role binding
- **THEN** Agent Team Instance creation treats it as a compatibility input only after validation derives the matching topic-local agent name, worktree path, and branch namespace

#### Scenario: Missing workspace plan blocks creation
- **WHEN** an active Agent Role binding does not have a validated topic-local agent name and Agent Workspace worktree plan
- **THEN** the system rejects Agent Team Instance creation with a launch-facing workspace planning diagnostic instead of silently falling back to `<topic-workspace>/agents/<agent-instance-id>`

#### Scenario: Duplicate team instance id is rejected
- **WHEN** a create request names an Agent Team Instance id that already exists in the selected Workspace Runtime
- **THEN** the system rejects the request with a validation diagnostic and leaves existing records unchanged

#### Scenario: Houmao launch material is out of scope
- **WHEN** an Agent Team Instance record is created in Milestone 4
- **THEN** the system does not create Houmao launch dossiers, mailboxes, gateways, managed-agent ids, live process ids, or adapter launch facts

### Requirement: Agent Instance ids are globally unique
The system SHALL generate Agent Instance ids that are globally unique within the Project and SHALL reject any creation or validation request that would produce a duplicate id.

#### Scenario: New Agent Instance receives a globally unique id
- **WHEN** the system creates an Agent Instance record for an Agent Team Instance
- **THEN** the generated Agent Instance id is unique across all Agent Instance records in the Project

#### Scenario: Duplicate Agent Instance id is rejected at creation
- **WHEN** an Agent Team Instance creation request would generate an Agent Instance id that already exists
- **THEN** the system rejects the request with a validation diagnostic and leaves existing records unchanged

#### Scenario: Runtime validation reports duplicate Agent Instance ids
- **WHEN** `project runtime validate` scans Agent Instance records and finds two records with the same id
- **THEN** the system reports a workspace issue identifying the duplicate id and both records

#### Scenario: Default Agent Workspace path does not use Agent Instance id
- **WHEN** the system creates an Agent Workspace path plan for an Agent Instance
- **THEN** the path plan derives the Agent Workspace directory from the validated topic-local agent name as `<topic-workspace>/agents/<agent-name>` rather than from the globally unique Agent Instance id

#### Scenario: Agent Workspace path does not change Agent Instance id
- **WHEN** the system creates an Agent Workspace path plan for `agent_name = "alice"`
- **THEN** the Agent Instance id remains globally unique and does not need to equal `alice`
