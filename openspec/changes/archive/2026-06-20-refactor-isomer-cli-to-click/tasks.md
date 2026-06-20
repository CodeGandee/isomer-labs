## 1. Planning Artifact Alignment

- [x] 1.1 Update the active Milestone 1 design decision so it names `click` as the command-boundary library instead of `argparse`.
- [x] 1.2 Update the active Milestone 1 task wording so command wiring refers to `click` rather than `argparse`.
- [x] 1.3 Confirm `click` remains present in package dependencies and the installed script entrypoint remains `isomer_labs.cli:main`.

## 2. Click Command Layer

- [x] 2.1 Replace the `argparse` parser construction in `src/isomer_labs/cli.py` with a Click root command group.
- [x] 2.2 Add Click nested groups and commands for `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`.
- [x] 2.3 Preserve `main(argv: Sequence[str] | None = None) -> int` as the package script wrapper around the Click command object.
- [x] 2.4 Preserve root-level and command-level support for `--project`, `--manifest`, `--format`, and `--json` where existing commands accept them.
- [x] 2.5 Preserve topic selection options for `context show` and `paths preview`, including Research Topic, Topic Workspace, Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, and Topic Agent Team Profile selectors.
- [x] 2.6 Keep Project discovery, validation, Effective Topic Context resolution, Workspace Path Resolution, diagnostics, and rendering delegated to the existing non-CLI modules.
- [x] 2.7 Ensure Click parser errors are used only for syntax-level command misuse, not for domain validation that should return Isomer diagnostics.

## 3. Tests

- [x] 3.1 Update CLI tests to use Click-native invocation where useful, including help and nested command discovery.
- [x] 3.2 Preserve tests for `init` file creation, explicit topic id behavior, non-overwrite behavior, and no Workspace Runtime side effects.
- [x] 3.3 Preserve tests for `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list` JSON output compatibility.
- [x] 3.4 Add or preserve tests that command outputs retain stable Isomer diagnostic codes and do not leak secret values.
- [x] 3.5 Add coverage for root-level and command-level placement of common options so existing invocation patterns remain valid.
- [x] 3.6 Smoke-test the installed `isomer-cli` script through Pixi after the Click refactor.

## 4. Validation

- [x] 4.1 Run targeted Ruff on `src/isomer_labs` and the CLI unit tests.
- [x] 4.2 Run `pixi run typecheck`.
- [x] 4.3 Run `pixi run test`.
- [x] 4.4 Run `pixi run validate-research-skills`.
- [x] 4.5 Run `pixi run lint` and record any remaining unrelated full-repo Ruff findings if the existing `teams/lfeng-team/execplan` issues are still present.

Validation note: `pixi run lint` still fails on pre-existing `teams/lfeng-team/execplan` Ruff findings outside this Click refactor. Targeted Ruff for `src/isomer_labs` and `tests/unit/test_isomer_cli.py` passes.
