# Nature Polishing Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/nature-polishing`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-nature-polishing`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-nature-polishing.md`, copied from `context/explore/deepscientist-skill-analysis/nature-polishing.md`.
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

- `<PAPER_TYPE_DIAGNOSIS>`
- `<PROSE_FAILURE_DIAGNOSIS>`
- `<CLAIM_BOUNDARY_CHECK>`
- `<SECTION_LOGIC_REBUILD>`
- `<POLISHED_MANUSCRIPT_TEXT>`
- `<POLISHING_STYLE_QA>`
- `<POLISHING_EVIDENCE_BLOCKER>`

## Unmatched Skill-Route Substitutions

- write maps to `isomer-rsch-write` for larger manuscript drafting.
- review maps to `isomer-rsch-review` for independent audit.
- rebuttal maps to `isomer-rsch-rebuttal` for reviewer-response text.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `UPSTREAM_LICENSE.txt`: upstream license notice retained.
- `references/phrasebank-playbook.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/section-moves.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/style-guardrails.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/writing-strategy.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Identify paper type | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |
| Diagnose failure mode | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |
| Check claim boundary | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |
| Rebuild section logic | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |
| Apply section moves and phrase support | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/phrasebank-playbook.md` |
| Polish sentences and paragraphs | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |
| Run style guardrails | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/style-guardrails.md` |
| Return revised text or caution | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/writing-strategy.md`, `references/section-moves.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce <PAPER_TYPE_DIAGNOSIS> for the manuscript logic: research, method, hypothesis-driven, algorithmic, device, resource, review, or another justified type.
- Produce <PROSE_FAILURE_DIAGNOSIS>: wrong paper-type logic, missing gap, unsupported claim, evidence without interpretation, missing boundary, Results/Discussion mixing, weak title or abstract, or sentence clutter.
- Produce <CLAIM_BOUNDARY_CHECK> from available evidence, citations, and user-provided context before polishing.
- Produce <SECTION_LOGIC_REBUILD> using references/writing-strategy.
- Use references/phrasebank-playbook.
- Produce <POLISHED_MANUSCRIPT_TEXT> with concise, calibrated, citation-aware prose while preserving the author meaning and evidence boundary.
- Produce <POLISHING_STYLE_QA> using references/style-guardrails.
- Return the polished text with a compact diagnosis and any <POLISHING_EVIDENCE_BLOCKER> or claim-scope warning that must accompany the revision.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
