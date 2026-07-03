## ADDED Requirements

### Requirement: Team Repository Manifest
The system SHALL support external Team Repository manifests that describe available Domain Agent Team Templates without placing the template sources under `src/isomer_labs`.

#### Scenario: Team Repository manifest lists template entries
- **WHEN** Isomer reads an `isomer-team-repo.toml` manifest
- **THEN** the manifest includes a schema version, repository id, and zero or more Domain Agent Team Template entries with id, path, source kind, and status

#### Scenario: Team Repository paths resolve inside repository root
- **WHEN** a Team Repository manifest entry declares a relative template path
- **THEN** Isomer resolves that path relative to the Team Repository root
- **AND** it rejects entries that escape the Team Repository root after path normalization

#### Scenario: Team Repository manifest keeps templates reusable
- **WHEN** a Team Repository entry points at a Domain Agent Team Template package
- **THEN** the template package remains reusable source material and is not treated as a Topic Agent Team Profile, Agent Team Instance, Topic Workspace, or runtime launch package

### Requirement: Team Repository Discovery
The system SHALL discover Domain Agent Team Templates from explicitly configured Team Repository roots rather than implicit core built-ins.

#### Scenario: Configured Team Repository is discoverable
- **WHEN** a user or test configures a local Team Repository root
- **THEN** `isomer-cli` can list that repository and the active templates declared in its manifest

#### Scenario: Missing Team Repository configuration is explicit
- **WHEN** no Team Repository roots are configured and the Project Manifest does not register any templates
- **THEN** template listing reports no available templates and explains that team definitions are external Team Repository content

#### Scenario: Broken Team Repository reports diagnostics
- **WHEN** a configured Team Repository root is missing, lacks an `isomer-team-repo.toml` manifest, contains malformed TOML, or references missing template files
- **THEN** `isomer-cli` reports deterministic diagnostics naming the repository root and failing manifest or template entry

### Requirement: Team Repository Template Selection
The system SHALL let users select a Team Repository template and register it for Project use before Topic Team Specialization.

#### Scenario: Template can be registered from Team Repository
- **WHEN** a user selects a template id from a configured Team Repository for a Project
- **THEN** Isomer records enough Project-facing metadata to resolve that template source later without copying template source material into the Topic Workspace

#### Scenario: Project registration preserves source provenance
- **WHEN** a Team Repository template is registered or selected for a Project
- **THEN** CLI output includes the template id, Team Repository id, source kind, resolved source path, and validation status

#### Scenario: Specialization consumes resolved repository template
- **WHEN** Topic Team Specialization runs for a template selected from a Team Repository
- **THEN** it validates the resolved Domain Agent Team Template package and copies topic-editable material into the Topic Agent Team Profile Bundle before applying topic-specific edits

### Requirement: Team Repository CLI Surface
The system SHALL expose CLI commands for listing and inspecting Team Repositories and their templates.

#### Scenario: Team repositories list command reports configured repositories
- **WHEN** a user runs the Team Repository list command
- **THEN** output includes each configured repository id, root path, manifest path, status, and diagnostics when available

#### Scenario: Team repository inspect command reports templates
- **WHEN** a user inspects a configured Team Repository
- **THEN** output includes active, archived, and invalid template entries with their source paths and validation status

#### Scenario: Project team-template commands include repository templates
- **WHEN** a Project has configured or selected Team Repository sources
- **THEN** `isomer-cli project team-templates list`, `inspect`, and `validate` include templates resolved from those sources alongside Project-local templates
