# Isomer Research Idea Production DeepSci Migration Provenance

This directory preserves the upstream DeepScientist `idea` source and the analysis used to refactor it into `isomer-rsch-idea`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/idea/`.
- `analysis/analysis-of-idea.md`: source-process inspection used by the refactor migration.

## Analysis Coverage

Analyzed files:

- `src/SKILL.md`
- `src/references/controlled-brainstorming-playbook.md`
- `src/references/current-board-packet-template.md`
- `src/references/high-value-idea-sourcing.md`
- `src/references/idea-generation-playbook.md`
- `src/references/idea-thinking-flow.md`
- `src/references/literature-survey-template.md`
- `src/references/objective-contract-template.md`
- `src/references/outline-seeding-example.md`
- `src/references/pre-idea-draft-template.md`
- `src/references/related-work-playbook.md`
- `src/references/research-history-playbook.md`
- `src/references/research-outline-template.md`
- `src/references/selection-gate.md`


## Notes

Files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those terms according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
