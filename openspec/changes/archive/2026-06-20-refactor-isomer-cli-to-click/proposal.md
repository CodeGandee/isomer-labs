## Why

The Milestone 1 CLI now has enough nested command structure that `click` is a better fit than hand-wired `argparse`. Refactoring the command layer now keeps the public `isomer-cli` surface stable while making future command additions easier to compose and test.

## What Changes

- Replace the `argparse` command parser in `src/isomer_labs/cli.py` with a `click` command group and nested subcommands.
- Preserve the existing command names, option names, exit codes, text output intent, and versioned JSON output shapes.
- Keep Project discovery, manifest parsing, validation, Effective Topic Context resolution, Workspace Path Resolution, diagnostics, rendering, and initialization logic in their existing domain modules.
- Update CLI tests to use Click-native invocation where useful while still covering the installed `isomer-cli` script behavior.
- Revise the Milestone 1 design note that currently chooses standard-library `argparse` so the accepted implementation direction matches the requested `click` refactor.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-project-discovery`: The command surface remains behavior-compatible, but the CLI parser and command registration implementation changes from `argparse` to `click`.

## Impact

- Affected package code: `src/isomer_labs/cli.py`, with possible small test-only helper changes.
- Affected tests: CLI help, installed script, command output, and failure-path tests should continue to pass after the `click` refactor.
- Affected dependency posture: `click` is already present in the project dependency list; no new runtime dependency should be needed.
- Affected OpenSpec artifacts: the active Milestone 1 CLI design and tasks should stop naming `argparse` as the intended implementation.
