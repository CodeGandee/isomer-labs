# Isomer Research Science Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `science` source and the analysis used to refactor it into `isomer-rsch-science`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/science/`.
- `analysis/analysis-of-science.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL-SOURCE.md`
- `src/references/artifact-science-tool.md`
- `src/references/claim-type-discipline.md`
- `src/references/domain-index.md`
- `src/references/hpc-via-bash-exec.md`
- `src/references/package-check-playbook.md`
- `src/references/package-index.min.json`
- `src/references/science-task-brief-template.md`


The source also contains 169 package-card files or catalog entries that were copied but summarized rather than expanded in the analysis.

## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
