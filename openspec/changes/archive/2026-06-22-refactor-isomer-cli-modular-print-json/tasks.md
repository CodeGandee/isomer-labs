## 1. Output Contract Foundation

- [x] 1.1 Add a shared CLI output mode model that records whether root-level `--print-json` is active and defaults to structured text.
- [x] 1.2 Add a shared command result or emit helper that renders the existing `isomer-cli-output.v1` JSON wrapper in JSON mode and text lines plus diagnostics in text mode.
- [x] 1.3 Add root Click option `--print-json` and pass the output mode through command context.
- [x] 1.4 Remove documented command-local `--json` and `--format` options from the CLI option decorators.
- [x] 1.5 Add tests proving `isomer-cli --print-json validate`, `doctor`, `runtime inspect`, and a nested `team-instances` command emit deterministic JSON.
- [x] 1.6 Add tests proving commands without `--print-json` emit structured human-readable text and do not emit the JSON wrapper.

## 2. CLI Package Split

- [x] 2.1 Convert `src/isomer_labs/cli.py` into a package-backed `src/isomer_labs/cli/` implementation while preserving the import path `isomer_labs.cli`.
- [x] 2.2 Add `src/isomer_labs/cli/__init__.py` exports for `app`, `main`, and `build_parser()`.
- [x] 2.3 Move root app construction and command registration orchestration into `src/isomer_labs/cli/app.py`.
- [x] 2.4 Move common CLI options, topic selection handling, and option merging into `src/isomer_labs/cli/options.py` or equivalent.
- [x] 2.5 Move shared CLI output rendering into `src/isomer_labs/cli/output.py` or equivalent.
- [x] 2.6 Split low-dependency command groups into command modules for `init`, `validate`, `topics`, `workspaces`, `context`, `paths`, and `schemas`.
- [x] 2.7 Split `doctor`, `runtime`, `team-templates`, and `team-profiles` command groups into command modules.
- [x] 2.8 Split Agent Team Instance, adapter-link, launch-material, launch, inspect-live, stop, reconcile, and adopt command handling into command-group modules under `cli/commands/team_instances/`.
- [x] 2.9 Add import and Click parser tests that prove `from isomer_labs import cli`, `cli.app`, `cli.main`, and `cli.build_parser()` still work.

## 3. Domain Package Modularization

- [x] 3.1 Move Houmao adapter command catalog, runner, facade, path helpers, and result dataclasses into a `src/isomer_labs/houmao/` package family.
- [x] 3.2 Move Houmao JSON manifest creation, validation, reconciliation, and live-state collection helpers into cohesive `houmao/` package modules.
- [x] 3.3 Keep `houmao_cli_adapter.py` and `houmao_manifests.py` as compatibility shims or update all repository imports and document intentional import removal.
- [x] 3.4 Split Workspace Runtime store schema creation, row mapping, store methods, and transaction helpers into a `src/isomer_labs/runtime/` package family.
- [x] 3.5 Split Workspace Runtime validation into focused runtime validation modules while preserving existing public validation functions.
- [x] 3.6 Keep `runtime_store.py`, `runtime_models.py`, and `runtime_validation.py` as compatibility shims or update all repository imports and document intentional import removal.
- [x] 3.7 Avoid generic `utils.py` modules unless the helper is used by multiple package families and has a specific owner name.

## 4. Regression Guards

- [x] 4.1 Add a repository-local module-size or package-boundary validation test for `src/isomer_labs`.
- [x] 4.2 Exempt explicit compatibility shims and documented edge cases from the module-size guard.
- [x] 4.3 Add tests or validation that fail when new CLI command implementation is added to a monolithic CLI module instead of command-group modules.
- [x] 4.4 Add checks that new package names use canonical Isomer language and do not promote Houmao-specific terms into generic package names.

## 5. Documentation and Spec Alignment

- [x] 5.1 Update `docs/isomer-cli.md` global options and all JSON examples to use root-level `--print-json`.
- [x] 5.2 Update README, getting-started, workflows, Houmao adapter, and troubleshooting docs to replace stale Isomer CLI `--json` examples.
- [x] 5.3 Preserve Houmao subprocess documentation that uses `houmao-mgr --print-json`, making clear that it is a Houmao command flag, not the Isomer output switch.
- [x] 5.4 Extend documentation validation to report stale `isomer-cli` examples using command-local `--json` or `--format json`.
- [x] 5.5 Update tests that parse the CLI reference or command coverage so they expect `--print-json` in examples and docs.

## 6. Verification

- [x] 6.1 Run `openspec validate refactor-isomer-cli-modular-print-json --strict`.
- [x] 6.2 Run `openspec validate --all --strict`.
- [x] 6.3 Run `pixi run lint`.
- [x] 6.4 Run `pixi run typecheck`.
- [x] 6.5 Run `pixi run test`.
- [x] 6.6 Run `pixi run validate-research-skills`.
- [x] 6.7 Run `pixi run docs-validate`.
