# Topic-specific Pixi Environments

Isomer Labs will treat Pixi as a required Project dependency and will use the Project-level Pixi manifest as the default environment authority. Research Topics use Pixi environments through explicit Project Manifest bindings to one or more environments declared at the Project root; environment names can follow human conventions such as `<topic-slug>-<env-purpose>`, but Isomer must not infer topic binding from names. A Topic Workspace may optionally use standalone isolated Pixi setup when the Project explicitly records that stronger isolation through `topic_standalone_pixi_bindings`. This keeps environment policy visible at the Project level, avoids making every Topic Workspace a nested Pixi workspace by default, and preserves an isolation escape hatch for topics with incompatible dependency or platform needs.

## Status

accepted

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
