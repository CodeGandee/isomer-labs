## Why

Milestone 4 needs a safe preflight surface that can tell users and the Operator Agent whether the local Project is ready for topic-scoped runtime preparation before Houmao launch work begins. Pixi is now a required Project dependency, and Isomer needs one read-only command that checks the Pixi installation, Project-level Pixi configuration, and explicit Project Manifest topic environment bindings without mutating Topic Workspaces or Workspace Runtime state.

## What Changes

- Add a top-level `isomer-cli doctor` command implemented through the existing Click command surface.
- Make `doctor` read-only: it reports diagnostics and readiness facts but never installs Pixi environments, writes Topic Workspace files, creates `state.sqlite`, or records Workspace Runtime readiness.
- Let `doctor` run in dependency-only mode when no Project is discoverable, and in Project or topic mode when Project discovery and optional topic selectors are available.
- Inspect the required Pixi binary, Pixi version, Project-level Pixi manifest (`pyproject.toml` or `pixi.toml`), optional `requires-pixi` compatibility, lockfile presence, and explicit Project Manifest topic-to-Pixi-environment bindings.
- Add a minimal Project Manifest environment-binding contract so `doctor` can validate topic use of one or more Project-root Pixi environments and explicit standalone Pixi manifest bindings without inferring topic relationships from environment names.
- Emit deterministic text and versioned JSON output that reuses Isomer diagnostics and avoids exposing secrets or raw provider payloads.

## Capabilities

### New Capabilities

- `isomer-cli-doctor-diagnostics`: Read-only CLI diagnostics for required dependencies, Pixi readiness, Project-level Pixi configuration, Project Manifest topic environment bindings, and launch preconditions.

### Modified Capabilities

- `isomer-cli-project-discovery`: Add `doctor` to the Click-backed command surface and JSON-output contract expectations.
- `cli-topic-context-resolution`: Extend Project Manifest topic registration semantics with provider-neutral Pixi environment bindings that `doctor` and later runtime preparation can validate before Workspace Runtime mutation.

## Impact

- Affected code: `src/isomer_labs/cli.py`, `src/isomer_labs/manifest.py`, `src/isomer_labs/models.py`, validation helpers, and new Pixi/doctor support module(s).
- Affected tests: unit tests for help text, dependency-only doctor output, Project-scoped doctor output, topic-scoped Project Manifest Pixi environment binding validation, read-only behavior, and JSON shape.
- Affected docs: README/CLAUDE command examples, Project Manifest topic environment binding docs, and Milestone 4 roadmap wording for read-only `doctor` versus future mutating preparation.
- Dependencies: no new Python package is required; implementation shells out to the required `pixi` executable or uses local TOML parsing for Project manifest checks.
