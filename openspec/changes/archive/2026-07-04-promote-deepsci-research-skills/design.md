## Context

The active research-paradigm skillset currently lives under `skillset/research-paradigm/v2/` with `isomer-rsch-*-v2` skill names. The same subtree also keeps retired `v1` skills for compatibility, and several validators, docs, specs, manifests, placeholder binding pages, and operator boundary notes still model the skillset as generationed.

The user direction is to delete `v1` skills because no one should be using them, then promote `v2` into the production-ready DeepSci skillset at `skillset/research-paradigm/deepsci/` with suffixless names.

## Goals / Non-Goals

**Goals:**

- Provide one production research-paradigm skill root: `skillset/research-paradigm/deepsci/`.
- Remove `skillset/research-paradigm/v1/*` from the working tree.
- Rename every active `isomer-rsch-*-v2` skill identity to the matching suffixless `isomer-rsch-*` identity.
- Update active docs, validators, manifest groups, placeholder binding metadata, and operator routing references to the production names.
- Preserve active DeepSci methodology, placeholder, structured-output, output-policy, and commit-preference behavior from the current `v2` skillset.

**Non-Goals:**

- Do not provide compatibility skill folders, symlinks, or aliases for `v1`, `v2`, or `-v2` names.
- Do not redesign research record schemas, artifact format profiles, placeholder meanings, or Isomer CLI command semantics.
- Do not reintroduce the richer `v1` runtime and storage vocabulary into active production guidance.
- Do not move operator admin or service skills into the research-paradigm skillset.

## Decisions

1. **Use `deepsci` as the production root and manifest group.** The active group becomes `[groups.deepsci]`, with skill paths such as `research-paradigm/deepsci/isomer-rsch-scout`. Alternative considered: keep `[groups.deepsci-v2]` as an alias during transition. That would preserve old entrypoints but keep the temporary generation vocabulary alive.

2. **Delete retired v1 folders instead of archiving them in-tree.** Git history is the source of truth for retired v1 material. Alternative considered: move v1 under `archive/` or `retired/`. That would keep readable provenance but would also require validators and installers to distinguish active and inactive research skill roots forever.

3. **Rename active skill identities, not just paths.** Each `SKILL.md` frontmatter name, `agents/openai.yaml` display/default prompt, sibling skill reference, placeholder producer/consumer field, and command example must use `isomer-rsch-*` without `-v2`. Alternative considered: move folders but keep `-v2` skill names. That would make the filesystem look production-ready while installed skills still look experimental.

4. **Preserve migration and provenance material inside promoted skills when it belongs to current v2.** Existing `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, license notices, and deferred-resource notes remain non-active traceability material. Alternative considered: strip those directories during promotion. That would make the production tree smaller but lose review history and source-lineage context that current specs already allow.

5. **Update validators around a single active inventory.** Replace `EXPECTED_V1_SKILLS` and `EXPECTED_V2_SKILLS` with a suffixless `EXPECTED_DEEPSCI_SKILLS`, point canonical registries to `deepsci/isomer-rsch-shared/...`, and treat `deepsci` active files as the strict validation target. Non-active traceability rules remain path-aware.

## Risks / Trade-offs

- **Risk: stale `-v2` references remain in active guidance** -> Mitigation: add validation checks and run repository-wide searches for `isomer-rsch-*-v2`, `research-paradigm/v2`, and `deepsci-v2` after migration.
- **Risk: provenance files contain historical `v2` names that trigger active validators** -> Mitigation: keep role classification clear so migration, provenance, and source-copy material can preserve history without becoming runtime instructions.
- **Risk: external users invoke old skill names** -> Mitigation: document this as a breaking change and require callers to use suffixless `isomer-rsch-*` skills.
- **Risk: deleting v1 removes convenient reference material** -> Mitigation: rely on git history and the promoted DeepSci skills; do not carry unused compatibility material in the active skill tree.

## Migration Plan

1. Move each `skillset/research-paradigm/v2/isomer-rsch-*-v2` directory to `skillset/research-paradigm/deepsci/isomer-rsch-*`.
2. Delete `skillset/research-paradigm/v1/`.
3. Rewrite active skill names and paths in promoted skill files, placeholder bindings, root README, manifest, docs, specs, and operator guidance.
4. Update research-paradigm and skillset validators for suffixless `deepsci` inventory and registry paths.
5. Run the focused validation harnesses, then repository lint/type/test commands as appropriate.

Rollback is a normal git revert of the migration commit. No persistent data migration is required because this change affects source-controlled skills and documentation rather than stored research records.

## Open Questions

None. The user explicitly chose deletion of v1 skills and a production promotion of v2 into suffixless DeepSci skills.
