---
name: isomer-deepsci-write
description: Use when a Research Inquiry has enough evidence to draft or revise a paper, report, research summary, oral-style package, or manuscript section without inventing missing support.
---

# Isomer Research Write

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: writing normally realizes papers and claims, not new ideas. If writing changes the accepted research concept, creates a follow-up idea, or marks an idea superseded, read `isomer-deepsci-shared` and realize the Research Idea with an exact object-valued source path, not a section draft, outline, claim ledger, or rendered Markdown.

Write turns validated research evidence into paper-facing prose. It refreshes the paper contract, repairs weak outlines before drafting, separates claims from source material, plans displays before prose, and routes evidence gaps back to the skill that can fix them.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A Research Inquiry has a selected paper idea, outline, evidence ledger, experiment matrix, or paper contract ready for writing.
- The task is to draft, revise, or align manuscript sections, report text, oral-style paper structure, or paper bundle status.
- Figures, citations, experiments, and claims need to be kept synchronized while writing proceeds.
- A draft needs route-aware validation before review, analysis, or finalization.

Do not use this skill when:

- The paper idea, claim boundary, or evidence mapping is still immature; use `isomer-deepsci-paper-outline` first.
- The requested change requires new results rather than writing from existing evidence; route to `isomer-deepsci-analysis` or `isomer-deepsci-experiment`.
- The task is only first-pass plotting or final figure QA; use `isomer-deepsci-paper-plot` or `isomer-deepsci-figure-polish`.
- The user asks for polished claims that are not supported by evidence.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Refresh control state**. Build `DEEPSCI:PAPER-CONTROL-STATE` from the Research Topic, paper contract, current outline, evidence ledger, experiment matrix, figures, references, available runtime context and active draft surfaces. Read `references/experiments_analysis_patterns.md` when experiment organization affects the draft.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-write --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Lock the paper contract**. Produce or update `DEEPSCI:PAPER-CONTRACT` with the central claim, venue or report target, evidence boundary, required figures, citation state, bundle status, and canonical parents from selected hypothesis, evidence ledger, or route decision. Use `references/oral_package_patterns.md` and `isomer-deepsci-shared` when the target is an oral-ready paper package.
4. **Validate the outline before drafting**. Check `DEEPSCI:PAPER-OUTLINE` for a real reader-facing thesis, scoped claims, method abstraction, evaluation plan, analysis plan, and evidence map. Route to `isomer-deepsci-paper-outline` when the outline cannot support writing.
5. **Compile the writing plan**. Turn a valid outline into `DEEPSCI:WRITING-PLAN` with section jobs, source inputs, claim limits, figure needs, citation needs, and draft-stop criteria. Read `references/oral_writing_principles.md` for reader-first ordering.
6. **Sort source material**. Create `DEEPSCI:SOURCE-MATERIAL-LEDGER` separating manuscript claims, experiment settings, reproducibility details, implementation details, artifact history, and appendix-only material. Keep local execution and route-control details out of manuscript prose.
7. **Refresh citations and references**. Create `DEEPSCI:CITATION-LEDGER` from verified sources before citing. Do not hand-write BibTeX, metrics, or literature claims from memory.
8. **Plan displays before prose**. Create `DEEPSCI:DISPLAY-PLAN` for figures, tables, and appendix displays. Route first-pass standard plots to `isomer-deepsci-paper-plot` and durable paper-facing figures to `isomer-deepsci-figure-polish`.
9. **Draft or revise sections**. Produce `DEEPSCI:DRAFT-SECTION-SET` from the section jobs with `derived_from` lineage from the writing plan and source ledger; use `ext research records revise <record-id>` with `revision_of` for content-changing accepted section revisions. Read `references/section_rewrite_checklist.md` before treating a section as stable.
10. **Validate the manuscript state**. Produce `DEEPSCI:MANUSCRIPT-VALIDATION-REPORT` covering claim support, citation legitimacy, figure readiness, section coverage, language hygiene, bundle readiness, and remaining blockers. For LaTeX/TeX manuscripts, validate compilation with Tectonic first; use LaTeX engine workflows only after a real Tectonic attempt fails or a concrete Tectonic blocker is recorded.
11. **Checkpoint or route next**. Submit `DEEPSCI:PAPER-BUNDLE-CHECKPOINT` when the draft, review package, or submission package is coherent; otherwise produce `DEEPSCI:WRITING-ROUTE-DECISION` to analysis, review, finalize, paper-outline, or a Nature companion skill as justified, linking the checkpoint or route decision to the manuscript state it follows.
12. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-write --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer durable evidence and explicit placeholders over concrete source paths until storage binding is finalized.
- Prefer the smallest route that preserves downstream trust, and route missing evidence to the skill that can actually produce it.
- Prefer source-compatible `isomer-cli ext deepsci call ... --input-json '{...}'` only when the source harness behavior matters; otherwise use native Isomer topic context, provider, and execution-adapter surfaces without binding storage prematurely.
- Prefer paper-facing language that names claims, evidence, limits, and next routes without exposing operator, agent, prompt, worktree, or local runtime details.
- Prefer Tectonic first for LaTeX/TeX manuscript compilation. Do not skip directly to TeX Live, `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, or Biber unless Tectonic was attempted and failed, Tectonic is unavailable, the template blocks Tectonic, or the venue requires a specific LaTeX engine or bibliography workflow. Record the Tectonic command or the concrete blocker, then record any fallback command and reason in the compile report.

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

- Ready evidence group count: number of ready paper-facing experiment or analysis groups supporting the active paper line; higher is better until the active target range is reached.
- Verified reference count: number of verified references in the active bibliography for a paper-like deliverable; higher is better until the scoped citation target is satisfied.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-write.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.
- Compile-order check: for LaTeX/TeX manuscripts, the compile report records a Tectonic attempt or a concrete Tectonic blocker before any LaTeX engine fallback.

## Reference Routing

Read these pages as needed:

- `references/oral_package_patterns.md` for oral-style paper package structure, evidence blocks, display program, appendix strategy, and objection handling.
- `references/oral_writing_principles.md` for reader-first narrative order, method defense, results organization, and figure-centered prose.
- `references/experiments_analysis_patterns.md` for experiment and analysis section separation, reviewer-facing question design, and table/figure roles.
- `references/section_rewrite_checklist.md` for section-level rewrite gates before bundling or review.
- `templates/` for passive upstream venue templates copied for audit and later storage-binding decisions.

## Exit Criteria

This skill can end when all applicable checks are true:

- `DEEPSCI:DRAFT-SECTION-SET` stays inside `DEEPSCI:PAPER-CONTRACT` and does not invent evidence.
- `DEEPSCI:MANUSCRIPT-VALIDATION-REPORT` records remaining gaps and the next route.
- `DEEPSCI:PAPER-BUNDLE-CHECKPOINT` exists for a coherent draft, review package, or submission package, or `DEEPSCI:WRITING-ROUTE-DECISION` names the blocker and responsible next skill.

## Guardrails

- DO NOT draft around a weak outline instead of routing to paper-outline.
- DO NOT use polished prose to hide missing evidence.
- DO NOT write citations, metrics, or method details from memory.
- DO NOT put user, operator, agent, route-control, worktree, or local execution details into manuscript text.
- DO NOT plan figures after prose has already forced unsupported claims.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
