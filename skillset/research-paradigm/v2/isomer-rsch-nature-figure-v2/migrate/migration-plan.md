# Nature Figure Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/nature-figure`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-nature-figure-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-nature-figure.md`, copied from `context/explore/deepscientist-skill-analysis/nature-figure.md`.
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
| `memory.*` | Use Workspace Runtime records when available; use `isomer-cli ext deepsci call memory.<tool> --input-json '{...}'` only for source-compatible behavior, then status durable meaning through placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, and Topic Workspace records; use `isomer-cli ext deepsci call artifact.<tool> --input-json '{...}'` only when preserving source-compatible behavior. |
| `bash_exec(...)` | Treat command execution as an Execution Adapter Command Request in the active Pixi-managed Project or Topic Workspace; use `isomer-cli ext deepsci call bash_exec.bash_exec --input-json '{...}'` only for compatibility. |
| concrete paper paths such as `paper/...` or `output/...` | Replace in migrated control text with semantic placeholders and leave storage binding to a later pass. |

## Storage and Artifact Substitutions

The migrated runtime entrypoint does not bind source artifacts to concrete paths. It uses placeholders defined in `migrate/placeholders.md`:

- `<NATURE_FIGURE_BACKEND_CHOICE>`
- `<NATURE_FIGURE_CONTRACT>`
- `<NATURE_FIGURE_RUNTIME_CHECK>`
- `<NATURE_PANEL_EVIDENCE_MAP>`
- `<NATURE_FIGURE_ARCHETYPE>`
- `<NATURE_EXPORT_CONTRACT>`
- `<NATURE_FIGURE_EXPORT_BUNDLE>`
- `<NATURE_FIGURE_QA_REPORT>`
- `<NATURE_FIGURE_BLOCKER>`

## Unmatched Skill-Route Substitutions

- paper-plot maps to `isomer-rsch-paper-plot-v2` for simpler first-pass standard figures.
- figure-polish maps to `isomer-rsch-figure-polish-v2` for non-Nature durable figure QA.
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
- `UPSTREAM_LICENSE.txt`: upstream license notice retained.
- `evals/evals.json`: passive eval fixture copied for provenance.
- `references/api.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/backend-selection.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/chart-types.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/common-patterns.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/design-theory.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/figure-contract.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/nature-2026-observations.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/qa-contract.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/r-template-index.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/r-workflow.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/tutorials.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Check backend selection | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/backend-selection.md` |
| Define the figure contract | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/figure-contract.md` |
| Check selected runtime | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/backend-selection.md`, `references/figure-contract.md` |
| Map the evidence chain | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/backend-selection.md`, `references/figure-contract.md` |
| Choose archetype and design system | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/common-patterns.md`, `references/chart-types.md`, `references/design-theory.md`, `references/nature-2026-observations.md` |
| Set journal export contract | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/backend-selection.md`, `references/figure-contract.md` |
| Generate with selected backend | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/api.md`, `references/tutorials.md`, `references/r-workflow.md`, `references/r-template-index.md` |
| Preview and QA | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/qa-contract.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <NATURE_FIGURE_BACKEND_CHOICE> as Python or R.
- Produce <NATURE_FIGURE_CONTRACT> with one-sentence conclusion, evidence chain, panel roles, dimensions, source data, statistics, integrity notes, and export formats.
- Produce <NATURE_FIGURE_RUNTIME_CHECK> for packages, fonts, device, renderer, and export capability in the selected backend only.
- Produce <NATURE_PANEL_EVIDENCE_MAP> linking each panel to unique evidence, source data, statistics, and claim.
- Produce <NATURE_FIGURE_ARCHETYPE> and read references/nature-2026-observations.
- Produce <NATURE_EXPORT_CONTRACT> covering SVG/PDF/TIFF/PNG, editable text, dimensions, color, line weights, image-integrity notes, and source-data expectations.
- Use Python guidance from references/api.
- Inspect rendered previews and produce <NATURE_FIGURE_QA_REPORT> using references/qa-contract.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
