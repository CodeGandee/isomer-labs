---
name: isomer-labs-research-analysis
description: Run focused follow-up evidence work that confirms, weakens, changes, or blocks a parent claim.
---

Use this skill after a main result when ablation, robustness, error analysis,
failure analysis, reviewer-linked evidence, or paper-gap analysis is needed.

Read first:

- `../isomer-labs-research-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/analysis-campaign.md`

## Entry Signals

- A main result, Research Claim, paper gap, reviewer item, failure mode, or
  Decision Record needs follow-up evidence.
- Ablation, robustness, error analysis, failure analysis, or focused gap work
  can change the parent claim or route.
- Execution limits and slice definitions can be bounded before running.

## Exit Criteria

- Each slice has recorded status, evidence, comparability verdict, caveat, and
  claim impact.
- The campaign interpretation is grounded in the recorded slices.
- The next route is experiment, idea, write, decision, pause, or blocker.

## Procedure

1. Lock the parent object: Research Claim, main result, paper gap, reviewer
   item, failure mode, or Decision Record.
2. Audit execution limits: compute, memory, time, storage, dependencies, queue,
   service constraints, and available evidence.
3. Choose the lightest analysis route that can change the parent claim.
4. Define slices with fixed conditions, metrics, observables, and stop rules.
5. Run the highest-value slices first.
6. Record each slice with status, evidence path, claim update, comparability
   verdict, caveat, and next action.
7. Aggregate only decision-relevant findings and route to experiment, idea,
   write, decision, pause, or blocker.

## Durable Outputs

- Slice Evidence Items and Artifacts.
- Campaign interpretation grounded in slices.
- Research Claim updates.
- Next route Decision Record or blocker.

## Guardrails

- Do not disguise a new main experiment as analysis.
- Do not widen the campaign after the next route is clear.
- Do not call subjective inspection objective without rubric, sample, trace,
   and caveat.
- Use `[[tbd-surface:path-analysis-output]]` for unsettled analysis layouts.
