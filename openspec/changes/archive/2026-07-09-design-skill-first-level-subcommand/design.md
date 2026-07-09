## Context

The `imsight-project-design` skill currently treats skill-design as a side branch of `design-interface`. When `design-interface` detects an agent-skill feature, it loads `references/skill-design.md`, which generates `design-overview.md` and can re-resolve the feature directory. This conflates two different design tasks:

1. Designing public interfaces and contracts for a feature (the normal `design-interface` job).
2. Designing a proposed agent skill before it is implemented (the skill-design job).

Users who point `design-interface` at an existing feature directory expect normal interface artifacts in that directory. The current auto-routing surprises them by changing both the artifact shape and the output location.

## Goals / Non-Goals

**Goals:**

- Make skill design a first-class, explicit subcommand: `design-skill`.
- Keep `design-interface` focused on non-skill interface and contract design.
- Ensure both subcommands reuse the feature directory already resolved by the entry workflow.
- Keep the skill self-contained by copying the needed skill-design guidance into the new `design-skill.md` command file.

**Non-Goals:**

- Changing the content or validation rules inside the skill-design workflow itself.
- Changing how the feature directory is resolved by the entry workflow.
- Modifying any other Imsight skills.

## Decisions

1. **Split into two subcommands instead of a flag.** A dedicated `design-skill` subcommand makes intent explicit and avoids surprising users who want normal interface design for a feature that happens to mention skills.
2. **Remove auto-detection from `design-interface`.** The only reliable signal that the user wants skill design is an explicit request. `feature-requirement.md` wording and example-prompt sections are too broad and cause false positives.
3. **Move `references/skill-design.md` content into `commands/design-skill.md`.** This keeps the skill self-contained and lets `design-skill` own its workflow without requiring agents to follow an indirection.
4. **Preserve the existing output location contract.** `design-skill` writes `<feature-dir>/design/<slug>/design-overview.md` using the same feature directory that the entry workflow already resolved.
5. **Update `SKILL.md` and `commands/help.md`.** Both must list `design-skill` and describe its purpose so agents discover it.

## Risks / Trade-offs

- **Risk**: Users who previously relied on `design-interface` auto-routing will now need to invoke `design-skill` explicitly.  
  **Mitigation**: The auto-routing was already surprising and poorly bounded; explicit invocation is clearer. Document the new subcommand in `help.md`.
- **Risk**: Copying `references/skill-design.md` into `commands/design-skill.md` creates a single larger command file.  
  **Mitigation**: The original reference was already skill-local; collapsing it removes one level of indirection without changing behavior.
- **Risk**: Existing in-flight feature designs that expected `design-interface` to produce `design-overview.md` will need to be re-run with `design-skill`.  
  **Mitigation**: This change is being tracked in a fresh OpenSpec change; no active incomplete changes depend on the old behavior.

## Migration Plan

1. Create `commands/design-skill.md` with the full skill-design workflow.
2. Edit `commands/design-interface.md` to remove the `## Skill Target Routing` section.
3. Edit `SKILL.md` to add `design-skill` to the subcommands table and update the artifact contracts list.
4. Edit `commands/help.md` to mention `design-skill`.
5. Optionally delete `references/skill-design.md` after confirming `commands/design-skill.md` is complete.

## Open Questions

- Should `references/skill-design.md` be deleted outright, or kept as a thin redirect to `commands/design-skill.md`? The proposal recommends deleting it to avoid maintaining two copies.
