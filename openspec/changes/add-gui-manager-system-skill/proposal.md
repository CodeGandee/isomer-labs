## Why

Isomer now has a Project Web GUI with lifecycle modes, topic-scoped read APIs, record views, and troubleshooting surfaces, but operators do not have a bundled skill that teaches when and how to run, inspect, refresh, and diagnose that GUI. A dedicated operator skill gives users one discoverable place for GUI lifecycle management and backend API reference without mixing GUI operations into Project or Topic Manager guidance.

## What Changes

- Add a bundled core operator system skill named `isomer-op-gui-mgr`.
- Define the skill as the user-facing owner for GUI Backend lifecycle guidance, GUI Renderer troubleshooting, cache-mode selection, API discovery, record-view refresh flows, and backend API reference lookup.
- Include the skill in the packaged system-skill manifest so core installation and package-resource discovery expose it.
- Add routing expectations so `isomer-op-entrypoint` can direct GUI operation requests to `isomer-op-gui-mgr`.
- Add welcome-menu discoverability so `isomer-op-welcome` lists GUI lifecycle and backend API reference work as a first-click owner route.
- Add validation and tests for skill structure, manifest inclusion, naming consistency, local references, and CLI-reference accuracy.

## Capabilities

### New Capabilities

- `isomer-op-gui-mgr-skill`: Defines the GUI manager operator skill, its command-style workflow, output contract, guardrails, and reference pages.

### Modified Capabilities

- `packaged-system-skills`: The core packaged system-skill group includes `operator/isomer-op-gui-mgr` and materializes it with the other core operator skills.

## Impact

- New packaged skill directory under `src/isomer_labs/assets/system_skills/operator/isomer-op-gui-mgr/`.
- Updates to `src/isomer_labs/assets/system_skills/manifest.toml`.
- Updates to `isomer-op-entrypoint` route references so GUI requests route to the new owner skill.
- Updates to `isomer-op-welcome` help, option, path-choice, and skill-map references so users can find GUI management from the welcome surface.
- Tests for packaged skill discovery/materialization and operator skill validation.
- Documentation or skill reference pages covering GUI Backend lifecycle commands, cache modes, health/status checks, API route families, and troubleshooting boundaries.
