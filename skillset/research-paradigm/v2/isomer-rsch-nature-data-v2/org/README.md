# Nature Data Migration Provenance

This directory preserves the upstream DeepScientist `nature-data` source and the analysis used to refactor it into `isomer-rsch-nature-data-v2`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/nature-data/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-nature-data.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/nature-data.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/chinese-author-alignment.md`
- `src/references/fair-metadata-checklist.md`
- `src/references/policy-principles.md`
- `src/references/repository-and-identifiers.md`
- `src/references/source-basis.md`
- `src/references/statement-patterns.md`

Copied but not treated as workflow-bearing instructions:

- `src/UPSTREAM_LICENSE.txt`
- `src/agents/openai.yaml`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
