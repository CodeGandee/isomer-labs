---
name: isomer-rsch-rebuttal-v2
description: Use when reviewer feedback must be normalized into manuscript deltas, evidence work, experiments, limitations, and a durable rebuttal or revision response.
---

# Isomer Research Rebuttal V2

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`, and request `--render markdown` only for the generated review view.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-rsch-shared-v2` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-rsch-shared-v2` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Rebuttal turns reviewer pressure into auditable work items. It preserves reviewer meaning, assigns stable item ids, classifies each issue, routes real evidence gaps to the right skill, records text deltas, and assembles a point-by-point response only after critical feasible rows are resolved or explicitly limited.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- Formal reviews, reviewer comments, meta-review, editorial feedback, or revision instructions exist.
- The task is to decide what changes are required and draft a response letter.
- Reviewer items need routing to literature, baseline, analysis, writing, limitation, or explanation-only work.
- Evidence updates and manuscript deltas must stay tied to reviewer item ids.

Do not use this skill when:

- The task is pre-submission manuscript review; use `isomer-rsch-review-v2`.
- The user only wants general polishing without reviewer items.
- Reviewer comments are unavailable or too vague to normalize.
- The response would require claiming completed experiments or fixes that have not been done.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Normalize the review package**. Produce `<REVIEW_PACKAGE_NORMALIZATION>` and `<REVIEWER_ITEM_MATRIX>` from reviewer text, keeping source-faithful wording, stable item ids, class, severity, affected claim, evidence anchor, and route. Use `references/review-matrix-template.md`.
2. **Decide required changes**. Produce `<REBUTTAL_ACTION_PLAN>` using `references/action-plan-template.md`, classifying each item as explanation, text edit, evidence repackaging, new analysis, baseline recovery, literature positioning, limitation, claim downgrade, or manuscript rewrite.
3. **Route evidence work only when needed**. For novelty or positioning route to scout, for comparator gaps route to baseline, and for reviewer-linked evidence route to analysis. Record `<REVIEWER_LINKED_EVIDENCE_TODO>` only when it answers named reviewer ids.
4. **Route manuscript changes explicitly**. Route structure, claim-scope, and wording changes to write, and record `<MANUSCRIPT_TEXT_DELTA>` for each changed claim, section, caption, or limitation.
5. **Update the rebuttal matrix**. After each routed fix, produce `<REBUTTAL_EVIDENCE_UPDATE>` using `references/evidence-update-template.md`, keeping status, evidence, text delta, limitation, and unresolved risk tied to item ids.
6. **Assemble the response letter**. Draft `<RESPONSE_LETTER_DRAFT>` using `references/response-letter-template.md`, with respectful point-by-point answers, evidence basis, manuscript deltas, and explicit limitations.
7. **Prepare final revision handoff**. Produce `<REVISION_HANDOFF_BUNDLE>` with response letter, text deltas, evidence updates, unresolved limitations, and route decision for finalization or continued work.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer durable evidence and explicit placeholders over concrete source paths until storage binding is finalized.
- Prefer the smallest route that preserves downstream trust, and route missing evidence to the skill that can actually produce it.
- Prefer source-compatible `isomer-cli ext deepsci call ... --input-json '{...}'` only when the source harness behavior matters; otherwise use native Isomer topic context, provider, and execution-adapter surfaces without binding storage prematurely.
- Prefer paper-facing language that names claims, evidence, limits, and next routes without exposing operator, agent, prompt, worktree, or local runtime details.

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- Every paper-facing claim must stay inside the current evidence boundary.
- Every placeholder used by runtime instructions must be listed in `migrate/placeholders.md`.
- Concrete source paths, source harness outputs, and source storage assumptions must not become final Isomer storage contracts.
- Routes to other research stages must use existing v2 skill names when an Isomer counterpart exists.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Reviewer-item resolution coverage: fraction of serious reviewer items with a stable id, action class, route, evidence or text delta, and response status; higher is better.
- Feasible critical-row blocker count: number of reviewer-critical and currently feasible experiment, analysis, or manuscript matrix rows still unresolved before package handoff; lower is better.

### Checks

- Review-matrix check: <REVIEWER_ITEM_MATRIX> preserves reviewer wording faithfully and gives each substantive item a stable id, class, severity, effect, evidence anchor, and preliminary route.
- Action-plan check: <REBUTTAL_ACTION_PLAN> records stance, route, sufficiency reason, existing evidence, missing work, and for experimental items a hypothesis, required metrics, minimal plan, enhanced plan, and fallback response.
- Experiment-routing check: supplementary runs are launched only for named reviewer concerns and link back to reviewer ids and paper experiment matrix ids when those ids exist.
- Text-delta check: <MANUSCRIPT_TEXT_DELTA> identifies section, old claim or weakness, new wording or scope, and evidence basis for manuscript changes.
- Response-honesty check: <RESPONSE_LETTER_DRAFT> is evidence-backed, calm, specific, and explicit about limitations or infeasible requests instead of promising unsupported work.
- Handoff check: <REVISION_HANDOFF_BUNDLE> covers overall response, reviewer-specific replies, revision strategy, evidence mapping, unresolved risks, and next route.

## Reference Routing

Read these pages as needed:

- `references/review-matrix-template.md` for stable reviewer item matrix.
- `references/action-plan-template.md` for required-change action plan.
- `references/evidence-update-template.md` for reviewer-linked evidence update.
- `references/response-letter-template.md` for point-by-point response letter.

## Exit Criteria

This skill can end when all applicable checks are true:

- Every reviewer-critical feasible matrix row is resolved, routed, or explicitly limited.
- `<RESPONSE_LETTER_DRAFT>` cites the evidence or text delta for each response.
- `<REVISION_HANDOFF_BUNDLE>` records remaining risks and final route.

## Common Mistakes

- Launching free-floating ablations that do not answer reviewer item ids.
- Rewriting reviewer meaning during normalization.
- Pretending limitations are solved when they are only reframed.
- Finalizing while reviewer-critical feasible rows remain unresolved.
- Writing a response before evidence and text deltas are clear.
