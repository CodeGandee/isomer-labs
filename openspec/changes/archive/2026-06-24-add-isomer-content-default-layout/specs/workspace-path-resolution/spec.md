## MODIFIED Requirements

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

## ADDED Requirements

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
