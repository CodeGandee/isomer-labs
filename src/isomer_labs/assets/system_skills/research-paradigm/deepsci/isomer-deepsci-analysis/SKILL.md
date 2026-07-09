---
name: isomer-deepsci-analysis
description: Use when a Research Inquiry or Research Task needs bounded follow-up evidence, ablations, robustness checks, failure analysis, or limitation analysis after a parent result already exists.
---

# Isomer Research Analysis

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: analysis revisions that refine the same concept update the existing Research Idea and add or refresh Idea Realizations with exact object-valued source paths. Create new Research Ideas and idea-level `follow_up_to`, `merged_from`, or `subsumes` edges only when the analysis introduces a new direction, split, merge, or return-to-ideation route; read `isomer-deepsci-shared/references/research-idea-recording.md` before such writes, and never use broad paths such as `$`, a section list, notes, metrics, or rendered Markdown for a Primary Idea source.

Analysis answers focused follow-up questions about an existing result. It decomposes a parent result into bounded evidence slices, records slice-level interpretations before campaign-level claims, and routes from the updated claim boundary.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

## When to Use

Use this skill when:

- A measured result, selected route, paper gap, reviewer item, or failure mode needs follow-up evidence.
- A claim needs ablation, robustness, sensitivity, qualitative, cost, efficiency, or boundary-case checks.
- The next route depends on whether a parent result survives a focused analysis slice.
- Writing-facing, review-facing, or rebuttal-facing evidence needs a bounded analysis plan rather than a new main run.

Do not use this skill when:

- No parent result, parent claim, paper gap, reviewer item, or route decision exists yet.
- The work is a new main experiment rather than follow-up evidence.
- The route question is still ideation or baseline recovery.
- The proposed slice cannot change, confirm, narrow, or block the parent claim boundary.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Lock the parent boundary**. Build <ANALYSIS_CONTEXT_BRIEF> from <PARENT_RESULT_EVIDENCE>, the parent result, parent claim, paper gap, reviewer item, route decision, or failure mode, then state the evidence question, stop condition, and immediate canonical parents for follow-up records. Read `references/campaign-design.md`, `references/boundary-cases.md`, `references/campaign-plan-template.md`, and `isomer-deepsci-shared/references/artifact-lineage-recording.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-analysis --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Audit the execution envelope**. Record <ANALYSIS_RESOURCE_ENVELOPE> with current device, memory, storage, wall-clock, dependency, credential, service, and concurrency limits when they affect slice design. Read `references/operational-guidance.md`, `references/campaign-design.md`, and `references/campaign-checklist-template.md`.
4. **Choose the smallest useful slice set**. Draft <ANALYSIS_CAMPAIGN_PLAN> and <ANALYSIS_SLICE_PLAN> with only slices that can change the parent claim, limitation, paper gap, reviewer answer, or next route. Read `references/campaign-design.md`, `references/boundary-cases.md`, and `references/writing-facing-slice-examples.md` when paper or review mapping matters.
5. **Gate resources and comparability**. Confirm each launched or deferred slice is runnable now, runnable with downscope, or blocked by resources, and confirm fixed conditions, comparison target, metric, observable, and non-comparability labels. Read `references/evidence-gate.md`, `references/campaign-checklist-template.md`, and `references/boundary-cases.md`.
6. **Run and record slices**. For every executed, failed, partial, infeasible, or superseded slice, produce <ANALYSIS_SLICE_RECORD> with `follow_up_to` lineage from the parent result, claim, or route decision before making campaign-level conclusions. Read `references/slice-record-template.md`, `references/artifact-flow-examples.md`, and `references/operational-guidance.md`.
7. **Interpret the campaign boundary**. Aggregate only decision-relevant slice evidence into <ANALYSIS_CAMPAIGN_SUMMARY> with `derived_from` lineage from the slice records, keeping stable support, contradiction, partial support, unresolved ambiguity, and skipped low-value slices separate. Read `references/evidence-gate.md`, `references/boundary-cases.md`, and `references/writing-facing-slice-examples.md` when write-back is required.
8. **Route from evidence**. Return <ANALYSIS_ROUTE_DECISION> or <ANALYSIS_BLOCKER_RECORD>, then preserve <ANALYSIS_CONTINUITY_UPDATE> and <ANALYSIS_WRITEBACK_MAP> with canonical lineage when the result changes future work, writing, review, or rebuttal state. If the route only revises an existing idea, update that Research Idea in place; if it creates a follow-up, split, merge, or return-to-ideation branch, record explicit idea lineage. Read `references/evidence-gate.md`, `references/artifact-flow-examples.md`, `references/operational-guidance.md`, and `isomer-deepsci-shared/references/research-idea-recording.md`.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-analysis --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer the lightest route that preserves trust and downstream utility (if one slice answers the question, otherwise use a larger campaign only when lineage, traceability, or multiple slices matter).
- Prefer claim-critical contradiction checks before broad supporting checks (if the claim boundary is already clear, otherwise stop widening).
- Prefer code-based and repeatable analysis when it is faithful to the evidence question (if qualitative inspection is more appropriate, otherwise record rubric, sample, prompt or inspection basis, and caveats).
- Prefer writing-facing metadata only when the slice supports a paper-like deliverable (if no selected outline exists yet, otherwise run pre-outline analysis and route to writing or decision afterward).

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- Every meaningful slice must map to a parent claim, parent result, paper gap, reviewer item, rebuttal item, or route decision.
- Campaign design must be conditioned on the current execution envelope, not an idealized future machine.
- Campaign-level interpretation must be derived from per-slice evidence rather than impressions.
- Null, negative, failed, partial, blocked, infeasible, superseded, and contradictory findings must remain visible.
- Same-factor comparability must be preserved unless the variation itself is the point.
- A writing-facing slice must be write-backable to an outline, paper matrix, evidence ledger, section, claim, table, reviewer item, or rebuttal item when it is called paper-ready.
- The campaign must not keep expanding after the next route is already clear.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Ready evidence group count: number of current ready paper-facing experiment or analysis groups mapped to the active paper line; higher is better until the active target range is reached.
- Reviewer-facing analysis job count: number of completed and mapped analysis jobs when a full empirical paper target names reviewer-facing analyses; closer to the active target is better.

### Checks

- Parent gate: <ANALYSIS_CONTEXT_BRIEF> names the parent object, parent claim or gap, evidence question, comparison target, and stop condition.
- Resource gate: <ANALYSIS_RESOURCE_ENVELOPE> screens slices as runnable now, runnable with downscope, or blocked by resources when execution constraints matter.
- Slice gate: each <ANALYSIS_SLICE_RECORD> includes question, intervention or inspection target, fixed conditions, metric or observable, evidence source, claim update, comparability verdict, and next action.
- Comparability gate: direct-comparison claims preserve the baseline or main comparison contract, and non-comparable slices are labeled.
- Interpretation gate: <ANALYSIS_CAMPAIGN_SUMMARY> separates stable support, contradiction, partial support, and unresolved ambiguity.
- Route gate: <ANALYSIS_ROUTE_DECISION> or <ANALYSIS_BLOCKER_RECORD> names continue analysis, return to experiment, return to idea, write, decide, stop, reset, or blocker with the reason.

## Reference Routing

Read these pages as needed:

- `references/campaign-design.md` for campaign route choice, priority order, slice classes, and resource-aware design.
- `references/campaign-plan-template.md` for a durable route record when analysis is multi-slice, writing-facing, route-changing, expensive, unstable, or long-running.
- `references/campaign-checklist-template.md` for acceptance gates around frontier, resource, evidence, comparability, paper or review write-back, blockers, and closeout.
- `references/evidence-gate.md` for checking whether slice evidence is strong enough to update a claim or route.
- `references/slice-record-template.md` for recording one follow-up slice before campaign-level interpretation.
- `references/artifact-flow-examples.md` for evidence-flow examples covering one-slice, multi-slice, writing-facing, failed, infeasible, and read-only audit paths.
- `references/boundary-cases.md` for stage-boundary, comparability, qualitative evidence, one-slice, repeated-failure, pre-outline, extra-comparator, and interpretation-boundary cases.
- `references/writing-facing-slice-examples.md` for paper-ready slice metadata.
- `references/operational-guidance.md` for execution tactics, resource gates, memory use, evidence records, and connector-facing campaign visuals.

## Exit Criteria

This skill can end only when one of the following is durably true:

- The campaign produced enough evidence for writing or decision-making.
- The campaign exposed a problem that requires returning to experiment, idea, baseline recovery, or decision.
- The campaign is blocked and <ANALYSIS_BLOCKER_RECORD> names the next best action.
- The campaign route changed because the original slice set is no longer the best evidence-per-cost path.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
- Do not skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
