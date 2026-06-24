## MODIFIED Requirements

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration, the selected Project-local generated content root, and the Project-level Houmao overlay without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli project init` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `isomer-content/topic-ws/default/`, a Project-local generated content root at `isomer-content/`, and a Project-level Houmao overlay at `.houmao/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli project init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name under the selected generated content root's `topic-ws/` directory

#### Scenario: Initialize records default path defaults
- **WHEN** `isomer-cli project init` writes the Project Manifest without a custom content directory
- **THEN** the Project Manifest includes path defaults for `isomer_content_root = "isomer-content"` and `topic_workspace_base_dir = "isomer-content/topic-ws"`

#### Scenario: Initialize accepts custom content directory
- **WHEN** a user runs `isomer-cli project init --content-dir custom-content` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates the generated content root at `custom-content/`, writes content-root policy files there, creates the first Topic Workspace under `custom-content/topic-ws/<topic-id>/`, and records Project Manifest path defaults for `isomer_content_root = "custom-content"` and `topic_workspace_base_dir = "custom-content/topic-ws"`

#### Scenario: Initialize custom content directory applies to explicit topic
- **WHEN** a user runs `isomer-cli project init paper --content-dir generated/isomer`
- **THEN** the system registers Research Topic id `paper`, writes the Research Topic Config for `paper`, creates the Topic Workspace at `generated/isomer/topic-ws/paper/`, and reports the selected generated content root and Topic Workspace path in deterministic text or JSON output

#### Scenario: Initialize creates content root policy files
- **WHEN** `isomer-cli project init` creates the Project-local generated content root
- **THEN** it writes `<content-dir>/README.md` and `<content-dir>/.gitignore`, and the `.gitignore` ignores generated contents while keeping `README.md` and `.gitignore` trackable

#### Scenario: Initialize rejects external content directory
- **WHEN** a user runs `isomer-cli project init --content-dir ../outside`
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, does not create the generated content root, and does not claim that the Isomer Project was initialized

#### Scenario: Initialize rejects config-local content directory
- **WHEN** a user runs `isomer-cli project init --content-dir .isomer-labs/generated`
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, does not create the generated content root, and explains that generated content must not live inside the Project Config Directory

#### Scenario: Initialize rejects unsafe content directory collisions
- **WHEN** a user runs `isomer-cli project init --content-dir .houmao` or another value that would make generated content collide with Project bootstrap directories
- **THEN** the system rejects the value before writing Isomer config or content material

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
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, does not create the selected generated content root, and does not claim that the Isomer Project was initialized

#### Scenario: Existing project is not overwritten
- **WHEN** a user runs `isomer-cli project init --content-dir custom-content` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest, does not create or modify the selected generated content root, and does not offer a force-overwrite behavior in Milestone 1
