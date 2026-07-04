# isomer-python-module-architecture Specification

## Purpose
TBD - created by archiving change refactor-isomer-cli-modular-print-json. Update Purpose after archive.
## Requirements
### Requirement: Modular Python Package Layout
The system SHALL organize `src/isomer_labs` implementation code into cohesive package families instead of allowing core behavior to accumulate in long single-file modules.

#### Scenario: Related implementation is package grouped
- **WHEN** source code for CLI commands, Workspace Runtime behavior, or Houmao adapter behavior is refactored
- **THEN** related implementation is grouped into purpose-named package modules such as `cli`, `runtime`, or `houmao` rather than appended to a broad top-level implementation file

#### Scenario: Package names follow Isomer language
- **WHEN** a new package or module is introduced under `src/isomer_labs`
- **THEN** its name uses canonical Isomer domain language or a concrete implementation boundary and does not promote Houmao-specific terms into generic Isomer package names

### Requirement: Modular CLI Package
The system SHALL implement `isomer-cli` through a modular `isomer_labs.cli` package with separate command registration, shared options, output rendering, and command-group modules.

#### Scenario: CLI package exports public entrypoints
- **WHEN** code imports `isomer_labs.cli`
- **THEN** the package exposes `app`, `main`, and `build_parser()` with the same public meanings as the previous single-file CLI module

#### Scenario: Command groups live in command modules
- **WHEN** a developer inspects CLI implementation for a public command group
- **THEN** the Click registration and command handler for that group are located in a command-group module instead of one monolithic CLI file

#### Scenario: Output rendering is shared
- **WHEN** a command returns text or JSON output
- **THEN** shared CLI output code selects the rendering mode instead of each command implementing its own JSON/text branch

### Requirement: Compatibility Import Shims
The system SHALL preserve the stable CLI entry point while requiring repository code to import moved non-CLI implementation from canonical package modules.

#### Scenario: Existing CLI import path still works
- **WHEN** packaging invokes the project script entry point `isomer_labs.cli:main`
- **THEN** the import resolves and dispatches through the modular CLI package

#### Scenario: Existing non-CLI shim modules are intentionally removed
- **WHEN** implementation has moved from top-level modules such as `runtime_store.py`, `runtime_validation.py`, `runtime_models.py`, `houmao_cli_adapter.py`, or `houmao_manifests.py` into package modules
- **THEN** those top-level compatibility modules are absent from `src/isomer_labs`

#### Scenario: Repository imports use canonical package paths
- **WHEN** source code, tests, scripts, or docs outside `isomer-history/` reference Houmao adapter behavior or Workspace Runtime behavior
- **THEN** they use canonical package imports such as `isomer_labs.houmao.adapter`, `isomer_labs.houmao.manifests`, `isomer_labs.runtime.records`, `isomer_labs.runtime.store`, or `isomer_labs.runtime.validation`

### Requirement: Monolith Regression Guard
The system SHALL include a repository-local validation path that reports new large implementation files and removed compatibility aliases when they indicate behavior is accumulating outside package boundaries.

#### Scenario: Large source files are reported
- **WHEN** the validation suite checks `src/isomer_labs`
- **THEN** it reports implementation files that exceed the accepted module-size threshold unless they are documented edge cases

#### Scenario: Removed compatibility shims are reported
- **WHEN** the validation suite checks `src/isomer_labs`
- **THEN** it fails if removed shim filenames such as `runtime_store.py`, `runtime_validation.py`, `runtime_models.py`, `houmao_cli_adapter.py`, or `houmao_manifests.py` exist

#### Scenario: Tests prevent CLI collapse
- **WHEN** CLI command groups are added after this refactor
- **THEN** tests or validation fail if the command implementation is added back into a single monolithic CLI file instead of a command-group module

### Requirement: Use-Case Source Boundary
The system SHALL keep named use-case acceptance orchestration out of `src/isomer_labs` unless a future accepted product spec explicitly promotes that use case into core Isomer behavior.

#### Scenario: Named use-case modules are rejected
- **WHEN** repository tests scan `src/isomer_labs`
- **THEN** they report named use-case orchestration modules or packages such as `uc01`, `uc07`, or `uc06` under source implementation paths unless the allowed package list has been deliberately updated by an accepted spec

#### Scenario: Core package names stay generic
- **WHEN** a new package is introduced under `src/isomer_labs`
- **THEN** its name describes a reusable Isomer platform boundary such as CLI, runtime, adapter, template, profile, validation, or another accepted domain concept rather than a use-case id

#### Scenario: Reusable helpers contain no pinned use-case ids
- **WHEN** code is promoted from a manual harness into `src/isomer_labs`
- **THEN** the promoted code does not hardcode pinned Research Topic ids, use-case names, deterministic fixture outputs, selected route classifications, or acceptance-only record ids

### Requirement: Manual Harnesses Are Not Architecture Violations
The architecture guardrail SHALL allow case-specific code under `tests/manual/<harness>/` while continuing to protect `src/isomer_labs`.

#### Scenario: Manual harness package is allowed
- **WHEN** a use-case acceptance harness is organized as Python modules under `tests/manual/uc01_headless_vertical_slice/`
- **THEN** source architecture tests do not treat that manual harness as a product package boundary

#### Scenario: Harness import direction is one-way
- **WHEN** source modules under `src/isomer_labs` are scanned
- **THEN** they do not import from `tests.manual`, fixture Projects, or use-case harness modules

### Requirement: Generic Core Additions Remain Allowed
The architecture boundary SHALL preserve reusable platform additions needed by acceptance harnesses while excluding reusable Agent Team template content from `src/isomer_labs`.

#### Scenario: Generic lifecycle support stays in core
- **WHEN** the platform needs provider-neutral lifecycle record kinds, statuses, persistence, or validation that apply beyond one use case
- **THEN** that code may remain in `src/isomer_labs/runtime` or another accepted core package

#### Scenario: Team template validation stays in core
- **WHEN** Isomer needs reusable Domain Agent Team Template discovery, validation, inspection, registration, or specialization logic
- **THEN** that protocol and implementation may remain in `src/isomer_labs`
- **AND** the concrete Agent Team template packages such as `deepsci-mini` or `deepsci-org` must be supplied by Project-local registrations or external Team Repositories rather than hardcoded core registries

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

### Requirement: Root Package Uses Bounded Contexts
The system SHALL keep `src/isomer_labs` root implementation minimal by organizing domain behavior into accepted bounded-context packages instead of adding feature-sized modules directly under the package root.

#### Scenario: Root implementation files stay minimal
- **WHEN** repository architecture tests scan `src/isomer_labs`
- **THEN** they fail if root-level implementation modules outside an explicit transition allowlist exceed the accepted root-module size threshold

#### Scenario: New root domain modules are rejected
- **WHEN** a developer adds a new Python file directly under `src/isomer_labs`
- **THEN** architecture tests require it to be an accepted bootstrap, compatibility, or low-level package file rather than a feature-sized domain module

#### Scenario: Domain behavior moves into accepted packages
- **WHEN** Project, Topic Workspace, Team, Records, or shared Core behavior is refactored
- **THEN** the implementation lives under packages such as `project`, `workspace`, `teams`, `records`, or `core` with canonical internal imports

### Requirement: CLI App Is a Bootstrap Surface
The system SHALL keep `isomer_labs.cli.app` focused on Click app creation, shared bootstrap wiring, and registration instead of hosting command handler implementations.

#### Scenario: Command handlers live outside app bootstrap
- **WHEN** a public CLI command executes Project, Workspace, Team, Runtime, Records, or Houmao behavior
- **THEN** its command handler implementation is located in a focused CLI handler module rather than implemented directly in `cli/app.py`

#### Scenario: CLI entry point stays stable
- **WHEN** packaging invokes the project script entry point `isomer_labs.cli:main`
- **THEN** the import resolves and dispatches through the modular CLI package with the existing public command surface

#### Scenario: CLI app size is guarded
- **WHEN** repository architecture tests inspect `src/isomer_labs/cli/app.py`
- **THEN** they fail if the file grows beyond the accepted bootstrap-size threshold or contains command-handler clusters that belong in handler modules

### Requirement: Package Moves Preserve Behavior
The system SHALL treat the modularization as an internal organization change that preserves externally visible behavior.

#### Scenario: CLI output remains compatible
- **WHEN** existing unit tests invoke CLI commands with JSON or text output
- **THEN** command names, status behavior, output schema names, and documented JSON fields remain compatible unless another accepted spec changes them

#### Scenario: Runtime data formats remain compatible
- **WHEN** Project, Topic Workspace, Team Repository, Team Profile, Workspace Runtime, or Houmao adapter material is read after the refactor
- **THEN** existing persisted file formats and manifest schemas continue to parse with the same meanings

#### Scenario: Validation remains green
- **WHEN** implementation of the modularization is complete
- **THEN** `pixi run lint`, `pixi run typecheck`, and `pixi run test` pass without relying on broad architecture-test exemptions for the moved root modules

### Requirement: Package Assets May Carry Runtime Resources
The architecture boundary SHALL allow `src/isomer_labs/assets/` to contain package-owned static runtime resources, including official system-skill assets.

#### Scenario: Package-owned skill assets are not checkout dependencies
- **WHEN** architecture tests scan source and packaged assets
- **THEN** paths under `src/isomer_labs/assets/system_skills` are treated as package resources
- **AND** source code may refer to `assets/system_skills` through package-resource APIs
- **AND** source code still fails architecture checks if it treats repository-root `skillset/` as a runtime dependency

#### Scenario: Development skills stay outside package assets
- **WHEN** architecture tests inspect packaged system-skill assets
- **THEN** they fail if `src/isomer_labs/assets/system_skills/dev` exists
- **AND** they pass when development-only skills remain only under repository-root `skillset/dev`

### Requirement: Workspace Runtime Package Has Canonical Internal Modules
The system SHALL organize `src/isomer_labs/runtime` around a small accepted set of internal modules that map to durable Workspace Runtime responsibilities.

#### Scenario: Runtime package file set is guarded
- **WHEN** repository architecture tests inspect `src/isomer_labs/runtime`
- **THEN** they require the canonical implementation modules `records.py`, `sqlite.py`, `store.py`, and `validation.py`
- **AND** they fail if obsolete helper modules such as `models.py`, `adapter_handoffs.py`, `identifiers.py`, `schema.py`, `reset_schema.py`, `rows.py`, `serialization.py`, `transactions.py`, `readiness.py`, `agent_identity.py`, `validation_checks.py`, `adapter_handoff_validation.py`, `validation_utils.py`, `workspace_layout_validation.py`, `workspace_visibility.py`, or `semantic_file_locator.py` return

#### Scenario: Runtime record imports use records module
- **WHEN** source code, tests, scripts, or docs outside `isomer-history/` need Workspace Runtime record dataclasses, status constants, timestamp helpers, or runtime id helpers
- **THEN** they import those symbols from `isomer_labs.runtime.records`

#### Scenario: Runtime persistence helpers stay internal
- **WHEN** runtime code needs SQLite schema creation, migration helpers, row mapping, JSON serialization helpers, table discovery, or transaction helpers
- **THEN** the implementation uses `isomer_labs.runtime.sqlite`
- **AND** callers outside the runtime package use `isomer_labs.runtime.store` or higher-level services instead of importing SQLite helper functions directly unless a focused test needs to validate persistence internals

#### Scenario: Runtime store and validation remain canonical service modules
- **WHEN** source code, tests, scripts, or docs outside `isomer-history/` need Workspace Runtime mutation, query, initialization, readiness preparation, inspection, or validation behavior
- **THEN** they use `isomer_labs.runtime.store` or `isomer_labs.runtime.validation`

#### Scenario: Internal import breakage preserves CLI behavior
- **WHEN** implementation migrates to the canonical runtime modules
- **THEN** internal Python imports for removed runtime helper modules may break
- **AND** existing `isomer-cli` command names, options, JSON output fields, exit behavior, and persisted runtime data meanings remain compatible

### Requirement: Domain Module Boundary Consolidation
The system SHALL keep tightly coupled domain helper code in cohesive package modules whose names match canonical Isomer language or a concrete processing boundary.

#### Scenario: Artifact Format processing has one pipeline module
- **WHEN** a developer inspects Artifact Format resolution, validation, payload loading, or rendering code
- **THEN** that processing behavior is located in `isomer_labs.artifact_formats.processing` while Artifact Format models, provider registry code, and workspace-backed provider code remain in their own modules

#### Scenario: DeepScientist compatibility tools have one tool adapter module
- **WHEN** a developer inspects DeepScientist compatibility tool discovery, dispatch, service execution, JSON input loading, or unsupported-tool payload construction
- **THEN** that behavior is located in `isomer_labs.deepsci_ext.tools` while compatibility persistence and Artifact Format provider code remain in their own modules

#### Scenario: Topic Team Specialization helper shards are folded into owning modules
- **WHEN** a developer inspects Domain Agent Team Template harness validation, Topic Team Instantiation Packet validation, or Topic Agent Team Profile provenance and bundle-layout validation
- **THEN** those helpers are located in `isomer_labs.teams.templates`, `isomer_labs.teams.instantiation`, or `isomer_labs.teams.profiles` according to the domain object they validate

#### Scenario: Workspace path helpers use canonical concepts
- **WHEN** a developer inspects Semantic Workspace Surface Label catalogs, Default Layout Profile helpers, Local Tmp Surface policy, Workspace Path Resolution, or Agent Workspace ref validation
- **THEN** those helpers are located in `isomer_labs.workspace.surfaces` or `isomer_labs.workspace.path_resolution` according to whether they define surfaces or resolve paths

#### Scenario: Removed helper modules stay absent
- **WHEN** source architecture tests scan `src/isomer_labs`
- **THEN** obsolete helper-shard modules such as `artifact_formats.resolver`, `artifact_formats.validation`, `artifact_formats.rendering`, `deepsci_ext.registry`, `deepsci_ext.rendering`, `deepsci_ext.service`, `teams.template_harness`, `teams.packet_validation`, `teams.profile_bundle_validation`, `workspace.layout`, `workspace.semantic_surfaces`, `workspace.tmp`, and `workspace.refs` are reported if they return

#### Scenario: CLI interface remains stable
- **WHEN** users invoke existing `isomer-cli` command groups that depend on Artifact Format processing, DeepScientist compatibility tools, Topic Team Specialization, or Workspace Path Resolution
- **THEN** the commands, options, text output intent, and JSON output structure remain compatible even though internal imports use the consolidated modules

