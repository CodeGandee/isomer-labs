# Nature Paper2PPT Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/nature-paper2ppt`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-nature-paper2ppt-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-nature-paper2ppt.md`, copied from `context/explore/deepscientist-skill-analysis/nature-paper2ppt.md`.
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

- `<PAPER_PRESENTATION_SOURCE_PACKET>`
- `<PAPER_TYPE_CLASSIFICATION>`
- `<CHINESE_PRESENTATION_PLAN>`
- `<PRESENTATION_FIGURE_SELECTION>`
- `<PRESENTATION_ASSET_MANIFEST>`
- `<CHINESE_SLIDE_CONTENT>`
- `<PPTX_DECK>`
- `<PPTX_QA_REPORT>`
- `<PPTX_REVISION_LOG>`

## Unmatched Skill-Route Substitutions

- nature-figure maps to `isomer-rsch-nature-figure-v2` only when paper figures need re-creation rather than extraction.
- write maps to `isomer-rsch-write-v2` only when manuscript text, not slides, needs repair.
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

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Extract source material | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Classify the paper type | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Choose presentation logic | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Build the Chinese plan | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Select evidence figures | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Extract and prepare assets | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Write slide content | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |
| Build and verify the PPTX | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `org/src/SKILL.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <PAPER_PRESENTATION_SOURCE_PACKET> with metadata, abstract, headings, figure legends, table captions, claims, methods, results, and limitations from available source material.
- Produce <PAPER_TYPE_CLASSIFICATION> before slide planning: discovery, mechanism, method, resource, clinical, materials/engineering, review, or another justified type.
- Select claim-first, question-to-evidence, problem-to-solution, workflow-to-validation, evidence-map, or another suited logic.
- Produce <CHINESE_PRESENTATION_PLAN> with 10-16 slide sequence, story spine, section flow, and audience-facing emphasis.
- Produce <PRESENTATION_FIGURE_SELECTION> with only figures and panels that carry the argument.
- Produce <PRESENTATION_ASSET_MANIFEST> for figure crops, rendered pages, provenance, captions, and local asset quality.
- Produce <CHINESE_SLIDE_CONTENT> with Chinese titles, bullets, captions, takeaways, and speaker notes, preserving evidence limits and citation/attribution needs.
- Create <PPTX_DECK>, reopen or inspect package structure, render previews when a renderer is available, revise defects, and produce <PPTX_QA_REPORT> plus <PPTX_REVISION_LOG> when revisions occur.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
