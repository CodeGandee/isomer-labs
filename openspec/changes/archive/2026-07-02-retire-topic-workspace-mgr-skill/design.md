## Context

`rename-topic-workspace-mgr-to-topic-mgr` introduced `isomer-admin-topic-mgr` as the canonical initialized-topic manager and kept `isomer-admin-topic-workspace-mgr` only as a temporary compatibility wrapper. A follow-up stale-reference sweep showed that active skill routing no longer needs the wrapper; the remaining references are the wrapper folder itself, manifest exposure, README compatibility text, validator wrapper checks, validator fixtures, and OpenSpec change/spec text that intentionally allowed the wrapper.

This change should be implemented after, or folded into, the completed rename change. Its purpose is not to redefine topic management; it only removes the old skill name as an invokable surface.

## Goals / Non-Goals

**Goals:**

- Delete `skillset/operator/isomer-admin-topic-workspace-mgr/` entirely.
- Remove the old skill from active skillset manifest entries and operator documentation.
- Ensure users and skills no longer route to `$isomer-admin-topic-workspace-mgr`.
- Change operator validation from wrapper acceptance to retirement enforcement.
- Keep `isomer-admin-topic-mgr` as the only initialized-topic manager and preserve its scoped subcommands.
- Sweep active specs, skill docs, tests, scripts, and context for stale old-skill routing.

**Non-Goals:**

- Do not rename or redesign `isomer-admin-topic-mgr`.
- Do not reintroduce old command aliases on the new topic manager.
- Do not edit historical archived OpenSpec material except where a current validation rule treats it as active.
- Do not remove old words that appear only as historical rationale inside this new change or already archived records.

## Decisions

### Remove the Wrapper Instead of Keeping a Tombstone Skill

Delete the entire old skill folder rather than leaving a tombstone `SKILL.md`. A tombstone still appears as an invokable skill to skill discovery and keeps the old name alive. The cleaner behavior is that `$isomer-admin-topic-workspace-mgr` is no longer a valid skill route.

Alternative considered: keep a minimal wrapper that only says “use `isomer-admin-topic-mgr`.” That is safer for users with stale prompts, but it contradicts the requirement that users should no longer invoke the old skill.

### Make Validation Reject Revival

Move `isomer-admin-topic-workspace-mgr` into the removed-operator-skill validation path instead of checking wrapper content. The validator should fail if the old folder returns, if the manifest lists it, or if active non-historical docs route users to it.

Alternative considered: remove all validator knowledge of the old skill. That would make deletion quieter, but a later accidental re-addition could pass as an ordinary operator skill.

### Treat Historical References Differently From Active Routes

Active skill docs, README material, manifest entries, tests, scripts, and main specs should not present the old skill as callable. Archived OpenSpec material and old change rationale can keep historical references unless current validators intentionally scan them as active material.

Alternative considered: rewrite all archive history. That would make text search cleaner but would damage the record of why the rename happened.

### Sequence After Rename

This change assumes the topic manager created by `rename-topic-workspace-mgr-to-topic-mgr` exists and active routing already points to it. If implementation happens before that change is archived, the implementation should still preserve the current uncommitted `isomer-admin-topic-mgr` files and only remove the old wrapper surface.

## Risks / Trade-offs

- [Risk] Stale user prompts invoking `$isomer-admin-topic-workspace-mgr` will stop resolving. → Mitigation: operator README, active specs, and skill guidance must name `isomer-admin-topic-mgr` directly, and validators must catch active stale routing before merge.
- [Risk] Main OpenSpec specs may still contain old workspace-manager requirements until the rename change is archived. → Mitigation: run strict validation on both the rename change and this retirement change, and archive/sync in an order that leaves main specs with the new topic-manager requirements and old-wrapper removal.
- [Risk] Removing wrapper tests may reduce coverage for old-to-new command mapping. → Mitigation: replace them with retirement tests and rely on topic-manager command tests for canonical behavior.
- [Risk] A broad `rg` sweep can flag historical archive text. → Mitigation: define active search roots for enforcement and report archived references separately as historical.

## Migration Plan

1. Delete `skillset/operator/isomer-admin-topic-workspace-mgr/`.
2. Remove `"operator/isomer-admin-topic-workspace-mgr"` from `skillset/manifest.toml`.
3. Remove the compatibility-wrapper note from `skillset/operator/README.md` and keep only `isomer-admin-topic-mgr` as the initialized-topic manager.
4. Replace wrapper validation constants, wrapper validation function, and wrapper unit fixtures with removed-skill enforcement for `isomer-admin-topic-workspace-mgr`.
5. Sweep active routes for `$isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-workspace-mgr`, and retired old subcommands used as skill commands; update them to `isomer-admin-topic-mgr` scoped commands or mark them as historical.
6. Run `openspec validate retire-topic-workspace-mgr-skill --strict`, `pixi run validate-operator-skills`, `pixi run lint`, and `pixi run test`.
