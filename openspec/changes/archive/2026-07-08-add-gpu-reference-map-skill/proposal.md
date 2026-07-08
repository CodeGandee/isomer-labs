## Why

GPU analytical-modeling source guidance is currently mixed into operational modeling and evidence skills. A dedicated reference-map skill will make source lookup rules easier to update while keeping operational skills focused on model shape, evidence gates, and reporting discipline.

## What Changes

- Add a project-local `gpu-reference-map` callback skill under `skillset/user-plugins/gpu-analytical-modeling/` that answers where to look for different classes of GPU analytical-modeling information.
- Move durable source-priority guidance out of operational flow as much as practical by making `gpu-modeling-method` consult the new reference-map skill instead of owning detailed source taxonomy.
- Add command pages for local topic sources, kernel implementation sources, hardware documentation, profiler/counter sources, simulator architecture sources, measurement sources, and literature sources.
- Register the new skill in the user-plugin manifest at source-discovery, framing, baseline, analysis, and experiment stages where agents need source lookup guidance.
- Keep the guidance generic to GPU kernel analytical modeling while allowing Isomer Labs system context, such as Pixi-managed NCU usage, where the source class is specifically profiler/counter evidence.
- Keep the change project-local under `skillset/user-plugins/gpu-analytical-modeling/`; do not modify packaged system skills, callback registry behavior, CLI/runtime behavior, or distribution assets.

## Capabilities

### New Capabilities

- `gpu-reference-map-skill`: Project-local user-plugin skill that centralizes GPU analytical-modeling source taxonomy, source priority, source limitations, and source-to-claim mapping.

### Modified Capabilities

- None.

## Impact

- Affected files are expected to stay under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory.
- No Python APIs, CLI commands, packaged system skills, distribution manifests, or callback registry behavior should change.
- Validation should use skill-file inspection, local metadata checks, and the available skill validator for the new and touched skill directories.
