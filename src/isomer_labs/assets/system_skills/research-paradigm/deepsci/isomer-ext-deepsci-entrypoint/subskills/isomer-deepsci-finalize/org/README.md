# Isomer Research Finalize Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `finalize` source and the analysis used to refactor it into `isomer-rsch-finalize`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/finalize/`.
- `analysis/analysis-of-finalize.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL-SOURCE.md`
- `src/references/checkpoint-memory-template.md`
- `src/references/finalization-checklist.md`
- `src/references/resume-packet-template.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
