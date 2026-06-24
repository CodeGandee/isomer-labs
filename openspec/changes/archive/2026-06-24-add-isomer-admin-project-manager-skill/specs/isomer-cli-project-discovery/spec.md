## MODIFIED Requirements

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration and the Project-level Houmao overlay without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli init` in a directory without `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `topic-workspaces/default/`, and a Project-level Houmao overlay at `.houmao/`

#### Scenario: Initialize explicit topic
- **WHEN** a user runs `isomer-cli init` with an explicit Research Topic id
- **THEN** the system uses that id for the Research Topic registration, Research Topic Config path, and default Topic Workspace directory name

#### Scenario: Initialize creates Houmao project overlay
- **WHEN** `isomer-cli init` completes successfully
- **THEN** the system has invoked the supported Houmao CLI project initialization boundary for the Project root and reports the resolved Houmao Project overlay path in deterministic text or JSON output

#### Scenario: Initialize does not create runtime database
- **WHEN** `isomer-cli init` completes
- **THEN** the system does not create `state.sqlite` or any Workspace Runtime database

#### Scenario: Initialize does not create runtime or live Houmao launch state
- **WHEN** `isomer-cli init` completes
- **THEN** the system does not create Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, Houmao managed agents, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Houmao bootstrap failure blocks project init
- **WHEN** a user runs `isomer-cli init` and the required Houmao command boundary is unavailable or returns a failing result
- **THEN** the system returns deterministic diagnostics, does not write `.isomer-labs/manifest.toml`, and does not claim that the Isomer Project was initialized

#### Scenario: Existing project is not overwritten
- **WHEN** a user runs `isomer-cli init` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest and does not offer a force-overwrite behavior in Milestone 1
