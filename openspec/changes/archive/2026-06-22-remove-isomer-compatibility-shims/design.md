## Context

The `refactor-isomer-cli-modular-print-json` change moved CLI, Houmao, and Workspace Runtime implementation into package families, then left five top-level import shims as a low-risk bridge: `houmao_cli_adapter.py`, `houmao_manifests.py`, `runtime_models.py`, `runtime_store.py`, and `runtime_validation.py`. That bridge helped the refactor land, but repository imports still use those names in several places, including CLI code, Houmao modules, runtime validation, and tests.

The project is pre-release, so keeping these aliases now creates more long-term cost than removing them. Contributors can see both the canonical package modules and old top-level names, and tests currently bless the shim files as acceptable architecture. This cleanup should make the package families the only internal import surface while preserving the `isomer_labs.cli` package entry point.

## Goals / Non-Goals

**Goals:**

- Remove the five non-CLI compatibility shim files from `src/isomer_labs`.
- Update source imports, tests, and mock patch targets to use canonical package paths.
- Update the source architecture guard so the removed shim names are forbidden and future compatibility shims need an explicit new decision.
- Preserve user-facing CLI behavior and Python APIs under the new package modules.
- Keep `isomer_labs.cli`, `isomer_labs.cli:main`, `cli.app`, and `cli.build_parser()` unchanged.

**Non-Goals:**

- Do not remove the `isomer_labs.cli` package compatibility surface, because it is the installed entry point.
- Do not rename the canonical package modules introduced by the refactor.
- Do not change Workspace Runtime schema, Houmao manifest schema, JSON output wrapper, or command behavior.
- Do not maintain deprecated imports with warnings or lazy aliases.
- Do not clean up unrelated large top-level domain modules in this change.

## Decisions

### Decision 1: Delete shims instead of deprecating them

Delete the five shim files outright and update every in-repository import. A warning-based deprecation path would preserve two import styles and require tests to keep covering the alias modules, which is exactly the ambiguity this cleanup is meant to remove.

Alternative considered: keep the files with `DeprecationWarning`. That is friendlier to unknown external callers, but Isomer Labs is still pre-release and the old names only existed as a short-lived refactor bridge.

### Decision 2: Canonical imports point at package families

Houmao adapter code should import from `isomer_labs.houmao.adapter` and `isomer_labs.houmao.manifests`; runtime code should import from `isomer_labs.runtime.models`, `isomer_labs.runtime.store`, and `isomer_labs.runtime.validation`. Tests should patch the canonical modules where the implementation now imports dependencies.

Alternative considered: add intermediate package-level re-exports such as `isomer_labs.houmao.HoumaoAdapterFacade`. That could be useful later, but doing it here would replace one alias layer with another.

### Decision 3: Make the architecture guard reject removed shim filenames

The current guard treats the shim files as expected thin modules. This change should invert that posture: the old filenames must not exist, and no new top-level compatibility shim should be accepted without a new proposal. The test should still allow documented edge cases such as existing large domain modules that are out of scope for this cleanup.

Alternative considered: rely on `rg` checks only. A dedicated architecture test gives a durable failure mode in the normal unit suite.

## Risks / Trade-offs

- [Risk] External scripts may still import the old shim module names. Mitigation: mark the change as breaking and keep the canonical package paths stable.
- [Risk] Updating mock patch paths can accidentally stop intercepting subprocess calls or helper functions. Mitigation: run focused Houmao adapter tests plus the full unit suite.
- [Risk] Removing shims can expose import cycles hidden by the alias modules. Mitigation: update imports package by package and run `pixi run typecheck` and `pixi run test`.
- [Risk] The active Milestone 5 change may have work-in-progress imports to old names. Mitigation: search the full repository, including OpenSpec and tests, before applying the cleanup.

## Migration Plan

1. Replace source imports from removed modules with canonical package imports.
2. Replace test imports and patch targets with canonical package paths.
3. Remove the five shim files.
4. Update `tests/unit/test_source_architecture.py` to assert the shim files are absent and repository imports do not reference them.
5. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and relevant OpenSpec validation.

Rollback is straightforward before release: restore the five shim files from version control and relax the architecture guard.

## Open Questions

None.
