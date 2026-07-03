## 1. Architecture Guardrails

- [x] 1.1 Update source architecture tests to describe the target package families and reject new feature-sized root modules.
- [x] 1.2 Replace broad large-file exemptions with transition-aware checks for root modules, package modules, and `cli/app.py`.

## 2. Core and Model Foundations

- [x] 2.1 Create a `core` package for low-level helpers and schema registries.
- [x] 2.2 Move diagnostics, path helpers, TOML loading, rendering helpers, and built-in schema registry code into `core`.
- [x] 2.3 Convert `models.py` into a package-owned transitional model surface that preserves existing `isomer_labs.models` imports.
- [x] 2.4 Update source and tests to use canonical `core` imports.

## 3. Domain Package Moves

- [x] 3.1 Create `project`, `workspace`, `teams`, and `records` package families.
- [x] 3.2 Move Project discovery, manifest parsing, validation, context resolution, topics, cleanup, content-root, and doctor code under `project`.
- [x] 3.3 Move Topic Workspace layout, manifest, semantic path, actor, guidance, Pixi, reset, temporary-surface, self-query, and workspace-ref code under `workspace`.
- [x] 3.4 Move Team Repository, Template, Profile, Profile Bundle, instantiation packet, and packet validation code under `teams`.
- [x] 3.5 Move research record store code under `records`.
- [x] 3.6 Update internal imports, tests, scripts, and docs to canonical package paths.

## 4. CLI Handler Extraction

- [x] 4.1 Add `cli.handlers` modules for Project, Workspace, Teams, Runtime, Team Instances, Records, Self, and Schemas command handlers.
- [x] 4.2 Move command handler bodies out of `cli/app.py` while preserving command registration modules and command output behavior.
- [x] 4.3 Keep `cli/app.py` as app bootstrap, shared Click app construction, command registration, and public `app`, `main`, and `build_parser()` exports.

## 5. Compatibility and Documentation

- [x] 5.1 Preserve documented public entry points such as `isomer_labs.cli:main` and package import smoke tests.
- [x] 5.2 Update architecture docs or developer-facing references that mention old root module paths.
- [x] 5.3 Remove obsolete architecture-test exemptions for moved root files.

## 6. Verification

- [x] 6.1 Run `pixi run lint`.
- [x] 6.2 Run `pixi run typecheck`.
- [x] 6.3 Run `pixi run test`.
- [x] 6.4 Run `openspec status --change modularize-isomer-labs-package`.
