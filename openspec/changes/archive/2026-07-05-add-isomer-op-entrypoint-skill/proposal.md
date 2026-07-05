## Why

Project Operator Sessions need a compact entrypoint for users who already know Isomer but need help selecting the right system skill or CLI surface for a task. The current welcome skill is intentionally read-only and menu-shaped, so it does not cover "route this prompt/file/task and proceed" behavior or the full system-skill catalog, including DeepSci extension skills.

## What Changes

- Add `isomer-op-entrypoint` as a packaged operator skill that classifies a user task, selects the correct Isomer system skill or CLI family, and proceeds with the selected route by default.
- Include operator, service, misc, and extension skill families in the entrypoint index, with DeepSci routes treated as first-class extension-skill routes.
- Keep `isomer-op-welcome` as the broad read-only welcome/menu surface and make `isomer-op-entrypoint` the informed-user routing surface.
- Add concise reference pages for routing rules, system-skill indexes, CLI indexes, input-surface handling, and extension-skill routing.
- Register the skill in the packaged core system-skill manifest and operator documentation.
- Add validation coverage so the entrypoint keeps owner-skill boundaries, does not promote service skills as normal first-click routes, rejects retired operator routes, and preserves "route then proceed" behavior.

## Capabilities

### New Capabilities
- `isomer-op-entrypoint-skill`: Defines the informed-user operator entrypoint that routes prompts, files, topic/actor/agent context, CLI needs, and extension-skill work to the correct Isomer system surface and proceeds.

### Modified Capabilities
- `operator-admin-skills`: Add `isomer-op-entrypoint` to the active operator inventory, documentation, validation, and boundary rules.
- `packaged-system-skills`: Require the packaged core skill group to include `operator/isomer-op-entrypoint` and materialize it with the rest of the core system skills.

## Impact

- Affected assets: `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/`, `src/isomer_labs/assets/system_skills/manifest.toml`, and operator README material.
- Affected validation: operator skill validation and packaged system-skill asset tests.
- No breaking CLI changes are expected; the new skill references existing `isomer-cli` project, extension, record, artifact-format, path, runtime, handoff, and self-query command families.
