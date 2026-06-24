## MODIFIED Requirements

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration, the selected Project-local generated content root, and the Isomer-managed Project-level Houmao overlay under the Project Config Directory through `isomer-cli project init` without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli project init` in a directory that is not inside an existing Isomer Project and does not contain `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `isomer-content/topic-ws/default/`, a Project-local generated content root at `isomer-content/`, and an Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli project init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name under the selected generated content root's `topic-ws/` directory

#### Scenario: Initialize accepts custom content directory
- **WHEN** a user runs `isomer-cli project init --content-dir custom-content` in a directory that is not inside an existing Isomer Project and does not contain `.isomer-labs/manifest.toml`
- **THEN** the system creates the generated content root at `custom-content/`, writes content-root policy files there, creates the first Topic Workspace under `custom-content/topic-ws/<topic-id>/`, and records Project Manifest path defaults for `isomer_content_root = "custom-content"` and `topic_workspace_base_dir = "custom-content/topic-ws"`

#### Scenario: Initialize rejects nested project
- **WHEN** a user runs `isomer-cli project init` from inside a directory tree that already has an ancestor `.isomer-labs/manifest.toml`
- **THEN** the system refuses to create a nested Isomer Project and reports the ancestor Project root

#### Scenario: Initialize creates Houmao project overlay
- **WHEN** `isomer-cli project init` completes successfully
- **THEN** the system has invoked the supported Houmao CLI project initialization boundary with `<project-root>/.isomer-labs/` as the Houmao project directory and reports the resolved Isomer-managed Houmao project directory and `.isomer-labs/.houmao/` overlay path in deterministic text or JSON output

#### Scenario: Existing root Houmao overlay is ignored
- **WHEN** a user runs `isomer-cli project init` in a Project root that already contains `.houmao/` but does not contain `.isomer-labs/manifest.toml`
- **THEN** the system treats root `.houmao/` as external user-owned Houmao state, leaves it unmodified, and creates or validates the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`

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
- **WHEN** a user runs `isomer-cli project init` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest and does not offer a force-overwrite behavior in Milestone 1

### Requirement: Project Cleanup Side-effect Boundaries
The system SHALL keep cleanup filesystem side effects explicit and SHALL avoid live runtime or service operations.

#### Scenario: Dry-run is side-effect free
- **WHEN** cleanup runs with `--dry-run`
- **THEN** it does not create, modify, or delete Project files, Workspace Runtime records, adapter manifests, live Houmao state, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Houmao overlay cleanup is local only
- **WHEN** cleanup applies `--part houmao-overlay --yes`
- **THEN** it may remove the local Isomer-managed `.isomer-labs/.houmao/` overlay, preserves root `.houmao/`, and does not stop, launch, inspect, message, or adopt live Houmao managed agents

#### Scenario: Runtime cleanup is filesystem scoped
- **WHEN** cleanup applies `--part runtime --topic <topic-id> --yes`
- **THEN** it removes only planned runtime files and directories under the selected Topic Workspace and does not invoke runtime prepare, runtime validate, or adapter live-state commands
