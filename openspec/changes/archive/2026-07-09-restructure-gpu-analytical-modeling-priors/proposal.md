## Why

The GPU analytical modeling Toolbox injects priors at DeepSci callback stages, but its current directory and skill names are organized by broad knowledge area. That makes it hard for an operator or agent to see which prior takes effect at `scout`, `idea`, `experiment`, `write`, or `finalize` insertion points.

## What Changes

- Restructure the project-local Toolbox guidance into stage-prior skills named `gpu-analytic-{stage}-prior`.
- Replace broad `skill_dir` callback entries with short prompt-file callbacks that explicitly say which installed skill and subcommand to invoke for the insertion-point purpose.
- Preserve the existing `gpu-analytical-modeling` Toolbox identity, install scope, and generic GPU kernel analytical-modeling boundary.
- Update README guidance so the manifest reads as a stage-prior injection map.
- Remove the old broad domain-skill callback layout after the stage-prior layout covers the same guidance.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `gpu-analytical-modeling-toolbox`: Clarify that the Toolbox organizes installed callback behavior as stage-specific priors with prompt-file invocation of installed prior skills and subcommands.
- `gpu-analytical-modeling-skill-guidance`: Preserve existing GPU analytical-modeling guidance while reorganizing it into stage-prior skills and reusable subcommands.

## Impact

- Affected files are limited to `skillset/toolboxes/gpu-analytical-modeling/` and this change directory.
- Operators will see callback entries by target stage and purpose rather than by broad source domain.
- The callback resolver and Toolbox manifest schema do not change.
