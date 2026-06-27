## MODIFIED Requirements

### Requirement: Workspace Runtime Creation and Reopening
The system SHALL create and reopen a Workspace Runtime for a selected Topic Workspace through explicit runtime commands or APIs, with schema metadata and default runtime directories.

#### Scenario: Runtime init creates state and directories
- **WHEN** a user runs the explicit Workspace Runtime initialization command for a valid Research Topic and Topic Workspace
- **THEN** the system creates `state.sqlite`, `repos/`, `agents/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, and `runtime/` directories under the Topic Workspace

#### Scenario: Runtime init does not create per-agent untracked shares
- **WHEN** Workspace Runtime is initialized before Agent Workspaces are prepared
- **THEN** the system does not create `isomer-managed/agent-owned/`, `isomer-managed/topic-owned/`, or `isomer-managed/links/` inside any Agent Workspace

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
The system SHALL instantiate Agent Team Instance records from validated Topic Agent Team Profiles without launching agents or creating adapter-specific launch material.

#### Scenario: Team instance create consumes a profile
- **WHEN** a user creates an Agent Team Instance record from a Topic Agent Team Profile
- **THEN** the system validates the selected Effective Topic Context, Project Manifest registration, Topic Agent Team Profile, and source Domain Agent Team Template before writing runtime records

#### Scenario: Active roles create agent records
- **WHEN** the selected Topic Agent Team Profile has active Agent Role bindings
- **THEN** the system creates Agent Instance records and Agent Workspace records for those active role bindings under the same Agent Team Instance

#### Scenario: Approved workspace refs create path plans
- **WHEN** an active Agent Role binding has a validated `agent_name`, expected branch namespace, and `agent_workspace_ref` under the selected Topic Workspace
- **THEN** Agent Team Instance creation records the Agent Workspace path plan and `isomer-managed/` support path plan from those refs before creating the Agent Workspace directory and Agent Workspace record

#### Scenario: Agent workspaces require planning identity
- **WHEN** an active Agent Role binding does not have an approved `agent_workspace_ref` or validated topic-local `agent_name`
- **THEN** the system reports a missing Agent Workspace planning diagnostic instead of silently creating `<topic-workspace>/agents/<agent-instance-id>`

#### Scenario: Duplicate team instance id is rejected
- **WHEN** a create request names an Agent Team Instance id that already exists in the selected Workspace Runtime
- **THEN** the system rejects the request with a validation diagnostic and leaves existing records unchanged

#### Scenario: Houmao launch material is out of scope
- **WHEN** an Agent Team Instance record is created in Milestone 4
- **THEN** the system does not create Houmao launch dossiers, mailboxes, gateways, managed-agent ids, live process ids, or adapter launch facts

### Requirement: Workspace Runtime Validation
The system SHALL validate Workspace Runtime records and report durable workspace issues without silently deleting or repairing records.

#### Scenario: Broken runtime refs are reported
- **WHEN** a runtime record references a missing Research Topic, Research Inquiry, Research Task, Run, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Agent Workspace, Artifact, Gate, Research Claim, Evidence Item, Decision Record, or Provenance Record
- **THEN** runtime validation reports the broken ref and identifies the referring record

#### Scenario: Missing readiness blocks launch preparation
- **WHEN** an Agent Team Instance or future launch-facing operation requires topic environment readiness and no successful readiness record exists
- **THEN** runtime validation reports the missing readiness record as a blocker for that launch-facing operation

#### Scenario: Missing Agent Workspace is reported
- **WHEN** an Agent Workspace record points to a project-local directory that no longer exists
- **THEN** runtime validation reports the missing Agent Workspace without deleting the record

#### Scenario: Missing Isomer-managed support path is reported
- **WHEN** an Agent Workspace record points to a standard worker worktree but the recorded `isomer-managed/` support path is missing
- **THEN** runtime validation reports the missing Isomer-managed support path without creating it silently

#### Scenario: Invalid lifecycle transition is reported
- **WHEN** a runtime lifecycle transition lacks actor, timestamp, previous status, next status, or rationale
- **THEN** runtime validation reports the transition as incomplete

#### Scenario: Stale handoff is reported
- **WHEN** a handoff state record is open beyond its recorded staleness threshold or has unresolved Completion Watcher Contract observations
- **THEN** runtime validation reports the handoff as stale without marking the delegated work complete

#### Scenario: Cross-topic leakage is reported
- **WHEN** a runtime record in one Topic Workspace references another Research Topic's Topic Workspace, Agent Team Instance, Agent Workspace, Run, Artifact, or path plan
- **THEN** runtime validation reports cross-topic leakage and names both conflicting refs when available

#### Scenario: Recording graph issues are included
- **WHEN** runtime validation sees unresolved Gates, supported Research Claims without valid Evidence Items, or records changed after their latest Provenance Record
- **THEN** it reports those recording graph issues in the same deterministic diagnostic stream as lifecycle and path issues

## ADDED Requirements

### Requirement: Isomer-Managed Runtime Metadata
The system SHALL persist enough metadata to validate `isomer-managed/` workspace boundaries without treating untracked large or temporary shares as durable research records by default.

#### Scenario: Agent Workspace record stores boundary refs
- **WHEN** an Agent Workspace record is created for a standard worktree
- **THEN** it stores or links the topic-local agent name, Agent Workspace path plan, `isomer-managed/` path plan, expected branch namespace, boundary material refs, and generated-link summary when known

#### Scenario: Untracked share dependencies require promotion
- **WHEN** a runtime record, handoff, Artifact, Finding, or Evidence Item depends on a file under `isomer-managed/agent-owned/` or `isomer-managed/topic-owned/`
- **THEN** Workspace Runtime records a diagnostic unless the dependency is promoted into a durable record, tracked Isomer material, or explicit Provenance Record

#### Scenario: Owner reader violations are recorded as diagnostics
- **WHEN** validation detects peer writes into an agent-owned public share without boundary permission
- **THEN** Workspace Runtime records or reports an owner/reader diagnostic linked to the affected Agent Workspace refs

#### Scenario: Legacy support refs remain visible
- **WHEN** an existing runtime record references `.isomer-agent/` support paths
- **THEN** validation reports a legacy support-path diagnostic and keeps the historical ref visible instead of rewriting it silently
