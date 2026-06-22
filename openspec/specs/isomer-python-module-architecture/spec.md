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
- **WHEN** source code, tests, scripts, or docs reference Houmao adapter behavior or Workspace Runtime behavior
- **THEN** they use canonical package imports such as `isomer_labs.houmao.adapter`, `isomer_labs.houmao.manifests`, `isomer_labs.runtime.models`, `isomer_labs.runtime.store`, or `isomer_labs.runtime.validation`

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
