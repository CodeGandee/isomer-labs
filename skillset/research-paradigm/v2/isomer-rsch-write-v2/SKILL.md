---
name: isomer-rsch-write-v2
description: Use when a Research Inquiry has enough evidence to draft or revise a paper, report, research summary, oral-style package, or manuscript section without inventing missing support.
---

# Isomer Research Write V2

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`, and request `--render markdown` only for the generated review view.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-rsch-shared-v2` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Write turns validated research evidence into paper-facing prose. It refreshes the paper contract, repairs weak outlines before drafting, separates claims from source material, plans displays before prose, and routes evidence gaps back to the skill that can fix them.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A Research Inquiry has a selected paper idea, outline, evidence ledger, experiment matrix, or paper contract ready for writing.
- The task is to draft, revise, or align manuscript sections, report text, oral-style paper structure, or paper bundle status.
- Figures, citations, experiments, and claims need to be kept synchronized while writing proceeds.
- A draft needs route-aware validation before review, analysis, or finalization.

Do not use this skill when:

- The paper idea, claim boundary, or evidence mapping is still immature; use `isomer-rsch-paper-outline-v2` first.
- The requested change requires new results rather than writing from existing evidence; route to `isomer-rsch-analysis-v2` or `isomer-rsch-experiment-v2`.
- The task is only first-pass plotting or final figure QA; use `isomer-rsch-paper-plot-v2` or `isomer-rsch-figure-polish-v2`.
- The user asks for polished claims that are not supported by evidence.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Refresh control state**. Build `<PAPER_CONTROL_STATE>` from the Research Topic, paper contract, current outline, evidence ledger, experiment matrix, figures, references, available runtime context and active draft surfaces. Read `references/experiments_analysis_patterns.md` when experiment organization affects the draft.
2. **Lock the paper contract**. Produce or update `<PAPER_CONTRACT>` with the central claim, venue or report target, evidence boundary, required figures, citation state, and bundle status. Use `references/oral_package_patterns.md` when the target is an oral-ready paper package.
3. **Validate the outline before drafting**. Check `<PAPER_OUTLINE>` for a real reader-facing thesis, scoped claims, method abstraction, evaluation plan, analysis plan, and evidence map. Route to `isomer-rsch-paper-outline-v2` when the outline cannot support writing.
4. **Compile the writing plan**. Turn a valid outline into `<WRITING_PLAN>` with section jobs, source inputs, claim limits, figure needs, citation needs, and draft-stop criteria. Read `references/oral_writing_principles.md` for reader-first ordering.
5. **Sort source material**. Create `<SOURCE_MATERIAL_LEDGER>` separating manuscript claims, experiment settings, reproducibility details, implementation details, artifact history, and appendix-only material. Keep local execution and route-control details out of manuscript prose.
6. **Refresh citations and references**. Create `<CITATION_LEDGER>` from verified sources before citing. Do not hand-write BibTeX, metrics, or literature claims from memory.
7. **Plan displays before prose**. Create `<DISPLAY_PLAN>` for figures, tables, and appendix displays. Route first-pass standard plots to `isomer-rsch-paper-plot-v2` and durable paper-facing figures to `isomer-rsch-figure-polish-v2`.
8. **Draft or revise sections**. Produce `<DRAFT_SECTION_SET>` from the section jobs, using `references/section_rewrite_checklist.md` before treating a section as stable.
9. **Validate the manuscript state**. Produce `<MANUSCRIPT_VALIDATION_REPORT>` covering claim support, citation legitimacy, figure readiness, section coverage, language hygiene, bundle readiness, and remaining blockers.
10. **Checkpoint or route next**. Submit `<PAPER_BUNDLE_CHECKPOINT>` when the draft, review package, or submission package is coherent; otherwise produce `<WRITING_ROUTE_DECISION>` to analysis, review, finalize, paper-outline, or a Nature companion skill as justified.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer durable evidence and explicit placeholders over concrete source paths until storage binding is finalized.
- Prefer the smallest route that preserves downstream trust, and route missing evidence to the skill that can actually produce it.
- Prefer source-compatible `isomer-cli ext deepsci call ... --input-json '{...}'` only when the source harness behavior matters; otherwise use native Isomer topic context, provider, and execution-adapter surfaces without binding storage prematurely.
- Prefer paper-facing language that names claims, evidence, limits, and next routes without exposing operator, agent, prompt, worktree, or local runtime details.
- Prefer Tectonic for LaTeX/TeX manuscript compilation. Use TeX Live, `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, or Biber only when Tectonic is unavailable, blocked by the template, or required by the venue, and record the fallback reason in the compile report.

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

- Ready evidence group count: number of ready paper-facing experiment or analysis groups supporting the active paper line; higher is better until the active target range is reached.
- Verified reference count: number of verified references in the active bibliography for a paper-like deliverable; higher is better until the scoped citation target is satisfied.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-write.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/oral_package_patterns.md` for oral-style paper package structure, evidence blocks, display program, appendix strategy, and objection handling.
- `references/oral_writing_principles.md` for reader-first narrative order, method defense, results organization, and figure-centered prose.
- `references/experiments_analysis_patterns.md` for experiment and analysis section separation, reviewer-facing question design, and table/figure roles.
- `references/section_rewrite_checklist.md` for section-level rewrite gates before bundling or review.
- `templates/` for passive upstream venue templates copied for audit and later storage-binding decisions.

## Exit Criteria

This skill can end when all applicable checks are true:

- `<DRAFT_SECTION_SET>` stays inside `<PAPER_CONTRACT>` and does not invent evidence.
- `<MANUSCRIPT_VALIDATION_REPORT>` records remaining gaps and the next route.
- `<PAPER_BUNDLE_CHECKPOINT>` exists for a coherent draft, review package, or submission package, or `<WRITING_ROUTE_DECISION>` names the blocker and responsible next skill.

## Common Mistakes

- Drafting around a weak outline instead of routing to paper-outline.
- Using polished prose to hide missing evidence.
- Writing citations, metrics, or method details from memory.
- Putting user, operator, agent, route-control, worktree, or local execution details into manuscript text.
- Planning figures after prose has already forced unsupported claims.
