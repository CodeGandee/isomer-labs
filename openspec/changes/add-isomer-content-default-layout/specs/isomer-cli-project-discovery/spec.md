## MODIFIED Requirements

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration, the Project-local generated content root, and the Project-level Houmao overlay without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli project init` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `isomer-content/topic-ws/default/`, a Project-local generated content root at `isomer-content/`, and a Project-level Houmao overlay at `.houmao/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli project init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name under `isomer-content/topic-ws/`

#### Scenario: Initialize records path defaults
- **WHEN** `isomer-cli project init` writes the Project Manifest
- **THEN** the Project Manifest includes path defaults for `isomer_content_root = "isomer-content"` and `topic_workspace_base_dir = "isomer-content/topic-ws"`

#### Scenario: Initialize creates content root policy files
- **WHEN** `isomer-cli project init` creates the Project-local generated content root
- **THEN** it writes `isomer-content/README.md` and `isomer-content/.gitignore`, and the `.gitignore` ignores generated contents while keeping `README.md` and `.gitignore` trackable

#### Scenario: Initialize creates Houmao project overlay
- **WHEN** `isomer-cli project init` completes successfully
- **THEN** the system has invoked the supported Houmao CLI project initialization boundary for the Project root and reports the resolved Houmao Project overlay path in deterministic text or JSON output

#### Scenario: Initialize does not create runtime database
- **WHEN** `isomer-cli project init` completes
- **THEN** the system does not create `state.sqlite` or any Workspace Runtime database

#### Scenario: Initialize does not create runtime or live Houmao launch state
- **WHEN** `isomer-cli project init` completes
- **THEN** the system does not create Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, Houmao managed agents, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Houmao bootstrap failure blocks project init
- **WHEN** a user runs `isomer-cli project init` and the required Houmao command boundary is unavailable or returns a failing result
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, does not create `isomer-content/`, and does not claim that the Isomer Project was initialized

#### Scenario: Existing project is not overwritten
- **WHEN** a user runs `isomer-cli project init` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest and does not offer a force-overwrite behavior in Milestone 1

### Requirement: Workspace Path Preview
The system SHALL preview Workspace Path Resolution outputs, including Project generated-content defaults, without creating Workspace Runtime state.

#### Scenario: Path preview shows generated content root
- **WHEN** a user runs `isomer-cli project paths preview` for a Project with generated-content path defaults
- **THEN** the output includes the generated content root path and labels whether it came from the Project Manifest or a built-in default

#### Scenario: Path preview shows topic workspace defaults
- **WHEN** a user runs `isomer-cli project paths preview` for a registered Research Topic without a configured Topic Workspace path
- **THEN** the output derives the Topic Workspace path as `<project>/isomer-content/topic-ws/<topic-id>/` and labels the source as `default`

#### Scenario: Path preview applies precedence
- **WHEN** a path surface has candidates from a supported `ISOMER_*` path override, Project Manifest default, and built-in default
- **THEN** the preview applies the Milestone 1 precedence of environment, manifest, then default and reports the chosen source

#### Scenario: Recorded plan source is unavailable in Milestone 1
- **WHEN** `isomer-cli project paths preview` runs before Workspace Runtime and recorded workspace plans are implemented
- **THEN** the command does not report any resolved path as coming from a recorded plan source

#### Scenario: Path preview validates bounds
- **WHEN** a resolved path points outside the Project root
- **THEN** the preview rejects the path without applying an external-root allowlist in Milestone 1

#### Scenario: Path preview is side-effect free
- **WHEN** `isomer-cli project paths preview` resolves generated content root, Topic Workspace, Workspace Runtime, Artifact, Run, log, View Manifest, or Agent Workspace paths
- **THEN** the command does not create `isomer-content/`, `state.sqlite`, Run directories, Artifact directories, Agent Workspace directories, or View Manifest directories by default

## ADDED Requirements

### Requirement: Project Manifest Path Defaults Validation
The system SHALL validate Project Manifest path defaults used for generated content and Topic Workspace bases before command behavior depends on them.

#### Scenario: Content path defaults stay project scoped
- **WHEN** the Project Manifest declares `isomer_content_root` or `topic_workspace_base_dir`
- **THEN** validation resolves each path relative to the Project root and rejects paths outside the Project root

#### Scenario: Content root stays out of project config
- **WHEN** the Project Manifest declares `isomer_content_root`
- **THEN** validation rejects values that resolve inside `.isomer-labs/`

#### Scenario: Explicit topic workspace registrations still win
- **WHEN** a Project Manifest registers an explicit Topic Workspace path such as `topic-workspaces/<topic-id>` or another project-local path
- **THEN** validation continues to accept that path when it resolves inside the Project root and does not rewrite it to the new default layout
