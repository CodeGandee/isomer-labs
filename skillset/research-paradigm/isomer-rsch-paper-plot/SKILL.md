---
name: isomer-rsch-paper-plot
description: Turn structured numeric evidence into a first-pass academic figure and hand paper-facing figures to final polish.
---

# Isomer Research Paper Plot

## Overview

Use this skill when structured numeric data, arrays, tables, or CSV-like measurements should become a durable first-pass academic figure in a standard bar, line, scatter, or radar family.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Confirm figure intent**. State the comparison, unit, grouping, uncertainty, source Evidence Items, and target surface before choosing a style.
3. **Route the chart style** using `references/style-routing.md`; if the task does not fit a supported family, ask for a narrower chart target or hand off to a custom figure route.
4. **Read the matching per-style reference** from **Reference Routing** and extract only the visual contract needed for the current Artifact.
5. **Create a figure-generation Artifact** under the host figure-output surface, keep source data beside it, and substitute data according to `references/data-substitution.md`.
6. **Render and inspect the first-pass figure** through an approved Execution Adapter and record the rendered output as an Evidence Item or Artifact.
7. **Route the result**. Keep it as a first-pass figure, or hand durable milestone, report, review, appendix, or manuscript figures to `$isomer-rsch-figure-polish`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user prompt, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, evidence boundaries, runtime boundaries, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/style-routing.md` when selecting among supported bar, line, scatter, and radar styles.
- `references/data-substitution.md` before adapting source data, labels, categories, colors, uncertainty, or export settings.
- `references/bar-paired-delta.md` for paired baseline-versus-method bars with delta labels and arrows.
- `references/bar-grouped-hatch.md` for grouped bars with a hatched or otherwise emphasized primary method.
- `references/line-confidence-band.md` for line charts with uncertainty bands.
- `references/line-training-curve.md` for ordered training curves with breakpoints or reference lines.
- `references/line-loss-with-inset.md` for loss curves that need a zoomed inset.
- `references/scatter-tsne-cluster.md` for clustered embedding plots with annotation boxes.
- `references/scatter-broken-axis.md` for scatter plots with discontinuous x-ranges.
- `references/radar-dual-series.md` for two-method radar charts across benchmark dimensions.
- `references/deferred-resources.md` for the script import decision and follow-up boundary.

## Entry Signals

- Structured numeric evidence needs a first-pass academic figure.
- The intended comparison, units, grouping, uncertainty, and output target are known or can be clarified from durable evidence.
- The result is intended for report, paper, review, milestone, or reusable analysis work rather than disposable debugging.

## Exit Criteria

- Source data, transformation notes, and the figure-generation Artifact are durable.
- The rendered figure has been inspected, not only generated.
- Labels, units, legends, categories, uncertainty, and visual hierarchy match the selected style contract.
- The handoff either keeps the figure as first-pass output or routes it to `$isomer-rsch-figure-polish`.

## Durable Outputs

- Source data Artifact or linked Evidence Item.
- Figure-generation Artifact, including script or notebook path through figure output Artifact through Workspace Path Resolution.
- First-pass rendered figure and inspection note.
- Optional handoff to figure polish with target surface, claim, comparison, and unresolved visual issues.

## Guardrails

- Do not use this skill for disposable debug plots.
- Do not treat an uninspected render as final.
- Do not mutate a shared template or style asset directly; create a task-local figure-generation Artifact.
- Do not invent missing units, uncertainty, categories, or comparison direction.
- Do not import source reproduction scripts as active templates unless they are sanitized for local paths, dependencies, output names, data blocks, and Isomer runtime boundaries.
