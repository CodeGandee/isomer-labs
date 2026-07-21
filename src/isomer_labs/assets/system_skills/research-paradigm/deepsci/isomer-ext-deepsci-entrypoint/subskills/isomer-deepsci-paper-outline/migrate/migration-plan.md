# Paper Outline Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/paper-outline`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-paper-outline`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-paper-outline.md`, copied from `context/explore/deepscientist-skill-analysis/paper-outline.md`.
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

- `DEEPSCI:PAPER-STATE-SNAPSHOT`
- `DEEPSCI:ONE-SENTENCE-PAPER-IDEA`
- `DEEPSCI:CLAIM-EVIDENCE-BOUNDARY`
- `DEEPSCI:PAPER-VIEW`
- `DEEPSCI:EVIDENCE-VIEW`
- `DEEPSCI:OUTLINE-VALIDATION-REPORT`
- `DEEPSCI:SECTION-WRITING-PLAN`
- `DEEPSCI:PAPER-OUTLINE-ROUTE-DECISION`

## Unmatched Skill-Route Substitutions

- write maps to `isomer-rsch-write`.
- analysis-campaign maps to `isomer-rsch-analysis`.
- decision maps to `isomer-rsch-decision`.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL-MAIN.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL-MAIN.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `references/outline-patterns.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Read paper state | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Name the one-sentence idea | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Separate facts from interpretation | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Build the paper view | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Build the evidence view | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Validate the outline | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Repair until mature or blocked | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |
| Compile writing plan | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/outline-patterns.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Build DEEPSCI:PAPER-STATE-SNAPSHOT from current outline, paper contract, evidence surfaces, run records, figures, reviewer needs, and user constraints.
- Produce DEEPSCI:ONE-SENTENCE-PAPER-IDEA stating what readers should remember and why the result matters.
- Produce DEEPSCI:CLAIM-EVIDENCE-BOUNDARY that distinguishes measured facts, allowed interpretations, limitations, and unsupported claims.
- Draft DEEPSCI:PAPER-VIEW with thesis, story spine, scoped claims, method abstraction, evaluation plan, analysis plan, and target reader logic.
- Draft DEEPSCI:EVIDENCE-VIEW with runs, paths, metrics, settings, source data, figures, reproducibility details, and appendix-only support separated from manuscript story.
- Produce DEEPSCI:OUTLINE-VALIDATION-REPORT using claim support, falsification boundary, method clarity, evaluation coverage, analysis maturity, and reviewer-risk checks.
- If validation fails, revise the paper view, evidence view, or claim boundary.
- When validation passes, produce DEEPSCI:SECTION-WRITING-PLAN for isomer-rsch-write, including section jobs, required displays, citation needs, and evidence limits.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
