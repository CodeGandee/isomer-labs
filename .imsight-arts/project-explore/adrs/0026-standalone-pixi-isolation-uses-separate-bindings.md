# Standalone Pixi Isolation Uses Separate Manifest Bindings

Isomer Labs will represent Topic Workspace Pixi workspace bindings with a separate Project Manifest table, `[[topic_standalone_pixi_bindings]]`, instead of mixing standalone manifest refs into Project-root Pixi environment bindings. Each explicit binding identifies `research_topic_id`, Project-root-relative `manifest_path_or_dir`, optional `pixi_environment`, optional `purpose`, and optional `status`. After ADR 0027, the table remains the explicit override surface, while the registered Topic Workspace directory is the implicit default target when no explicit entry exists.

## Status

accepted, with updated default semantics after ADR-0027

## Considered Options

- Use one union table for both Project-root Pixi environments and standalone Pixi manifests.
- Use a separate `topic_standalone_pixi_bindings` table.
- Defer standalone Pixi isolation out of the first `doctor` design.

## Consequences

- `topic_pixi_environment_bindings` remains limited to environments declared in the Project-level Pixi manifest.
- `topic_standalone_pixi_bindings` records explicit Topic Workspace Pixi file or directory targets; absent explicit bindings use the registered Topic Workspace directory default instead of a filesystem crawl.
- `doctor` can ask Pixi to resolve explicit or implicit targets and validate Project and Topic Workspace containment without installing environments.
- Runtime preparation can later record resolved standalone environment readiness and provenance in Workspace Runtime.
- After ADR 0027, `topic_standalone_pixi_bindings` is the explicit override representation for Topic Workspace Pixi workspaces, not only an opt-in isolation escape hatch. Missing explicit entries fall back to the registered Topic Workspace directory with binding source `implicit-default`.
