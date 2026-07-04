## ADDED Requirements

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
- **WHEN** source code, tests, scripts, or docs outside `isomer-history/` reference Houmao adapter behavior or Workspace Runtime behavior
- **THEN** they use canonical package imports such as `isomer_labs.houmao.adapter`, `isomer_labs.houmao.manifests`, `isomer_labs.runtime.records`, `isomer_labs.runtime.store`, or `isomer_labs.runtime.validation`
