## Why

Several `src/isomer_labs` packages still split tightly coupled classes and helper functions across neighboring files whose names describe implementation fragments rather than Isomer concepts. The recent Workspace Runtime consolidation showed that fewer, clearer modules make ownership easier to read without changing the `isomer-cli` command surface.

## What Changes

- **BREAKING**: Remove or rename internal non-CLI modules whose contents are helper shards, and migrate repository imports to the new canonical package paths.
- Consolidate Artifact Format processing helpers so resolution, validation, payload loading, and rendering live in one processing module.
- Consolidate DeepScientist compatibility tool registry, service dispatch, and CLI JSON helpers into one tool-facing module while keeping the existing `isomer-cli deepsci-ext` behavior.
- Consolidate Topic Team Specialization helpers by folding template harness checks into template handling and packet validation into Topic Team Instantiation handling.
- Rename and consolidate Workspace path helpers around canonical terms: Semantic Workspace Surface Label, Workspace Path Resolution, and Local Tmp Surface policy.
- Update source architecture tests so the accepted module set prevents the old helper-shard files from returning.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-python-module-architecture`: Require cohesive domain package modules for Artifact Format processing, DeepScientist extension tooling, Topic Team Specialization, and Workspace Path Resolution helpers while preserving the stable `isomer-cli` interface.

## Impact

Affected code is internal to `src/isomer_labs/artifact_formats`, `src/isomer_labs/deepsci_ext`, `src/isomer_labs/teams`, `src/isomer_labs/workspace`, repository imports, and source architecture tests. The project script entry point and CLI command names remain unchanged; internal imports from the removed modules become breaking changes.
