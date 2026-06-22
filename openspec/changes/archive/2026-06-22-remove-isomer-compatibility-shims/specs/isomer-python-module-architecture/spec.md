## MODIFIED Requirements

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
