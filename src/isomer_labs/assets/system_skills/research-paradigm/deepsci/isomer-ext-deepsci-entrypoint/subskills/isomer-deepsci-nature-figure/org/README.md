# Nature Figure Migration Provenance

This directory preserves the upstream DeepScientist `nature-figure` source and the analysis used to refactor it into `isomer-rsch-nature-figure`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/nature-figure/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-nature-figure.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/nature-figure.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL-SOURCE.md`
- `src/references/api.md`
- `src/references/backend-selection.md`
- `src/references/chart-types.md`
- `src/references/common-patterns.md`
- `src/references/design-theory.md`
- `src/references/figure-contract.md`
- `src/references/nature-2026-observations.md`
- `src/references/qa-contract.md`
- `src/references/r-template-index.md`
- `src/references/r-workflow.md`
- `src/references/tutorials.md`

Copied but not treated as workflow-bearing instructions:

- `src/UPSTREAM_LICENSE.txt`
- `src/agents/openai.yaml`
- `src/evals/evals.json`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
