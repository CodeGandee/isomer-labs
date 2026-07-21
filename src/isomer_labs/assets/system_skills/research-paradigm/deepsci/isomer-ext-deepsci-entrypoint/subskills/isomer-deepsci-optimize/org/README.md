# Isomer Research Optimize Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `optimize` source and the analysis used to refactor it into `isomer-rsch-optimize`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/optimize/`.
- `analysis/analysis-of-optimize.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL-SOURCE.md`
- `src/references/brief-shaping-playbook.md`
- `src/references/candidate-board-template.md`
- `src/references/candidate-ranking-template.md`
- `src/references/codegen-route-playbook.md`
- `src/references/debug-response-template.md`
- `src/references/frontier-review-template.md`
- `src/references/fusion-playbook.md`
- `src/references/method-brief-template.md`
- `src/references/operational-guidance.md`
- `src/references/optimization-memory-template.md`
- `src/references/optimize-checklist-template.md`
- `src/references/plateau-response-playbook.md`
- `src/references/prompt-patterns.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
