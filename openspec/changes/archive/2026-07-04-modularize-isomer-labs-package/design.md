## Context

`src/isomer_labs` already has several healthy package boundaries: `cli`, `runtime`, `houmao`, `artifact_formats`, and `deepsci_ext`. The package root still holds many feature modules directly, including Project discovery and validation, Topic Workspace Manifest handling, semantic path resolution, Team Template and Profile logic, records, reset, doctor checks, and shared dataclasses. Several files exceed 700 lines, and architecture tests currently permit them through broad exemptions.

The refactor should preserve behavior while changing ownership. This is an internal architecture change, not a CLI or data-format change.

## Goals / Non-Goals

**Goals:**

- Move root implementation modules into bounded-context packages with canonical import paths.
- Keep root package files minimal and enforceable through architecture tests.
- Split large model and service modules by responsibility without changing public CLI behavior.
- Move command handler bodies out of `cli/app.py` while preserving Click command registration and output contracts.
- Keep the change incremental enough that lint, typecheck, and unit tests can validate each phase.

**Non-Goals:**

- Do not rename public CLI commands or JSON output fields.
- Do not change Project Manifest, Topic Workspace Manifest, Team Repository, Runtime, or Houmao adapter data formats.
- Do not introduce new runtime dependencies.
- Do not archive or redesign existing OpenSpec capabilities beyond Python module architecture.
- Do not refactor external `teams/`, `skillset/`, or Houmao checkout material.

## Decisions

### Use bounded-context packages instead of type-only folders

The package will group implementation by Isomer domain boundary:

```text
isomer_labs/
  core/
  project/
  workspace/
  teams/
  records/
  runtime/
  houmao/
  artifact_formats/
  deepsci_ext/
  cli/
```

This is preferable to folders such as `utils`, `services`, or `models` alone because Isomer concepts already provide clearer ownership boundaries. Shared low-level helpers belong in `core`; domain dataclasses should live with their domain package and be re-exported through compatibility surfaces only while migration is underway.

### Preserve public behavior and update internal imports

The stable public surfaces are CLI entry points, command names, output schema, and runtime behavior. Internal imports may change. Where a module is too widely imported to move atomically, create package `__init__.py` re-exports during the same change, then update repository imports toward canonical paths.

Long-lived top-level compatibility shim modules should not be introduced. The package is preparing for PyPI, so this is the right time to make source imports canonical.

### Split CLI in two layers

`cli/commands/*` should remain the Click registration layer. Command handler implementations should move to `cli/handlers/*`, with shared context discovery and output helpers in `cli/context.py` and `cli/emit.py`. `cli/app.py` should define the app, register command groups, expose `app`, `main`, and `build_parser()`, and little else.

This avoids hiding business behavior in Click glue while preserving the command modules already introduced by earlier refactors.

### Split large modules by responsibility before moving tests

Largest root modules should move in a priority order that reduces dependency churn:

1. `core`: `diagnostics`, `path_utils`, `toml_loader`, `rendering`, `builtins`.
2. `teams`: Team Repositories, Team Templates, Team Profiles, Profile Bundles, instantiation packets, and workspace refs used by profiles.
3. `workspace`: semantic surfaces, Topic Workspace Manifest parsing and rendering, semantic path resolution, topic actors, topic guidance, Topic Pixi, temporary surfaces.
4. `project`: discovery, init, manifest parsing, validation, effective context, topics, cleanup, content root, doctor.
5. `records`: research record store.
6. `cli.handlers`: command handlers extracted from `cli/app.py`.

Runtime and Houmao are already package-scoped and should be left mostly intact except for import updates caused by moved modules.

## Risks / Trade-offs

- Import-cycle risk -> Move dependency-light modules first, keep package `__init__.py` exports narrow, and run mypy after each package move.
- Large diff risk -> Use mechanical moves before semantic splits when possible; split files along existing function clusters.
- Test fragility -> Preserve function names while relocating modules, then update imports in tests and source together.
- Hidden public import users -> This project is pre-PyPI, but `isomer_labs.cli:main` and documented package imports must keep working.
- Architecture tests becoming too strict -> Introduce limits after each package boundary exists, then remove broad exemptions gradually.

## Migration Plan

1. Add architecture tests that describe the target root layout and maximum root-module/file sizes, initially with a small transition allowlist.
2. Move low-level helpers into `core` and update imports.
3. Split domain model dataclasses into package-owned modules while keeping `isomer_labs.models` as a transitional re-export surface.
4. Move Teams, Workspace, Project, and Records modules into their packages, updating source and tests.
5. Extract `cli/app.py` command handlers into `cli/handlers`.
6. Tighten architecture tests by removing transition exemptions.
7. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `openspec status`.

Rollback is straightforward because this is source organization only: revert the package moves and import updates as one commit if the refactor destabilizes behavior.

## Open Questions

- Should `doctor` live under `project` because it inspects Project health, or under an `operations` package with cleanup and content-root relocation?
- Should `topic_reset` be part of `workspace` or become an `operations.topic_reset` package?
- Should `models.py` remain as a public re-export facade after this change, or should architecture tests require direct domain model imports?
