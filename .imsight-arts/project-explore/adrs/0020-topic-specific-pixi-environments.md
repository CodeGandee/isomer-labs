# Topic-specific Pixi Environments

This superseded ADR previously made the Project-level Pixi manifest the default environment authority. ADR 0027 replaces that default with Topic Workspace Pixi workspaces: Project-root Pixi environment bindings remain explicit through `topic_pixi_environment_bindings`, explicit Topic Workspace Pixi targets use `topic_standalone_pixi_bindings.manifest_path_or_dir`, and absent explicit standalone bindings default to the registered Topic Workspace directory. Environment names can follow human conventions such as `<topic-slug>-<env-purpose>`, but Isomer must not infer topic binding from names.

## Status

superseded by ADR-0027

## Considered Options

- Use only one Project-level Pixi environment for all topics.
- Make every Topic Workspace a standalone Pixi workspace by default.
- Make every Agent Workspace own a separate Pixi environment by default.
- Use the Project-level Pixi manifest as the default authority for topic-specific Pixi environments, with optional standalone Topic Workspace isolation.

## Consequences

- `isomer-cli doctor` should check that Pixi is installed, that the Project exposes valid Pixi configuration, and that topic-specific environment declarations can be inspected or verified before Workspace Runtime or Agent Workspace preparation depends on them.
- The Project Manifest should record Research Topic to Project-root Pixi environment bindings and standalone Pixi manifest bindings explicitly; Workspace Runtime should record resolved environment use, readiness status, and provenance for each Topic Workspace and Agent Workspace preparation step.
- Topic Workspaces must not be called Pixi workspaces in Isomer schema or CLI labels unless they explicitly opt into standalone Pixi isolation.
- Agent Workspaces inherit the selected topic environment binding by default; per-agent environment divergence should be represented as an explicit readiness or Service Request decision rather than hidden adapter behavior.
