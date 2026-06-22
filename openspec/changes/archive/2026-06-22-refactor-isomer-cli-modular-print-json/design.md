## Context

The current `src/isomer_labs` package has grown through milestone slices that favored fast feature delivery. That worked, but it left several high-traffic surfaces as long modules: `cli.py` is roughly 3,000 lines, `runtime_store.py` is over 2,000 lines, and Houmao adapter behavior is split across large files. The next Milestone 5 work will add more CLI groups and adapter operations, so leaving the current shape in place will make every new command harder to review.

The public CLI also carries JSON mode as a repeated command option. Most tests and docs use command-local `--json`, while the desired shape is a single root-level switch: `isomer-cli --print-json <command> ...`. This mirrors the Houmao adapter habit of calling `houmao-mgr --print-json ...`, but the two flags live in different programs. Isomer's `--print-json` controls Isomer output only; Houmao's `--print-json` remains the adapter boundary for Houmao subprocess calls.

The refactor needs to preserve the package entry point `isomer_labs.cli:main` and the test-facing `build_parser()` surface. Turning `isomer_labs.cli` into a package is compatible with that import path, but it means `src/isomer_labs/cli.py` must be removed or moved because Python cannot import both a `cli.py` module and a `cli/` package with the same name from one directory.

## Goals / Non-Goals

**Goals:**

- Move CLI construction and command implementation into a modular `isomer_labs.cli` package organized by command group.
- Add root-level `--print-json` as the canonical way to request deterministic JSON for all `isomer-cli` command calls.
- Preserve structured human-readable text output when `--print-json` is absent.
- Keep the installed entry point, `main()`, `app`, and `build_parser()` import surfaces stable for tests and packaging.
- Split large source files into coherent package families with compatibility import shims where module names already exist and can be shimmed safely.
- Update tests and docs to prevent stale command-local JSON examples from returning.

**Non-Goals:**

- Do not change the JSON wrapper schema version or payload field names except where a command's existing behavior already changes in another accepted change.
- Do not change Houmao's public `houmao-mgr --print-json` command contract.
- Do not implement new Milestone 5 handoff behavior as part of this refactor.
- Do not redesign Workspace Runtime schema or adapter persistence semantics.
- Do not introduce a new CLI framework; keep Click.

## Decisions

### Decision 1: Convert `isomer_labs.cli` from one module into a package

Use `src/isomer_labs/cli/__init__.py` to export `app`, `main`, and `build_parser`, with implementation in package modules such as `app.py`, `options.py`, `output.py`, and `commands/`. This preserves the import path `isomer_labs.cli:main` while allowing command groups to live in separate files.

Alternative considered: keep `cli.py` as a thin shim over `cli/`. That is not viable with the same import name in the same directory; Python will choose one filesystem entry, and keeping both invites import ambiguity.

### Decision 2: Separate command registration from command execution

Each Click command module should register options and translate Click arguments into typed command inputs, then delegate to a command handler that returns one command result object. Shared output code should be the only place that decides between JSON and text rendering.

Alternative considered: move the existing `_cmd_*` functions into files with minimal restructuring. That lowers initial effort but preserves the core tangle between Click, orchestration, diagnostics, and rendering.

### Decision 3: Use root-level `--print-json` as the only documented JSON switch

Add `--print-json` to the root Click group and remove command-local `--json` and `--format` from the documented command surface. Tests and docs should invoke JSON mode as `isomer-cli --print-json validate`, `isomer-cli --print-json doctor`, or `isomer-cli --print-json runtime inspect --topic default`.

Alternative considered: keep `--json` everywhere as a compatibility alias. That reduces short-term churn but leaves two ways to express the same mode and undercuts the requested CLI shape. Because Isomer is still pre-release, the clean switch is preferable.

### Decision 4: Preserve compatibility surfaces at import boundaries

The refactor may leave compatibility modules for existing non-CLI imports, such as `houmao_cli_adapter.py`, `houmao_manifests.py`, `runtime_store.py`, `runtime_models.py`, and `runtime_validation.py`, if their implementation moves into package families. Those shims should re-export public names and contain little or no business logic.

Alternative considered: update every import and remove all old module files in one pass. That creates a large mechanical diff and raises the chance of missing external or test imports.

### Decision 5: Use package families, not a generic utilities drawer

Organize code around domain and command ownership: `cli/`, `runtime/`, `houmao/`, and later package families as needed. Shared helpers should move only when at least two module families use them and the target name is more specific than `utils`.

Alternative considered: create broad `commands.py`, `services.py`, or `utils.py` modules. Those names make the tree look smaller while recreating the same long-file problem under new names.

### Decision 6: Make module size a review guard, not a hard runtime rule

Add lightweight tests or validation that report unexpectedly large implementation files and direct contributors toward package modules. Compatibility shims and generated or schema-adjacent files may be exempt when they contain little behavior.

Alternative considered: enforce a strict line-count cap in lint. That is brittle during active refactors and can encourage arbitrary file splits that do not improve ownership.

## Risks / Trade-offs

- [Risk] The CLI package conversion can break `isomer_labs.cli:main` or `from isomer_labs import cli`. Mitigation: make the package `__init__.py` export the same public names and add direct import tests.
- [Risk] Moving command code while changing output flags can make test failures hard to diagnose. Mitigation: stage implementation so the command-result/output layer lands before command groups move one by one.
- [Risk] Docs and tests may leave stale `--json` examples. Mitigation: add repository-local checks for stale `isomer-cli ... --json` and `--format json` documentation examples.
- [Risk] A package split can create import cycles between command modules, context resolution, runtime store, and Houmao adapter helpers. Mitigation: keep command modules thin and move shared command support into explicit `cli.context`, `cli.selection`, or domain package modules.
- [Risk] The active Milestone 5 change may touch nearby CLI and Houmao adapter code. Mitigation: implement this refactor before adding more Milestone 5 commands or rebase Milestone 5 work onto the new command module boundaries.

## Migration Plan

1. Introduce shared command-result and output-mode helpers with `--print-json` support while the existing command bodies are still available.
2. Convert `isomer_labs.cli` from `cli.py` to a package and preserve `app`, `main`, and `build_parser()` imports.
3. Move command groups into `cli/commands/` modules, starting with low-dependency commands (`schemas`, `topics`, `workspaces`) and ending with runtime and Houmao-heavy commands.
4. Move reusable Houmao manifest CLI helpers out of CLI command modules into `houmao/` package modules.
5. Split large runtime and adapter modules into package families with compatibility shims where useful.
6. Update tests to use `--print-json` before the command name and verify text output remains structured by default.
7. Update docs and documentation validation to remove stale command-local JSON examples.

Rollback is straightforward before release: restore the previous `cli.py` command registration and command-local JSON options from version control. Runtime data is not migrated by this change.

## Open Questions

None.
