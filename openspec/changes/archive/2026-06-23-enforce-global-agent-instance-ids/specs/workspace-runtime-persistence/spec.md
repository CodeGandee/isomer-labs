# workspace-runtime-persistence Delta Specification

## ADDED Requirements

### Requirement: Agent Instance ids are globally unique
The system SHALL generate Agent Instance ids that are globally unique within the Project and SHALL reject any creation or validation request that would produce a duplicate id.

#### Scenario: New Agent Instance receives a globally unique id
- **WHEN** the system creates an Agent Instance record for an Agent Team Instance
- **THEN** the generated Agent Instance id is unique across all Agent Instance records in the Project

#### Scenario: Duplicate Agent Instance id is rejected at creation
- **WHEN** an Agent Team Instance creation request would generate an Agent Instance id that already exists
- **THEN** the system rejects the request with a validation diagnostic and leaves existing records unchanged

#### Scenario: Runtime validation reports duplicate Agent Instance ids
- **WHEN** `runtime validate` scans Agent Instance records and finds two records with the same id
- **THEN** the system reports a workspace issue identifying the duplicate id and both records

#### Scenario: Agent Workspace path uses the globally unique Agent Instance id
- **WHEN** the system creates an Agent Workspace path plan for an Agent Instance
- **THEN** the path plan derives the Agent Workspace directory from the globally unique Agent Instance id as `<topic-workspace>/agents/<agent-instance-id>/`
