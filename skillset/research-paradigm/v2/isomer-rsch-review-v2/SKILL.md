---
name: isomer-rsch-review-v2
description: Use when a substantial draft, paper, report, or paper-like bundle needs an independent skeptical audit before finalization, rebuttal, or revision routing.
---

# Isomer Research Review V2

## Overview

Review audits from evidence rather than author optimism. It builds an audit plan, benchmarks nearby literature and venue expectations, writes a skeptical review report, turns issues into a revision log, creates experiment TODOs only for real evidence gaps, and routes the next step.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A substantial manuscript, report, review package, or submission bundle exists.
- The user needs weaknesses, likely rejection routes, novelty or comparator checks, and actionable fixes.
- A draft needs routing to writing, scout, baseline, analysis, decision, rebuttal, or finalize work.
- Review needs to separate text fixes from evidence gaps.

Do not use this skill when:

- There is no substantial draft or paper-like object to review.
- The user only wants line editing; use `isomer-rsch-write-v2` or `isomer-rsch-nature-polishing-v2`.
- The task is reviewer-response work after formal reviews; use `isomer-rsch-rebuttal-v2`.
- The manuscript blocker is already known and needs direct analysis or baseline recovery.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Plan the audit**. Produce `<REVIEW_AUDIT_PLAN>` with claim set, strongest and weakest evidence, likely rejection reasons, experiment/analysis inventory, comparator papers, language hygiene risks, and likely routes.
2. **Run literature and benchmark checks**. Produce `<LITERATURE_BENCHMARK_NOTE>` from nearby strong papers, official venue expectations, existing literature notes, and verified sources when novelty or positioning is uncertain.
3. **Write the review report**. Produce `<REVIEW_REPORT>` using `references/review-report-template.md`, naming strengths, weaknesses, key issues, actionable suggestions, storyline advice, experiment inventory, novelty verification, and comparison to strong papers.
4. **Produce the revision log**. Produce `<REVISION_LOG>` using `references/revision-log-template.md`, turning review findings into concrete text, evidence, figure, analysis, baseline, literature, and decision items.
5. **Create evidence TODOs only when needed**. If real evidence is missing, produce `<REVIEW_EXPERIMENT_TODO>` with concrete follow-up work using `references/experiment-todo-template.md`; otherwise avoid fake experiments.
6. **Update paper experiment planning**. When experiment planning changes, produce `<PAPER_EXPERIMENT_MATRIX_UPDATE>` so writing and rebuttal-facing work remain aligned.
7. **Route the next step**. Produce `<REVIEW_ROUTE_DECISION>` to write, scout, baseline, analysis, decision, rebuttal, or finalize with evidence and priority ordering.

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

- Real ready evidence count: number of non-duplicate, non-stale ready experiment or analysis groups that support the active paper line; higher is better until the current target is reached.
- Verified reference coverage: count of verified references compared with nearby strong papers and venue expectations; higher is better until citation sufficiency is justified.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-review.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/review-report-template.md` for skeptical review report structure.
- `references/revision-log-template.md` for issue-to-fix revision log.
- `references/experiment-todo-template.md` for follow-up evidence TODOs when real evidence is missing.

## Exit Criteria

This skill can end when all applicable checks are true:

- `<REVIEW_REPORT>` and `<REVISION_LOG>` exist for the reviewed draft.
- Any new evidence request appears in `<REVIEW_EXPERIMENT_TODO>` with concrete scope, or the report explains why no new evidence is needed.
- `<REVIEW_ROUTE_DECISION>` names the next responsible route.

## Common Mistakes

- Writing no weaknesses without showing likely rejection routes.
- Turning manuscript blockers into fake experiments.
- Requesting new experiments before checking recorded evidence.
- Letting review work perform follow-up experiments itself instead of routing to analysis.
- Reviewing from author optimism rather than evidence.
