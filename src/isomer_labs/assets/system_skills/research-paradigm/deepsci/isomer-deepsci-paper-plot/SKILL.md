---
name: isomer-deepsci-paper-plot
description: Use when structured numeric data should become a first-pass publication-quality figure by adapting one of the bundled plotting templates.
---

# Isomer Research Paper Plot

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Paper Plot is a template-adaptation skill for standard bar, line, scatter, and radar figures. It clarifies the chart question, chooses the closest bundled style, copies the template script into the active Topic Workspace or Agent Workspace, changes only the data and labels needed, renders, inspects, and hands durable paper-facing figures to figure polish.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A standard quantitative figure is needed from structured numeric data.
- The chart family matches a bundled bar, line, scatter, or radar template.
- The user needs a first-pass figure before paper-level figure QA.
- A writing or analysis step needs a visual display quickly while preserving reproducibility.

Do not use this skill when:

- The figure is disposable debug output.
- The figure already exists and needs final QA; use `isomer-deepsci-figure-polish`.
- The visualization requires a custom domain-specific plotting system not covered by templates.
- The data, units, grouping, or comparison question is unknown.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Confirm the chart question**. Produce `<CHART_QUESTION>` with comparison, units, grouping, key message, required labels, and output target.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-paper-plot --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Choose the bundled style**. Select `<PLOT_STYLE_SELECTION>` from the available style table: paired delta bar, grouped hatch bar, confidence-band line, training curve line, loss with inset, t-SNE scatter, broken-axis scatter, or radar dual series.
4. **Read the style reference**. Read the matching reference page before editing code, including colors, rcParams, layout, legend, width, tick, and annotation expectations.
5. **Copy the template script**. Create `<PLOT_TEMPLATE_COPY>` by copying the matching script from `scripts/` into a Research Task figure area in the active Topic Workspace or Agent Workspace. Do not mutate the bundled template.
6. **Replace data and labels only**. Record `<PLOT_DATA_SUBSTITUTION_RECORD>` for changed data arrays, labels, units, category names, legend text, and output filenames. Avoid unrelated style rewrites.
7. **Run and inspect the copied script**. Generate `<FIRST_PASS_FIGURE>` through the selected execution route, then inspect the actual render and record `<PLOT_RENDER_INSPECTION>`.
8. **Route durable figures**. If the figure is paper-facing, appendix-facing, milestone-facing, or final, create `<FIGURE_POLISH_HANDOFF>` for `isomer-deepsci-figure-polish`; otherwise stop with the first-pass figure and substitution record.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-paper-plot --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer durable evidence and explicit placeholders over concrete source paths until storage binding is finalized.
- Prefer the smallest route that preserves downstream trust, and route missing evidence to the skill that can actually produce it.
- Prefer source-compatible `isomer-cli ext deepsci call ... --input-json '{...}'` only when the source harness behavior matters; otherwise use native Isomer topic context, provider, and execution-adapter surfaces without binding storage prematurely.
- Prefer paper-facing language that names claims, evidence, limits, and next routes without exposing operator, agent, prompt, worktree, or local runtime details.

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- Every paper-facing claim must stay inside the current evidence boundary.
- Every placeholder used by runtime instructions must be listed in `migrate/placeholders.md`.
- Concrete source paths, source harness outputs, and source storage assumptions must not become final Isomer storage contracts.
- Routes to other research stages must use existing production DeepSci skill names when an Isomer counterpart exists.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Render inspection coverage: fraction of generated first-pass figures that were actually opened and inspected before handoff; higher is better.
- Template mutation count: number of bundled template files mutated instead of copied before editing; lower is better.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-paper-plot.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/bar_paired_delta.md` for paired bar comparison with explicit gain arrows.
- `references/bar_grouped_hatch.md` for grouped/ablation bar chart.
- `references/line_confidence_band.md` for line plot with uncertainty band.
- `references/line_training_curve.md` for ordered curves and reference lines.
- `references/line_loss_with_inset.md` for curve with zoom inset.
- `references/scatter_tsne_cluster.md` for clustered embedding scatter.
- `references/scatter_broken_axis.md` for broken-axis scatter for outliers.
- `references/radar_dual_series.md` for dual-series radar comparison.
- `scripts/` for passive plotting templates to copy before editing.

## Exit Criteria

This skill can end when all applicable checks are true:

- A copied script exists outside the bundled template area.
- `<FIRST_PASS_FIGURE>` was rendered and inspected.
- Durable or paper-facing outputs have a `<FIGURE_POLISH_HANDOFF>`.

## Common Mistakes

- Mutating the bundled template instead of a copied script.
- Picking a chart style before clarifying the comparison and units.
- Skipping the rendered-output inspection.
- Using this skill for final figure QA.
- Changing style and data at the same time without recording the substitution.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
