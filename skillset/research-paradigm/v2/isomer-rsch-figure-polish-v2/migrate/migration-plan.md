# Figure Polish Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/figure-polish`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-figure-polish-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-figure-polish.md`, copied from `context/explore/deepscientist-skill-analysis/figure-polish.md`.
- Exclusions from workflow-bearing deep inspection: passive templates, assets, plotting scripts, upstream licenses, eval fixtures, and source agent metadata were copied but not treated as control-flow instructions unless the entrypoint routed to them.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on scope. |
| quest state, quest files, paper directory | Workspace Runtime records, Artifacts, Evidence Items, Findings, Decision Records, Topic Workspace material, or semantic placeholders. |
| stage or companion skill | v2 Isomer research skill route. |
| memory cards | Workspace Runtime-backed continuity records or DeepScientist-compatible memory calls summarized through placeholders. |
| artifact paths and paper files | Semantic placeholders until storage binding is finalized. |
| operator/agent provenance in manuscript text | Excluded from paper-facing prose unless explicitly part of reproducibility material. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Use Workspace Runtime records when available; use `isomer-cli ext deepsci call memory.<tool> --input-json '{...}'` only for source-compatible behavior, then summarize durable meaning through placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, and Topic Workspace records; use `isomer-cli ext deepsci call artifact.<tool> --input-json '{...}'` only when preserving source-compatible behavior. |
| `bash_exec(...)` | Treat command execution as an Execution Adapter Command Request in the active Pixi-managed Project or Topic Workspace; use `isomer-cli ext deepsci call bash_exec.bash_exec --input-json '{...}'` only for compatibility. |
| concrete paper paths such as `paper/...` or `output/...` | Replace in migrated control text with semantic placeholders and leave storage binding to a later pass. |

## Storage and Artifact Substitutions

The migrated runtime entrypoint does not bind source artifacts to concrete paths. It uses placeholders defined in `migrate/placeholders.md`:

- `<FIGURE_SURFACE_CLASS>`
- `<FIGURE_MESSAGE>`
- `<FIGURE_STYLE_CONTRACT>`
- `<FIGURE_RENDER_REVIEW>`
- `<FINAL_FIGURE_EXPORT>`
- `<FIGURE_PROVENANCE_RECORD>`

## Unmatched Skill-Route Substitutions

- paper-plot maps to `isomer-rsch-paper-plot-v2` for first-pass standard figures.
- write maps to `isomer-rsch-write-v2` for manuscript integration.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the v2 batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer v2 research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `assets/deepscientist-academic.mplstyle`: passive style or image asset copied for compatibility.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Classify the figure surface | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Define the figure message | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Choose the chart form | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Apply the style contract | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Render the first draft | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Inspect and revise the render | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Export final formats | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |
| Record durable provenance | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `assets/deepscientist-academic.mplstyle`, `org/src/SKILL.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <FIGURE_SURFACE_CLASS> as milestone, paper main figure, appendix figure, internal review figure, or another justified surface.
- Produce <FIGURE_MESSAGE> with the one comparison or claim the figure must communicate.
- Select the chart form by research question, not visual taste, and remove panels that do not carry unique evidence.
- Produce <FIGURE_STYLE_CONTRACT> with restrained academic styling, readable labels, muted palette, clear hierarchy, and surface-appropriate dimensions.
- Generate an actual image output through the active execution adapter and record the script, input data, and output paths semantically.
- Inspect the rendered output and produce <FIGURE_RENDER_REVIEW>.
- Produce <FINAL_FIGURE_EXPORT> in the surface-appropriate formats, usually PNG for milestones and PDF/SVG plus PNG preview for paper-facing figures.
- Produce <FIGURE_PROVENANCE_RECORD> linking the figure to source data, script, claim, paper section, review item, or Artifact placeholder.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
