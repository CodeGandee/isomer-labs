---
name: isomer-labs-research-paper-plot
description: Turn structured numeric evidence into a first-pass academic figure and hand paper-facing figures to final polish.
---

Use this skill for standard bar, line, scatter, or radar-style figures from
structured numeric data when the chart issue, units, grouping, and output
target are known or can be clarified from evidence.

Read first:

- `../isomer-labs-research-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/paper-plot.md`

## Entry Signals

- Structured numeric evidence needs a first-pass academic figure.
- The chart issue, units, grouping, uncertainty, and output target are known or
  can be clarified from evidence.
- The result is intended for report, paper, review, or milestone use rather
  than disposable debugging.

## Exit Criteria

- Source data and figure-generation Artifact or script are durable.
- The rendered figure has been inspected.
- The handoff either keeps the figure as first-pass output or routes it to
  figure-polish.

## Procedure

1. Confirm the comparison, units, grouping, uncertainty, and target surface.
2. Select the closest existing style or template capability provided by the
   host; if no template surface is settled, mark it with
   `[[tbd-surface:path-figure-output]]`.
3. Keep source data near the figure-generation Artifact.
4. Edit only data, labels, categories, and required style settings.
5. Render the first-pass figure and inspect the actual output.
6. Hand durable or paper-facing figures to figure-polish.

## Durable Outputs

- Source data Artifact.
- Figure-generation Artifact or script.
- First-pass rendered figure.
- Optional handoff to figure-polish.

## Guardrails

- Do not use this for disposable debug plots.
- Do not mutate a shared template directly.
- Do not finalize an uninspected figure.
- Keep labels, units, legends, categories, and colors consistent.
