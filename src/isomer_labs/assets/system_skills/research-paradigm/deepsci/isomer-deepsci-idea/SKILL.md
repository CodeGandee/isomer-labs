---
name: isomer-deepsci-idea
description: Use when a framed Research Topic and comparator basis need one falsifiable hypothesis, route, or algorithm-first brief before experiment or optimization work.
---

# Isomer Research Idea

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: before raw slates, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected/deferred ideas, route decisions, or paper-facing idea seeds are accepted, follow `isomer-deepsci-shared` Research Idea Recording. Use `isomer-cli --print-json ext research ideas upsert`, `realize --source-json-path <exact-object-path>`, `lineage add`, and `generation upsert` so Research Ideas, Primary Idea visibility, Idea Realizations, sibling groups, `selected_from`, `merged_from`, `follow_up_to`, and `subsumes` edges are canonical instead of inferred from Markdown or extracted record facets.

Idea selects a research direction by grounding the objective, current board, literature, bottleneck, and candidate frontier. It promotes one falsifiable route to experiment, records a blocker, or hands an algorithm-first frontier to optimize.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

## When to Use

Use this skill when:

- The Research Topic has a clear enough frame, comparator basis, dataset, metric, and code surface to choose a direction.
- The current route is stale, weak, contradicted, or exhausted and needs re-ideation.
- Literature, local evidence, or prior failed attempts must shape the next hypothesis.
- A bounded candidate frontier needs selection before experiment or optimization work.

Do not use this skill when:

- The frame, dataset, metric, or comparator gate is still unresolved and scout or baseline should run first.
- The current board state is too stale or conflicting to say what the mainline is.
- A selected route is already experiment-ready.
- The task is only within-family method-brief ranking or branch management, which should route to optimize.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check readiness and recover context**. Confirm the Research Topic has an accepted comparator basis, metric contract, relevant code path, and searchable evidence surface. Read `references/objective-contract-template.md`, `references/current-board-packet-template.md`, and `references/selection-gate.md` for the readiness gates. If the gate is not met, create <IDEA_BLOCKER_RECORD> and <IDEA_ROUTE_DECISION> instead of widening the frontier.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-idea --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Lock the objective and board**. Create or refresh <OBJECTIVE_CONTRACT> and <CURRENT_BOARD_PACKET>. Read `references/objective-contract-template.md` for target, proxy, false-progress, and constraint rules, and read `references/current-board-packet-template.md` for incumbent, blocker, stale-route, and budget-class rules.
4. **Plan and refresh evidence**. Reuse Workspace Runtime records before opening new discovery, then produce <LITERATURE_SURVEY_REPORT> and <RELATED_WORK_MAP>. Read `references/literature-survey-template.md`, `references/related-work-playbook.md`, and `references/research-history-playbook.md` before judging novelty or value.
5. **Extract the limitation and mechanism frame**. Produce <LIMITATIONS_MAP> and <MECHANISM_FRAMING> from the survey, board packet, current codebase, and comparator evidence. Read `references/high-value-idea-sourcing.md`, `references/idea-thinking-flow.md`, and `references/research-outline-template.md` before proposing mechanisms.
6. **Generate a bounded frontier**. Run one deliberate divergence pass unless durable evidence already makes the route obvious. Produce <RAW_IDEA_SLATE>, <CANDIDATE_IDEA_FRONTIER>, and <REJECTED_AND_DEFERRED_IDEAS> with canonical parents from objective, board, survey, and mechanism records; use one generation group when sibling candidates share the same parent set. Read `references/controlled-brainstorming-playbook.md`, `references/idea-generation-playbook.md`, `isomer-deepsci-shared/references/artifact-lineage-recording.md`, and `isomer-deepsci-shared/references/research-idea-recording.md` before narrowing.
7. **Record canonical raw and candidate ideas**. Upsert each durable raw idea and serious candidate as a Research Idea with semantic `idea_id`, `visibility=primary` only for top-level map items, aliases for source labels, and status for raw, candidate, rejected, or deferred state. Realize those ideas to <RAW_IDEA_SLATE>, <CANDIDATE_IDEA_FRONTIER>, and <REJECTED_AND_DEFERRED_IDEAS> with exact object-valued paths such as `$.sections.raw_ideas[0]`, never `$`, a collection, filter notes, route context, or rendered Markdown. Then record sibling generation groups and any explicit `merged_from`, `selected_from`, `alternative_to`, or `subsumes` idea edges.
8. **Challenge serious candidates**. Write or refresh <PRE_IDEA_DRAFT> for the top serious candidates before formal promotion, linking each draft with `derived_from` or `selected_from` to the candidate frontier and evidence it challenges. Realize the same candidate Research Ideas rather than creating new ideas for ordinary draft revisions. Read `references/pre-idea-draft-template.md` and keep hidden assumptions, local-optimum risk, strongest rejection case, and cheapest falsification path explicit.
9. **Select, branch, reject, or block**. Apply the selection gate, create <SELECTED_HYPOTHESIS> and <SELECTED_IDEA_DRAFT> with `selected_from` lineage from the chosen drafts and <IDEA_ROUTE_DECISION>, or create <IDEA_BLOCKER_RECORD> when no route is ready. Update selected, rejected, or deferred Research Idea status explicitly; record `subsumes` when the selected idea covers another candidate as an ablation, mechanism subset, or test role. Read `references/selection-gate.md` and `references/selected-hypothesis-template.md` for scoring, novelty labels, handoff fields, citations, and routing.
10. **Record durable outcomes and route next**. Preserve <IDEA_ROUTE_DECISION>, <IDEA_MEMORY_RECORD>, and, when the line is paper-facing, <PAPER_OUTLINE_SEED> or <RESEARCH_OUTLINE_NOTE> with `follow_up_to`, `derived_from`, or record-level `revision_of` lineage as appropriate. If the route introduces a new research direction, create an explicit follow-up Research Idea and idea lineage edge; if it only revises an existing direction, update the existing Research Idea and add a realization. Read `references/literature-survey-template.md`, `references/outline-seeding-example.md`, and `references/research-outline-template.md` before exiting.
11. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-idea --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/objective-contract-template.md` for target, proxy, false-progress, and constraint rules.
- `references/current-board-packet-template.md` for incumbent, blocker, stale-route, and budget-class context.
- `references/selection-gate.md` for scoring, novelty labels, handoff fields, citations, and routing.
- `references/literature-survey-template.md`, `references/related-work-playbook.md`, and `references/research-history-playbook.md` for evidence refresh and novelty checks.
- `references/high-value-idea-sourcing.md`, `references/idea-thinking-flow.md`, and `references/idea-generation-playbook.md` for bounded candidate generation.
- `isomer-deepsci-shared/references/research-idea-recording.md` for canonical Research Ideas, Primary Idea visibility, Idea Realizations, idea generation groups, `subsumes`, and idea lineage edges.
- `references/pre-idea-draft-template.md`, `references/selected-hypothesis-template.md`, `references/outline-seeding-example.md`, and `references/research-outline-template.md` for promotion, paper-facing seeding, and final handoff shape.

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- The accepted dataset, metric, and evaluation contract must stay fixed unless the Research Topic scope explicitly changed.
- The skill must not propose routes that depend on submit-time unavailable features, leakage-prone labels, or post-hoc information.
- Serious ideation must not start from memory, taste, or implementation convenience alone; it must use durable local evidence and literature coverage or record why the existing survey is sufficient.
- The skill should inspect code and papers during ideation but should avoid substantial implementation changes.
- A selected route must remain automatable with accepted metrics; subjective or human-only validation is not enough.
- The skill must not exit with a selected route when the survey, novelty or value verdict, falsification path, or handoff contract is still hand-wavy.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Usable literature coverage: count of directly usable or mechanism-relevant papers grounding a paper-ready idea package; higher is better until the active survey floor is satisfied.
- Ideation lens diversity: count of distinct relevant ideation lenses used before convergence; higher is better until the required diversity floor is satisfied.

### Checks

- Evidence coverage: <LITERATURE_SURVEY_REPORT> identifies reused evidence, new evidence, unresolved gaps, and closest prior work before selection.
- Candidate diversity: <CANDIDATE_IDEA_FRONTIER> contains meaningfully different route families unless durable evidence justifies a single route.
- Challenge coverage: every serious surviving candidate has a <PRE_IDEA_DRAFT> or equivalent challenge memo before promotion.
- Selection integrity: <SELECTED_HYPOTHESIS> includes a falsifiable claim, mechanism sketch, anti-win condition, minimal validation, abandonment condition, and next route.
- Outcome durability: <IDEA_ROUTE_DECISION>, <IDEA_MEMORY_RECORD>, and rejected or deferred rationale are explicit enough that later production DeepSci skills do not need to infer what changed.

## Exit Criteria

This skill can end only when one of these is durably true:

- One falsifiable idea is selected and ready for experiment.
- An algorithm-first frontier is shaped and routed to optimize.
- Several ideas are retained with an explicit branch or decision record.
- The current line is rejected and routed back to scout, baseline, or decision.
- The stage is blocked and the missing evidence, unresolved gate, or user-sensitive tradeoff is recorded in <IDEA_BLOCKER_RECORD>.

## Guardrails

- DO NOT continue after the route, gate, or blocker is already clear.
- DO NOT replace evidence requirements with optimistic prose.
- DO NOT treat a small implementable tweak as a strong idea unless literature and local evidence show it is the highest-value surviving route.
- DO NOT skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
- DO NOT bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
