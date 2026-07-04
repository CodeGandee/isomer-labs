# Rebuttal Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/rebuttal`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-rebuttal`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-rebuttal.md`, copied from `context/explore/deepscientist-skill-analysis/rebuttal.md`.
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

- `<REVIEW_PACKAGE_NORMALIZATION>`
- `<REVIEWER_ITEM_MATRIX>`
- `<REBUTTAL_ACTION_PLAN>`
- `<REVIEWER_LINKED_EVIDENCE_TODO>`
- `<REBUTTAL_EVIDENCE_UPDATE>`
- `<MANUSCRIPT_TEXT_DELTA>`
- `<RESPONSE_LETTER_DRAFT>`
- `<REVISION_HANDOFF_BUNDLE>`

## Unmatched Skill-Route Substitutions

- scout maps to `isomer-rsch-scout`.
- baseline maps to `isomer-rsch-baseline`.
- analysis-campaign maps to `isomer-rsch-analysis`.
- write maps to `isomer-rsch-write`.
- decision maps to `isomer-rsch-decision`.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `references/action-plan-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/evidence-update-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/response-letter-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/review-matrix-template.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Normalize the review package | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-matrix-template.md` |
| Decide required changes | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/action-plan-template.md` |
| Route evidence work only when needed | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-matrix-template.md`, `references/action-plan-template.md` |
| Route manuscript changes explicitly | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-matrix-template.md`, `references/action-plan-template.md` |
| Update the rebuttal matrix | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/evidence-update-template.md` |
| Assemble the response letter | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/response-letter-template.md` |
| Prepare final revision handoff | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/review-matrix-template.md`, `references/action-plan-template.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <REVIEW_PACKAGE_NORMALIZATION> and <REVIEWER_ITEM_MATRIX> from reviewer text, keeping source-faithful wording, stable item ids, class, severity, affected claim, evidence anchor, and route.
- Produce <REBUTTAL_ACTION_PLAN> using references/action-plan-template.
- For novelty or positioning route to scout, for comparator gaps route to baseline, and for reviewer-linked evidence route to analysis.
- Route structure, claim-scope, and wording changes to write, and record <MANUSCRIPT_TEXT_DELTA> for each changed claim, section, caption, or limitation.
- After each routed fix, produce <REBUTTAL_EVIDENCE_UPDATE> using references/evidence-update-template.
- Draft <RESPONSE_LETTER_DRAFT> using references/response-letter-template.
- Produce <REVISION_HANDOFF_BUNDLE> with response letter, text deltas, evidence updates, unresolved limitations, and route decision for finalization or continued work.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
