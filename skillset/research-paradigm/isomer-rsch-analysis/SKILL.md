---
name: isomer-rsch-analysis
description: Run focused follow-up evidence work that confirms, weakens, changes, or blocks a parent claim.
---

Use this skill after a main result when ablation, robustness, error analysis, failure analysis, reviewer-linked evidence, or paper-gap analysis is needed.

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/campaign-design.md` when choosing route type, slice priority, or resource-aware frontier.
- `references/evidence-flow-examples.md` when deciding how to record launched, failed, infeasible, writing-facing, or read-only analysis work.
- `references/campaign-record-template.md` when a durable route record would reduce ambiguity.
- `references/analysis-gate-checklist.md` before closing a campaign or Gate.
- `references/boundary-cases.md` when stage, success, or comparability boundaries are fuzzy.
- `references/operational-guidance.md` when execution monitoring, durable context, or operator-facing chart notes affect the route.
- `references/writing-facing-slice-fields.md` when analysis supports a report, paper, review, or rebuttal package.

## Entry Signals

- A main result, Research Claim, paper gap, reviewer item, failure mode, or Decision Record needs follow-up evidence.
- Ablation, robustness, error analysis, failure analysis, or focused gap work can change the parent claim or route.
- Execution limits and slice definitions can be bounded before running.

## Exit Criteria

- Each slice has recorded status, evidence, comparability verdict, caveat, and claim impact.
- The campaign interpretation is grounded in the recorded slices.
- The next route is experiment, idea, write, decision, pause, or blocker.

## Procedure

1. Lock the parent object: Research Claim, main result, paper gap, reviewer item, failure mode, or Decision Record.
2. Audit execution limits: compute, memory, time, storage, dependencies, queue, service constraints, and available evidence.
3. Choose the lightest route that preserves trust: analysis-lite, durable evidence package, writing-facing campaign, review/rebuttal campaign, or failure-analysis route.
4. Define slices with class, fixed conditions, metrics or observables, comparison target, resource class, expected evidence, and stop rules.
5. Run the highest-value slices first.
6. Record each slice with status, evidence path, claim update, comparability verdict, caveat, and next action.
7. Aggregate only decision-relevant findings and route to experiment, idea, write, decision, pause, or blocker.

## Slice Evidence Contract

For each meaningful slice, define and record enough of the following to make the evidence reusable:

- research question and expected decision-relevant pattern
- intervention, ablation, variation, inspection target, or failure bucket
- controls or fixed conditions
- metric, observable, table, qualitative artifact, or rubric
- comparison target and comparability boundary
- expected resource class or major execution constraint
- stop condition or completion condition
- evidence path expectations
- claim update, comparability verdict, and next action

Code-based analysis is preferred when it is the most faithful and repeatable path. Qualitative inspection can be valid when the sample is concrete, the rubric or inspection basis is explicit, and the evidence is presented as supporting or boundary evidence rather than objective measurement.

## Comparability Contract

Comparability is a hard boundary:

- keep the same evaluation contract unless the variation is the point
- keep slice comparisons aligned with the accepted baseline metric contract when baseline comparison matters
- state exactly what changed and what stayed fixed
- label new datasets, splits, metrics, or protocols as generalization, stress-test, boundary, failure-analysis, or non-comparable slices
- do not mix non-comparable slices into the main comparison as direct support

If a slice needs an extra comparator, treat it as analysis-local support and do not overwrite the accepted baseline Gate.

## Durable Outputs

- Slice Evidence Items and Artifacts.
- Campaign interpretation grounded in slices.
- Research Claim updates.
- Next route Decision Record or blocker.
- Optional campaign record, frontier, checklist, or writing-facing mapping Artifact when the route is multi-slice, expensive, unstable, long-running, or report-facing.

## Guardrails

- Do not disguise a new main experiment as analysis.
- Do not hide null, negative, failed, partial, blocked, infeasible, or contradictory slices.
- Do not widen the campaign after the next route is clear.
- Do not call subjective inspection objective without rubric, sample, trace, and caveat.
- Do not call a writing-facing slice complete while its target outline, evidence ledger, section, claim, table, reviewer item, or rebuttal item is stale or unmapped.
- If two slices in a row fail to change the claim boundary, frontier, or next route, stop widening and route through decision, write, experiment, or an explicit blocker.
- Use `[[tbd-surface:path-analysis-output]]` for unsettled analysis layouts.
