## Why

`isomer-cli` is primarily operated by agents, but invocation failures can currently fall outside the deterministic Isomer output path. Raw Click messages or Python tracebacks leave agents guessing which argument was wrong, which command shape was expected, and whether a failed command mutated state.

## What Changes

- Add an agent-readable CLI error reporting contract for invocation errors, domain failures, and unexpected internal exceptions.
- Convert Click parse and usage errors into Isomer diagnostics instead of printing Click's raw error surface directly.
- Ensure unexpected Python exceptions are caught at the installed `isomer-cli` entrypoint and rendered as structured internal-error diagnostics by default.
- Preserve raw traceback visibility only behind an explicit debug mode for human debugging.
- Require wrong-format command invocations to include the problem, the expected command shape, and one to three valid examples for the nearest matching command.
- Preserve the existing `isomer-cli-output.v1` JSON wrapper when `--print-json` is requested, including for failures that happen before full command dispatch.
- Add tests and documentation for text and JSON failure behavior.

## Capabilities

### New Capabilities
- `isomer-cli-error-reporting`: define deterministic, agent-readable CLI failure output, invocation examples, traceback suppression, debug escape hatch behavior, and mutation-state reporting for command failures.

### Modified Capabilities
- None.

## Impact

- Affected code: `src/isomer_labs/cli/app.py`, `src/isomer_labs/cli/output.py`, `src/isomer_labs/diagnostics.py`, `src/isomer_labs/rendering.py`, and CLI command registration metadata for examples.
- Affected tests: unit tests that invoke `cli.main(...)`, Click usage-error paths, JSON/text output rendering, and unexpected exception handling.
- Affected docs: `docs/isomer-cli.md` output posture and command examples.
- Affected behavior: normal command diagnostics stay compatible; invocation failures and internal exceptions become structured, no-traceback failures by default; `--print-json` remains the deterministic path for agents.
