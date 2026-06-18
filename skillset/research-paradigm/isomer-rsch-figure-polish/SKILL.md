---
name: isomer-rsch-figure-polish
description: Turn a meaningful draft figure into a durable, readable milestone, manuscript, appendix, or review figure.
---

# Isomer Research Figure Polish

## Overview

Use this skill when an already meaningful draft figure needs render-inspect-revise quality control, final exports, claim linkage, or paper-facing polish.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Classify the surface** using `references/surface-class.md`: milestone, manuscript main figure, appendix or supplement, review response, or internal review.
3. **State the one message** the figure must communicate and link the source Evidence Items, Research Claims, report section, or reviewer item.
4. **Choose or confirm the chart form** using `references/chart-selection.md`; split the figure if unrelated claims compete inside one panel.
5. **Apply the style contract** from `references/style-contract.md` and, for Python Matplotlib figures, prefer `assets/isomer-academic.mplstyle` unless the host style asset overrides it.
6. **Render, inspect, and revise** using `references/self-review.md`; inspect the actual output rather than only reading plotting code.
7. **Export and record the final figure** using `references/export-recording.md`, then update or create the relevant Artifact, Evidence Item, Research Claim link, Decision Record, or Gate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user prompt, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, evidence boundaries, runtime boundaries, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/surface-class.md` when deciding export expectations, review depth, or handoff shape.
- `references/chart-selection.md` when choosing whether the current chart form matches the research issue.
- `references/style-contract.md` before changing colors, fonts, grids, legends, hierarchy, or Matplotlib style.
- `references/self-review.md` before accepting any durable or paper-facing figure.
- `references/export-recording.md` when recording exports, source data, scripts, claims, and self-review deltas.

## Entry Signals

- An already meaningful figure needs final visual quality control or durable export.
- The figure has a known surface: milestone, manuscript, appendix, review, or internal review.
- The comparison, Research Claim, report section, or reviewer item the figure supports can be stated.

## Exit Criteria

- Final exports have been rendered and inspected.
- Source data, plotting Artifact, generation path, and export paths are linked through existing Isomer records.
- The figure's claim, Evidence Item, report, or review linkage is explicit.
- Any remaining limitations, down-scaling risks, color risks, or schema gaps are recorded.

## Durable Outputs

- Final figure exports as figure output Artifacts resolved by Workspace Path Resolution.
- Source plotting Artifact or generation path.
- Visual inspection note and self-review delta.
- Linked Evidence Item, Research Claim, report section, reviewer item, Decision Record, Gate, or Provenance Record through `[[tbd-surface:api-artifact-record]]`.

## Guardrails

- Do not treat uninspected renders as final.
- Do not polish disposable debug plots unless the Operator Agent explicitly asks for a durable figure.
- Do not overload one figure with unrelated claims.
- Do not use decorative effects that obscure the comparison.
- Do not invent a dedicated final figure schema; use existing Artifact, Evidence Item, Provenance Record, and figure-output placeholders until that surface is accepted.
