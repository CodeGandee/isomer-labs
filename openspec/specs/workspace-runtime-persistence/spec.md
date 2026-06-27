# workspace-runtime-persistence Specification

## Purpose
Define topic-scoped Workspace Runtime persistence for initialization, readiness, lifecycle records, path plans, Agent Team Instance records, validation, and inspection before Houmao launch material exists.
## Requirements
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
The system SHALL prepare and record selected Research Topic Pixi environment readiness through explicit `project runtime prepare` commands before Houmao launch material depends on it.

#### Scenario: Runtime prepare requires initialized runtime
- **WHEN** a user runs `isomer-cli project runtime prepare` for a selected Research Topic and Topic Workspace
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
- **THEN** the system reports the issue and directs repair through a Service Request instead of hiding repair work inside `project runtime prepare`

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

### Requirement: Workspace Runtime CLI and API Surface
The system SHALL expose deterministic CLI and Python APIs for Workspace Runtime initialization, inspection, validation, and Agent Team Instance record management.

#### Scenario: Runtime commands are available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface includes `project runtime init`, `project runtime prepare`, `project runtime inspect`, `project runtime validate`, `project team-instances create`, `project team-instances list`, and `project team-instances show`

#### Scenario: Runtime init emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json project runtime init`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, runtime path, created-or-opened status, and diagnostics

#### Scenario: Runtime prepare emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json project runtime prepare`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, readiness records, readiness status, preparation status, and diagnostics

#### Scenario: Team instance list is topic scoped
- **WHEN** a user runs `isomer-cli project team-instances list`
- **THEN** the command lists only Agent Team Instance records from the selected Topic Workspace unless a later accepted contract adds a Project-wide listing mode

#### Scenario: Team instance show reports related records
- **WHEN** a user runs `isomer-cli project team-instances show <agent-team-instance-id>`
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

### Requirement: Adapter Handoff Dispatch Persistence
The system SHALL persist Houmao-backed manual handoff dispatch state through provider-neutral handoff records linked to opaque adapter refs and payload refs.

#### Scenario: Dispatch record is persisted
- **WHEN** a Houmao-backed manual handoff is dispatched
- **THEN** Workspace Runtime records the handoff ref, Agent Team Instance ref, source Agent Instance ref, target Agent Instance ref, Run or Research Task ref, Execution Adapter ref, dispatch status, expected output refs, Completion Watcher Contract refs, timestamps, diagnostics, adapter payload refs, and Provenance refs

#### Scenario: Dispatch refs are opaque
- **WHEN** Workspace Runtime records Houmao-specific message ids, mailbox ids, gateway event ids, managed-agent ids, session refs, or command payload ids for a handoff
- **THEN** it stores them as opaque adapter refs, adapter payload refs, or adapter command refs rather than generic handoff, Run, Agent Team Instance, or Agent Instance fields

#### Scenario: Dispatch state is topic scoped
- **WHEN** handoff dispatch state is written
- **THEN** validation requires every linked Agent Team Instance, Agent Instance, Run, Research Task, path plan, Artifact, and adapter payload ref to belong to the selected Topic Workspace

### Requirement: Signal Observation Persistence
The system SHALL persist Houmao mail, gateway, file, command, and bounded inspection signals as Signal Observations linked to runtime lifecycle refs.

#### Scenario: Observation is persisted
- **WHEN** Houmao mail, gateway events, files, command output, or inspection snapshots indicate handoff progress, failure, or candidate completion
- **THEN** Workspace Runtime records a Signal Observation with handoff ref, Run ref when known, Agent Team Instance ref, Agent Instance refs when known, adapter refs, adapter payload refs, timestamp, diagnostics, and Provenance refs

#### Scenario: Observation does not silently change lifecycle
- **WHEN** a Signal Observation suggests candidate completion or failure
- **THEN** Workspace Runtime keeps the observation visible without silently changing handoff, Run, Agent Team Instance, or Workflow Stage Cursor terminal state

#### Scenario: Observation payload is bounded
- **WHEN** an observation includes rich reply text, logs, transcripts, command output, mailbox content, or generated files
- **THEN** Workspace Runtime stores refs to Artifacts, logs, or adapter payload files rather than embedding rich content inline in lifecycle records

### Requirement: Handoff Normalization Persistence
The system SHALL persist accepted, rejected, blocked, superseded, and repair-routed handoff normalization outcomes.

#### Scenario: Accepted normalization is durable
- **WHEN** the Operator Agent accepts a Houmao-observed handoff result
- **THEN** Workspace Runtime records accepted handoff state, Run updates, output Artifact refs, normalization rationale, actor ref, timestamp, and Provenance refs

#### Scenario: Rejected or repair-routed normalization is durable
- **WHEN** the Operator Agent rejects a candidate result, blocks it, supersedes it, or routes repair
- **THEN** Workspace Runtime records the outcome status, rationale, affected Signal Observation refs, produced refs when retained, corrective Service Request or follow-up handoff refs when present, actor ref, timestamp, and Provenance refs

#### Scenario: Normalization state survives restart
- **WHEN** Isomer restarts after a handoff dispatch, observation, or normalization
- **THEN** Workspace Runtime can reconstruct the handoff state, linked Signal Observations, output refs, adapter payload refs, and Provenance refs from persisted records

### Requirement: UC-01 Runtime Research Records
The system SHALL persist the minimal research records needed by the UC-01 headless path in Workspace Runtime or file-backed payloads linked from Workspace Runtime.

#### Scenario: Runtime stores UC-01 records
- **WHEN** the UC-01 runner records Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, or Provenance Records
- **THEN** Workspace Runtime stores stable ids, record kinds, statuses, Topic Workspace refs, Research Topic refs, lifecycle refs, content refs when applicable, timestamps, and Provenance refs

#### Scenario: Runtime records remain topic scoped
- **WHEN** a UC-01 runtime record is written
- **THEN** validation confirms that its Research Topic, Topic Workspace, Agent Team Instance, Run, Artifact, Gate, Decision Record, and path refs belong to the selected Topic Workspace

### Requirement: UC-01 Manual Harness Recording
The system SHALL let the manual harness write and read UC-01 research records through generic runtime store helpers without exposing SQL details to product CLI or adapter code.

#### Scenario: Harness writes record bundle
- **WHEN** the UC-01 manual harness accepts a handoff result
- **THEN** runtime helpers can write the associated Artifact, Evidence Item, Finding or claim candidate, Provenance Record, and lifecycle links in one transaction

#### Scenario: Harness reads summary
- **WHEN** the UC-01 manual harness requests a UC-01 summary
- **THEN** harness code returns Research Inquiry, Research Task, Run, handoff, Artifact, Evidence Item, Gate, Decision Record, View Manifest, and Provenance refs needed for deterministic JSON output

### Requirement: UC-01 Harness Validation
The manual harness SHALL validate the UC-01 recording graph and report incomplete vertical-slice state without silently repairing it.

#### Scenario: Missing UC-01 record is reported by the harness
- **WHEN** a UC-01 run is missing a required Artifact, Evidence Item, Gate, Decision Record, View Manifest, or Provenance ref
- **THEN** the harness reports a diagnostic naming the missing record type and referring lifecycle object

#### Scenario: Open follow-up Gate is reported
- **WHEN** a UC-01 follow-up Gate remains open after runner closeout is requested
- **THEN** the harness reports the open Gate as a blocker for UC-01 completion while preserving all recorded options

### Requirement: UC-01 Harness Inspection Summary
The manual harness SHALL include UC-01 research records in deterministic inspection output.

#### Scenario: Runtime inspect reports counts
- **WHEN** a user inspects or validates the Workspace Runtime after a UC-01 run
- **THEN** harness JSON includes counts or summaries for UC-01 Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, and Provenance Records

#### Scenario: Team instance show includes UC-01 refs
- **WHEN** a user shows the UC-01 Agent Team Instance after runner completion
- **THEN** the summary includes linked Research Inquiry, Research Task, Run, handoff, accepted output Artifact, Gate, Decision Record, and View Manifest refs without exposing Houmao native fields

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

### Requirement: Agent Team Instance Instantiation Provenance
The system SHALL record the approved instantiation source when creating Agent Team Instance runtime records.

#### Scenario: Team instance links packet and profile
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile materialized by an approved instantiation packet
- **THEN** Workspace Runtime records or links the Agent Team Instance to the Topic Agent Team Profile ref, Topic Agent Team Profile Bundle ref, packet ref, bundle-local approval ref, project operator actor or session ref, Topic Service Agent refs when used, and validation result provenance

#### Scenario: Runtime creation rejects unapproved packet
- **WHEN** a launch-facing Agent Team Instance creation request references an instantiation packet that is missing, invalid, rejected, or unapproved
- **THEN** Workspace Runtime rejects the create request and leaves existing runtime records unchanged

#### Scenario: Preview profile remains non-launching
- **WHEN** a Topic Agent Team Profile only has preview provenance and no approved instantiation packet with validated approval provenance
- **THEN** launch-facing Agent Team Instance creation reports a diagnostic rather than silently treating synthetic preview defaults as authoritative

#### Scenario: Competing team instance for one topic is rejected
- **WHEN** a launch-facing Agent Team Instance creation request would create a competing active topic team for a Research Topic that already has an active Agent Team Instance lineage
- **THEN** Workspace Runtime rejects the request and explains that topic-level parallelism requires another Research Topic with its own dedicated team

### Requirement: Project Operator and Topic Service Runtime Actor Records
The system SHALL represent project operator provenance and Topic Service Agent provenance distinctly from research team membership.

#### Scenario: Project operator actor or session is recorded
- **WHEN** a Project Operator Session or Operator Agent materializes a profile, creates or launches an Agent Team Instance, dispatches handoffs, dispatches Service Requests, or records task routing decisions
- **THEN** runtime records include project operator actor or session provenance distinct from team member Agent Instances and Service Agent Instances

#### Scenario: Topic Service Agent support is recorded
- **WHEN** a Topic Service Agent supports profile bundle materialization, environment setup, diagnostics, monitoring, or launch preparation
- **THEN** Workspace Runtime or linked support metadata records the Service Request ref, Topic Service Agent ref, support Artifacts, and Provenance Records

#### Scenario: Operators and service agents are not team members by default
- **WHEN** an Agent Team Instance is created from a Topic Agent Team Profile
- **THEN** Workspace Runtime does not add the Project Operator Session, Operator Agent, or Topic Service Agent as a member Agent Instance unless the profile explicitly defines a corresponding operator role inside that research team

### Requirement: Manifest-sourced Runtime Path Plans
Workspace Runtime SHALL persist selected semantic path resolutions before durable runtime records depend on manifest-backed paths.

#### Scenario: Runtime init records semantic path sources
- **WHEN** Workspace Runtime initialization creates path plans for the selected Topic Workspace
- **THEN** each new semantic path plan records `semantic_label`, `scope_ref`, canonical path, source, source detail, and any compatibility surface id used by Workspace Path Resolution

#### Scenario: Manifest source is preserved
- **WHEN** a path plan is selected from the Topic Workspace Manifest
- **THEN** the stored path plan identifies the source as Topic Workspace Manifest-backed, records the semantic label in `semantic_label`, records the selected topic or agent scope in `scope_ref`, and records the manifest path in source detail

#### Scenario: Default profile source is preserved
- **WHEN** a path plan is selected from the built-in `isomer-default.v1` layout profile
- **THEN** the stored path plan identifies the source as default-profile-backed rather than pretending it came from an authored manifest

#### Scenario: Semantic identity is not encoded only in source detail
- **WHEN** a new path plan is created from a semantic label
- **THEN** validation and inspection can read the semantic label and scope from first-class fields without parsing source detail

#### Scenario: Existing path plan precedence is preserved
- **WHEN** a runtime record already references a stored path plan
- **THEN** later path resolution for that record uses the stored path plan before current manifest or default-profile bindings

### Requirement: Runtime Initialization Uses Semantic Surfaces
Workspace Runtime initialization SHALL create only the runtime-owned directories required by semantic resolution for the selected Topic Workspace.

#### Scenario: Runtime init may prepare topic tmp posture without durable dependency
- **WHEN** runtime initialization or an explicit materialization flow owns Topic Workspace local setup
- **THEN** it may create or validate resolved `topic.tmp` and the owning Topic Workspace root ignore rule
- **AND** it does not record tmp contents as durable runtime evidence

#### Scenario: Optional tmp surfaces are not required for minimal runtime init
- **WHEN** runtime initialization runs without repository setup, profile materialization, environment setup, or Agent Workspace setup
- **THEN** it does not require `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp` merely because those labels exist in the default layout profile

### Requirement: Agent Workspace Runtime Records Use Semantic Bindings
Agent Workspace runtime records SHALL use semantic `agent.workspace` resolution rather than hard-coded path assembly as the primary planning contract.

#### Scenario: Agent Workspace setup may prepare agent tmp posture
- **WHEN** Agent Team Instance creation or delegated Agent Workspace setup prepares an Agent Workspace for topic-local Agent Name `alice`
- **THEN** it may create or validate resolved `agent.tmp` and the Topic Main Repository ignore rule that keeps tmp material untracked
- **AND** it does not store files under `agent.tmp` as durable Agent Workspace evidence

### Requirement: Manifest Drift Validation
Workspace Runtime validation SHALL report drift between stored path plans and current semantic resolution without rewriting historical runtime records.

#### Scenario: Manifest change differs from stored path plan
- **WHEN** a stored path plan for a semantic label points to a different path than the current Topic Workspace Manifest binding resolves
- **THEN** validation reports a path-plan drift diagnostic and preserves the stored path plan

#### Scenario: Missing current binding is diagnostic
- **WHEN** a stored path plan references a semantic label that no longer resolves from the current manifest or default profile
- **THEN** validation reports that the historical path plan remains but the current binding is missing

#### Scenario: Drift does not delete files
- **WHEN** validation detects semantic path drift
- **THEN** it does not move, delete, archive, or rewrite files or runtime rows automatically

#### Scenario: Rebinding needs explicit action
- **WHEN** an operator wants a durable record to depend on a new semantic binding
- **THEN** the system requires an explicit migration, repair, or new runtime action rather than silently rebinding existing records

### Requirement: Runtime Inspection Reports Semantic Paths
Runtime inspection SHALL expose semantic path metadata for stored path plans when available.

#### Scenario: Inspect includes semantic labels
- **WHEN** a user inspects Workspace Runtime path plans
- **THEN** the output includes semantic labels, compatibility surface ids when present, canonical paths, sources, source detail, and drift diagnostics when validation has computed them

#### Scenario: Compatibility-only plans remain readable
- **WHEN** an older path plan has only a compatibility surface id and no semantic label metadata
- **THEN** runtime inspection still reports the path plan and maps it to a semantic label when a known alias exists

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

### Requirement: Runtime Validation Handles Local Tmp Surfaces
Workspace Runtime validation SHALL recognize resolved standard tmp-label paths as disposable local material and reject durable dependencies on them.

#### Scenario: Runtime validation reports durable tmp dependencies
- **WHEN** Workspace Runtime validation finds a runtime record, handoff, Artifact locator, Provenance Record, Evidence Item, Decision Record, profile output, or readiness record that depends on a resolved tmp path
- **THEN** it reports a non-durable temporary path diagnostic
- **AND** it does not treat the referring record as ready until the material is promoted to an approved durable surface

#### Scenario: Runtime validation reports tracked tmp contents
- **WHEN** Workspace Runtime validation finds tracked files under a resolved tmp path
- **THEN** it reports that tmp material must stay ignored and disposable unless the content is moved to an approved durable surface

#### Scenario: Runtime validation does not delete tmp
- **WHEN** Workspace Runtime validation finds files under a standard tmp path
- **THEN** it does not delete, move, archive, or promote those files automatically

