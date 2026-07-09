## Context

The pending `create-toolbox-creator-system-skill` implementation created a packaged operator skill named `isomer-op-toolbox-creator`. Its actual scope already includes Toolbox authoring, conversion, callback insertion, Runtime Param definition, validation, install, inspection, enablement, disablement, source update, uninstall, and effective-state explanation.

The name `creator` is too narrow for that surface. The feature requirement also left the name open and explicitly mentioned `isomer-op-toolbox-mgr` as a candidate. This change resolves that open question before the skill becomes a stable packaged operator interface.

## Goals / Non-Goals

**Goals:**
- Rename the active packaged operator skill to `isomer-op-toolbox-mgr`.
- Keep the current command pages and behavior intact.
- Update package manifest, UI metadata, tests, and active docs so all active references use the manager name.
- Update or supersede pending OpenSpec artifacts from `create-toolbox-creator-system-skill` so the active contract does not preserve the old name.
- Avoid duplicate active names.

**Non-Goals:**
- No command-surface redesign.
- No CLI, schema, callback, Runtime Param, or Toolbox behavior changes.
- No compatibility shim or alias folder for `isomer-op-toolbox-creator`.
- No rename of historical archive material unless it is active implementation guidance for the pending skill.

## Decisions

### Decision: Use `isomer-op-toolbox-mgr` as the only active skill name

The skill handles the full lifecycle of project-local Toolboxes, so `mgr` better matches the responsibility boundary than `creator`. This also aligns with existing operator names such as `isomer-op-project-mgr` and `isomer-op-topic-mgr`.

Alternative considered: keep `isomer-op-toolbox-creator` and rely on subcommands to reveal the broader scope. That would leave the public invocation misleading and would make install/discovery output look creation-only.

### Decision: Rename rather than alias

Move the folder from `operator/isomer-op-toolbox-creator` to `operator/isomer-op-toolbox-mgr`, update frontmatter and UI metadata, and replace the manifest entry. Do not keep a creator alias because active packaged system-skill inventory should not expose duplicate names for one owner.

Alternative considered: keep an alias wrapper for compatibility. The skill is not yet archived or released as a stable package surface, so a shim would add needless long-term inventory noise.

### Decision: Preserve command names

Keep `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, `identify-insertion-points`, and helper command names. They are action-specific and remain accurate under the manager skill.

Alternative considered: rename `author-toolbox` to `create-toolbox`. That would blur authoring source with installing or registering the Toolbox and is not necessary for the top-level skill rename.

## Risks / Trade-offs

- Stale references remain in active docs or tests -> Mitigate with `rg` for `isomer-op-toolbox-creator`, `Toolbox Creator`, and `toolbox-creator` across active assets, tests, and pending OpenSpec artifacts.
- OpenSpec capability names diverge between pending changes -> Mitigate by updating the pending creation change artifacts or clearly superseding them so archive output uses `isomer-op-toolbox-mgr-skill`.
- Users may remember the short-lived creator name -> Mitigate by making the manager name appear in operator README, manifest, UI metadata, and help output; do not add a code shim unless a later release requires compatibility.
- Broad text replacement may touch historical context that should stay immutable -> Mitigate by limiting edits to active implementation assets, active tests, and pending design artifacts.

## Migration Plan

1. Rename the packaged skill directory to `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/`.
2. Replace skill identity strings in `SKILL.md`, `agents/openai.yaml`, command help output, package manifest, operator README, and package asset tests.
3. Update pending `create-toolbox-creator-system-skill` artifacts and feature design overview where they describe the active skill to avoid reintroducing the old name.
4. Run focused package asset tests, skill validation, OpenSpec validation, and the standard repo checks.

Rollback is asset-only: rename the folder and manifest entry back, restore tests and docs, and rerun the same validations.

## Open Questions

- Should the feature directory name `2026-07-08-toolbox-creator-skill` remain as historical planning context, or should a later cleanup rename it after this change is applied?
