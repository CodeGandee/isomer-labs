## ADDED Requirements

### Requirement: PyPI Package Source Boundary
The system SHALL keep `src/isomer_labs` importable and runnable as an installed Python package without depending on repository-local development directories.

#### Scenario: Source does not derive repository root from package files
- **WHEN** architecture tests scan Python files under `src/isomer_labs`
- **THEN** they fail if source code derives the repository root from `Path(__file__)`, `__file__`, parent traversal, or equivalent package-file-relative assumptions

#### Scenario: Source avoids repository-only runtime paths
- **WHEN** architecture tests scan files under `src/isomer_labs`
- **THEN** they fail if source code references repository-only directories such as `teams/`, `skillset/`, `tests/`, `openspec/`, `.imsight-arts/`, or `extern/` as runtime dependencies
- **AND** they allow Project content path examples only when those paths are clearly user Project paths rather than repository checkout paths

#### Scenario: Package smoke test does not need checkout-only teams
- **WHEN** the package is built or imported in a wheel-like environment
- **THEN** importing `isomer_labs`, invoking the CLI entry point, listing schemas, and listing team templates do not require checkout-local `teams/` directories

### Requirement: PyPI Runtime Metadata
The system SHALL keep PyPI-facing package metadata release-compatible and limited to runtime requirements.

#### Scenario: Runtime dependencies match source imports
- **WHEN** package metadata is inspected for default runtime dependencies
- **THEN** it includes only dependencies needed by `src/isomer_labs` at runtime and excludes development, documentation, lint, typecheck, and test-only tools

#### Scenario: Development dependencies remain available outside runtime install
- **WHEN** repository developers use Pixi tasks for linting, typechecking, documentation, validation, or tests
- **THEN** those tools remain available through Pixi or optional development groups rather than default PyPI install requirements

#### Scenario: Package version is release-compatible
- **WHEN** PyPI-facing metadata is prepared for release
- **THEN** the version string does not use a local-only suffix such as `+local`

## MODIFIED Requirements

### Requirement: Generic Core Additions Remain Allowed
The architecture boundary SHALL preserve reusable platform additions needed by acceptance harnesses while excluding reusable Agent Team template content from `src/isomer_labs`.

#### Scenario: Generic lifecycle support stays in core
- **WHEN** the platform needs provider-neutral lifecycle record kinds, statuses, persistence, or validation that apply beyond one use case
- **THEN** that code may remain in `src/isomer_labs/runtime` or another accepted core package

#### Scenario: Team template validation stays in core
- **WHEN** Isomer needs reusable Domain Agent Team Template discovery, validation, inspection, registration, or specialization logic
- **THEN** that protocol and implementation may remain in `src/isomer_labs`
- **AND** the concrete Agent Team template packages such as `deepsci-mini` or `deepsci-org` must be supplied by Project-local registrations or external Team Repositories rather than hardcoded core registries
