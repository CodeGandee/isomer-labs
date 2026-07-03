# Paper Plot Migration Provenance

This directory preserves the upstream DeepScientist `paper-plot` source and the analysis used to refactor it into `isomer-rsch-paper-plot`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/paper-plot/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-paper-plot.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/paper-plot.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/bar_grouped_hatch.md`
- `src/references/bar_paired_delta.md`
- `src/references/line_confidence_band.md`
- `src/references/line_loss_with_inset.md`
- `src/references/line_training_curve.md`
- `src/references/radar_dual_series.md`
- `src/references/scatter_broken_axis.md`
- `src/references/scatter_tsne_cluster.md`

Copied but not treated as workflow-bearing instructions:

- `src/agents/openai.yaml`
- `src/scripts/bar_memevolve.py`
- `src/scripts/bar_spice.py`
- `src/scripts/line_aime.py`
- `src/scripts/line_loss_inset.py`
- `src/scripts/line_selfdistill.py`
- `src/scripts/radar_dora.py`
- `src/scripts/scatter_break.py`
- `src/scripts/scatter_tsne.py`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
