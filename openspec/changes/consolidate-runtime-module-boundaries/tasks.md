## 1. Architecture Guardrails

- [x] 1.1 Update `tests/unit/test_source_architecture.py` so `src/isomer_labs/runtime` is expected to contain only `__init__.py`, `records.py`, `sqlite.py`, `store.py`, and `validation.py`.
- [x] 1.2 Remove runtime transition allowlist entries for the old helper files and add assertions that the obsolete runtime modules are absent.
- [x] 1.3 Update repository import-surface checks to accept `isomer_labs.runtime.records`, `isomer_labs.runtime.store`, and `isomer_labs.runtime.validation` as canonical runtime imports.
- [x] 1.4 Ensure architecture scans and import rewrites ignore `isomer-history/`.

## 2. Runtime Records

- [x] 2.1 Create `src/isomer_labs/runtime/records.py` from the current runtime record dataclasses, status constants, `utc_timestamp`, and runtime id helper functions.
- [x] 2.2 Move adapter handoff record dataclasses and statuses into `records.py`.
- [x] 2.3 Update runtime and in-scope caller imports from `isomer_labs.runtime.models`, `isomer_labs.runtime.adapter_handoffs`, and `isomer_labs.runtime.identifiers` to `isomer_labs.runtime.records`.
- [x] 2.4 Delete the obsolete `models.py`, `adapter_handoffs.py`, and `identifiers.py` files after imports are migrated.

## 3. SQLite Persistence

- [x] 3.1 Create `src/isomer_labs/runtime/sqlite.py` from schema creation, reset schema creation, migration helpers, row mapping, JSON serialization helpers, table discovery, and transaction helpers.
- [x] 3.2 Update `store.py` and focused tests to import persistence internals from `isomer_labs.runtime.sqlite`.
- [x] 3.3 Keep SQLite table names, column names, schema version handling, row ordering, and record JSON serialization behavior unchanged.
- [x] 3.4 Delete the obsolete `schema.py`, `reset_schema.py`, `rows.py`, `serialization.py`, and `transactions.py` files.

## 4. Runtime Store

- [x] 4.1 Update `src/isomer_labs/runtime/store.py` to use `runtime.records` and `runtime.sqlite`.
- [x] 4.2 Fold readiness diagnostic helper behavior from `readiness.py` into `store.py`.
- [x] 4.3 Fold Project-level Agent Instance id scan and uniqueness helper behavior from `agent_identity.py` into `store.py`.
- [x] 4.4 Delete the obsolete `readiness.py` and `agent_identity.py` files.
- [x] 4.5 Preserve `WorkspaceRuntimeStore`, `initialize_workspace_runtime`, `open_workspace_runtime`, `prepare_topic_environment_readiness`, and `run_runtime_transaction` behavior for CLI callers.

## 5. Runtime Validation

- [x] 5.1 Fold validation checks, adapter handoff validation, validation utilities, workspace layout validation, workspace visibility validation, and semantic file locator helpers into `src/isomer_labs/runtime/validation.py`.
- [x] 5.2 Keep `RuntimeInspection`, `inspect_workspace_runtime`, and `validate_workspace_runtime` as the canonical validation API.
- [x] 5.3 Preserve diagnostic codes, severities, concepts, and CLI validation output shape unless existing tests only assert equivalent behavior.
- [x] 5.4 Delete the obsolete `validation_checks.py`, `adapter_handoff_validation.py`, `validation_utils.py`, `workspace_layout_validation.py`, `workspace_visibility.py`, and `semantic_file_locator.py` files.

## 6. Import Migration

- [x] 6.1 Update in-scope imports in `src/`, `tests/`, `scripts/`, and docs from removed runtime modules to the new canonical runtime modules.
- [x] 6.2 Do not edit historical imports or prose under `isomer-history/`.
- [x] 6.3 Update patch targets in tests that patch private runtime helper names so they reference the new module paths.
- [x] 6.4 Run a search to confirm no in-scope reference remains to removed runtime module paths.

## 7. Validation

- [x] 7.1 Run `pixi run lint`.
- [x] 7.2 Run `pixi run typecheck`.
- [x] 7.3 Run `pixi run test`.
- [x] 7.4 Run representative CLI smoke checks for `project runtime init`, `project runtime prepare`, `project runtime inspect`, and `project runtime validate` if the unit suite does not already cover the changed paths in the current run.
- [x] 7.5 Run `openspec status --change consolidate-runtime-module-boundaries` and confirm the change remains apply-ready.
