## MODIFIED Requirements

### Requirement: System Skills Are Package Assets
The system SHALL distribute official non-development Isomer system skills as package-owned public packs containing independent welcome and entrypoint skills with `SKILL.md` plus protected nested capabilities with `SKILL-MAIN.md` under the `isomer_labs` package.

#### Scenario: Packaged root contains distributable pack material
- **WHEN** package resources are inspected for system skills
- **THEN** the packaged root contains `manifest.toml`, `README.md`, the core public welcome and entrypoint, and the optional DeepSci and Kaoju public welcome and entrypoint pairs
- **AND** every protected capability is below its owning execution entrypoint's `subskills/` directory
- **AND** the packaged root does not contain `dev/`

#### Scenario: Manifest paths resolve inside package assets
- **WHEN** the system loads `assets/system_skills/manifest.toml`
- **THEN** every public-skill path and protected capability path resolves below the packaged system-skill root
- **AND** each resolved public skill directory contains `SKILL.md`
- **AND** each resolved protected capability directory contains `SKILL-MAIN.md` and does not contain `SKILL.md`

#### Scenario: Protected capability is not duplicated
- **WHEN** package assets are inspected
- **THEN** no manifest-declared protected logical id also exists as an independently installable top-level skill directory
- **AND** the independent welcome directories are classified as public skills rather than protected capabilities

### Requirement: System Skill Discovery Uses Package Resources
The system SHALL expose package-resource helpers for discovering and reading official system skills without a repository checkout and SHALL resolve the entrypoint filename from the manifest-owned public or protected role.

#### Scenario: Installed package can list system skill groups
- **WHEN** code asks for packaged system-skill groups
- **THEN** the result is derived from the packaged `manifest.toml`
- **AND** group skill paths are returned as manifest-relative paths rather than repository checkout paths

#### Scenario: Package resource lookup avoids checkout assumptions
- **WHEN** code locates packaged system skills
- **THEN** it uses package resources rather than `Path(__file__)` repository-root traversal
- **AND** it does not require repository-root `skillset/` to exist

#### Scenario: Caller resolves a public entrypoint
- **WHEN** a caller requests the entrypoint resource for a manifest-declared public skill
- **THEN** the role-aware helper returns that directory's `SKILL.md`

#### Scenario: Caller resolves a protected entrypoint
- **WHEN** a caller requests the entrypoint resource for a manifest-declared protected capability
- **THEN** the role-aware helper returns that directory's `SKILL-MAIN.md`
- **AND** callers do not need to concatenate a hard-coded filename

### Requirement: System Skills Can Be Materialized Safely
The system SHALL materialize manifest-selected packs as complete sets of top-level public skill directories while preserving protected nested paths and `SKILL-MAIN.md` entrypoints under the designated execution entrypoint.

#### Scenario: Materialize core group
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `manifest.toml`, `isomer-op-welcome`, and `isomer-op-entrypoint`
- **AND** protected core capabilities remain below `isomer-op-entrypoint/subskills/` with `SKILL-MAIN.md`
- **AND** no protected capability is copied beside the two public skills or retains nested `SKILL.md`

#### Scenario: Materialize selected extension
- **WHEN** a caller materializes extension `deepsci` or `kaoju`
- **THEN** the target receives the complete core public pair and the selected extension's welcome and entrypoint pair
- **AND** it does not receive the unselected extension pack

#### Scenario: Materialized host recursively scans discovery files
- **WHEN** a supported host recursively searches the materialized target for `SKILL.md`
- **THEN** it finds exactly the selected packs' public welcome and execution entrypoint roots
- **AND** it does not find protected members or provenance snapshots

#### Scenario: Development skills are never materialized from package assets
- **WHEN** a caller materializes any packaged system-skill selection
- **THEN** no `dev/` directory or `isomer-dev-*` skill is copied from package assets

### Requirement: Materialized Skills Preserve Standalone Resource Boundaries
Public pack materialization and protected private projection SHALL preserve every declared skill bundle's active resource boundary while applying the destination role's canonical entrypoint filename.

#### Scenario: Public pack is materialized
- **WHEN** a caller materializes a packaged public pack
- **THEN** every nested protected skill can resolve its `SKILL-MAIN.md` and bundle-local resources without leaving its directory
- **AND** shared machine resources remain available through the installed extension CLI

#### Scenario: Protected member is privately projected
- **WHEN** an internal adapter projects a protected logical capability and its dependencies into a flat private skill root
- **THEN** each copied member remains a self-contained ordinary directory whose source `SKILL-MAIN.md` is promoted to destination `SKILL.md`
- **AND** no source-package sibling, symlink, undeclared family-root support file, or destination `SKILL-MAIN.md` is required

#### Scenario: Family-root support file is undeclared
- **WHEN** a system-skill family root contains a file or directory that is not a manifest-listed skill bundle
- **THEN** materialization does not copy it as an implicit dependency of selected skills
- **AND** validation fails if active skill guidance requires that undeclared path

#### Scenario: Undeclared support path is required
- **WHEN** active guidance depends on a path not owned by its bundle or declared package service
- **THEN** validation fails with a deterministic resource-boundary diagnostic

#### Scenario: Materialized projection does not preserve symlinks
- **WHEN** package tests materialize skills into a temporary target
- **THEN** the test target uses ordinary directories and files with no link back to the package source or repository checkout
- **AND** each active local link is validated relative to its owning copied skill
