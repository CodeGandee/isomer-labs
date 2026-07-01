## Context

The research-paradigm skillset has moved from the first v2 core-method pass to a broader v2 bundle. The tree now contains v1 preserved skills, v2 core skills, migrated v2 paper-writing and review skills, Nature-facing companion skills, local migration notes, source-analysis material, source-copy trees under `org/`, and runtime support files under `references/`, `assets/`, and `scripts/`.

The current specification and tests partly assume the first-pass v2 boundary. The validator also applies many strict runtime checks across every Markdown and YAML file, which makes traceability material such as `migrate/`, `org/analysis/`, `org/src/`, and top-level source-analysis notes fail rules that were meant for active skill guidance.

## Goals / Non-Goals

**Goals:**

- Align the `research-paradigm-skills` spec with the current v1 and v2 skill inventory.
- Define a validation scope model that separates active skill material from provenance, migration, analysis, source-copy, license, and template material.
- Update validator tests so future skillset changes break in small, explainable ways instead of producing broad false-positive floods.
- Preserve strict checks for active `SKILL.md`, manifests, active local references, runtime scripts, and active assets.

**Non-Goals:**

- Do not bind v2 semantic placeholders to storage or add new runtime APIs.
- Do not rewrite the migrated skill content beyond what validation requires.
- Do not remove provenance or source-copy material that exists to make migration reviewable.
- Do not change operator/admin skill boundaries.

## Decisions

1. Treat validation scope as file-role classification before rule execution.

Active runtime files include each skill's `SKILL.md`, `agents/openai.yaml`, directly linked active references, active scripts, active assets, and suite documentation that describes current use. Non-active or constrained files include `migrate/**`, `org/analysis/**`, `org/src/**`, top-level source-analysis folders, provenance files, license notices, deferred-resource notes, and configured template/source-copy paths. This keeps the existing whole-subtree scan while preventing active-guidance rules from firing on archival context.

Alternative considered: shrink the scan to only `SKILL.md` files. That would reduce noise, but it would miss stale terminology and broken references in active local references and support files.

2. Keep the expected skill inventory explicit and tested.

The expanded v2 inventory is part of the skillset contract, so the validator and tests may keep an explicit expected list if that list matches the spec. A future implementation may move the list into `validation.toml`, but the test contract still needs to assert v1 and v2 inventory separately.

Alternative considered: derive expected skills from the filesystem. That would make the validator less brittle, but it would also stop catching accidentally deleted or renamed skills.

3. Make reference checks pattern-aware.

The validator should continue to report broken concrete links from `SKILL.md`, but placeholder-like reference patterns such as `references/packages/<package_id>.md` are documentation patterns, not literal paths. Tests should cover both broken concrete references and accepted pattern references.

Alternative considered: allow all missing paths in code spans. That would hide real broken local references and reduce the value of the self-containment check.

4. Preserve v2 storage-binding deferral.

The migrated v2 skills can use semantic placeholders and local migration placeholder notes, but active v2 guidance must not require Artifact storage binding, concrete Isomer runtime APIs, or host-specific storage paths until a later accepted contract introduces them.

Alternative considered: relax storage-binding checks for all migrated paper skills. That would make the current migration pass easier, but it would weaken the v2 contract exactly where generic portability matters most.

## Risks / Trade-offs

- False negatives from broad allow zones -> Keep allow zones path-specific and rule-specific, and add tests that the same stale term still fails in active guidance.
- Validator config drift -> Test the expected inventory and file-role classification so changes to `validation.toml` or constants have visible effects.
- Source-copy trees may contain many stale terms -> Treat them as non-active traceability material, but keep provenance/license checks and lint exclusions explicit.
- Pattern-aware references could mask mistakes -> Accept only clearly marked placeholder segments such as `<package_id>` while continuing to fail ordinary missing `references/`, `assets/`, and `scripts/` links.

## Migration Plan

1. Update the delta spec and main spec expectations for the expanded v2 inventory.
2. Update the validator's file-role classification, allow zones, pattern-reference handling, and expected inventory checks.
3. Extend unit tests with fixture coverage for migrated v2 companion skills, non-active migration/source-copy zones, pattern references, and active-guidance rejections.
4. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, `pixi run validate-research-skills`, and `openspec validate update-skillset-validation-specs --strict`.

Rollback is limited to reverting this OpenSpec change and the validator/test edits; no data migration is involved.

## Open Questions

- Should expected skill inventories stay in Python constants for now, or move to `skillset/research-paradigm/validation.toml` during implementation?
- Should migrated paper-skill local placeholder registries remain skill-local permanently, or should a later change normalize them into the shared v2 semantic placeholder registry?
