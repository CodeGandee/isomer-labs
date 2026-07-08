## Why

GPU kernel analytical modeling needs stronger domain-specific callback guidance than generic DeepSci stages can provide. The Flash Attention 4 modeling topic showed recurring risks: agents overclaimed emulator evidence, accepted coarse compute/memory bottleneck labels, drifted from real NCU validation, and needed repeated user correction before producing component-level saturation evidence.

## What Changes

- Add a project-local user-plugin named `gpu-analytical-modeling` under `skillset/user-plugins/gpu-analytical-modeling/`.
- Add a required project-local `manifest.toml` that describes the callback bundle and the desired callback registrations for future installer support.
- Make the manifest compatible with all existing User Skill Callback source types: callback skill directories, prompt files, and inline prompts.
- Structure the plugin as a small set of callback skill entrypoints with command-style reference pages, matching the Isomer system skill pattern of one entrance skill grouping related subcommands.
- Author the callback skills using the `$imsight-agent-skill-handling create` style guidance for skill layout, frontmatter, workflow structure, command pages, and validation.
- Provide three user-plugin callback skills:
  - `gpu-modeling-method` for source priority, analytical model shape, and baseline/evidence class discipline.
  - `gpu-evidence-and-experiment` for evaluation contracts, NCU evidence protocol, component bottleneck proof, and model-failure refinement.
  - `gpu-reporting-and-closure` for claim gating, math-writing discipline, and closure limitations.
- Add operator-facing README guidance that maps each callback skill to recommended DeepSci target skills and `begin` or `end` callback stages.
- Keep manual `isomer-cli project skill-callbacks register ...` commands as the current activation path, with the manifest serving as the declarative recipe for equivalent `--skill-dir`, `--prompt-file`, or `--prompt` registrations.
- Keep the plugin generic to GPU kernel analytical modeling rather than binding it to Flash Attention 4, B200, or one Topic Workspace.
- Keep these skills only in their project-local user-plugin directory; they are not part of the packaged Isomer distribution.
- Do not change callback registry semantics, callback stages, packaged system skill authority, DeepSci workflow behavior, distribution packaging, or add installer command behavior.

## Capabilities

### New Capabilities

- `gpu-analytical-modeling-user-plugin`: Defines the project-local GPU analytical modeling user-plugin layout, callback skill entrypoints, internal command pages, registration guidance, and domain quality gates for hardware-grounded GPU kernel models.

### Modified Capabilities

None.

## Impact

- New documentation, manifest, prompt material, and callback skill material under `skillset/user-plugins/gpu-analytical-modeling/`.
- Skill authoring follows the Imsight agent skill creation style rather than ad hoc Markdown prompts.
- New OpenSpec delta spec for the user-plugin contract only.
- No changes to `isomer-cli project skill-callbacks` command behavior are required for the first implementation.
- No automatic manifest installer is added in this change.
- No changes to packaged `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/isomer-deepsci-*` workflows are required.
- No packaged distribution, install manifest, or system skill inventory is affected.
- Validation should use filesystem checks and existing Markdown/skill conventions rather than introducing new runtime dependencies.
