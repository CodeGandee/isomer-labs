## Why

`isomer-op-houmao-interop` is currently exposed as a user-facing operator skill, but its actual responsibility is bridging Isomer project concepts to Houmao adapter/runtime details. Moving it into the service namespace keeps `isomer-op-*` reserved for user-facing operator workflows and keeps Houmao interop as bounded operational support routed from those workflows.

## What Changes

- **BREAKING** Rename the active skill identity from `isomer-op-houmao-interop` to `isomer-srv-houmao-interop`.
- Move the packaged skill folder from `operator/isomer-op-houmao-interop` to `service/isomer-srv-houmao-interop`, with matching `SKILL.md` frontmatter, agent metadata, local references, scenarios, manifest entry, and authoring-view path.
- Remove Houmao interop from the direct operator owner-skill inventory and welcome/menu surfaces; user-facing operator skills route Houmao-specific support to the service skill only when needed.
- Update docs, validators, tests, active OpenSpec guidance, and generated/synced skill catalogs so no active guidance invokes the old operator skill name.
- Do not keep an active compatibility shim for `isomer-op-houmao-interop`; stale invocation should fail visibly rather than preserving the wrong responsibility boundary.

## Capabilities

### New Capabilities

- `isomer-houmao-interop-service-skill`: Defines the service skill contract for `isomer-srv-houmao-interop`, including its service namespace, bounded Houmao adapter-support responsibility, routing posture, and validation requirements.

### Modified Capabilities

- `operator-admin-skills`: Removes Houmao interop from the user-facing operator skill inventory and requires operator guidance to route Houmao adapter-support work to `isomer-srv-houmao-interop` rather than presenting it as a direct operator owner skill.

## Impact

- Affects packaged system skill assets under `src/isomer_labs/assets/system_skills/`, the repository-root `skillset/` authoring symlink view, and `src/isomer_labs/assets/system_skills/manifest.toml`.
- Affects operator welcome/help/routing pages, service README guidance, skill frontmatter, `agents/openai.yaml`, validator constants, validation fixtures, and unit tests that assert active skill inventories or direct invocation text.
- Affects generated or synchronized agent skill catalogs such as `.kimi-code/skills` when they mirror active packaged skills.
- Affects active OpenSpec guidance that currently classifies Houmao interop as an operator skill, especially the complete but unarchived namespace-rename change.
