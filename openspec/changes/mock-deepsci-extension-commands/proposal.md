## Why

The DeepScientist skills we are migrating expect an MCP-style harness for durable memory, quest artifacts, and background command state. Isomer Labs needs a first compatibility layer that preserves those command input and output shapes while the migrated skills are still being rewritten and before the final Isomer research-storage semantics are bound.

## What Changes

- Add a mocked `isomer-cli ext deepsci` command family for DeepScientist-flavored harness calls.
- Preserve the DeepScientist-visible request and response formats for the first supported `memory`, `artifact`, and `bash_exec` commands.
- Store mock state in the existing Isomer workspace runtime SQLite database, with Python query code providing search, listing, and lookup behavior.
- Mark mocked responses explicitly enough for operators and tests to know that no real shell execution, remote fetch, Git mutation, or final research artifact binding has occurred.
- Use DeepScientist source-code fixtures as the compatibility reference during implementation, then replace individual mocks with real Isomer behavior as each migrated skill is completed.

## Capabilities

### New Capabilities

- `deepsci-extension-command-mocks`: Defines the mocked DeepScientist-compatible `isomer-cli ext deepsci` command surface, SQLite-backed mock storage, and compatibility response envelopes.

### Modified Capabilities

- None.

## Impact

This change affects the Isomer CLI command tree, runtime persistence layer, and test fixtures. It should not change the existing research recording contracts, workspace runtime contract, or topic workspace layout requirements; it reuses them as the substrate for a temporary DeepScientist compatibility extension.
