# Scout Migration Provenance

This directory preserves the upstream DeepScientist `scout` source and the analysis used to refactor it into `isomer-rsch-scout`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/scout/`, including `SKILL.md` and all source reference pages.
- `analysis/analysis-of-scout.md`: self-contained deep inspection of the source skill process, generated through the `$imsight-agent-skill-handling deep-inspect` procedure.

## Analysis Coverage

Analyzed files:

- `src/SKILL.md`
- `src/references/operational-guidance.md`
- `src/references/literature-scout-template.md`
- `src/references/paper-triage-playbook.md`
- `src/references/eval-contract-template.md`
- `src/references/baseline-shortlist-template.md`

No source files were excluded. The source skill has no agent config, scripts, assets, fixtures, or generated files.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, and `artifact.*`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
