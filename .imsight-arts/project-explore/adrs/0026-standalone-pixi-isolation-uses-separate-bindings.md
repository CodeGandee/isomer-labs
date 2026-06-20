# Standalone Pixi Isolation Uses Separate Manifest Bindings

Isomer Labs will represent optional standalone topic Pixi isolation with a separate Project Manifest table, `[[topic_standalone_pixi_bindings]]`, instead of mixing standalone manifest refs into Project-root Pixi environment bindings. Each binding identifies `research_topic_id`, Project-root-relative `manifest_path`, optional `pixi_environment`, optional `purpose`, and optional `status`, making the stronger isolation opt-in visible and keeping Project-root environment validation simple.

## Status

accepted

## Considered Options

- Use one union table for both Project-root Pixi environments and standalone Pixi manifests.
- Use a separate `topic_standalone_pixi_bindings` table.
- Defer standalone Pixi isolation out of the first `doctor` design.

## Consequences

- `topic_pixi_environment_bindings` remains limited to environments declared in the Project-level Pixi manifest.
- `topic_standalone_pixi_bindings` records explicit standalone manifest refs and must not be discovered by crawling Topic Workspaces.
- `doctor` can validate standalone manifest presence and Project containment without installing environments.
- Runtime preparation can later record resolved standalone environment readiness and provenance in Workspace Runtime.
