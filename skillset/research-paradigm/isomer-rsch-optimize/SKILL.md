---
name: isomer-rsch-optimize
description: Manage algorithm-first candidates, frontier ranking, promotion, bounded attempts, and fusion or debug routes.
---

Use this skill when a selected route needs algorithm-first exploration,
candidate ranking, frontier management, branch promotion, fusion, or debug
work before a main experiment.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/optimize.md`

## Entry Signals

- A selected route needs algorithm-first exploration, candidate ranking,
  frontier management, fusion, or debug work before the main experiment.
- Candidate briefs or Research Branches exist but promotion criteria are
  unclear.
- One bounded attempt can materially change the frontier or next route.

## Exit Criteria

- Candidate briefs, frontier state, and any attempt evidence are durable.
- Exactly one dominant next route is recommended, promoted, stopped, or blocked.
- The handoff separates frontier updates from implementation attempts.

## Procedure

1. Refresh current candidate Artifacts, Research Branches, Findings, and
   evidence from the active line.
2. Choose one submode: brief, rank, seed, loop, fusion, debug, or stop.
3. Keep candidate briefs, durable lines, and implementation attempts separate.
4. Promote a candidate to a durable line only when expected value,
   differentiation, and execution path are clear.
5. Run one bounded attempt when execution is justified.
6. Record result, frontier update, and one dominant next route.

## Durable Outputs

- Refreshed frontier Artifact or View Manifest.
- Candidate brief Artifacts.
- Decision Record for promoted line or stopped route.
- Attempt Artifact with evidence and next action.

## Guardrails

- Do not create a Research Branch for every small attempt.
- Do not promote every plausible candidate.
- Do not mix several major route changes in one optimization pass.
- Use `[[tbd-surface:schema-stage-cursor]]` for unsettled next-stage records.
