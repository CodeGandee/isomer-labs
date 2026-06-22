## Why

The `src/isomer_labs` package has reached the point where core behavior is concentrated in long modules, especially the roughly 3,000-line `cli.py`, which slows down review and makes the upcoming Milestone 5 CLI work harder to extend safely. The CLI also repeats command-local `--json` and `--format json` options even though users and future Operator Agent callers need one global machine-output switch that applies consistently to every command.

## What Changes

- Introduce a modular source layout under `src/isomer_labs/` that groups related implementation into package families instead of expanding long single-file modules.
- Split the `isomer-cli` implementation into a CLI package with root app construction, shared option parsing, output rendering, and command-group modules.
- **BREAKING** Replace command-local `--json` and `--format json` as the canonical JSON interface with root-level `isomer-cli --print-json <command> ...`, which switches every command invocation to deterministic JSON output.
- Preserve structured human-readable text output as the default when `--print-json` is not present.
- Keep the installed entry point `isomer_labs.cli:main` and `build_parser()` compatibility surface available while moving implementation behind it.
- Update CLI tests and docs so examples, command reference text, and troubleshooting guidance use root-level `--print-json`.

## Capabilities

### New Capabilities

- `isomer-python-module-architecture`: Defines maintainable Python package boundaries for Isomer source modules, including CLI package structure, cohesive module families, compatibility shims, and tests that prevent large monolithic implementation files from returning.

### Modified Capabilities

- `isomer-cli-project-discovery`: Replace command-local JSON output options with root-level `--print-json`, preserve deterministic JSON payloads, and require structured text output when JSON mode is not selected.
- `isomer-cli-doctor-diagnostics`: Update the doctor output contract so `isomer-cli --print-json doctor` is the canonical JSON invocation while the read-only text posture remains unchanged.
- `workspace-runtime-persistence`: Update runtime command JSON scenarios to use root-level `--print-json` for runtime commands and Agent Team Instance command output.
- `isomer-documentation-system-guide`: Update documentation requirements so the CLI reference, workflows, troubleshooting, and command coverage validation reflect the new global JSON mode and stale `--json` examples are removed.

## Impact

- Affects `src/isomer_labs/cli.py`, `src/isomer_labs/__main__.py`, CLI command tests, documentation validation, and public CLI documentation.
- Likely introduces `src/isomer_labs/cli/`, `src/isomer_labs/runtime/`, and `src/isomer_labs/houmao/` package families while keeping compatibility imports where existing tests or entry points require them.
- Requires updating tests that currently invoke `--json` on individual commands and docs that show command-local JSON flags.
- Does not change Houmao's own `houmao-mgr --print-json` boundary, which remains the adapter-facing Houmao CLI contract.
