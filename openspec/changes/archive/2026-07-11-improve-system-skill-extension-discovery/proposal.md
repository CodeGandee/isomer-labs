## Why

Packaged skill extensions such as Kaoju can be selected when their ids are already known, but the CLI does not provide a focused way to discover an extension's purpose, entry skill, procedures, installation command, or status command. The neighboring `isomer-cli ext` runtime namespace makes this harder to understand because it contains a DeepSci compatibility surface but no Kaoju command group.

## What Changes

- Add focused extension listing and inspection commands under `isomer-cli system-skills extensions`.
- Add manifest-owned extension entry-skill and procedure metadata so discovery remains package-derived and works outside a source checkout.
- Show valid packaged extension ids in selector help and completion while preserving deterministic unknown-id errors.
- Clarify that `isomer-cli ext` contains runtime and compatibility command surfaces, while installable agent-skill extensions are discovered under `system-skills extensions`.
- Keep Kaoju agent-skill driven through `$isomer-kaoju-pipeline`; do not add an `isomer-cli ext kaoju` runtime command group.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `packaged-system-skills`: Add package-owned discovery metadata for each optional system-skill extension.
- `system-skill-installer-cli`: Add focused extension list/show commands, selector discoverability, and clear runtime-versus-skill-extension guidance.

## Impact

- Updates the packaged system-skill manifest and parser models.
- Updates the `system-skills` and `ext` Click help and JSON/human output contracts.
- Adds CLI, package-asset, and documentation coverage for DeepSci and Kaoju discovery.
- Does not change installed skill layouts, selection semantics, Project extension declarations, research records, or extension runtime behavior.
