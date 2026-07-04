# Rebuttal Migration Provenance

This directory preserves the upstream DeepScientist `rebuttal` source and the analysis used to refactor it into `isomer-rsch-rebuttal`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/rebuttal/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-rebuttal.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/rebuttal.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/action-plan-template.md`
- `src/references/evidence-update-template.md`
- `src/references/response-letter-template.md`
- `src/references/review-matrix-template.md`

No source files were excluded from workflow-bearing analysis.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
