# Isomer Research Analysis Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/analysis-campaign`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-analysis`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source file is copied and refactored under the target runtime tree with source-relative paths preserved, except the source entrypoint and `agents/openai.yaml`.
- Source files covered: `SKILL.md`, `references/artifact-flow-examples.md`, `references/boundary-cases.md`, `references/campaign-checklist-template.md`, `references/campaign-design.md`, `references/campaign-plan-template.md`, `references/operational-guidance.md`, `references/writing-facing-slice-examples.md`.
- Source analysis: `org/analysis/analysis-of-analysis-campaign.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native production DeepSci pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | production DeepSci research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `<ANALYSIS_ROUTE_DECISION>` or `<ANALYSIS_BLOCKER_RECORD>`, later bound to production DeepSci skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |
| `PLAN.md`, local matrices, or checklist files | `<ANALYSIS_CAMPAIGN_PLAN>`, `<ANALYSIS_CAMPAIGN_CHECKLIST>`, or `<ANALYSIS_WRITEBACK_MAP>` depending on the source meaning. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Source campaign objects, paper matrices, slice worktrees, and slice records | Use `<ANALYSIS_CAMPAIGN_PLAN>`, `<ANALYSIS_WRITEBACK_MAP>`, `<ANALYSIS_SLICE_RECORD>`, and related placeholders until storage bindings are finalized. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `<ANALYSIS_CONTEXT_BRIEF>`
- `<PARENT_RESULT_EVIDENCE>`
- `<ANALYSIS_RESOURCE_ENVELOPE>`
- `<ANALYSIS_CAMPAIGN_PLAN>`
- `<ANALYSIS_CAMPAIGN_CHECKLIST>`
- `<ANALYSIS_SLICE_PLAN>`
- `<ANALYSIS_SLICE_RECORD>`
- `<ANALYSIS_WRITEBACK_MAP>`
- `<ANALYSIS_CAMPAIGN_SUMMARY>`
- `<ANALYSIS_ROUTE_DECISION>`
- `<ANALYSIS_BLOCKER_RECORD>`
- `<ANALYSIS_CONTINUITY_UPDATE>`

## Unmatched Skill-Route Substitutions

analysis-campaign maps to isomer-rsch-analysis. Source routes to experiment, idea, write, decision, review, or rebuttal map to production DeepSci route decisions where matching production DeepSci skills exist, otherwise to semantic route placeholders in the local registry.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native production DeepSci control surface with workflow steps that reference the required support pages.
- `references/campaign-design.md`: source-preserved campaign design page refactored into route shape, priority, slice class, and resource-aware support.
- `references/campaign-plan-template.md`: source-preserved campaign plan template refactored into native route-record support and template fields.
- `references/campaign-checklist-template.md`: source-preserved campaign checklist template refactored into acceptance-boundary support and template fields.
- `references/evidence-gate.md`: production DeepSci support page distilled from source validation, hard success gates, comparability contract, negative cases, and aggregation rules.
- `references/slice-record-template.md`: production DeepSci support page distilled from source slice evidence contract and durable route-record rules.
- `references/artifact-flow-examples.md`: source-preserved evidence-flow examples refactored into native Isomer evidence-record sequences.
- `references/boundary-cases.md`: source-preserved boundary-case page refactored into stage-boundary, comparability, qualitative, one-slice, repeated-failure, pre-outline, extra-comparator, and interpretation-boundary support.
- `references/writing-facing-slice-examples.md`: source-preserved writing-facing example page refactored into paper, review, and rebuttal write-back support.
- `references/operational-guidance.md`: source-preserved operational support page refactored into durable route, resource, execution, memory, and charting rules.

## Main Workflow Support Mapping

| Target Workflow Step | Source Support Material | Target Runtime Support |
| --- | --- | --- |
| Lock the parent boundary | `SKILL.md` Match signals, Control workflow step 1, Hard success gates, Analysis routes, Durable route records, Negative cases; `references/campaign-design.md`; `references/boundary-cases.md`; `references/campaign-plan-template.md`. | `references/campaign-design.md`, `references/boundary-cases.md`, `references/campaign-plan-template.md` |
| Audit the execution envelope | `SKILL.md` Control workflow step 2, Paper-facing quantity reminder, Authority and freedom, Hard success gates; `references/campaign-design.md` resource gate; `references/operational-guidance.md`; `references/campaign-checklist-template.md`. | `references/operational-guidance.md`, `references/campaign-design.md`, `references/campaign-checklist-template.md` |
| Choose the smallest useful slice set | `SKILL.md` Control workflow step 3, Analysis routes, Slice evidence contract, Writing-facing boundary; `references/campaign-design.md`; `references/writing-facing-slice-examples.md`; `references/boundary-cases.md`. | `references/campaign-design.md`, `references/boundary-cases.md`, `references/writing-facing-slice-examples.md` |
| Gate resources and comparability | `SKILL.md` Constraints, Validation, Hard success gates, Comparability contract, Negative cases; `references/campaign-checklist-template.md`; `references/boundary-cases.md`. | `references/evidence-gate.md`, `references/campaign-checklist-template.md`, `references/boundary-cases.md` |
| Run and record slices | `SKILL.md` Control workflow steps 4-5, Slice evidence contract, Durable route records, Operational guidance; `references/artifact-flow-examples.md`; `references/operational-guidance.md`. | `references/slice-record-template.md`, `references/artifact-flow-examples.md`, `references/operational-guidance.md` |
| Interpret the campaign boundary | `SKILL.md` Control workflow step 6, Aggregation and reporting, Writing-facing boundary, Negative cases; `references/boundary-cases.md`; `references/writing-facing-slice-examples.md`; `references/campaign-checklist-template.md`. | `references/evidence-gate.md`, `references/boundary-cases.md`, `references/writing-facing-slice-examples.md` |
| Route from evidence | `SKILL.md` Hard success gates, Durable route records, Negative cases and stop rules, Exit criteria; `references/artifact-flow-examples.md`; `references/operational-guidance.md`. | `references/evidence-gate.md`, `references/artifact-flow-examples.md`, `references/operational-guidance.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Parent result, parent claim, paper gap, reviewer item, or route decision exists before analysis begins.
- The parent evidence question, comparison target, stop condition, and route condition are explicit.
- Current execution envelope conditions campaign design, slice ordering, and infeasible-slice handling.
- The lightest trustworthy route is selected rather than defaulting to heavy campaign machinery.
- Slice frontier is bounded and prioritized by soundness gain per cost.
- Comparability is explicit, and non-comparable evidence is labeled.
- Writing-facing slices are write-backable or blocked explicitly.
- Slice records precede campaign-level claims.
- Null, negative, failed, partial, blocked, infeasible, superseded, and contradictory findings remain visible.
- Campaign aggregation separates stable support, contradiction, partial support, and unresolved ambiguity.
- Next route or blocker is explicit and evidence-backed.
