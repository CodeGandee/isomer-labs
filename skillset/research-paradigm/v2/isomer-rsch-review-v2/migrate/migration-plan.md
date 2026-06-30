# Review Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/review`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-review-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-review.md`, copied from `context/explore/deepscientist-skill-analysis/review.md`.
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

- `<REVIEW_AUDIT_PLAN>`
- `<LITERATURE_BENCHMARK_NOTE>`
- `<REVIEW_REPORT>`
- `<REVISION_LOG>`
- `<REVIEW_EXPERIMENT_TODO>`
- `<PAPER_EXPERIMENT_MATRIX_UPDATE>`
- `<REVIEW_ROUTE_DECISION>`

## Unmatched Skill-Route Substitutions

- write maps to `isomer-rsch-write-v2`.
- scout maps to `isomer-rsch-scout-v2`.
- baseline maps to `isomer-rsch-baseline-v2`.
- analysis-campaign maps to `isomer-rsch-analysis-v2`.
- decision maps to `isomer-rsch-decision-v2`.
- rebuttal maps to `isomer-rsch-rebuttal-v2`.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the v2 batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer v2 research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `references/experiment-todo-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/review-report-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/revision-log-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Plan the audit | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-report-template.md`, `references/revision-log-template.md` |
| Run literature and benchmark checks | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-report-template.md`, `references/revision-log-template.md` |
| Write the review report | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-report-template.md` |
| Produce the revision log | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/revision-log-template.md` |
| Create evidence TODOs only when needed | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/experiment-todo-template.md` |
| Update paper experiment planning | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-report-template.md`, `references/revision-log-template.md` |
| Route the next step | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-report-template.md`, `references/revision-log-template.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <REVIEW_AUDIT_PLAN> with claim set, strongest and weakest evidence, likely rejection reasons, experiment/analysis inventory, comparator papers, language hygiene risks, and likely routes.
- Produce <LITERATURE_BENCHMARK_NOTE> from nearby strong papers, official venue expectations, existing literature notes, and verified sources when novelty or positioning is uncertain.
- Produce <REVIEW_REPORT> using references/review-report-template.
- Produce <REVISION_LOG> using references/revision-log-template.
- If real evidence is missing, produce <REVIEW_EXPERIMENT_TODO> with concrete follow-up work using references/experiment-todo-template.
- When experiment planning changes, produce <PAPER_EXPERIMENT_MATRIX_UPDATE> so writing and rebuttal-facing work remain aligned.
- Produce <REVIEW_ROUTE_DECISION> to write, scout, baseline, analysis, decision, rebuttal, or finalize with evidence and priority ordering.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
