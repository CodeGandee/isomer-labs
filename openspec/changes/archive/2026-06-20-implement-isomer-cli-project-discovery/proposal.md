## Why

Milestone 1 needs the first runnable Isomer core: a CLI that can discover a user-owned Project, load `.isomer-labs/manifest.toml`, validate registered Research Topic Config files, resolve Effective Topic Context, and preview workspace paths before any Workspace Runtime or agent execution exists. This gives later milestones a stable, testable foundation instead of letting project discovery, topic selection, and path rules become implicit behavior inside agents or adapters.

## What Changes

- Add the first platform-level `isomer-cli` command surface for project initialization, validation, topic listing, workspace listing, effective context inspection, path preview, and built-in schema listing.
- Implement Project discovery from explicit selectors, current directory ancestry, and supported Project environment overrides.
- Implement Project Manifest and Research Topic Config loading with validation for refs, schema versions, path bounds, topic-config mismatches, forbidden runtime truth, and forbidden secret material.
- Implement Effective Topic Context resolution for topic-scoped commands using explicit selectors, current-directory Topic Workspace selection, supported identity environment refs, `.isomer-labs/local.toml`, and Project Manifest defaults.
- Implement Workspace Path Resolution preview for Topic Workspace, Workspace Runtime, Artifact, Run, log, View Manifest, and Agent Workspace path surfaces without creating Workspace Runtime state.
- Add deterministic diagnostics and JSON-friendly output so tests, Operator Agent workflows, and future Execution Adapters can rely on stable behavior.
- Leave agent launch, Workspace Runtime SQLite creation, durable research records, Runs, Gates, and GUI startup out of scope for this change.

## Capabilities

### New Capabilities

- `isomer-cli-project-discovery`: Covers the Milestone 1 CLI command surface, Project discovery, manifest and topic-config validation, Effective Topic Context inspection, path preview, diagnostics, and initialization behavior needed before Workspace Runtime or team execution.

### Modified Capabilities

- None. Existing `cli-topic-context-resolution` and `workspace-path-resolution` requirements remain the source contracts; this change adds the concrete v1 CLI capability that implements and exposes their Milestone 1 subset.

## Impact

- Affected package code: `src/isomer_labs/`, especially new CLI, project discovery, manifest parsing, topic config, context resolution, path resolution, validation, and diagnostic modules.
- Affected packaging: `pyproject.toml` should expose an `isomer-cli` project script.
- Affected tests: unit tests should cover project discovery, manifest validation, topic selection precedence, path preview, diagnostics, and command output.
- Affected docs: `ROADMAP.md` can mark Milestone 1 steps complete as implementation lands; existing design docs remain authoritative for later milestones.
- New runtime dependencies should be avoided unless they materially simplify schema validation or command parsing; the current standard library plus existing project dependencies are enough for the first pass.
