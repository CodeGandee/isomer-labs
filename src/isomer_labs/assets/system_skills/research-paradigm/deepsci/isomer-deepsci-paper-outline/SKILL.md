---
name: isomer-deepsci-paper-outline
description: Use when evidence exists but the paper idea, outline, claim boundary, method abstraction, evaluation plan, analysis plan, or writing plan is not yet mature enough for drafting.
---

# Isomer Research Paper Outline

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Paper Outline separates the paper view from the evidence view. It builds the reader-facing thesis, claims, method abstraction, evaluation plan, and analysis plan while keeping runs, paths, metrics, commands, and reproducibility details in a separate evidence structure.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A Research Inquiry has results or evidence but lacks a mature paper-native outline.
- A section list, run log, or project chronology needs conversion into a reader-facing paper structure.
- Claims need explicit evidence and falsification boundaries before writing.
- A writing pass is blocked by weak thesis, weak method abstraction, missing analysis plan, or poor claim-evidence mapping.

Do not use this skill when:

- No meaningful evidence exists yet; route to scout, baseline, idea, experiment, or analysis first.
- The task is already a mature section rewrite; use `isomer-deepsci-write`.
- The user wants final review or rebuttal routing rather than outline repair.
- The outline would require unsupported claims or invented novelty.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Read paper state**. Build `<PAPER_STATE_SNAPSHOT>` from current outline, paper contract, evidence surfaces, run records, figures, reviewer needs, and user constraints.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-paper-outline --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Name the one-sentence idea**. Produce `<ONE_SENTENCE_PAPER_IDEA>` stating what readers should remember and why the result matters.
4. **Separate facts from interpretation**. Produce `<CLAIM_EVIDENCE_BOUNDARY>` that distinguishes measured facts, allowed interpretations, limitations, and unsupported claims.
5. **Build the paper view**. Draft `<PAPER_VIEW>` with thesis, story spine, scoped claims, method abstraction, evaluation plan, analysis plan, and target reader logic. Read `references/outline-patterns.md` when choosing outline structure.
6. **Build the evidence view**. Draft `<EVIDENCE_VIEW>` with runs, paths, metrics, settings, source data, figures, reproducibility details, and appendix-only support separated from manuscript story.
7. **Validate the outline**. Produce `<OUTLINE_VALIDATION_REPORT>` using claim support, falsification boundary, method clarity, evaluation coverage, analysis maturity, and reviewer-risk checks.
8. **Repair until mature or blocked**. If validation fails, revise the paper view, evidence view, or claim boundary. Stop with `<PAPER_OUTLINE_ROUTE_DECISION>` when missing evidence or a strategic decision blocks maturity.
9. **Compile writing plan**. When validation passes, produce `<SECTION_WRITING_PLAN>` for `isomer-deepsci-write`, including section jobs, required displays, citation needs, and evidence limits.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-paper-outline --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

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
- Routes to other research stages must use existing production DeepSci skill names when an Isomer counterpart exists.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Reviewer objection coverage: count of likely reviewer objections mapped to evidence, revision, claim downgrade, or accepted limitation; higher is better until the required objection set is covered.
- Paper-facing evidence group count: number of ready experiment or analysis groups planned for the paper line; higher is better until the active target range is reached.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-paper-outline.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/outline-patterns.md` for outline examples, paper-view/evidence-view patterns, and repair cues.

## Exit Criteria

This skill can end when all applicable checks are true:

- `<PAPER_VIEW>` and `<EVIDENCE_VIEW>` are both present and separated.
- `<OUTLINE_VALIDATION_REPORT>` either passes or names a concrete blocker.
- `<SECTION_WRITING_PLAN>` exists when the outline is ready for writing.

## Common Mistakes

- Copying run logs into the paper plan.
- Treating a section list as a mature outline.
- Leaving claims without evidence or falsification boundaries.
- Planning too little reviewer-facing analysis for an empirical paper.
- Inventing a paper story that the evidence cannot support.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
