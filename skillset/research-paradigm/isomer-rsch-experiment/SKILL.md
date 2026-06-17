---
name: isomer-rsch-experiment
description: Turn one selected route into one trustworthy measured result and route from the resulting Isomer Labs evidence.
---

Use this skill when a selected route or promoted candidate needs a bounded
implementation pass, main run, metric validation, and durable result.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/experiment.md`

## Entry Signals

- A selected route or promoted candidate is ready for one bounded
  implementation pass or main run.
- Comparator status, metric contract, expected outputs, and stop rules are
  known or can be locked before execution.
- The Research Task needs a measured result that can support or weaken a
  Research Claim.

## Exit Criteria

- Run contract, inputs, commands, configs, logs, outputs, and metrics are
  durable.
- Metric completeness and comparator comparability have been checked.
- The handoff recommends optimize, analysis, write, decision, or blocker.

## Procedure

1. Recover selected route, comparator status, metric contract, current
   workspace context, and expected outputs.
2. Lock the run contract: research issue, comparator, stop rule, abandonment
   rule, output schema, evidence target, and comparability rules.
3. Plan the smallest hypothesis-bound code, config, or execution change.
4. Use smoke or pilot checks only to validate wiring.
5. Run the evidence-bearing attempt and preserve commands, configs, logs,
   outputs, and last-good state.
6. Validate metric completeness and comparator comparability.
7. Record the measured result and recommend optimize, analysis, write,
   decision, or blocker.

## Durable Outputs

- Run contract Artifact.
- Run logs, configs, outputs, and metric records.
- Evidence Items and Research Claim update.
- Next route Decision Record or blocker.

## Guardrails

- Do not silently change dataset, split, metric, evaluator, or comparator.
- Do not claim success before durable output exists.
- Do not rerun without a real change in code, command, environment, evidence,
  or route.
- Use `[[tbd-surface:path-run-logs]]` and `[[tbd-surface:api-execution-command]]`
  for unsettled execution surfaces.
