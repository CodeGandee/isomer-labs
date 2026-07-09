## Why

The `imsight-project-design` skill currently auto-routes any feature that looks like an agent skill from `design-interface` into a skill-design branch that writes `design-overview.md`. This causes two problems: (1) `design-interface` unexpectedly changes its output shape and location when the feature happens to mention skills or include example-prompt use cases, and (2) the skill-design branch re-resolves the feature directory and can drop the design into `.imsight-arts/feature-design/` instead of the existing feature directory the user pointed to.

## What Changes

- Add `design-skill` as a first-level subcommand in `imsight-project-design`.
- Move the skill-design workflow out of `design-interface` and into `commands/design-skill.md`.
- Remove the auto-detection and skill-routing logic from `design-interface`; `design-interface` will write only non-skill interface and contract artifacts (`design/public-interfaces.md` and related module files).
- Update `SKILL.md` to list `design-skill` in the subcommands table and describe when to use it.
- Update `commands/help.md` to mention the new subcommand.
- Require `design-skill` to reuse the feature directory already resolved by the entry workflow instead of re-resolving it.

## Capabilities

### New Capabilities

- `imsight-project-design-skill`: Teach the `imsight-project-design` skill to expose `design-skill` as a dedicated subcommand and keep `design-interface` focused on non-skill interfaces.

### Modified Capabilities

- None.

## Impact

- Affects `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-design/SKILL.md`, `commands/help.md`, `commands/design-interface.md`, and a new `commands/design-skill.md` file.
- Features that are agent skills will now need an explicit `design-skill` invocation instead of relying on `design-interface` auto-detection.
- Non-skill features that mention skills in their requirements will no longer be mis-routed.
