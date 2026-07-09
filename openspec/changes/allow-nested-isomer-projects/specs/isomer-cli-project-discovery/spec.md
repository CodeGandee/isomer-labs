## MODIFIED Requirements

### Requirement: Project Initialization
The system SHALL initialize the smallest valid Isomer-managed Project configuration, the selected Project-local generated content root, and the Isomer-managed Project-level Houmao overlay under the Project Config Directory through `isomer-cli project init` without creating Research Topic registrations, Topic Workspace registrations, Workspace Runtime state, or live Houmao agent state.

#### Scenario: Initialize empty project registry
- **WHEN** a user runs `isomer-cli project init` in a directory that does not contain `.isomer-labs/manifest.toml`
- **THEN** the system creates `.isomer-labs/manifest.toml`, a Project-local generated content root at `isomer-content/`, generated content-root policy files, and an Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`
- **AND** the system does not create a Research Topic Config, a Research Topic registration, a Topic Workspace registration, or a Topic Workspace directory

#### Scenario: Initialize rejects topic argument
- **WHEN** a user runs `isomer-cli project init <topic-id>`
- **THEN** the system rejects the command with a deterministic diagnostic that Research Topics must be created through `isomer-cli project topics create`
- **AND** the system does not create or modify Project files

#### Scenario: Initialize rejects topic options
- **WHEN** a user runs `isomer-cli project init --topic-id <topic-id>` or `isomer-cli project init --topic-statement "<research topic>"`
- **THEN** the system rejects the command with a deterministic diagnostic that Research Topics must be created through `isomer-cli project topics create`
- **AND** the system does not create or modify Project files

#### Scenario: Initialize accepts custom content directory
- **WHEN** a user runs `isomer-cli project init --content-dir custom-content` in a directory that does not contain `.isomer-labs/manifest.toml`
- **THEN** the system creates the generated content root at `custom-content/`, writes content-root policy files there, and records Project Manifest path defaults for `isomer_content_root = "custom-content"` and `topic_workspace_base_dir = "custom-content/topic-ws"`
- **AND** the system does not create `custom-content/topic-ws/<topic-id>/` or any other Topic Workspace directory

#### Scenario: Initialize writes no topic defaults
- **WHEN** `isomer-cli project init` writes the Project Manifest
- **THEN** the manifest contains no `[defaults].research_topic_id`, no `[defaults].topic_workspace_id`, no `[[research_topics]]`, and no `[[topic_workspaces]]`

#### Scenario: Empty project manifest is valid
- **WHEN** Project validation reads a fresh Project Manifest created by `isomer-cli project init`
- **THEN** it treats the empty Research Topic registry as valid for Project-scoped commands

#### Scenario: Initialize allows nested project
- **WHEN** a user runs `isomer-cli project init` for a target directory inside another Isomer Project tree
- **THEN** the system creates or validates the selected target as its own Isomer Project
- **AND** the system does not mutate the ancestor Project Manifest
- **AND** the system does not report the ancestor Project root as a blocker

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

### Requirement: Project Discovery
The system SHALL discover the active Project before resolving Project-scoped command behavior under `isomer-cli project`, using nearest Project Manifest semantics for cwd-based discovery.

#### Scenario: Explicit root selector wins
- **WHEN** a user provides `isomer-cli project --root <project-root> <subcmd>`
- **THEN** the system loads that Project before checking the current directory or environment-derived Project fallbacks

#### Scenario: Explicit manifest selector wins
- **WHEN** a user provides `isomer-cli project --manifest <manifest-path> <subcmd>`
- **THEN** the system loads that Project Manifest before checking the current directory or environment-derived Project fallbacks

#### Scenario: Current directory discovers nearest project
- **WHEN** a user runs `isomer-cli project <subcmd>` from inside a directory tree containing one or more ancestor `.isomer-labs/manifest.toml` files
- **THEN** the system resolves the nearest ancestor Project Manifest as the Project root and loads that Project Manifest

#### Scenario: Nested project discovery prefers child
- **WHEN** a parent Project and a nested child Project both have `.isomer-labs/manifest.toml` and a user runs `isomer-cli project <subcmd>` from inside the nested child Project tree
- **THEN** the system resolves the nested child Project
- **AND** the system does not resolve the parent Project unless the parent is explicitly selected

#### Scenario: Parent project discovery outside child
- **WHEN** a parent Project contains a nested child Project and a user runs `isomer-cli project <subcmd>` from a parent Project directory outside the child Project tree
- **THEN** the system resolves the parent Project

#### Scenario: Project environment fallback is used
- **WHEN** no explicit Project selector or current-directory Project applies and a supported Project environment override is set
- **THEN** the system treats that override as the candidate Project source and reports the source in diagnostic or JSON output

#### Scenario: Missing project is rejected
- **WHEN** no explicit selector, current-directory discovery, or supported Project environment override resolves a Project Manifest
- **THEN** the system rejects Project-scoped and topic-scoped commands with a validation diagnostic instead of creating implicit Project state
