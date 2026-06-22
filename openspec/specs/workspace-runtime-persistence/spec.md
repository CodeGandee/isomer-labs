# workspace-runtime-persistence Specification

## Purpose
Define topic-scoped Workspace Runtime persistence for initialization, readiness, lifecycle records, path plans, Agent Team Instance records, validation, and inspection before Houmao launch material exists.
## Requirements
### Requirement: Workspace Runtime Creation and Reopening
The system SHALL create and reopen a Workspace Runtime for a selected Topic Workspace through explicit runtime commands or APIs, with schema metadata and default runtime directories.

#### Scenario: Runtime init creates state and directories
- **WHEN** a user runs the explicit Workspace Runtime initialization command for a valid Research Topic and Topic Workspace
- **THEN** the system creates `state.sqlite` plus `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/` directories under the Topic Workspace

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
- **WHEN** a user runs `doctor`, `validate`, `context show`, `paths preview`, `team-templates`, or Topic Agent Team Profile validation commands
- **THEN** the system does not create `state.sqlite` or Workspace Runtime directories

### Requirement: Workspace Runtime Record Store
The system SHALL store durable runtime records for lifecycle, readiness, team instance, path, and handoff state inside the Topic Workspace's Workspace Runtime.

#### Scenario: Core lifecycle records are stored
- **WHEN** the Workspace Runtime records Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Topic Agent Team Profile ref, Agent Team Instance, Agent Instance, Agent Workspace, path plan, topic environment readiness, or handoff state
- **THEN** each record has a stable id, Topic Workspace id, Research Topic id when applicable, record type, status, created timestamp, updated timestamp, and Provenance Record refs when known

#### Scenario: Runtime records keep refs instead of rich content
- **WHEN** runtime state depends on prompts, command outputs, reports, tables, figures, notes, or logs
- **THEN** the runtime record stores refs to Artifacts, path plans, logs, or Provenance Records instead of embedding rich content inline

#### Scenario: Runtime records are topic scoped
- **WHEN** a runtime record is written
- **THEN** validation requires its Research Topic and Topic Workspace refs to match the selected Workspace Runtime owner

#### Scenario: Runtime record ids remain stable after restart
- **WHEN** the process exits and the Workspace Runtime is reopened
- **THEN** previously created runtime records are recoverable with the same ids, refs, statuses, and path-plan links

### Requirement: Topic Environment Readiness Preparation
The system SHALL prepare and record selected Research Topic Pixi environment readiness through explicit `runtime prepare` commands before Houmao launch material depends on it.

#### Scenario: Runtime prepare requires initialized runtime
- **WHEN** a user runs `isomer-cli runtime prepare` for a selected Research Topic and Topic Workspace
- **THEN** the system requires an initialized current-schema Workspace Runtime before recording readiness state

#### Scenario: Runtime prepare consumes explicit bindings
- **WHEN** runtime preparation checks topic environment readiness
- **THEN** it uses Project Manifest `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings` without inferring bindings from Research Topic ids, Topic Workspace paths, or Pixi environment names

#### Scenario: Runtime prepare records readiness
- **WHEN** runtime preparation completes a readiness check or preparation step
- **THEN** the system records selected environment refs, readiness status, readiness diagnostics, checked or prepared timestamp, actor ref when known, and Provenance Record refs

#### Scenario: Readiness status is explicit
- **WHEN** a topic environment readiness record is inspected
- **THEN** its status is one of `ready`, `failed`, `blocked`, `stale`, or `superseded`, or a later accepted contract has explicitly extended the status set

#### Scenario: Missing readiness has no placeholder record
- **WHEN** no readiness preparation has been recorded for a selected Research Topic and Topic Workspace
- **THEN** the system represents readiness as missing by the absence of a readiness record rather than by creating an `unknown` readiness record

#### Scenario: Runtime prepare keeps repair explicit
- **WHEN** readiness preparation discovers missing dependencies, incompatible environments, or setup work that mutates Project, Topic Workspace, dependency, runtime, or environment state beyond bounded preparation
- **THEN** the system reports the issue and directs repair through a Service Request instead of hiding repair work inside `runtime prepare`

#### Scenario: Readiness is topic scoped
- **WHEN** a readiness record is written
- **THEN** validation requires the readiness record to belong to the selected Research Topic and Topic Workspace and rejects cross-topic reuse

#### Scenario: Failed readiness is durable
- **WHEN** runtime preparation cannot establish readiness
- **THEN** the system records `failed` or `blocked` readiness diagnostics and does not mark the selected Topic Workspace as prepared for Houmao launch

### Requirement: Agent Team Instance Record Instantiation
The system SHALL instantiate Agent Team Instance records from validated Topic Agent Team Profiles without launching agents or creating adapter-specific launch material.

#### Scenario: Team instance create consumes a profile
- **WHEN** a user creates an Agent Team Instance record from a Topic Agent Team Profile
- **THEN** the system validates the selected Effective Topic Context, Project Manifest registration, Topic Agent Team Profile, and source Domain Agent Team Template before writing runtime records

#### Scenario: Active roles create agent records
- **WHEN** the selected Topic Agent Team Profile has active Agent Role bindings
- **THEN** the system creates Agent Instance records and Agent Workspace records for those active role bindings under the same Agent Team Instance

#### Scenario: Agent workspaces are materialized from path plans
- **WHEN** Agent Instance records require Agent Workspaces
- **THEN** the system resolves and records Agent Workspace path plans before creating the Agent Workspace directories and Agent Workspace records

#### Scenario: Duplicate team instance id is rejected
- **WHEN** a create request names an Agent Team Instance id that already exists in the selected Workspace Runtime
- **THEN** the system rejects the request with a validation diagnostic and leaves existing records unchanged

#### Scenario: Houmao launch material is out of scope
- **WHEN** an Agent Team Instance record is created in Milestone 4
- **THEN** the system does not create Houmao launch dossiers, mailboxes, gateways, managed-agent ids, live process ids, or adapter launch facts

### Requirement: Workspace Runtime CLI and API Surface
The system SHALL expose deterministic CLI and Python APIs for Workspace Runtime initialization, inspection, validation, and Agent Team Instance record management.

#### Scenario: Runtime commands are available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface includes `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show`

#### Scenario: Runtime init emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json runtime init`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, runtime path, created-or-opened status, and diagnostics

#### Scenario: Runtime prepare emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json runtime prepare`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, readiness records, readiness status, preparation status, and diagnostics

#### Scenario: Team instance list is topic scoped
- **WHEN** a user runs `isomer-cli team-instances list`
- **THEN** the command lists only Agent Team Instance records from the selected Topic Workspace unless a later accepted contract adds a Project-wide listing mode

#### Scenario: Team instance show reports related records
- **WHEN** a user runs `isomer-cli team-instances show <agent-team-instance-id>`
- **THEN** the command reports the Agent Team Instance record, Agent Instance refs, Agent Workspace refs, active Run refs when known, Workflow Stage Cursor refs, status, blocker refs, and diagnostics

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

### Requirement: Houmao CLI adapter command records
The system SHALL persist Houmao CLI adapter command runs and payload references as Workspace Runtime records linked to generic Isomer runtime records.

#### Scenario: Command run is persisted
- **WHEN** the Houmao adapter invokes `houmao-mgr --print-json`
- **THEN** Workspace Runtime records the command run id, Agent Team Instance ref when known, Agent Instance ref when known, Execution Adapter ref, operation kind, sanitized argv, cwd ref, payload refs, exit status, timestamp, diagnostics, and Provenance refs

#### Scenario: Raw command output is file-backed
- **WHEN** Houmao CLI output is safe to retain after redaction checks
- **THEN** the adapter stores the raw or normalized payload as a durable file-backed adapter payload ref instead of embedding rich command output inline in lifecycle records

#### Scenario: Command records survive restart
- **WHEN** Isomer restarts after a launch, inspect, prepare-only, or stop command
- **THEN** the Workspace Runtime can reconstruct the adapter command history and linked manifest refs for the Agent Team Instance from persisted records

### Requirement: Houmao launch attempt persistence
The system SHALL persist quick-launch and prepare-only adapter outcomes separately from generic Agent Team Instance identity.

#### Scenario: Launch attempt links generic and adapter refs
- **WHEN** a Houmao-backed quick launch starts
- **THEN** Workspace Runtime records a launch attempt with Agent Team Instance ref, selected Agent Instance refs, Execution Adapter ref, launch material refs, adapter manifest refs, per-agent command refs, status, diagnostics, timestamps, and Provenance refs

#### Scenario: Prepare-only outcome is not launched state
- **WHEN** launch material is prepared without running Houmao launch commands
- **THEN** Workspace Runtime records materialization and manifest refs without marking the Agent Team Instance or Agent Instances as launched or active

#### Scenario: Partial launch keeps known mappings
- **WHEN** a quick launch partially succeeds
- **THEN** Workspace Runtime stores known Agent Instance to Houmao adapter ref mappings, failed command diagnostics, manifest refs, and recovery status without deleting started-agent records

### Requirement: Houmao inspection and stop persistence
The system SHALL persist Houmao live inspection snapshots and stop outcomes as adapter-linked runtime records.

#### Scenario: Inspection snapshot is bounded
- **WHEN** live inspection returns Houmao state
- **THEN** Workspace Runtime records or returns a bounded inspection snapshot linked to Agent Team Instance refs, Agent Instance refs when known, adapter refs, manifest refs, timestamp, diagnostics, and Provenance refs

#### Scenario: Stop outcome is preserved
- **WHEN** a Houmao stop command completes
- **THEN** Workspace Runtime records stopped, failed, partial, or stale outcome state with target refs, command refs, remaining live refs when known, diagnostics, timestamp, and Provenance refs

#### Scenario: Generic records do not contain Houmao internals
- **WHEN** Workspace Runtime stores Houmao managed-agent ids, profile names, tmux session refs, mailbox refs, gateway refs, or project overlay refs
- **THEN** those values remain in opaque adapter refs, adapter payload refs, manifests, or adapter tables rather than generic Agent Team Instance, Agent Instance, Run, handoff, or Artifact core fields

### Requirement: JSON Adapter Manifest Refs
The system SHALL persist Houmao adapter JSON manifest refs through opaque adapter payload refs linked to generic Workspace Runtime records.

#### Scenario: Manifest refs are adapter scoped
- **WHEN** Workspace Runtime stores refs to `adapter-link.json`, `launch-material-manifest.json`, or `adapter-runtime-manifest.json`
- **THEN** those refs are stored as adapter payload refs linked to Agent Team Instance, Agent Instance, Run, handoff, Artifact, path plan, and Provenance records without adding Houmao-specific generic fields

#### Scenario: Manifest refs survive restart
- **WHEN** a Houmao-backed Agent Team Instance is inspected after process restart
- **THEN** Workspace Runtime can resolve the stored JSON manifest refs and reconstruct the adapter state summary before optionally performing live Houmao inspection

### Requirement: Reconciliation Record Persistence
The system SHALL persist explicit reconciliation and adoption outcomes for Houmao-backed Agent Team Instances.

#### Scenario: Reconciliation is recorded
- **WHEN** a reconcile command records an outcome for a Houmao-backed Agent Team Instance
- **THEN** Workspace Runtime stores the reconciliation state, manifest digest summary, live observation summary, mapping confidence, diagnostics, timestamp, actor ref, and Provenance refs

#### Scenario: Adoption links external runtime
- **WHEN** an adopt command accepts externally launched Houmao runtime state
- **THEN** Workspace Runtime records the adopted adapter refs and Agent Instance mappings while preserving existing generic Agent Team Instance identity

#### Scenario: Drift does not delete records
- **WHEN** reconciliation reports drift, conflict, stale state, or rejection
- **THEN** Workspace Runtime preserves prior launch, manifest, adapter, Artifact, and Provenance refs and records the new diagnostic outcome separately

### Requirement: Generic Runtime Schema Boundary
The system SHALL keep Houmao manifest and runtime details out of generic Workspace Runtime schema fields.

#### Scenario: Generic inspection hides Houmao field names
- **WHEN** generic Isomer APIs inspect Agent Team Instance, Agent Instance, Run, handoff, or Artifact records linked to Houmao manifests
- **THEN** the records expose generic refs and adapter payload refs, not generic fields named after Houmao project profiles, gateways, mailboxes, managed agents, sessions, or native manifest paths

