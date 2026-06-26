## MODIFIED Requirements

### Requirement: Agent Team Instance Record Instantiation
The system SHALL instantiate Agent Team Instance records from validated Topic Agent Team Profiles without launching agents or creating adapter-specific launch material.

#### Scenario: Team instance create consumes a profile
- **WHEN** a user creates an Agent Team Instance record from a Topic Agent Team Profile
- **THEN** the system validates the selected Effective Topic Context, Project Manifest registration, Topic Agent Team Profile, and source Domain Agent Team Template before writing runtime records

#### Scenario: Active roles create agent records
- **WHEN** the selected Topic Agent Team Profile has active Agent Role bindings
- **THEN** the system creates Agent Instance records and Agent Workspace records for those active role bindings under the same Agent Team Instance

#### Scenario: Approved workspace refs create path plans
- **WHEN** an active Agent Role binding has a validated `agent_workspace_ref` under the selected Topic Workspace
- **THEN** Agent Team Instance creation records the Agent Workspace path plan from that ref before creating the Agent Workspace directory and Agent Workspace record

#### Scenario: Agent workspaces fall back to generated paths
- **WHEN** an active Agent Role binding does not have an approved `agent_workspace_ref`
- **THEN** the system resolves and records the default Agent Workspace path under `<topic-workspace>/agents/<agent-instance-id>` before creating the Agent Workspace directory and Agent Workspace record

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

#### Scenario: Default Agent Workspace path uses the globally unique Agent Instance id
- **WHEN** the system creates an Agent Workspace path plan for an Agent Instance and no approved `agent_workspace_ref` exists for the active role binding
- **THEN** the path plan derives the Agent Workspace directory from the globally unique Agent Instance id as `<topic-workspace>/agents/<agent-instance-id>`

#### Scenario: Approved Agent Workspace ref does not change Agent Instance id
- **WHEN** the system creates an Agent Workspace path plan from `agent_workspace_ref = "<topic-workspace>/agents/alice"`
- **THEN** the Agent Instance id remains globally unique and does not need to equal `alice`
