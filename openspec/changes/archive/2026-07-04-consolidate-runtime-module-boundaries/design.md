## Context

The previous package modularization moved root-level runtime code into `src/isomer_labs/runtime`, but it deliberately left the internal runtime package mostly intact. The current package now has a large `store.py`, a large `validation_checks.py`, a broad `models.py`, and many small helper files that are coupled to those larger modules. The result is an architecture that is package-scoped but still difficult to navigate because record definitions, schema creation, row mapping, serialization, validation helpers, and domain service behavior are spread across file boundaries that do not match durable responsibilities.

The user-facing contract is `isomer-cli`, not the internal Python runtime import paths. This change can therefore be breaking for internal imports while preserving command names, options, JSON output shape, persisted runtime schema meanings, and other externally visible CLI behavior. Historical material under `isomer-history/` is out of scope and should not drive migration decisions or architecture-test failures.

## Goals / Non-Goals

**Goals:**

- Reduce `src/isomer_labs/runtime` to a small canonical module set with clear responsibilities: `records.py`, `sqlite.py`, `store.py`, and `validation.py`.
- Move runtime record dataclasses, status constants, timestamp helpers, and runtime id helpers into `runtime.records`.
- Move SQLite schema creation, migration helpers, row mapping, JSON serialization helpers, and transaction/table helpers into `runtime.sqlite`.
- Keep `runtime.store` as the canonical Workspace Runtime query and mutation service used by CLI handlers, Houmao adapter integration, artifact format integration, records code, workspace reset code, tests, and manual harnesses.
- Keep `runtime.validation` as the canonical Workspace Runtime inspection and validation service.
- Update all in-scope repository imports to the new canonical runtime paths.
- Tighten architecture tests so old helper files cannot return and broad transition exemptions for runtime files are removed.

**Non-Goals:**

- Do not change the `isomer-cli` command surface, flags, options, JSON field names, output contracts, or exit behavior.
- Do not change Workspace Runtime SQLite table names, column meanings, schema version semantics, persisted file formats, Project Manifest formats, Topic Workspace Manifest formats, or Houmao adapter material formats.
- Do not introduce new runtime dependencies.
- Do not preserve compatibility for internal Python import paths such as `isomer_labs.runtime.models`, `isomer_labs.runtime.rows`, `isomer_labs.runtime.schema`, or `isomer_labs.runtime.validation_checks`.
- Do not update or validate historical material under `isomer-history/`.

## Decisions

### Use Four Runtime Modules as the Accepted Boundary

The accepted runtime implementation boundary will be:

```text
runtime/
  __init__.py
  records.py
  sqlite.py
  store.py
  validation.py
```

`records.py` owns the typed runtime record contract. `sqlite.py` owns persistence mechanics. `store.py` owns runtime queries, mutations, initialization, readiness preparation, and Agent Team Instance creation. `validation.py` owns inspection and validation orchestration plus validator helpers.

Alternative considered: keep `models.py` as a compatibility facade and only merge smaller helper files. That would reduce file count, but it would preserve the old import shape and weaken the architecture signal. Since the user accepts internal breakage, a clean canonical import set is preferable.

### Keep Store as the Runtime Mutation Service, Not a Table-by-Table Helper Folder

`WorkspaceRuntimeStore` should stay in `store.py` because many callers already depend on it as the durable mutation and query API. The refactor should remove incidental helper imports around the store, not create many new table-specific store modules that force callers to learn a larger API.

Alternative considered: split store methods into separate files by record type. That would reduce line count quickly, but it would keep coupled record, schema, and validation concepts scattered and would not address the user's complaint about blurry boundaries.

### Move Persistence Mechanics Behind `runtime.sqlite`

Schema creation, reset schema creation, row-to-record mapping, JSON serialization helpers, table discovery, and transaction helpers all change for the same reason: the SQLite representation of Workspace Runtime. Putting them in `sqlite.py` makes it obvious that these helpers are persistence internals rather than domain concepts.

Alternative considered: keep `schema.py` and `rows.py` separate because they are distinct technical activities. That split is mechanically neat but makes each runtime record change touch multiple sibling files, so it is not the best boundary for this package.

### Preserve CLI Behavior While Breaking Internal Runtime Imports

All CLI entry points and output contracts must remain stable. The breaking surface is limited to Python imports inside the repository and any untracked local callers that imported runtime internals directly.

Alternative considered: preserve compatibility shims for `runtime.models` and related modules. That would soften migration for unknown callers, but the repository is preparing for a clean package layout and the user explicitly allowed breaking internal changes.

### Treat `isomer-history/` as Out of Scope

Search-and-rewrite passes, architecture tests, and documentation migration should ignore `isomer-history/`. The directory is historical material and must not block the runtime boundary cleanup.

Alternative considered: update every matching import in the repository tree. That would create noise in archival material and risk making history look current.

## Risks / Trade-offs

- Import churn may hide a behavior change → Keep implementation moves mechanical first, update imports in one pass, and rely on existing CLI-heavy tests for behavior.
- `store.py` may remain large after consolidation → Accept size temporarily only if architecture tests document the bound, then split internal helpers within `store.py` by cohesive method groups if needed.
- `runtime.validation` may become large after absorbing validators → Keep validator functions grouped by runtime concern inside the file and consider later extraction only if a new stable boundary appears.
- Internal users outside the repository may import removed modules → Treat this as an accepted breaking change and document the new import paths in the architecture spec.
- Merging schema and row mapping can make `sqlite.py` dense → Keep SQL table groups and row mapper groups in the same order so record changes are easy to audit.

## Migration Plan

1. Update architecture tests to describe the target runtime file set and ignore `isomer-history/` for import migration checks.
2. Rename or move `models.py` content into `records.py`, including adapter handoff records and runtime id helper functions.
3. Create `sqlite.py` from schema, reset schema, row mapping, JSON serialization, table discovery, and transaction helper code.
4. Update `store.py` imports to use `records.py` and `sqlite.py`, then fold readiness and Agent Instance identity helpers into `store.py`.
5. Update `validation.py` imports and fold validation checks, adapter handoff validation, validation utilities, workspace layout validation, workspace visibility validation, and semantic file locator helpers into it.
6. Delete obsolete runtime helper files and update all in-scope imports in `src/`, `tests/`, `scripts/`, and docs.
7. Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
8. If the refactor destabilizes behavior, roll back the runtime file moves and import rewrites as one source organization change.

## Open Questions

- Should architecture tests allow `store.py` or `validation.py` to exceed the current package-size threshold during this consolidation, or should implementation include enough local restructuring to keep both under the threshold immediately?
