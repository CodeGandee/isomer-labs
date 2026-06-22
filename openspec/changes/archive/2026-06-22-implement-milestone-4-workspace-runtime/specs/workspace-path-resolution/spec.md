## ADDED Requirements

### Requirement: Runtime Path Plan Persistence
The system SHALL persist selected Workspace Path Resolution outputs as Workspace Runtime path plans before dependent runtime records use those paths.

#### Scenario: Runtime init records topic workspace paths
- **WHEN** Workspace Runtime is initialized
- **THEN** the system records path plans for `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/` with canonical paths and resolution sources

#### Scenario: Agent workspace creation records path plan first
- **WHEN** an Agent Workspace is created for an Agent Instance
- **THEN** the system records the Agent Workspace path plan before creating the directory or Agent Workspace lifecycle record

#### Scenario: Run path creation records path plan first
- **WHEN** a Run record or Run support directory is created
- **THEN** the system records the Run path plan and source before any Run logs, prompts, tool-call records, outputs, or Artifacts depend on that path

#### Scenario: Environment-derived paths keep source detail
- **WHEN** a runtime path plan is selected from a supported `ISOMER_*` environment override
- **THEN** the stored path plan records the environment variable name as source detail without storing unrelated environment values

#### Scenario: Historical path plans are not silently rewritten
- **WHEN** the Project Manifest, environment, or built-in defaults would now resolve a different path for an existing runtime record
- **THEN** the system keeps the historical path plan and reports any mismatch as a validation issue rather than silently rewriting dependent records

#### Scenario: Path plan ownership is validated
- **WHEN** a runtime record references a path plan
- **THEN** validation confirms that the path plan belongs to the same Topic Workspace and semantic surface as the referring record
