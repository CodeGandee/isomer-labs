# Nature Polishing Migration Provenance

This directory preserves the upstream DeepScientist `nature-polishing` source and the analysis used to refactor it into `isomer-rsch-nature-polishing`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/nature-polishing/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-nature-polishing.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/nature-polishing.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL-SOURCE.md`
- `src/references/phrasebank-playbook.md`
- `src/references/section-moves.md`
- `src/references/style-guardrails.md`
- `src/references/writing-strategy.md`

Copied but not treated as workflow-bearing instructions:

- `src/UPSTREAM_LICENSE.txt`
- `src/agents/openai.yaml`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
