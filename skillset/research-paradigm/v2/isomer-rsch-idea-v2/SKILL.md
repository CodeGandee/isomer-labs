---
name: isomer-rsch-idea-v2
description: Use when a framed Research Topic and comparator basis need one falsifiable hypothesis, route, or algorithm-first brief before experiment or optimization work.
---

# Isomer Research Idea V2

## Overview

Idea selects a research direction by grounding the objective, current board, literature, bottleneck, and candidate frontier. It promotes one falsifiable route to experiment, records a blocker, or hands an algorithm-first frontier to optimize.

Placeholder definitions live in `migrate/placeholders.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

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
2. **Lock the objective and board**. Create or refresh <OBJECTIVE_CONTRACT> and <CURRENT_BOARD_PACKET>. Read `references/objective-contract-template.md` for target, proxy, false-progress, and constraint rules, and read `references/current-board-packet-template.md` for incumbent, blocker, stale-route, and budget-class rules.
3. **Plan and refresh evidence**. Reuse Workspace Runtime records before opening new discovery, then produce <LITERATURE_SURVEY_REPORT> and <RELATED_WORK_MAP>. Read `references/literature-survey-template.md`, `references/related-work-playbook.md`, and `references/research-history-playbook.md` before judging novelty or value.
4. **Extract the limitation and mechanism frame**. Produce <LIMITATIONS_MAP> and <MECHANISM_FRAMING> from the survey, board packet, current codebase, and comparator evidence. Read `references/high-value-idea-sourcing.md`, `references/idea-thinking-flow.md`, and `references/research-outline-template.md` before proposing mechanisms.
5. **Generate a bounded frontier**. Run one deliberate divergence pass unless durable evidence already makes the route obvious. Produce <RAW_IDEA_SLATE>, <CANDIDATE_IDEA_FRONTIER>, and <REJECTED_AND_DEFERRED_IDEAS>. Read `references/controlled-brainstorming-playbook.md` and `references/idea-generation-playbook.md` before narrowing.
6. **Challenge serious candidates**. Write or refresh <PRE_IDEA_DRAFT> for the top serious candidates before formal promotion. Read `references/pre-idea-draft-template.md` and keep hidden assumptions, local-optimum risk, strongest rejection case, and cheapest falsification path explicit.
7. **Select, branch, reject, or block**. Apply the selection gate, create <SELECTED_HYPOTHESIS> and <SELECTED_IDEA_DRAFT> when one route passes, or create <IDEA_BLOCKER_RECORD> when no route is ready. Read `references/selection-gate.md` and `references/selected-hypothesis-template.md` for scoring, novelty labels, handoff fields, citations, and routing.
8. **Record durable outcomes and route next**. Preserve <IDEA_ROUTE_DECISION>, <IDEA_MEMORY_RECORD>, and, when the line is paper-facing, <PAPER_OUTLINE_SEED> or <RESEARCH_OUTLINE_NOTE>. Read `references/literature-survey-template.md`, `references/outline-seeding-example.md`, and `references/research-outline-template.md` before exiting.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/objective-contract-template.md` for target, proxy, false-progress, and constraint rules.
- `references/current-board-packet-template.md` for incumbent, blocker, stale-route, and budget-class context.
- `references/selection-gate.md` for scoring, novelty labels, handoff fields, citations, and routing.
- `references/literature-survey-template.md`, `references/related-work-playbook.md`, and `references/research-history-playbook.md` for evidence refresh and novelty checks.
- `references/high-value-idea-sourcing.md`, `references/idea-thinking-flow.md`, and `references/idea-generation-playbook.md` for bounded candidate generation.
- `references/pre-idea-draft-template.md`, `references/selected-hypothesis-template.md`, `references/outline-seeding-example.md`, and `references/research-outline-template.md` for promotion, paper-facing seeding, and final handoff shape.

## Cross-Step Constraints

- The accepted dataset, metric, and evaluation contract must stay fixed unless the Research Topic scope explicitly changed.
- The skill must not propose routes that depend on submit-time unavailable features, leakage-prone labels, or post-hoc information.
- Serious ideation must not start from memory, taste, or implementation convenience alone; it must use durable local evidence and literature coverage or record why the existing survey is sufficient.
- The skill should inspect code and papers during ideation but should avoid substantial implementation changes.
- A selected route must remain automatable with accepted metrics; subjective or human-only validation is not enough.
- The skill must not exit with a selected route when the survey, novelty or value verdict, falsification path, or handoff contract is still hand-wavy.

## Cross-Step Quality Gates

- Evidence coverage: <LITERATURE_SURVEY_REPORT> identifies reused evidence, new evidence, unresolved gaps, and closest prior work before selection.
- Candidate diversity: <CANDIDATE_IDEA_FRONTIER> contains meaningfully different route families unless durable evidence justifies a single route.
- Challenge coverage: every serious surviving candidate has a <PRE_IDEA_DRAFT> or equivalent challenge memo before promotion.
- Selection integrity: <SELECTED_HYPOTHESIS> includes a falsifiable claim, mechanism sketch, anti-win condition, minimal validation, abandonment condition, and next route.
- Outcome durability: <IDEA_ROUTE_DECISION>, <IDEA_MEMORY_RECORD>, and rejected or deferred rationale are explicit enough that later v2 skills do not need to infer what changed.

## Exit Criteria

This skill can end only when one of these is durably true:

- One falsifiable idea is selected and ready for experiment.
- An algorithm-first frontier is shaped and routed to optimize.
- Several ideas are retained with an explicit branch or decision record.
- The current line is rejected and routed back to scout, baseline, or decision.
- The stage is blocked and the missing evidence, unresolved gate, or user-sensitive tradeoff is recorded in <IDEA_BLOCKER_RECORD>.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not treat a small implementable tweak as a strong idea unless literature and local evidence show it is the highest-value surviving route.
- Do not skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
