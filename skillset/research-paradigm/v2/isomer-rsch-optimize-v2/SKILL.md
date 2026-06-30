---
name: isomer-rsch-optimize-v2
description: Use when algorithm-first research needs candidate briefs, frontier ranking, promotion, fusion, debug, plateau response, or route selection before or after measured runs.
---

# Isomer Research Optimize V2

## Overview

Optimize manages an algorithm-first frontier. It chooses one submode per pass, keeps candidate briefs distinct from durable lines and implementation attempts, and records exactly one next route or stop condition.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- The research line is algorithm-first and needs frontier management.
- Candidate briefs must be shaped, ranked, promoted, fused, debugged, or stopped.
- A measured result needs frontier review before another run.
- A plateau or repeated failure requires route review instead of more micro-edits.

Do not use this skill when:

- The task is broad ideation before an algorithm frontier exists.
- A single selected route is ready for experiment with no frontier decision needed.
- The work is baseline recovery or paper writing.
- The request is simply to run an already locked experiment.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Recover the frontier**. Build <OPTIMIZATION_CONTEXT_BRIEF> and <OPTIMIZATION_FRONTIER> from candidate briefs, active lines, measured results, failures, and current route.
2. **Choose one submode**. Select brief, rank, seed, loop, fusion, debug, or stop based on the frontier, not momentum.
3. **Shape or rank candidates**. Create <CANDIDATE_BRIEF> and <CANDIDATE_RANKING> when the next route needs differentiated options.
4. **Promote or execute one line**. Record <PROMOTED_OPTIMIZATION_LINE> or <OPTIMIZATION_ATTEMPT_RECORD> when the route justifies implementation or measured testing.
5. **Review plateau, debug, or fusion evidence**. Produce <FRONTIER_REVIEW> when results, repeated failures, or complementary lines change the frontier.
6. **Record exactly one next route**. Return <OPTIMIZE_ROUTE_DECISION> or <OPTIMIZE_BLOCKER_RECORD> and stop.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/frontier-management.md` for keep algorithm-first state explicit.
- `references/candidate-brief-template.md` for shape loose methods into comparable briefs.
- `references/candidate-ranking.md` for choose a route by criteria rather than enthusiasm.
- `references/run-recording.md` for record implementation-level attempts without confusing them with durable lines.
- `references/plateau-and-fusion.md` for respond to repeated non-improvement or complementary lines.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
