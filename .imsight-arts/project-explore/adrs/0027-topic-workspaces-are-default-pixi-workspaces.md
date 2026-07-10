# Topic Workspaces Are Default Pixi Workspaces

Isomer Labs will make every Topic Workspace a Pixi workspace by default. Each Topic Workspace contains its own Pixi manifest and lockfile, installs its own environment under `<topic-workspace>/.pixi/`, and exposes that environment as the shared default Python environment for all Agent Workspaces under the topic. The Project root may keep a Project-level Pixi environment for Isomer platform tooling, but research-specific dependencies live in Topic Workspace Pixi environments. This replaces the previous default of binding Research Topics to environments declared in the Project-level Pixi manifest.

## Status

accepted

## Considered Options

- Bind every Research Topic to one or more environments declared in the Project-level Pixi manifest, with optional standalone topic isolation.
- Make every Topic Workspace a standalone Pixi workspace by default, so each topic has its own manifest, lockfile, and environment directory.
- Give every Agent Workspace its own Pixi environment by default.

## Decision

Adopt the second option. Topic Workspaces are Pixi workspaces by default. Agent Workspaces share the Topic Workspace Pixi environment unless an explicit Service Request creates a divergent environment.

## Consequences

- The default Python environment for agents is topic-scoped. Agents working on the same Research Topic share dependencies, while agents on different topics are isolated.
- Each Topic Workspace needs a Pixi manifest, typically `<topic-workspace>/pixi.toml` or `<topic-workspace>/pyproject.toml`, and a matching `<topic-workspace>/pixi.lock`.
- The Project Manifest may record an explicit Topic Workspace Pixi target through `[[topic_standalone_pixi_bindings]]`, using Project-root-relative `manifest_path_or_dir`. The target may be a Pixi manifest file or a directory that Pixi can resolve. When no explicit standalone binding exists, the effective target is the registered Topic Workspace directory, the Pixi environment is `default`, and the binding source is `implicit-default`.
- The Project-level Pixi environment, when present, runs Isomer platform tools such as `isomer-cli`. It is not the default execution environment for research agents.
- `isomer-cli doctor` uses `pixi info --json --manifest-path <target>` to resolve explicit file targets, explicit directory targets, or the implicit Topic Workspace directory default. It accepts the binding only when Pixi reports a manifest and environment prefix confined to the registered Topic Workspace. It does not install environments.
- `isomer-cli runtime prepare` checks and records Topic Environment Readiness for the Topic Workspace Pixi environment. It does not perform hidden repair.
- Pixi is required for Topic Workspace binding resolution. If `pixi` is missing or cannot produce usable JSON, diagnostics report a Pixi tooling failure with online install guidance and offline executable-provisioning guidance rather than treating the Research Topic as unbound.
- Environment repair, dependency installation, lockfile updates, or platform compatibility work are recorded as Service Requests.
- ADR 0020 is superseded by this decision. ADR 0025 and ADR 0026 remain in force with updated semantics: Project Manifest still owns bindings, and the standalone-style binding table is now the default.
