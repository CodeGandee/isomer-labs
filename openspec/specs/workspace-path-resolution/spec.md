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
The system SHALL provide built-in project-local defaults for Topic Workspaces, Workspace Runtime files, Run records, Artifacts, View Manifests, logs, and Agent Workspaces.

#### Scenario: Default topic workspace root is visible
- **WHEN** a Project has no configured Topic Workspace root
- **THEN** the resolver uses `<project>/topic-workspaces/` as the built-in Topic Workspace root

#### Scenario: Default topic workspace path is topic scoped
- **WHEN** a Research Topic has no recorded or configured Topic Workspace path
- **THEN** the resolver derives the Topic Workspace path as `<project>/topic-workspaces/<topic-id>/`

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
