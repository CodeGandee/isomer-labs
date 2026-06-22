## 1. Import Migration

- [x] 1.1 Replace source imports from `isomer_labs.houmao_cli_adapter` with `isomer_labs.houmao.adapter`.
- [x] 1.2 Replace source imports from `isomer_labs.houmao_manifests` with `isomer_labs.houmao.manifests`.
- [x] 1.3 Replace source imports from `isomer_labs.runtime_models` with `isomer_labs.runtime.models`.
- [x] 1.4 Replace source imports from `isomer_labs.runtime_store` with `isomer_labs.runtime.store`.
- [x] 1.5 Replace source imports from `isomer_labs.runtime_validation` with `isomer_labs.runtime.validation`.

## 2. Test and Patch Target Migration

- [x] 2.1 Update unit test imports to use canonical Houmao and runtime package paths.
- [x] 2.2 Update mock patch targets that currently reference removed shim module paths.
- [x] 2.3 Add or update import smoke tests for canonical package modules.

## 3. Shim Removal

- [x] 3.1 Delete `src/isomer_labs/houmao_cli_adapter.py`.
- [x] 3.2 Delete `src/isomer_labs/houmao_manifests.py`.
- [x] 3.3 Delete `src/isomer_labs/runtime_models.py`.
- [x] 3.4 Delete `src/isomer_labs/runtime_store.py`.
- [x] 3.5 Delete `src/isomer_labs/runtime_validation.py`.

## 4. Architecture Guard Updates

- [x] 4.1 Update `tests/unit/test_source_architecture.py` so the removed shim filenames are forbidden.
- [x] 4.2 Add a repository import-surface check that fails on references to the removed shim module paths.
- [x] 4.3 Keep documented module-size exemptions scoped to current edge cases and avoid adding a new shim exemption.

## 5. Verification

- [x] 5.1 Run `openspec validate remove-isomer-compatibility-shims --strict`.
- [x] 5.2 Run `openspec validate --all --strict`.
- [x] 5.3 Run `pixi run lint`.
- [x] 5.4 Run `pixi run typecheck`.
- [x] 5.5 Run `pixi run test`.
