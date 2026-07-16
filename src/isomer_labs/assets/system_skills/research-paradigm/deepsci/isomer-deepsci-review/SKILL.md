---
name: isomer-deepsci-review
description: Use when a substantial draft, paper, report, or paper-like bundle needs an independent skeptical audit before finalization, rebuttal, or revision routing.
---

# Isomer Research Review

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: review findings should not mutate idea state implicitly. If review routes a concept to rejection, follow-up, merge, or supersession, read `isomer-deepsci-shared` and realize the Research Idea with an exact object-valued source path, not the review report, issue list, TODO list, or rendered Markdown.

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
- The user only wants line editing; use `isomer-deepsci-write` or `isomer-deepsci-nature-polishing`.
- The task is reviewer-response work after formal reviews; use `isomer-deepsci-rebuttal`.
- The manuscript blocker is already known and needs direct analysis or baseline recovery.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Plan the audit**. Produce `DEEPSCI:REVIEW-AUDIT-PLAN` with claim set, strongest and weakest evidence, likely rejection reasons, experiment/analysis inventory, comparator papers, language hygiene risks, and likely routes.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-review --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Run literature and benchmark checks**. Produce `DEEPSCI:LITERATURE-BENCHMARK-NOTE` from nearby strong papers, official venue expectations, existing literature notes, and verified sources when novelty or positioning is uncertain.
4. **Write the review report**. Produce `DEEPSCI:REVIEW-REPORT` using `references/review-report-template.md`, naming strengths, weaknesses, key issues, actionable suggestions, storyline advice, experiment inventory, novelty verification, comparison to strong papers, and canonical parents from the manuscript or paper bundle under review.
5. **Produce the revision log**. Produce `DEEPSCI:REVISION-LOG` using `references/revision-log-template.md`, turning review findings into concrete text, evidence, figure, analysis, baseline, literature, and decision items; link it with `follow_up_to` lineage from `DEEPSCI:REVIEW-REPORT`.
6. **Create evidence TODOs only when needed**. If real evidence is missing, produce `DEEPSCI:REVIEW-EXPERIMENT-TODO` with concrete follow-up work using `references/experiment-todo-template.md`; otherwise avoid fake experiments.
7. **Update paper experiment planning**. When experiment planning changes, produce `DEEPSCI:PAPER-EXPERIMENT-MATRIX-UPDATE` so writing and rebuttal-facing work remain aligned.
8. **Route the next step**. Produce `DEEPSCI:REVIEW-ROUTE-DECISION` to write, scout, baseline, analysis, decision, rebuttal, or finalize with evidence, priority ordering, and lineage to the review report or revision log that caused the route.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-review --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

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

- `DEEPSCI:REVIEW-REPORT` and `DEEPSCI:REVISION-LOG` exist for the reviewed draft.
- Any new evidence request appears in `DEEPSCI:REVIEW-EXPERIMENT-TODO` with concrete scope, or the report explains why no new evidence is needed.
- `DEEPSCI:REVIEW-ROUTE-DECISION` names the next responsible route.

## Guardrails

- DO NOT write no weaknesses without showing likely rejection routes.
- DO NOT turn manuscript blockers into fake experiments.
- DO NOT request new experiments before checking recorded evidence.
- DO NOT let review work perform follow-up experiments itself instead of routing to analysis.
- DO NOT review from author optimism rather than evidence.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
