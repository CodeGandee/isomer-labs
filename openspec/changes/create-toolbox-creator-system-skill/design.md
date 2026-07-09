## Context

Isomer already specifies Toolbox callback manifests, runtime-param configuration, callback insertion-point catalogs, workspace path rules, and packaged system-skill distribution. The missing piece is an operator-facing system skill that uses those existing surfaces to help users author and manage project-local Toolboxes without learning every low-level command first.

The source design is `context/features/2026-07-08-toolbox-creator-skill/design/isomer-op-toolbox-mgr/design-overview.md`. It defines `isomer-op-toolbox-mgr` as a packaged operator skill that writes Toolbox source under `skillset/toolboxes/<toolbox-id>/`, calls `isomer-cli` for installation and validation, and reports scope, ids, files, diagnostics, and rollback hints.

## Goals / Non-Goals

**Goals:**
- Package `operator/isomer-op-toolbox-mgr` as a core system skill.
- Keep the skill concise while preserving the design overview's six procedural subcommands and four grouped helper subcommands.
- Use canonical Toolbox terms: Toolbox, Toolbox ID, Callback Insertion Point, Toolbox-Local Key, Runtime Param, and Toolbox Scope.
- Make all mutation paths rely on project-local file edits and existing `isomer-cli project toolboxes`, `project skill-callbacks`, and `project toolbox-params` commands.
- Follow shared Essential Output and Complete Output reporting.

**Non-Goals:**
- No new Toolbox manifest schema, callback registry schema, runtime-param schema, or CLI command behavior.
- No marketplace, registry, downloader, dependency resolver, or arbitrary external code execution.
- No direct mutation of packaged system skills, installed callback registries, or Project/Topic manifests except through existing CLI-backed operations.
- No legacy extension naming or broad project-global defaults for topic-scoped asks.

## Decisions

### Decision: Package as Core Operator Skill

Place the skill at `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/` and list it in `groups.core.skills` in `src/isomer_labs/assets/system_skills/manifest.toml`. This matches the `isomer-op-*` namespace rule for user-facing Project Operator Session skills and keeps Toolbox authoring available without optional extension activation.

Alternative considered: place the skill under `skillset/toolboxes/` as a Toolbox example. That would make it a sample asset, not an always-available operator workflow.

### Decision: Keep Procedural Subcommands User-Facing and Helpers Grouped

Keep the procedural subcommands from the design overview: `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`. Keep helper guidance grouped as `author-toolbox-source`, `edit-callback-declarations`, `edit-runtime-params`, and `inspect-effective-state` so CRUD operations that target the same material do not explode into separate create, update, remove, and list pages.

Alternative considered: create a page for every low-level CRUD action. That would make discovery noisy and conflict with the recent design direction to combine CRUD operations around the same resource.

### Decision: Reuse CLI and Existing Specs as the Authority

The skill should author local Toolbox files itself, but should use existing `isomer-cli` commands for validation, install, registration, runtime-param mutation, callback installation, and state inspection. This keeps the skill from becoming a second implementation of Toolbox semantics.

Alternative considered: have the skill directly edit callback registries and manifests for all operations. That would duplicate validation logic and weaken the existing callback and runtime-param contracts.

### Decision: Use Reference Pages for Bounded Subcommand Logic

Follow the existing packaged operator skill pattern: a compact `SKILL.md` selects a subcommand, loads only the selected reference page, and reports through the output contract. This keeps the main skill readable while preserving enough detail for safe operator workflows.

Alternative considered: keep all workflow instructions in one `SKILL.md`. That would make the system skill harder to maintain and would increase context load for simple operations.

## Risks / Trade-offs

- Skill guidance drifts from CLI behavior -> Mitigate by requiring the skill to cite existing CLI command families as authority and by adding tests or validation that check packaged skill assets and named command surfaces.
- Too many subcommands make the skill hard to use -> Mitigate by keeping six procedural subcommands and grouping helper CRUD operations by target resource.
- A Toolbox install can affect project-wide behavior -> Mitigate by requiring explicit scope reporting, warnings for project scope, and validation before install or update.
- Runtime params can accidentally capture secrets -> Mitigate by requiring secret hygiene language and by routing mutation through existing validation.
- The skill can create incomplete Toolbox source -> Mitigate by requiring validation guidance, diagnostics, rollback hints, and blocked status when required ids, target skills, insertion points, or source paths are missing.

## Migration Plan

1. Add the packaged skill directory, `SKILL.md`, and concise reference pages.
2. Add `operator/isomer-op-toolbox-mgr` to the core packaged system-skill manifest.
3. Add or update package asset tests that assert manifest resolution, `SKILL.md` presence, and namespace consistency.
4. Run packaged skill validation plus relevant lint and test commands.

Rollback is asset-only: remove the manifest entry and skill directory, then rerun package asset tests.

## Open Questions

- Should `isomer-op-entrypoint` mention Toolbox creation directly, or is manifest discovery enough for the first version?
- Should `manage-toolbox` require an extra confirmation phrase for uninstall and source replacement, beyond the existing CLI confirmation flags?
- Which package asset test currently gives the narrowest coverage for adding a core operator skill?
