# Paper Outline Migration Provenance

This directory preserves the upstream DeepScientist `paper-outline` source and the analysis used to refactor it into `isomer-rsch-paper-outline`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/paper-outline/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-paper-outline.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/paper-outline.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/outline-patterns.md`

No source files were excluded from workflow-bearing analysis.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
