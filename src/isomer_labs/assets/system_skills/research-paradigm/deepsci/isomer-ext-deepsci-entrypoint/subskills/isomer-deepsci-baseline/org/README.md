# Isomer Research Baseline Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `baseline` source and the analysis used to refactor it into `isomer-rsch-baseline`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/baseline/`.
- `analysis/analysis-of-baseline.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL-SOURCE.md`
- `src/references/artifact-flow-examples.md`
- `src/references/artifact-payload-examples.md`
- `src/references/baseline-checklist-template.md`
- `src/references/baseline-plan-template.md`
- `src/references/boundary-cases.md`
- `src/references/codebase-audit-checklist.md`
- `src/references/comparability-contract.md`
- `src/references/operational-guidance.md`
- `src/references/route-selection.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
