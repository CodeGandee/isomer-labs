# workspace-path-resolution Specification

## Purpose
TBD - created by archiving change define-workspace-path-resolution. Update Purpose after archive.
## Requirements
### Requirement: Workspace Path Resolution Precedence
The system SHALL resolve Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, and Agent Workspace paths through a single Workspace Path Resolver using deterministic precedence.

#### Scenario: Recorded workspace plan wins
- **WHEN** a Research Task, Run, handoff, Agent Team Instance, or Agent Instance has a recorded workspace plan for a path surface
- **THEN** the resolver uses the recorded plan value before checking environment variables, Project Manifest defaults, or built-in defaults

#### Scenario: Environment overrides manifest defaults
- **WHEN** no recorded workspace plan value exists and a supported `ISOMER_*` environment variable is set for the path surface
- **THEN** the resolver uses the environment value before checking Project Manifest defaults or built-in defaults

#### Scenario: Manifest defaults override built-in defaults
- **WHEN** no recorded workspace plan value or supported environment override exists and the Project Manifest defines a default for the path surface
- **THEN** the resolver uses the Project Manifest value instead of the built-in default

#### Scenario: Resolution source is reported
- **WHEN** the resolver returns an effective path set
- **THEN** each returned path includes whether it came from `plan`, `env`, `manifest`, or `default`

### Requirement: Effective Topic Context Input
The system SHALL allow Workspace Path Resolution to consume a validated Effective Topic Context from `isomer-cli`, an Operator Agent, or an Execution Adapter before resolving Topic Workspace and related path surfaces.

#### Scenario: Context supplies selected topic
- **WHEN** Workspace Path Resolution receives an Effective Topic Context with Project, Research Topic, and Topic Workspace refs
- **THEN** the resolver uses those refs to select the applicable recorded workspace plan, Project Manifest defaults, and built-in defaults without performing independent Research Topic selection

#### Scenario: Context supplies optional run and agent refs
- **WHEN** Effective Topic Context includes validated Research Task, Run, Agent Team Instance, or Agent Instance refs
- **THEN** the resolver uses those refs to choose applicable task support, run, log, Agent Workspace, Agent Runtime, and Artifact path surfaces according to the existing path precedence rules

#### Scenario: Path precedence is unchanged
- **WHEN** Effective Topic Context is present and a path surface has recorded plan, supported path environment variable, Project Manifest default, or built-in default candidates
- **THEN** the resolver still applies the accepted precedence of recorded plan, environment path override, Project Manifest default, then built-in default

#### Scenario: Topic context does not become durable path truth
- **WHEN** path values are resolved from Effective Topic Context and Workspace Path Resolution inputs
- **THEN** the system records the effective paths and sources in Workspace Runtime or Provenance Records before downstream research work depends on those paths

#### Scenario: Context mismatch blocks path resolution
- **WHEN** Effective Topic Context names a Research Topic, Topic Workspace, Research Task, Run, Agent Team Instance, or Agent Instance that is inconsistent with the Project Manifest or Workspace Runtime refs needed for a path surface
- **THEN** path resolution fails with a validation error instead of choosing a path from an ambiguous or mismatched context

### Requirement: Default Workspace Layout
The system SHALL provide built-in project-local defaults for the Project generated-content root, Topic Workspaces, Workspace Runtime files, Run records, Artifacts, View Manifests, logs, and Agent Workspaces.

#### Scenario: Default generated content root is visible
- **WHEN** a Project has no configured generated content root
- **THEN** the resolver uses `<project>/isomer-content/` as the built-in generated content root

#### Scenario: Default topic workspace root is visible
- **WHEN** a Project has no configured Topic Workspace root
- **THEN** the resolver uses `<project>/isomer-content/topic-ws/` as the built-in Topic Workspace root

#### Scenario: Default topic workspace path is topic scoped
- **WHEN** a Research Topic has no recorded or configured Topic Workspace path
- **THEN** the resolver derives the Topic Workspace path as `<project>/isomer-content/topic-ws/<topic-id>/`

#### Scenario: Workspace runtime defaults exist
- **WHEN** a Topic Workspace is resolved from built-in defaults
- **THEN** the Topic Workspace contains default paths for `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`

#### Scenario: Task support directory defaults exist
- **WHEN** a Research Task has no recorded or configured task support directory
- **THEN** the resolver derives the task support directory under `<topic-workspace>/tasks/<task-id>/`

#### Scenario: Run layout defaults exist
- **WHEN** a Run has no recorded or configured run directory
- **THEN** the resolver derives the Run directory under `<topic-workspace>/runs/<run-id>/` with subpaths for `prompts/`, `tool-calls/`, `logs/`, and `outputs/`

#### Scenario: Agent workspace layout defaults exist
- **WHEN** an Agent Instance needs an Agent Workspace and no recorded or configured Agent Workspace path exists
- **THEN** the resolver derives the Agent Workspace under `<topic-workspace>/agents/<agent-instance-id>/` with subpaths for `runtime/`, `artifacts/`, `scratch/`, and `logs/`

#### Scenario: Artifact class defaults exist
- **WHEN** a skill requests a semantic Artifact class path and no recorded or configured path exists for that class
- **THEN** the resolver derives the class path under the Topic Workspace artifact root using stable class directories for intake, baselines, experiments, analysis, figures, paper, decisions, evidence, findings, and handoffs

### Requirement: Supported Environment Overrides
The system SHALL support a bounded set of `ISOMER_*` environment variables for launch-time path overrides.

#### Scenario: Project and topic workspace roots can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_PROJECT_ROOT`, `ISOMER_PROJECT_CONFIG_DIR`, `ISOMER_TOPIC_WORKSPACE_BASE_DIR`, `ISOMER_CURRENT_TOPIC_WORKSPACE_DIR`, or `ISOMER_TOPIC_WORKSPACE_RUNTIME_DB`
- **THEN** the resolver treats those values as candidate overrides for the current process according to resolution precedence

#### Scenario: Topic workspace subdirectories can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR`, `ISOMER_TOPIC_WORKSPACE_TASKS_DIR`, `ISOMER_TOPIC_WORKSPACE_RUNS_DIR`, `ISOMER_TOPIC_WORKSPACE_VIEWS_DIR`, or `ISOMER_TOPIC_WORKSPACE_LOGS_DIR`
- **THEN** the resolver treats those values as candidate Topic Workspace subdirectory overrides according to resolution precedence

#### Scenario: Agent workspace subdirectories can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_AGENT_WORKSPACE_DIR`, `ISOMER_AGENT_WORKSPACE_RUNTIME_DIR`, `ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR`, `ISOMER_AGENT_WORKSPACE_SCRATCH_DIR`, or `ISOMER_AGENT_WORKSPACE_LOGS_DIR`
- **THEN** the resolver treats those values as candidate Agent Workspace overrides according to resolution precedence

#### Scenario: Unknown variables are ignored
- **WHEN** an environment variable is not part of the supported path override set
- **THEN** the resolver does not use that variable to resolve workspace paths

### Requirement: Path Validation and Durability
The system SHALL canonicalize, validate, and durably record resolved paths before downstream research work depends on them.

#### Scenario: Paths are canonicalized before use
- **WHEN** the resolver accepts a path from a plan, environment variable, manifest default, or built-in default
- **THEN** it canonicalizes the path before returning it to the Operator Agent, Execution Adapter, or Agent Instance

#### Scenario: External paths are rejected by default
- **WHEN** a resolved path points outside the Project root
- **THEN** validation rejects the path unless the recorded workspace plan or Project Manifest explicitly permits the external root

#### Scenario: Resolved paths are recorded
- **WHEN** an Operator Agent, Execution Adapter, or Agent Instance uses a resolved path for a Run, handoff, Artifact, View Manifest, log, or Agent Workspace
- **THEN** the effective path and resolution source are recorded in Workspace Runtime or a Provenance Record before downstream state depends on it

#### Scenario: Missing files remain visible
- **WHEN** Workspace Runtime references an Artifact or path that no longer exists on disk
- **THEN** validation reports the missing file as a workspace issue without silently deleting the durable reference

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

### Requirement: Houmao CLI adapter path plans
The system SHALL resolve and record path plans for Houmao CLI adapter material, command payloads, logs, and snapshots before those files are written or referenced.

#### Scenario: Adapter root is topic scoped
- **WHEN** the Houmao adapter prepares material for an Agent Team Instance
- **THEN** the adapter root resolves under the selected Topic Workspace runtime area or an accepted recorded Topic Workspace path plan and is linked to the Agent Team Instance

#### Scenario: Per-agent material is agent scoped
- **WHEN** the Houmao adapter writes per-Agent Instance launch material
- **THEN** the material resolves under the selected Agent Workspace path plan or an adapter path plan explicitly linked to that Agent Instance

#### Scenario: Command payload paths are durable
- **WHEN** the adapter writes command JSON payloads, sanitized outputs, launch logs, inspection snapshots, stop outcomes, or generated Houmao profile material
- **THEN** each path is recorded as durable adapter material before Workspace Runtime records depend on it

### Requirement: Houmao CLI adapter path validation
The system SHALL validate Houmao adapter paths against Project, Topic Workspace, and Agent Workspace ownership boundaries.

#### Scenario: Generated paths stay out of config and source checkouts
- **WHEN** the adapter generates launch material, command payloads, or logs
- **THEN** validation rejects writes into `.isomer-labs/`, the Houmao source checkout, another Topic Workspace, or untracked workspace-local team directories

#### Scenario: External direct Houmao refs remain explicit
- **WHEN** reconciliation or adoption references user-authored Houmao material outside Isomer-generated adapter paths
- **THEN** Workspace Runtime records the external ref source explicitly and validation reports missing or changed files without moving, rewriting, or deleting them

#### Scenario: Missing adapter files remain visible
- **WHEN** a recorded Houmao adapter material file, payload file, manifest, or snapshot is missing
- **THEN** runtime validation reports the missing durable path and preserves the referring adapter, Artifact, and Provenance refs

### Requirement: Houmao JSON Manifest Path Plans
The system SHALL resolve durable path plans for Houmao adapter JSON manifests before writing or relying on those manifests.

#### Scenario: Manifest path is topic scoped
- **WHEN** the adapter creates `adapter-link.json`, `launch-material-manifest.json`, or `adapter-runtime-manifest.json` for an Agent Team Instance
- **THEN** each manifest path resolves under the selected Topic Workspace or an accepted Topic Workspace path plan and is recorded as durable runtime evidence

#### Scenario: Manifest path is not cache-like
- **WHEN** a Houmao adapter JSON manifest is written or updated
- **THEN** the path plan or Artifact locator marks the file as durable adapter runtime evidence rather than disposable cache material

### Requirement: Direct Houmao Path References
The system SHALL validate and record referenced Houmao project overlay paths without treating them as Isomer-owned generated launch material.

#### Scenario: Direct material path is adopted
- **WHEN** a user adopts direct Houmao launch material from a project overlay path outside Isomer-generated launch-material paths
- **THEN** the system records the path as adapter-external or user-authored launch material with digest, source, diagnostics, and Provenance refs

#### Scenario: External path requires explicit adoption
- **WHEN** reconciliation discovers a Houmao launch-material path that is outside recorded Topic Workspace or Agent Workspace path plans
- **THEN** the system reports the path as externally detected and does not treat it as trusted launch material until an explicit adopt operation accepts it

#### Scenario: Missing referenced path is diagnostic
- **WHEN** a JSON manifest references a launch-material, native runtime, log, or snapshot path that no longer exists
- **THEN** runtime validation reports a missing durable path diagnostic without deleting adapter, Artifact, or Provenance refs

### Requirement: Adapter Handoff Path Plans
The system SHALL resolve and record path plans for Houmao handoff payloads, observations, normalization artifacts, and logs before Workspace Runtime records depend on those files.

#### Scenario: Handoff payload root is topic scoped
- **WHEN** the Houmao adapter writes handoff dispatch payloads, mailbox payload copies, gateway payload copies, or command payloads
- **THEN** the payload root resolves under the selected Topic Workspace or an accepted Topic Workspace path plan

#### Scenario: Agent-scoped handoff files are agent scoped
- **WHEN** the adapter writes per-Agent Instance handoff payloads or observation files
- **THEN** the generated files resolve under the corresponding Agent Workspace or a recorded Agent Workspace path plan

#### Scenario: Path plans precede handoff files
- **WHEN** the adapter writes dispatch payloads, observation snapshots, normalization artifacts, mailbox metadata, gateway metadata, or adapter logs
- **THEN** Workspace Runtime records the semantic path plan and source before those files are referenced by handoff, Signal Observation, Artifact, or Provenance records

#### Scenario: Handoff payloads are not cache-like
- **WHEN** adapter handoff payloads, observations, normalization artifacts, or logs are written for a handoff round
- **THEN** the path plan or Artifact locator marks them as durable handoff evidence rather than cache-like generated material

#### Scenario: Adapter paths preserve source detail
- **WHEN** adapter paths come from supported `ISOMER_*` path overrides, Project Manifest defaults, Topic Workspace plans, or Agent Workspace plans
- **THEN** the stored path plans preserve source and source detail without storing unrelated environment values

#### Scenario: External handoff material is rejected by default
- **WHEN** a handoff payload, observation, normalization artifact, or log path resolves outside the Project root or selected Topic Workspace without an accepted external-root contract
- **THEN** validation rejects the path before downstream records depend on it

### Requirement: Adapter Observation and Log Paths
The system SHALL keep Houmao adapter observations, mailbox or gateway snapshots, normalization artifacts, and logs under recorded Workspace Runtime path plans.

#### Scenario: Observation snapshot path is planned
- **WHEN** adapter observation persists a mailbox, gateway, file, command, or inspection snapshot
- **THEN** the snapshot path is recorded as a path plan or Artifact locator before the snapshot is referenced by Workspace Runtime

#### Scenario: Normalization artifact path is planned
- **WHEN** Operator Agent normalization creates or retains an output Artifact, rejection rationale, repair payload, or follow-up handoff payload
- **THEN** the file path is recorded through Workspace Path Resolution before downstream diagnostics or research records depend on it

#### Scenario: Adapter log path is planned
- **WHEN** the Houmao adapter writes handoff dispatch, observe, normalize, mailbox, gateway, or diagnostic logs
- **THEN** the log path is recorded through Workspace Path Resolution before downstream diagnostics depend on it

#### Scenario: Missing adapter files remain visible
- **WHEN** an adapter handoff payload, observation snapshot, normalization artifact, or log path no longer exists
- **THEN** runtime validation reports the missing durable path without deleting the adapter, Artifact, Signal Observation, handoff, or Provenance refs

### Requirement: Project Generated Content Root
The system SHALL resolve a Project generated-content root through Workspace Path Resolution so CLI commands and skills can share the same default location for generated material.

#### Scenario: Manifest content root overrides built-in root
- **WHEN** no recorded workspace plan or supported environment override exists and the Project Manifest defines `isomer_content_root`
- **THEN** the resolver uses that Project Manifest value instead of the built-in `<project>/isomer-content/` default

#### Scenario: Content root is project scoped
- **WHEN** the resolver accepts a generated-content root from the Project Manifest or built-in default
- **THEN** it canonicalizes the path and rejects it if the path points outside the Project root or inside `.isomer-labs/`

#### Scenario: Topic workspace base can depend on content root
- **WHEN** the Project Manifest defines `isomer_content_root` but does not define `topic_workspace_base_dir`
- **THEN** the resolver derives the built-in Topic Workspace root under the effective content root as `<isomer-content-root>/topic-ws/`

#### Scenario: Existing topic workspace base alias remains supported
- **WHEN** the Project Manifest defines `topic_workspace_base_dir`
- **THEN** the resolver uses that value for default Topic Workspace derivation and does not require the value to equal `isomer-content/topic-ws`

