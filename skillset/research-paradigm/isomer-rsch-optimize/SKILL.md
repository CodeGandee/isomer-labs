---
name: isomer-rsch-optimize
description: Manage algorithm-first candidates, frontier ranking, promotion, bounded attempts, and fusion or debug routes.
---

# Isomer Research Optimize

## Overview

Use this skill when a selected route needs algorithm-first candidate shaping, frontier ranking, Research Branch promotion, bounded implementation attempts, fusion, debug, or stop decisions before or after a measured Run.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when brief shaping, candidate ranking, frontier review, execution routing, fusion, debug, plateau, or memory recording matters.
3. **Recover the current frontier**. Refresh candidate Artifacts, View Manifests, Research Branch decisions, recent Runs, Findings, and any existing frontier record before creating or promoting anything.
4. **Choose exactly one optimize submode**. Pick `brief`, `rank`, `seed`, `loop`, `fusion`, `debug`, or `stop`, and keep one dominant route meaning: `explore`, `exploit`, `fusion`, `debug`, or `stop`.
5. **Keep object levels separate**. Treat method briefs, durable Research Branch lines, and implementation attempts as different objects with different evidence and promotion thresholds.
6. **Advance one bounded move**. Shape and rank briefs, promote a line, seed a small implementation pool, run or route one bounded attempt through an Execution Adapter, handle debug, fuse complementary lines, or stop a plateau.
7. **Record the frontier update and next action**. Store the result as Artifacts, Evidence Items, Research Branch decisions, Run references, Decision Records, and Provenance Records as appropriate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/method-brief.md` when shaping or reviewing a candidate method brief.
- `references/candidate-board.md` when the candidate ledger, active pool, or implementation attempts need one shared surface.
- `references/candidate-ranking.md` before promoting a candidate brief into a durable Research Branch.
- `references/frontier-review.md` when deciding explore, exploit, fusion, debug, or stop.
- `references/optimize-checklist.md` for pass-level control and closeout.
- `references/brief-shaping.md` when loose directions need a small differentiated slate.
- `references/operational-guidance.md` for submode selection, promotion policy, seed and loop policy, memory, Execution Adapter routing, and stage completion.
- `references/fusion.md` when combining complementary strengths from multiple lines.
- `references/debug.md` when a strategically valuable candidate failed for a concrete and likely fixable reason.
- `references/plateau.md` when repeated attempts stop improving the frontier.
- `references/codegen-route.md` when choosing brief-only, stepwise, patch, or rewrite implementation routes.
- `references/optimization-memory.md` when recording reusable success patterns, failure patterns, fusion lessons, or non-repeat rules.
- `references/prompt-patterns.md` when prompt shape affects candidate generation, plateau handling, fusion, or debug work.

## Entry Signals

- A selected route needs algorithm-first exploration, candidate ranking, frontier management, fusion, or debug work before a main experiment.
- Candidate method briefs or Research Branches exist but promotion criteria are unclear.
- A durable line has an implementation-candidate pool, plateau, failure, fusion opportunity, or measured Run that needs a frontier decision.
- One bounded attempt can materially change the frontier or the next route.

## Exit Criteria

- Candidate briefs, frontier state, Research Branch decisions, implementation attempts, and any Run evidence are durable.
- Exactly one dominant next route is recommended, promoted, stopped, debugged, fused, or blocked.
- The handoff separates frontier updates from implementation attempts and identifies the next Workflow Stage.

## Object Model

- Method brief: an Artifact describing a possible direction without opening a durable Research Branch.
- Durable line: a promoted Research Branch with enough expected value, differentiation, and execution path clarity to deserve branch-level state under `[[tbd-surface:policy-branching]]`.
- Implementation attempt: a bounded Run or Evidence Item inside one durable line, such as one patch, smoke candidate, debug candidate, or fusion candidate.
- Frontier record: an Artifact or View Manifest summarizing active lines, recent Runs, stagnant branches, candidate backlog, route meaning, and next action.

## Optimize Submodes

- `brief`: turn loose directions into compact method briefs.
- `rank`: compare briefs on one shared surface and choose promotion candidates.
- `seed`: create a small implementation-attempt pool inside one durable line.
- `loop`: advance one durable line with bounded smoke, full evaluation, archive, or record actions.
- `fusion`: combine complementary strengths from multiple lines.
- `debug`: repair a strategically valuable candidate blocked by a concrete failure mode.
- `stop`: record that the remaining routes are not justified now.

## Durable Outputs

- Refreshed frontier Artifact or View Manifest.
- Method brief Artifacts.
- Candidate board, ranking, checklist, or optimization-memory Artifacts when the pass is non-trivial.
- Decision Record for promoted, deferred, fused, debugged, stopped, or blocked routes.
- Implementation-attempt Evidence Items and Run references.
- Provenance Records for execution, source records, and route-changing evidence.

## Guardrails

- Do not create a Research Branch for every implementation attempt.
- Do not promote every plausible method brief.
- Do not mix several major route changes in one optimize pass.
- Do not hide a plateau under repeated near-duplicate tweaks.
- Do not use debug as a performance-improvement route; it is bugfix-only.
- Do not fuse weak or redundant lines merely because multiple branches exist.
- Use `[[tbd-surface:schema-stage-cursor]]` for unsettled next-stage records and `[[tbd-surface:api-execution-command]]` for unsettled execution surfaces.
