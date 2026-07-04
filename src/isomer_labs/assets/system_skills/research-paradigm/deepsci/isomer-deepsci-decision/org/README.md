# Isomer Research Decision Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `decision` source and the analysis used to refactor it into `isomer-rsch-decision`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/decision/`.
- `analysis/analysis-of-decision.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL.md`
- `src/references/checkpoint-memory-template.md`
- `src/references/operational-guidance.md`
- `src/references/research-route-criteria.md`
- `src/references/strategic-decision-template.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
