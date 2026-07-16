---
name: isomer-deepsci-optimize
description: Use when algorithm-first research needs candidate briefs, frontier ranking, promotion, fusion, debug, plateau response, or route selection before or after measured runs.
---

# Isomer Research Optimize

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: invoke `$isomer-research-idea-recording` when optimization proposes durable concepts, promotes an option, fuses or splits concepts, follows up an idea, or changes exploration or evidence assessment. Record exact candidate-object realizations, one generation per sibling pass, the full option set for promotion decisions, terminal result refs, explicit transitions, and justified lineage. Frontier boards, debug notes, metrics, implementation attempts, and rendered Markdown are not Research Ideas by default.

Optimize manages an algorithm-first frontier one justified move at a time. It recovers current frontier state, chooses one submode for the pass, keeps candidate briefs distinct from durable lines and implementation attempts, and records exactly one next route or stop condition.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

## When to Use

Use this skill when:

- The research line is algorithm-first and needs frontier management.
- Candidate briefs must be shaped, ranked, promoted, fused, debugged, archived, or stopped.
- A measured result needs frontier review before another run.
- A plateau or repeated failure requires route review instead of more micro-edits.

Do not use this skill when:

- The task is broad ideation before an algorithm frontier exists.
- A single selected route is ready for experiment with no frontier decision needed.
- The work is baseline recovery, paper writing, or one already locked experiment.

## Workflow

When this skill is invoked, execute these steps in order.


1. **Recover the frontier**. Build DEEPSCI:OPTIMIZATION-CONTEXT-BRIEF, DEEPSCI:OPTIMIZATION-FRONTIER, DEEPSCI:CANDIDATE-BOARD, and DEEPSCI:OPTIMIZE-CHECKLIST from candidate briefs, active lines, measured results, failures, prior lessons, and current route. Read `references/operational-guidance.md`, `references/candidate-board-template.md`, `references/optimize-checklist-template.md`, and `references/frontier-review-template.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-optimize --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Choose one submode**. Select exactly one primary submode: brief, rank, seed, loop, fusion, debug, or stop. Use frontier state, plateau signals, failure class, and candidate slate quality, not momentum. Read `references/operational-guidance.md`, `references/frontier-review-template.md`, and `references/plateau-response-playbook.md`.
4. **Shape or rank candidates**. Create DEEPSCI:CANDIDATE-BRIEF, DEEPSCI:METHOD-BRIEF, or DEEPSCI:CANDIDATE-RANKING when the next route needs differentiated options or promotion-ready comparison, linking sibling candidates to the candidate board with one generation group. Read `references/brief-shaping-playbook.md`, `references/method-brief-template.md`, `references/candidate-ranking-template.md`, `references/prompt-patterns.md`, and `isomer-deepsci-shared`.
5. **Promote or prepare one line**. Record DEEPSCI:PROMOTED-OPTIMIZATION-LINE with `selected_from` lineage when a brief deserves durable line status, or create DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD with `derived_from` lineage for a within-line seed, loop, smoke, patch, or quick validation candidate. Read `references/operational-guidance.md`, `references/codegen-route-playbook.md`, and `references/candidate-board-template.md`.
6. **Handle debug, fusion, or plateau evidence**. Produce DEEPSCI:DEBUG-RESPONSE, DEEPSCI:FUSION-PLAN, DEEPSCI:PLATEAU-RESPONSE, or DEEPSCI:FRONTIER-REVIEW when a failure, complementary line, repeated non-improvement, or measured result changes the frontier; use `merged_from` for fusions and `follow_up_to` for plateau or debug responses. Read `references/debug-response-template.md`, `references/fusion-playbook.md`, `references/plateau-response-playbook.md`, and `references/frontier-review-template.md`.
7. **Record the lesson and route**. Write DEEPSCI:OPTIMIZATION-MEMORY-CARD only when a reusable success pattern, failure pattern, fusion lesson, or non-retry rule was learned, then return DEEPSCI:OPTIMIZE-ROUTE-DECISION or DEEPSCI:OPTIMIZE-BLOCKER-RECORD with canonical lineage to the frontier, attempt, result, or decision it follows. Read `references/optimization-memory-template.md`, `references/frontier-review-template.md`, and `references/operational-guidance.md`.
8. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-optimize --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer one primary optimize submode per pass (if new evidence changes the submode, otherwise record the route shift before continuing).
- Prefer mechanism-level distinctness over candidate volume (if a slate collapses into one familiar family, otherwise widen once before ranking).
- Prefer one atomic improvement per loop pass (if changes are tightly coupled or fusion is explicit, otherwise split them).
- Prefer targeted debug over broad rewrite (if the failure changes the mechanism, otherwise route back to brief or loop).
- Prefer stopping or route-changing when the frontier is saturated (if remaining moves are redundant or low value, otherwise record a non-retry rule).

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- Candidate briefs, durable optimization lines, implementation attempts, measured results, failures, and stopped routes must remain distinct.
- Candidate briefs must not be promoted automatically.
- Same-family slates should not fill the frontier unless one candidate clearly dominates.
- Measured runs belong to the experiment route; optimize should manage frontier decisions and then hand off when real execution is needed.
- Debug is bugfix-only and must not smuggle in a new performance-improvement mechanism.
- Fusion must not combine redundant or weak lines just because multiple lines exist.
- A pass must end with one durable next action, stop condition, blocker, or route decision.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Quick validation latency: expected time for seed or candidate checks in fast-validation mode; lower is better when the check still answers the target.
- Complementary line count: number of durable optimization lines with meaningful complementary strengths before fusion; higher is better until the fusion precondition is satisfied.

### Checks

- Frontier gate: DEEPSCI:OPTIMIZATION-FRONTIER separates candidate briefs, durable lines, implementation attempts, measured results, failures, blockers, and route recommendation.
- Submode gate: exactly one primary submode is selected with a reason.
- Brief gate: DEEPSCI:CANDIDATE-BRIEF or DEEPSCI:METHOD-BRIEF states bottleneck, mechanism, family, change layer, keep-unchanged contract, expected gain, risks, foundation, and next target.
- Ranking gate: DEEPSCI:CANDIDATE-RANKING compares serious candidates on one shared surface and states winner, non-winner handling, and promotion cap.
- Attempt gate: DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD records candidate id, parent line, strategy, mechanism family, change plan, validation step, status, and archive condition.
- Frontier-review gate: DEEPSCI:FRONTIER-REVIEW names strongest support, contradiction, unresolved risk, active submode, exact next action, and trigger for another review.
- Closeout gate: DEEPSCI:OPTIMIZE-ROUTE-DECISION or DEEPSCI:OPTIMIZE-BLOCKER-RECORD leaves later stages with no guesswork.

## Reference Routing

Read these pages as needed:

- `references/operational-guidance.md` for the full native optimize protocol: frontier recovery, submode selection, candidate, promotion, seed, loop, memory, evidence records, execution, codegen, debug, fusion, plateau, and completion.
- `references/brief-shaping-playbook.md` for turning fuzzy directions into differentiated, ranking-ready candidate briefs.
- `references/method-brief-template.md` for method brief fields.
- `references/candidate-board-template.md` for the compact candidate ledger.
- `references/candidate-ranking-template.md` for shared-surface ranking and promotion caps.
- `references/frontier-review-template.md` for route choice, active submode, and immediate next action.
- `references/optimize-checklist-template.md` for pass-level frontier tracking.
- `references/optimization-memory-template.md` for reusable success, failure, fusion, and non-retry lessons.
- `references/codegen-route-playbook.md` for brief-only, stepwise, diff/patch, or full-rewrite code-generation route choice.
- `references/debug-response-template.md` for concrete failure repair without scope creep.
- `references/fusion-playbook.md` for justified complementary-line fusion.
- `references/plateau-response-playbook.md` for route review after repeated non-improvement.
- `references/prompt-patterns.md` for stable optimization, plateau, fusion, and debug prompt contracts.

## Exit Criteria

This skill can end only when one of these states is durable:

- A stronger line was promoted and the next anchor is clear.
- The current line produced a measured result and the next frontier route is recorded.
- The frontier says stop and the stop decision is recorded.
- A blocker explains why frontier work cannot proceed responsibly.

Do not treat one candidate creation or one smoke pass as completion.

## Guardrails

- DO NOT continue after the route, gate, or blocker is already clear.
- DO NOT replace evidence requirements with optimistic prose.
- DO NOT bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.
- DO NOT skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
