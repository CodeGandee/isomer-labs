## Why

The installed CLI currently treats most group invocations without a subcommand as invocation errors, even though the output mostly resembles help text. This makes basic discovery paths like `isomer-cli project`, `isomer-cli project topics`, and `isomer-cli ext research` feel broken and buries the useful top-level command list below a stale long command dump.

## What Changes

- Make every CLI command group render its help and exit successfully when invoked without a subcommand.
- Refresh the top-level `isomer-cli` help introduction so it names the main command groups, links to the GitHub repository and GitHub Pages documentation, and explains each top-level subcommand.
- Preserve explicit `--help` behavior and existing invocation diagnostics for genuinely malformed commands such as unknown subcommands, invalid options, or missing required command arguments.
- Add tests covering top-level and nested no-argument group invocation.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-project-discovery`: Define CLI group help as the normal discovery behavior at every command level and refresh the top-level help contract with canonical project links and top-level command descriptions.

## Impact

- Affected code: Click app bootstrap and command group registration under `src/isomer_labs/cli/`.
- Affected tests: CLI tests for help output, exit status, and no-argument nested group behavior.
- User-facing behavior: no-argument group invocations that currently exit `2` will exit `0` and print help.
- Dependencies: no new runtime dependencies.
