## ADDED Requirements

### Requirement: Project Command Namespace
The system SHALL expose Project-targeted command behavior under a root-level `project` command group and SHALL treat `isomer-cli project <subcmd>` as the canonical command surface for Project-scoped operations.

#### Scenario: Project group appears at root
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the help lists a `project` command group for Project-scoped operations

#### Scenario: Project group lists lifecycle commands
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the help lists Project lifecycle commands including `init`, `validate`, `doctor`, and `cleanup` when cleanup is implemented

#### Scenario: Project group lists nested Project command groups
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the help lists Project-scoped command groups including `topics`, `workspaces`, `context`, `paths`, `runtime`, `team-instances`, `handoffs`, `team-templates`, and `team-profiles`

#### Scenario: Project selector lives on project group
- **WHEN** a user runs `isomer-cli project --root <project-root> validate`
- **THEN** the system treats `<project-root>` as the explicit Project root selector for the nested command

#### Scenario: Manifest selector lives on project group
- **WHEN** a user runs `isomer-cli project --manifest <manifest-path> validate`
- **THEN** the system treats `<manifest-path>` as the explicit Project Manifest selector for the nested command

#### Scenario: Root print-json still applies
- **WHEN** a user runs `isomer-cli --print-json project validate`
- **THEN** the system emits the same versioned deterministic JSON wrapper used by other CLI commands

#### Scenario: Root global commands remain available
- **WHEN** a user runs `isomer-cli schemas list`
- **THEN** the system lists built-in schemas without requiring `project` or an active Project

### Requirement: Project Namespace Migration
The system SHALL make `isomer-cli project ...` canonical for Project-scoped commands and SHALL keep any legacy root-level Project command forms out of new docs and operator guidance.

#### Scenario: Legacy root command help is not canonical
- **WHEN** root-level Project command aliases are retained for compatibility
- **THEN** they are hidden from canonical root help or clearly marked as deprecated

#### Scenario: Canonical docs use project namespace
- **WHEN** CLI docs, workflow docs, troubleshooting docs, or operator skill command examples mention Project-scoped commands
- **THEN** they use `isomer-cli project ...` command shapes

#### Scenario: Cleanup canonical namespace
- **WHEN** Project cleanup is implemented
- **THEN** the canonical command shape is `isomer-cli project cleanup`, not root-level `isomer-cli cleanup`

## MODIFIED Requirements

### Requirement: CLI Entrypoint and Command Surface
The system SHALL provide an installed `isomer-cli` command with a global command surface and a `project` command group for Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile validation commands.

#### Scenario: CLI exposes project group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `project` and global Project-independent commands such as `schemas`

#### Scenario: Project group exposes project-discovery commands
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists `init`, `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show`

#### Scenario: Project group exposes template and profile commands
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists `team-templates` and `team-profiles` command groups

#### Scenario: Project script is installed through package metadata
- **WHEN** the package is installed through the repository's editable Pixi PyPI dependency
- **THEN** the environment can invoke `isomer-cli` as a project script

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration, the selected Project-local generated content root, and the Project-level Houmao overlay through `isomer-cli project init` without creating Workspace Runtime state or live Houmao agent state.

#### Scenario: Initialize default project
- **WHEN** a user runs `isomer-cli project init` in a directory that is not inside an existing Isomer Project and does not contain `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, one registered Research Topic Config for Research Topic id `default`, one project-local Topic Workspace directory at `isomer-content/topic-ws/default/`, a Project-local generated content root at `isomer-content/`, and a Project-level Houmao overlay at `.houmao/`

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
- **WHEN** a user runs `isomer-cli project init` in a Project that already has `.isomer-labs/manifest.toml`
- **THEN** the system refuses to overwrite the existing Project Manifest and does not offer a force-overwrite behavior in Milestone 1

### Requirement: Project Discovery
The system SHALL discover the active Project before resolving Project-scoped command behavior under `isomer-cli project`.

#### Scenario: Explicit root selector wins
- **WHEN** a user provides `isomer-cli project --root <project-root> <subcmd>`
- **THEN** the system loads that Project before checking the current directory or environment-derived Project fallbacks

#### Scenario: Explicit manifest selector wins
- **WHEN** a user provides `isomer-cli project --manifest <manifest-path> <subcmd>`
- **THEN** the system loads that Project Manifest before checking the current directory or environment-derived Project fallbacks

#### Scenario: Current directory discovers project
- **WHEN** a user runs `isomer-cli project <subcmd>` from inside a directory tree containing an ancestor `.isomer-labs/manifest.toml`
- **THEN** the system resolves that ancestor as the Project root and loads its Project Manifest

#### Scenario: Project environment fallback is used
- **WHEN** no explicit Project selector or current-directory Project applies and a supported Project environment override is set
- **THEN** the system treats that override as the candidate Project source and reports the source in diagnostic or JSON output

#### Scenario: Missing project is rejected
- **WHEN** no explicit selector, current-directory discovery, or supported Project environment override resolves a Project Manifest
- **THEN** the system rejects Project-scoped and topic-scoped commands with a validation diagnostic instead of creating implicit Project state

### Requirement: Diagnostics and Output Formats
The system SHALL produce deterministic diagnostics, structured human-readable text, and machine-readable output for global commands and for Project-scoped commands under `isomer-cli project`.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output with root-level `--print-json` for `project validate`, `project doctor`, `project topics list`, `project workspaces list`, `project context show`, `project paths preview`, `schemas list`, `project runtime init`, `project runtime prepare`, `project runtime inspect`, `project runtime validate`, `project team-instances create`, `project team-instances list`, `project team-instances show`, `project team-templates list`, `project team-templates inspect`, `project team-templates validate`, `project team-profiles specialize`, or `project team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template registration, or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API

### Requirement: Runtime Command Side-effect Boundaries
The system SHALL make Workspace Runtime mutations explicit under `isomer-cli project runtime` while preserving the read-only guarantees of inspection and design-time commands.

#### Scenario: Runtime init is the runtime creation command
- **WHEN** a user runs `isomer-cli project runtime init`
- **THEN** the command may create or reopen `state.sqlite` and the default Workspace Runtime directories for the selected Topic Workspace

#### Scenario: Runtime prepare is the readiness preparation command
- **WHEN** a user runs `isomer-cli project runtime prepare`
- **THEN** the command may record selected topic Pixi environment use, readiness status, readiness diagnostics, and preparation provenance in the selected Workspace Runtime

#### Scenario: Runtime inspect is read-only
- **WHEN** a user runs `isomer-cli project runtime inspect`
- **THEN** the command reads Workspace Runtime metadata and selected record counts without creating or mutating runtime state

#### Scenario: Runtime validate is read-only
- **WHEN** a user runs `isomer-cli project runtime validate`
- **THEN** the command reports Workspace Runtime diagnostics without creating directories, changing statuses, or repairing records

#### Scenario: Team instance create is explicit mutation
- **WHEN** a user runs `isomer-cli project team-instances create`
- **THEN** the command may create Agent Team Instance, Agent Instance, Agent Workspace, path plan, Workflow Stage Cursor, and Provenance records for the selected Topic Workspace

#### Scenario: Team instance inspection is read-only
- **WHEN** a user runs `isomer-cli project team-instances list` or `isomer-cli project team-instances show`
- **THEN** the command reads Workspace Runtime records without creating Agent Team Instances, Agent Instances, Agent Workspaces, Runs, Houmao launch material, or adapter refs

### Requirement: Click Command Registration
The system SHALL implement the `isomer-cli` command surface with a modular Click root group and a nested Project command group while preserving established Project discovery behavior.

#### Scenario: Root command is Click backed
- **WHEN** the package exposes `isomer-cli` through `isomer_labs.cli:main`
- **THEN** the command dispatch uses a Click command group rather than an `argparse` parser tree

#### Scenario: Root help exposes project group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `project` and does not present root-level Project command forms as the canonical surface

#### Scenario: Project commands remain available under project
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists `init`, `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, and `paths preview`

#### Scenario: Existing command outputs remain compatible under project namespace
- **WHEN** a user runs `project validate`, `project topics list`, `project workspaces list`, `project context show`, `project paths preview`, or `schemas list` with JSON output requested through root-level `--print-json`
- **THEN** the command emits the same versioned JSON contract shape used by the Milestone 1 project-discovery implementation

#### Scenario: Domain diagnostics remain Isomer diagnostics
- **WHEN** Project discovery, Project Manifest validation, Research Topic Config validation, Effective Topic Context resolution, or Workspace Path Resolution fails under the `project` group
- **THEN** the command reports stable Isomer diagnostics rather than replacing domain validation failures with Click parser errors
