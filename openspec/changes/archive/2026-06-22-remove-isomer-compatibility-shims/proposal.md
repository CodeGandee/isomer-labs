## Why

The previous modularization kept top-level compatibility shims so the refactor could land safely, but this repository is still pre-release and those aliases now make `src/isomer_labs` look more stable and broader than it should be. Removing the shims now forces internal code and tests to use the canonical package families before more Milestone 5 work depends on the old names.

## What Changes

- **BREAKING** Remove the top-level compatibility modules `houmao_cli_adapter.py`, `houmao_manifests.py`, `runtime_models.py`, `runtime_store.py`, and `runtime_validation.py`.
- Update all repository imports, tests, mocks, and patch targets to import from `isomer_labs.houmao.*` and `isomer_labs.runtime.*`.
- Update the source architecture regression guard so the removed shim filenames are disallowed rather than treated as allowed thin files.
- Keep `isomer_labs.cli` package entry points unchanged; this cleanup only removes non-CLI shim modules.
- Do not add new replacement shims, generic `compat.py`, or broad alias modules.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-python-module-architecture`: Remove the compatibility-shim allowance for moved non-CLI modules and require canonical package imports inside the repository.

## Impact

- Affects imports in `src/isomer_labs/cli/app.py`, `src/isomer_labs/houmao/`, `src/isomer_labs/runtime/`, and unit tests that currently import or patch shim module paths.
- Removes five top-level Python files from `src/isomer_labs`.
- Changes no runtime database schema, CLI command behavior, JSON output contract, or Houmao subprocess contract.
- May break external callers that still import the old top-level module names; the project will treat those names as intentionally removed internal compatibility aliases.
