## MODIFIED Requirements

### Requirement: Default Workspace Layout
The system SHALL provide built-in project-local defaults for the Project generated-content root, Topic Workspaces, Workspace Runtime files, Topic Main repositories, Isomer-managed worker-facing paths, owner-preserved records, runtime internals, and Agent Workspace worktrees.

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
- **THEN** the Topic Workspace contains default paths for `state.sqlite`, `repos/`, `repos/topic-main/`, `repos/topic-main/isomer-managed/`, `agents/`, `records/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, and `runtime/`

#### Scenario: Isomer-managed tracked defaults exist
- **WHEN** a Topic Main Repository is resolved from built-in defaults
- **THEN** the resolver derives tracked Isomer paths under `<topic-workspace>/repos/topic-main/isomer-managed/tracked/` for `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `tools/`, `boundaries/`, and `manifests/`

#### Scenario: Task support directory defaults exist
- **WHEN** a Research Task has no recorded or configured task support directory
- **THEN** the resolver derives the owner-preserved task support directory under `<topic-workspace>/records/tasks/<task-id>/`

#### Scenario: Run layout defaults exist
- **WHEN** a Run has no recorded or configured run directory
- **THEN** the resolver derives the owner-preserved Run directory under `<topic-workspace>/records/runs/<run-id>/` with subpaths for `prompts/`, `tool-calls/`, `logs/`, and `outputs/`

#### Scenario: Agent workspace layout defaults exist
- **WHEN** an Agent Instance needs an Agent Workspace and the launch context supplies a validated topic-local agent name
- **THEN** the resolver derives the Agent Workspace under `<topic-workspace>/agents/<agent-name>/` with Isomer-managed support paths under `<topic-workspace>/agents/<agent-name>/isomer-managed/`

#### Scenario: Agent workspace id fallback is not silent
- **WHEN** an Agent Instance needs an Agent Workspace and no recorded workspace plan or validated topic-local agent name exists
- **THEN** the resolver reports a missing Agent Workspace planning diagnostic instead of silently deriving `<topic-workspace>/agents/<agent-instance-id>/`

#### Scenario: Agent-owned support defaults exist
- **WHEN** an Agent Workspace path is resolved
- **THEN** the resolver derives `isomer-managed/agent-owned/runtime/`, `isomer-managed/agent-owned/artifacts/`, `isomer-managed/agent-owned/scratch/`, `isomer-managed/agent-owned/logs/`, `isomer-managed/agent-owned/public/`, and `isomer-managed/agent-owned/inbox/` beneath that Agent Workspace

#### Scenario: Topic-owned projection defaults exist
- **WHEN** an Agent Workspace path is resolved
- **THEN** the resolver derives `isomer-managed/topic-owned/readonly/`, `isomer-managed/topic-owned/writable/`, and `isomer-managed/links/` beneath that Agent Workspace

#### Scenario: Artifact class defaults exist
- **WHEN** a skill requests a semantic Artifact class path and no recorded or configured path exists for that class
- **THEN** the resolver derives the class path under the Topic Workspace artifact record root using stable class directories for intake, baselines, experiments, analysis, figures, paper, decisions, evidence, findings, and handoffs

### Requirement: Supported Environment Overrides
The system SHALL support a bounded set of `ISOMER_*` environment variables for launch-time path overrides and SHALL distinguish owner-preserved record surfaces from worker-visible Isomer-managed surfaces.

#### Scenario: Project and topic workspace roots can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_PROJECT_ROOT`, `ISOMER_PROJECT_CONFIG_DIR`, `ISOMER_TOPIC_WORKSPACE_BASE_DIR`, `ISOMER_CURRENT_TOPIC_WORKSPACE_DIR`, or `ISOMER_TOPIC_WORKSPACE_RUNTIME_DB`
- **THEN** the resolver treats those values as candidate overrides for the current process according to resolution precedence

#### Scenario: Topic repository and Isomer-managed roots can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_TOPIC_MAIN_REPO_DIR`, `ISOMER_TOPIC_MAIN_ISOMER_MANAGED_DIR`, or `ISOMER_TOPIC_MAIN_TRACKED_DIR`
- **THEN** the resolver treats those values as candidate overrides for `repos/topic-main`, `repos/topic-main/isomer-managed`, or `repos/topic-main/isomer-managed/tracked` according to resolution precedence

#### Scenario: Topic workspace owner record subdirectories can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR`, `ISOMER_TOPIC_WORKSPACE_TASKS_DIR`, `ISOMER_TOPIC_WORKSPACE_RUNS_DIR`, `ISOMER_TOPIC_WORKSPACE_VIEWS_DIR`, or `ISOMER_TOPIC_WORKSPACE_LOGS_DIR`
- **THEN** the resolver treats those values as compatibility candidate overrides for owner-preserved `records/artifacts`, `records/tasks`, `records/runs`, `records/views`, and `records/logs` and records source detail that the legacy variable name was used

#### Scenario: Agent workspace and Isomer-managed root can be overridden
- **WHEN** an Execution Adapter exports `ISOMER_AGENT_WORKSPACE_DIR`, `ISOMER_AGENT_ISOMER_MANAGED_DIR`, `ISOMER_AGENT_OWNED_DIR`, `ISOMER_AGENT_TOPIC_OWNED_DIR`, or `ISOMER_AGENT_LINKS_DIR`
- **THEN** the resolver treats those values as candidate Agent Workspace, agent-owned, topic-owned projection, or generated-link overrides according to resolution precedence

#### Scenario: Legacy agent support variables map to agent-owned support
- **WHEN** an Execution Adapter exports `ISOMER_AGENT_WORKSPACE_RUNTIME_DIR`, `ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR`, `ISOMER_AGENT_WORKSPACE_SCRATCH_DIR`, or `ISOMER_AGENT_WORKSPACE_LOGS_DIR`
- **THEN** the resolver treats those values as compatibility candidate overrides for `isomer-managed/agent-owned/runtime`, `isomer-managed/agent-owned/artifacts`, `isomer-managed/agent-owned/scratch`, or `isomer-managed/agent-owned/logs` and records source detail that the legacy variable name was used

#### Scenario: Unknown variables are ignored
- **WHEN** an environment variable is not part of the supported path override set
- **THEN** the resolver does not use that variable to resolve workspace paths

### Requirement: Runtime Path Plan Persistence
The system SHALL persist selected Workspace Path Resolution outputs as Workspace Runtime path plans before dependent runtime records use those paths.

#### Scenario: Runtime init records topic workspace paths
- **WHEN** Workspace Runtime is initialized
- **THEN** the system records path plans for `state.sqlite`, `repos/`, `repos/topic-main/`, `repos/topic-main/isomer-managed/`, `agents/`, `records/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, and `runtime/` with canonical paths and resolution sources

#### Scenario: Agent workspace creation records path plan first
- **WHEN** an Agent Workspace is created for an Agent Instance
- **THEN** the system records the Agent Workspace path plan, topic-local agent name, expected branch namespace, and `isomer-managed/` support path plan before creating the directory or Agent Workspace lifecycle record

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

## ADDED Requirements

### Requirement: Isomer-Managed Path Surfaces
The system SHALL expose named path surfaces for the standard `isomer-managed/` layout so commands, skills, and adapters do not assemble those paths ad hoc.

#### Scenario: Topic-main Isomer-managed surfaces are named
- **WHEN** path preview or runtime path planning returns Topic Main Repository surfaces
- **THEN** the result includes named surfaces for `topic_main_repo`, `topic_main_isomer_managed`, `topic_main_tracked`, `topic_main_tracked_shared`, `topic_main_tracked_artifacts`, `topic_main_tracked_tasks`, `topic_main_tracked_runs`, `topic_main_tracked_views`, `topic_main_tracked_tools`, `topic_main_tracked_boundaries`, and `topic_main_tracked_manifests`

#### Scenario: Agent Isomer-managed surfaces are named
- **WHEN** path preview or runtime path planning returns Agent Workspace surfaces
- **THEN** the result includes named surfaces for `agent_isomer_managed`, `agent_owned`, `agent_runtime`, `agent_artifacts`, `agent_scratch`, `agent_logs`, `agent_public_share`, `agent_inbox`, `agent_topic_readonly`, `agent_topic_writable`, and `agent_links`

#### Scenario: Legacy support surface is not canonical
- **WHEN** a caller asks for an `.isomer-agent/` surface by old name
- **THEN** the resolver reports legacy compatibility diagnostics and returns the corresponding `isomer-managed/agent-owned/` or `isomer-managed/links/` surface when compatibility mode allows it
