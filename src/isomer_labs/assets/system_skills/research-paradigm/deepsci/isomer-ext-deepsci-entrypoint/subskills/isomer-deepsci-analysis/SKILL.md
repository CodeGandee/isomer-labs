---
name: isomer-deepsci-analysis
description: Use when a Research Inquiry or Research Task needs bounded follow-up evidence, ablations, robustness checks, failure analysis, or limitation analysis after a parent result already exists.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Research Analysis

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-ext-deepsci-entrypoint->shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-ext-deepsci-entrypoint->shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-ext-deepsci-entrypoint->shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: invoke `isomer-op-entrypoint->research-ideas` when accepted analysis changes a durable concept or its exploration or evidence assessment. Cite the accepted terminal result refs on explicit transitions; retain the existing Research Idea for concept-stable revisions and add an exact realization. Create a new idea and justified `follow_up_to`, `merged_from`, or `subsumes` edge only for a new direction, split, merge, or return-to-ideation route. Use the exact structured source object, never rendered Markdown, as the realization source.

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

1. **Lock the parent boundary**. Build DEEPSCI:ANALYSIS-CONTEXT-BRIEF from DEEPSCI:PARENT-RESULT-EVIDENCE, the parent result, parent claim, paper gap, reviewer item, route decision, or failure mode, then state the evidence question, stop condition, and immediate canonical parents for follow-up records. Read `references/campaign-design.md`, `references/boundary-cases.md`, `references/campaign-plan-template.md`, and `isomer-ext-deepsci-entrypoint->shared`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-analysis --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Audit the execution envelope**. Record DEEPSCI:ANALYSIS-RESOURCE-ENVELOPE with current device, memory, storage, wall-clock, dependency, credential, service, and concurrency limits when they affect slice design. Read `references/operational-guidance.md`, `references/campaign-design.md`, and `references/campaign-checklist-template.md`.
4. **Choose the smallest useful slice set**. Draft DEEPSCI:ANALYSIS-CAMPAIGN-PLAN and DEEPSCI:ANALYSIS-SLICE-PLAN with only slices that can change the parent claim, limitation, paper gap, reviewer answer, or next route. Read `references/campaign-design.md`, `references/boundary-cases.md`, and `references/writing-facing-slice-examples.md` when paper or review mapping matters.
5. **Gate resources and comparability**. Confirm each launched or deferred slice is runnable now, runnable with downscope, or blocked by resources, and confirm fixed conditions, comparison target, metric, observable, and non-comparability labels. Read `references/evidence-gate.md`, `references/campaign-checklist-template.md`, and `references/boundary-cases.md`.
6. **Run and record slices**. For every executed, failed, partial, infeasible, or superseded slice, produce DEEPSCI:ANALYSIS-SLICE-RECORD with `follow_up_to` lineage from the parent result, claim, or route decision before making campaign-level conclusions. Read `references/slice-record-template.md`, `references/artifact-flow-examples.md`, and `references/operational-guidance.md`.
7. **Interpret the campaign boundary**. Aggregate only decision-relevant slice evidence into DEEPSCI:ANALYSIS-CAMPAIGN-SUMMARY with `derived_from` lineage from the slice records, keeping stable support, contradiction, partial support, unresolved ambiguity, and skipped low-value slices separate. Read `references/evidence-gate.md`, `references/boundary-cases.md`, and `references/writing-facing-slice-examples.md` when write-back is required.
8. **Route from evidence**. Return DEEPSCI:ANALYSIS-ROUTE-DECISION or DEEPSCI:ANALYSIS-BLOCKER-RECORD, then preserve DEEPSCI:ANALYSIS-CONTINUITY-UPDATE and DEEPSCI:ANALYSIS-WRITEBACK-MAP with canonical lineage when the result changes future work, writing, review, or rebuttal state. If the route only revises an existing idea, update that Research Idea in place; if it creates a follow-up, split, merge, or return-to-ideation branch, record explicit idea lineage. Read `references/evidence-gate.md`, `references/artifact-flow-examples.md`, `references/operational-guidance.md`, and `isomer-ext-deepsci-entrypoint->shared`.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-analysis --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
10. **Close the operation set**. After end callbacks, invoke `isomer-ext-deepsci-entrypoint->shared`, follow its Operation Set Closeout reference, and invoke `isomer-op-entrypoint->operation-sets`. When material operation-set files exist, accept and verify every disposition, require a `complete` receipt, and return the receipt id with durable record refs; treat a path, rendered file, Git commit, or terminal prose as unavailable for handoff. When no operation set was opened and only durable records were used, return `closeout: not_applicable` with those refs. If closeout is partial, stale, or invalid, return `paused` with accepted refs, the partial receipt when present, diagnostics, and the exact resume command.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

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

- Parent gate: DEEPSCI:ANALYSIS-CONTEXT-BRIEF names the parent object, parent claim or gap, evidence question, comparison target, and stop condition.
- Resource gate: DEEPSCI:ANALYSIS-RESOURCE-ENVELOPE screens slices as runnable now, runnable with downscope, or blocked by resources when execution constraints matter.
- Slice gate: each DEEPSCI:ANALYSIS-SLICE-RECORD includes question, intervention or inspection target, fixed conditions, metric or observable, evidence source, claim update, comparability verdict, and next action.
- Comparability gate: direct-comparison claims preserve the baseline or main comparison contract, and non-comparable slices are labeled.
- Interpretation gate: DEEPSCI:ANALYSIS-CAMPAIGN-SUMMARY separates stable support, contradiction, partial support, and unresolved ambiguity.
- Route gate: DEEPSCI:ANALYSIS-ROUTE-DECISION or DEEPSCI:ANALYSIS-BLOCKER-RECORD names continue analysis, return to experiment, return to idea, write, decide, stop, reset, or blocker with the reason.

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
- The campaign is blocked and DEEPSCI:ANALYSIS-BLOCKER-RECORD names the next best action.
- The campaign route changed because the original slice set is no longer the best evidence-per-cost path.

## Guardrails

- DO NOT continue after the route, gate, or blocker is already clear.
- DO NOT replace evidence requirements with optimistic prose.
- DO NOT bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.
- DO NOT skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
