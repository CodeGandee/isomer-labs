## Context

The Milestone 1 CLI implementation currently concentrates parser setup, command callbacks, output formatting dispatch, and helper wrappers in `src/isomer_labs/cli.py`. The deeper Project discovery, TOML loading, Project Manifest parsing, Research Topic Config parsing, validation, Effective Topic Context resolution, Workspace Path Resolution, built-in registry, and rendering logic already live outside the parser layer.

The active `implement-isomer-cli-project-discovery` design chose `argparse` as a conservative first implementation. That choice is now worth revisiting because the command surface already has nested groups (`topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`), Click is already in the package dependencies, and future CLI growth will benefit from Click's command composition and test runner.

## Goals / Non-Goals

**Goals:**

- Replace the `argparse` parser tree with a Click group and nested commands.
- Preserve existing user-facing command names, options, JSON response shapes, text output intent, and exit-code behavior.
- Keep parser concerns in `src/isomer_labs/cli.py` and avoid moving domain rules into Click callbacks.
- Keep `isomer_labs.cli:main` as the installed script entrypoint.
- Update tests so command behavior is covered through Click invocation and the installed script remains smoke-tested.
- Update the active Milestone 1 design and task wording so it no longer says `argparse`.

**Non-Goals:**

- Do not change Project Manifest, Research Topic Config, local active context, Effective Topic Context, Workspace Path Resolution, or diagnostic schemas.
- Do not add new commands, rename commands, or change command output contracts.
- Do not use Click parser errors for domain validation that should remain Isomer diagnostics.
- Do not resolve the unrelated full-repo Ruff findings under `teams/lfeng-team/execplan`.

## Decisions

### Decision 1: Use Click Only at the Command Boundary

Implement a Click root group for `isomer-cli` and nested groups for `topics`, `workspaces`, `context`, `paths`, and `schemas`. Keep command callbacks thin: they should collect option values, call existing domain helpers, and route output through the existing rendering helpers.

Alternative considered: rewrite the CLI around richer Click parameter types and callbacks that perform validation. Rejected because Isomer diagnostics need stable domain codes and JSON output; Click should parse syntax, not replace domain validation.

### Decision 2: Preserve the `main(argv) -> int` Test and Script Shape

Keep a `main(argv: Sequence[str] | None = None) -> int` wrapper around the Click command object so existing script metadata remains `isomer_labs.cli:main` and tests can still call `cli.main([...])`. The wrapper should invoke Click with controlled standalone behavior so command callbacks can return the same success or error status expected by current tests.

Alternative considered: expose the Click group directly as the script entrypoint. Rejected because it would force more test churn and make return-code handling less explicit.

### Decision 3: Model Global Options with Click Context Defaults

Support `--project`, `--manifest`, `--format`, and `--json` on commands that currently accept them. Use a small immutable or dictionary context object to pass parsed global options into callbacks instead of depending on `argparse.Namespace`.

Alternative considered: rely only on root-level options. Rejected because existing tests and users may place options near the leaf command, and preserving that flexibility reduces behavioral surprise.

### Decision 4: Use Click Testing for Parser Behavior

Update CLI tests to use `click.testing.CliRunner` where parser behavior matters, while keeping at least one installed-script smoke check through Pixi or direct `main` invocation. Domain behavior tests should continue to assert JSON bodies and diagnostics, not Click internals.

Alternative considered: keep stdout redirection around `main([...])` only. Rejected because Click has its own invocation semantics and test helpers that produce clearer parser-level assertions.

## Risks / Trade-offs

- [Risk] Click may render help text differently from `argparse`. → Mitigation: tests should assert command names and important options rather than exact full help formatting.
- [Risk] Option placement can regress when moving to nested Click groups. → Mitigation: add tests for root-level and command-level `--project` or `--json` forms that must remain valid.
- [Risk] Click exceptions or parser errors could bypass Isomer diagnostic JSON. → Mitigation: keep domain validation outside Click parameter types and reserve Click errors for syntax-level misuse.
- [Risk] The active Milestone 1 OpenSpec change currently names `argparse`. → Mitigation: update that design and task wording as part of this refactor so artifacts and implementation agree.

## Migration Plan

1. Update the active Milestone 1 design and task wording from `argparse` to `click`.
2. Replace `argparse` parser construction in `src/isomer_labs/cli.py` with a Click command tree.
3. Preserve existing command callback payloads and output paths by reusing the current `_cmd_*` logic or equivalent thin Click callbacks.
4. Update unit tests to use `CliRunner` for Click command invocation and keep installed script behavior covered.
5. Run targeted Ruff on the CLI and tests, plus `pixi run typecheck`, `pixi run test`, `pixi run validate-research-skills`, and record the existing full-repo `pixi run lint` limitation if unchanged.

Rollback is simple: revert the `src/isomer_labs/cli.py` parser-layer refactor and restore the previous `argparse` tests. Project files produced by `isomer-cli init` do not need migration because this change does not alter generated file formats.

## Open Questions

- Should root-level options remain accepted before every nested command, or is command-level option placement enough after the Click refactor? The safer first implementation should support both where practical.
