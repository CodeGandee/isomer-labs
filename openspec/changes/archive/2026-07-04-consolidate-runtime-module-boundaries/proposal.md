## Why

`src/isomer_labs/runtime` is already package-scoped, but its implementation is split across many small helper files while tightly coupled records, schema, row mapping, store methods, and validation checks remain dependent on each other. This makes Workspace Runtime changes harder to review, and it leaves broad architecture-test exemptions in place after the larger package modularization work.

## What Changes

- **BREAKING**: Replace internal Python import paths such as `isomer_labs.runtime.models`, `isomer_labs.runtime.schema`, `isomer_labs.runtime.rows`, `isomer_labs.runtime.validation_checks`, and related helper modules with a smaller canonical runtime module set.
- Consolidate Workspace Runtime record dataclasses, status constants, timestamp helpers, and runtime id helpers into `isomer_labs.runtime.records`.
- Consolidate SQLite schema creation, migration helpers, row mapping, JSON serialization helpers, and transaction/table helpers into `isomer_labs.runtime.sqlite`.
- Keep `isomer_labs.runtime.store` as the canonical Workspace Runtime query and mutation service, backed by the new records and SQLite modules.
- Keep `isomer_labs.runtime.validation` as the canonical Runtime inspection and validation service, including semantic file locator and validation helper logic.
- Preserve the `isomer-cli` user interface: command names, flags, JSON output fields, exit behavior, and persisted runtime data meanings remain compatible unless another accepted spec changes them.
- Update source, tests, scripts, and docs to use the new canonical runtime imports, while treating `isomer-history/` as historical material outside the refactor scope.
- Tighten architecture tests so the runtime package has an explicit accepted file set and no longer relies on broad transition exemptions for the old runtime helper files.

## Capabilities

### New Capabilities

### Modified Capabilities

- `isomer-python-module-architecture`: Add requirements for the accepted internal Workspace Runtime module layout, breaking Python import migration, CLI compatibility preservation, and architecture guardrails for the consolidated runtime package.

## Impact

Affected code includes `src/isomer_labs/runtime`, runtime imports in `src/isomer_labs`, unit tests, manual harness helpers, scripts, and docs outside `isomer-history/`. The change intentionally breaks internal Python imports but does not change the `isomer-cli` interface, external command behavior, runtime SQLite schema meanings, Project Manifest formats, Topic Workspace Manifest formats, Houmao adapter material formats, or package dependencies.
