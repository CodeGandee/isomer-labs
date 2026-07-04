# Review Migration Provenance

This directory preserves the upstream DeepScientist `review` source and the analysis used to refactor it into `isomer-rsch-review`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/review/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-review.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/review.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/experiment-todo-template.md`
- `src/references/review-report-template.md`
- `src/references/revision-log-template.md`

No source files were excluded from workflow-bearing analysis.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
