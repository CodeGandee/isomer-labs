---
name: isomer-rsch-baseline
description: Establish the lightest trustworthy comparator and resolve baseline readiness through Isomer Labs evidence and decisions.
---

Use this skill when a Research Task needs a trusted comparator, metric
contract, baseline waiver, or blocker before ideation or experimentation.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/baseline.md`

## Entry Signals

- A Research Task needs a trusted comparator, metric contract, baseline waiver,
  or baseline blocker.
- Proposed baseline evidence needs source identity, metric, dataset, split, or
  evaluator checks before downstream use.
- Ideation or experimentation is blocked by unclear comparator status.

## Exit Criteria

- Comparator identity, source, metric contract, and evidence are durable.
- Comparability deviations are visible rather than hidden in prose.
- A Decision Record accepts, waives, replaces, or blocks the comparator.

## Procedure

1. Decide the minimum comparator trust needed for the current downstream use.
2. Prefer attach, import, or local verification before full reproduction.
3. Define the metric contract: task, dataset, split, evaluator, metric ids,
   metric directions, source identity, and caveats.
4. Gather real evidence from files, logs, service output, or source documents.
5. Verify comparability against the metric contract.
6. Record a Decision Record that confirms, waives, replaces, or blocks the
   baseline gate.

## Durable Outputs

- Comparator identity and source.
- Metric contract Artifact.
- Evidence Items for logs, outputs, source documents, or measurements.
- Decision Record for accepted, waived, replaced, or blocked comparator status.

## Guardrails

- Importing a comparator is not enough; comparability must be checked.
- Keep dataset, split, metric, evaluator, and source deviations visible.
- Do not copy numbers from prose unless the source is trusted and traceable.
- Use `[[tbd-surface:policy-baseline-waiver]]` for unsettled waiver rules.
