# Isomer Research Analysis Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `analysis-campaign` source and the analysis used to refactor it into `isomer-rsch-analysis`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/analysis-campaign/`.
- `analysis/analysis-of-analysis-campaign.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL.md`
- `src/references/artifact-flow-examples.md`
- `src/references/boundary-cases.md`
- `src/references/campaign-checklist-template.md`
- `src/references/campaign-design.md`
- `src/references/campaign-plan-template.md`
- `src/references/operational-guidance.md`
- `src/references/writing-facing-slice-examples.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
