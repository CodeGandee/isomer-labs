# Isomer Research Experiment V2 Migration Provenance

This directory preserves the upstream DeepScientist `experiment` source and the analysis used to refactor it into `isomer-rsch-experiment-v2`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/experiment/`.
- `analysis/analysis-of-experiment.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL.md`
- `src/references/evidence-ladder.md`
- `src/references/execution-playbook.md`
- `src/references/main-experiment-checklist-template.md`
- `src/references/main-experiment-plan-template.md`
- `src/references/operational-guidance.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
