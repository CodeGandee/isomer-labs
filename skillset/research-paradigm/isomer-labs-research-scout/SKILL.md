---
name: isomer-labs-research-scout
description: Frame a research task, narrow unknowns, inspect literature or local evidence, and recommend baseline, idea, or blocker routing.
---

Use this skill when the research frame, metric, benchmark neighborhood, or
baseline direction is not clear enough to choose the next Workflow Stage.

Read first:

- `../isomer-labs-research-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/scout.md`

## Entry Signals

- The research frame, metric, benchmark neighborhood, or baseline direction is
  too unclear for route selection.
- Local evidence or literature could change whether the next stage is baseline,
  idea, Gate, Decision Record, or blocker.
- The Operator Agent needs a bounded scout result, not an exhaustive survey.

## Exit Criteria

- The task frame and evaluation contract are recorded.
- A comparator shortlist exists, or the handoff justifies why ideation can
  proceed without more baseline scouting.
- The next Workflow Stage, Gate, Decision Record, or blocker is explicit.

## Procedure

1. Reconstruct the task frame from durable Artifacts, Research Goal, metric
   hints, baseline status, and blockers.
2. List only unknowns that can change the next stage.
3. Reuse local Artifacts and Findings before external literature lookup.
4. Search or read papers only in the unresolved benchmark neighborhood.
5. Build a comparator shortlist or justify why ideation can proceed.
6. Recommend baseline, idea, Gate, Decision Record, or blocker.

## Durable Outputs

- Task frame and evaluation contract Artifact.
- Comparator shortlist or route justification.
- Literature notes only when they change routing.
- Next Workflow Stage or blocker.

## Guardrails

- Do not turn scouting into an exhaustive survey.
- Stop searching once the next stage is clear.
- Do not ask for routine technical clarification before checking local evidence.
- Use `[[tbd-surface:provider-literature-search]]` for unsettled paper search.
