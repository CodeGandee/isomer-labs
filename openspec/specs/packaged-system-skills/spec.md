# packaged-system-skills Specification

## Purpose
TBD - created by archiving change package-system-skills-as-assets. Update Purpose after archive.
## Requirements
### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned resources under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable skillset material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, `misc/`, `operator/`, `research-paradigm/`, and `service/`
- **AND** it does not contain `dev/`

#### Scenario: Manifest-listed skills resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every skill path listed in every manifest group resolves below the packaged system-skill root
- **AND** each listed skill directory contains `SKILL.md`

### Requirement: System Skill Discovery Uses Package Resources
The system SHALL expose package-resource helpers for discovering and reading official system skills without a repository checkout.

#### Scenario: Installed package can list system skill groups
- **WHEN** code asks for packaged system-skill groups
- **THEN** the result is derived from the packaged `manifest.toml`
- **AND** group skill paths are returned as manifest-relative paths rather than repository checkout paths

#### Scenario: Package resource lookup avoids checkout assumptions
- **WHEN** code locates packaged system skills
- **THEN** it uses package resources rather than `Path(__file__)` repository-root traversal
- **AND** it does not require repository-root `skillset/` to exist

### Requirement: System Skills Can Be Materialized Safely
The system SHALL support copying manifest-selected packaged system skills to a filesystem target while preserving relative skill paths.

#### Scenario: Materialize selected group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml` and only the skill directories listed for that group
- **AND** each copied skill keeps its manifest-relative path such as `operator/isomer-admin-project-mgr`

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill group
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

