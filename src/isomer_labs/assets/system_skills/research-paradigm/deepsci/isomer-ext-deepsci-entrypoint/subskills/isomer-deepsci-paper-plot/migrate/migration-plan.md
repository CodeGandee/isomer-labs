# Paper Plot Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/paper-plot`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-paper-plot`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-paper-plot.md`, copied from `context/explore/deepscientist-skill-analysis/paper-plot.md`.
- Exclusions from workflow-bearing deep inspection: passive templates, assets, plotting scripts, upstream licenses, eval fixtures, and source agent metadata were copied but not treated as control-flow instructions unless the entrypoint routed to them.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on scope. |
| quest state, quest files, paper directory | Workspace Runtime records, Artifacts, Evidence Items, Findings, Decision Records, Topic Workspace material, or semantic placeholders. |
| stage or companion skill | production DeepSci Isomer research skill route. |
| memory cards | Workspace Runtime-backed continuity records or DeepScientist-compatible memory calls summarized through placeholders. |
| artifact paths and paper files | Semantic placeholders until storage binding is finalized. |
| operator/agent provenance in manuscript text | Excluded from paper-facing prose unless explicitly part of reproducibility material. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Use Workspace Runtime records when available; use `isomer-cli ext deepsci call memory.<tool> --input-json '{...}'` only for source-compatible behavior, then status durable meaning through placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, and Topic Workspace records; use `isomer-cli ext deepsci call artifact.<tool> --input-json '{...}'` only when preserving source-compatible behavior. |
| `bash_exec(...)` | Treat command execution as an Execution Adapter Command Request in the active Pixi-managed Project or Topic Workspace; use `isomer-cli ext deepsci call bash_exec.bash_exec --input-json '{...}'` only for compatibility. |
| concrete paper paths such as `paper/...` or `output/...` | Replace in migrated control text with semantic placeholders and leave storage binding to a later pass. |

## Storage and Artifact Substitutions

The migrated runtime entrypoint does not bind source artifacts to concrete paths. It uses placeholders defined in `migrate/placeholders.md`:

- `DEEPSCI:CHART-QUESTION`
- `DEEPSCI:PLOT-STYLE-SELECTION`
- `DEEPSCI:PLOT-TEMPLATE-COPY`
- `DEEPSCI:PLOT-DATA-SUBSTITUTION-RECORD`
- `DEEPSCI:FIRST-PASS-FIGURE`
- `DEEPSCI:PLOT-RENDER-INSPECTION`
- `DEEPSCI:FIGURE-POLISH-HANDOFF`

## Unmatched Skill-Route Substitutions

- figure-polish maps to `isomer-rsch-figure-polish`.
- write maps to `isomer-rsch-write`.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `references/bar_grouped_hatch.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/bar_paired_delta.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/line_confidence_band.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/line_loss_with_inset.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/line_training_curve.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/radar_dual_series.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/scatter_broken_axis.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/scatter_tsne_cluster.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `scripts/bar_memevolve.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/bar_spice.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/line_aime.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/line_loss_inset.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/line_selfdistill.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/radar_dora.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/scatter_break.py`: passive plotting/script template copied for adaptation into task-local workspaces.
- `scripts/scatter_tsne.py`: passive plotting/script template copied for adaptation into task-local workspaces.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Confirm the chart question | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Choose the bundled style | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Read the style reference | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Copy the template script | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Replace data and labels only | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Run and inspect the copied script | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |
| Route durable figures | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/bar_paired_delta.md`, `references/bar_grouped_hatch.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce DEEPSCI:CHART-QUESTION with comparison, units, grouping, key message, required labels, and output target.
- Select DEEPSCI:PLOT-STYLE-SELECTION from the available style table: paired delta bar, grouped hatch bar, confidence-band line, training curve line, loss with inset, t-SNE scatter, broken-axis scatter, or radar dual series.
- Read the matching references/*.
- Create DEEPSCI:PLOT-TEMPLATE-COPY by copying the matching scripts/*.
- Record DEEPSCI:PLOT-DATA-SUBSTITUTION-RECORD for changed data arrays, labels, units, category names, legend text, and output filenames.
- Generate DEEPSCI:FIRST-PASS-FIGURE through the active execution adapter, then inspect the actual render and record DEEPSCI:PLOT-RENDER-INSPECTION.
- If the figure is paper-facing, appendix-facing, milestone-facing, or final, create DEEPSCI:FIGURE-POLISH-HANDOFF for isomer-rsch-figure-polish; otherwise stop with the first-pass figure and substitution record.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
