## MODIFIED Requirements

### Requirement: Durable Research Record Identity
The system SHALL define durable research records for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates inside a Topic Workspace.

#### Scenario: Record ids are stable within a Topic Workspace
- **WHEN** the system creates an Artifact, Provenance Record, Evidence Item, Finding, Research Claim, Decision Record, or Gate
- **THEN** the record has a stable id, `topic_workspace_id`, created timestamp, updated timestamp, status, and record type

#### Scenario: Records carry lifecycle refs
- **WHEN** a record is created for bounded research work
- **THEN** the record carries applicable refs to accepted Research Lifecycle State objects such as Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, Agent Team Instance, Agent Instance, or Agent Workspace

#### Scenario: Records do not define lifecycle state machines
- **WHEN** a durable research record references a Research Lifecycle State object
- **THEN** the record stores the lifecycle ref and does not redefine that lifecycle object's status set, transition rules, parallel execution scope, or relationship policy

#### Scenario: Rich content stays file-backed
- **WHEN** a record needs rich text, large JSON, tables, figures, logs, prompts, tool outputs, or reports
- **THEN** the record references an Artifact or other file-backed content instead of requiring the rich content to be stored inline
