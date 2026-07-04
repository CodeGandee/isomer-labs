## Why

New Isomer users need a concise way to see what the system can do and choose the right operator path without reading the system model first. The current operator skills are well-scoped, but there is no user-facing capability menu that says which skill to invoke for each supported workflow.

## What Changes

- Add a new command-style operator skill, `isomer-admin-welcome`, as the action-oriented entrypoint for users who ask what Isomer Labs can do or which path they should choose.
- Make the welcome skill present supported operator workflows as options, name the owner skill for each option, and invite the user to choose a path or invoke an owner skill directly.
- Publish typical usage paths directly in `SKILL.md`, including paths such as `start-research-manually` and `start-research-by-agent-team`, so common workflows are visible before any goal interpretation by `choose-path`.
- Keep the welcome skill read-only by default: it may inspect current Project context for recommendations, but it must not initialize projects, create topics, mutate topic environments, install packages, specialize teams, launch agents, or perform v2 research bootstrap.
- Update operator skill inventory and validation so `isomer-admin-welcome` is listed, validated, and installed with the core operator skillset.
- Preserve retired-skill boundaries: the welcome skill must not route users to `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, or `isomer-admin-manual-research-session`.

## Capabilities

### New Capabilities

- `isomer-admin-welcome-skill`: Defines the user-facing welcome skill as a capability menu, path chooser, direct skill invocation map, and optional read-only context-aware recommender.

### Modified Capabilities

- `operator-admin-skills`: Adds `isomer-admin-welcome` to the active operator inventory and validation expectations.

## Impact

- Adds `skillset/operator/isomer-admin-welcome/` with `SKILL.md`, `agents/openai.yaml`, and focused reference pages.
- Updates `skillset/operator/README.md` and `skillset/manifest.toml`.
- Updates `openspec/specs/operator-admin-skills/spec.md` through the change delta and adds a new welcome-skill spec.
- Extends skillset validation and unit tests for naming, metadata, local references, action-oriented menu behavior, read-only default posture, direct owner-skill routing, and retired-skill exclusions.
