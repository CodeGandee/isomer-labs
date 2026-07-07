## ADDED Requirements

### Requirement: Public repository is created with correct identity
The system SHALL create a public GitHub repository named `isomer-example-fa4-analytical-model` under the `CodeGandee` organization.

#### Scenario: Repository creation
- **WHEN** the publication script runs with organization `CodeGandee`
- **THEN** a public repository exists at `https://github.com/CodeGandee/isomer-example-fa4-analytical-model`

### Requirement: Redownloadable content is excluded
The published repository SHALL omit the Pixi environment directory, simulator checkouts in `tmp/`, vendored upstream full histories, caches, and intermediate verification images.

#### Scenario: Fresh clone size
- **WHEN** a user clones the public repository without submodules
- **THEN** the total size of tracked files is under 100 MB

#### Scenario: Pixi lockfile is present
- **WHEN** a user inspects the repository root
- **THEN** `pixi.toml` and `pixi.lock` are present
- **AND** `.pixi/` is absent

### Requirement: Upstream dependencies are declared as submodules
The published repository SHALL declare upstream dependencies (`flash-attention`, `accel-sim-framework`) as Git submodules pointing to their canonical upstream repositories at the commits used in the workspace.

#### Scenario: Submodule registration
- **WHEN** a user opens `.gitmodules`
- **THEN** each upstream dependency is listed with a path and a URL to its canonical repository

### Requirement: Reproduction instructions are provided
The published repository SHALL contain a `README.md` with instructions to install the environment, fetch submodules, and build the paper.

#### Scenario: Reproduction from scratch
- **WHEN** a user follows the `README.md` on a clean machine
- **THEN** the user can run the unit tests and regenerate the PDF
