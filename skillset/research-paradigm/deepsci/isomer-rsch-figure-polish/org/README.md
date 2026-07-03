# Figure Polish Migration Provenance

This directory preserves the upstream DeepScientist `figure-polish` source and the analysis used to refactor it into `isomer-rsch-figure-polish`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/figure-polish/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-figure-polish.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/figure-polish.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`

Copied but not treated as workflow-bearing instructions:

- `src/assets/deepscientist-academic.mplstyle`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
