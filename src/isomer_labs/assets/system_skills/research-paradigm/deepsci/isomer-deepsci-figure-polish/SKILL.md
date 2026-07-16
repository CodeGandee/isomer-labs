---
name: isomer-deepsci-figure-polish
description: Use when an already meaningful figure needs durable academic styling, render inspection, revision, final export, and evidence-linked recording.
---

# Isomer Research Figure Polish

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Figure Polish makes figures durable. It classifies the surface, states the one message, chooses a chart form that matches the research question, applies a restrained academic style, renders, inspects the actual output, revises until the check passes, exports the right formats, and records the figure against its evidence or claim.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A first-pass figure is ready for manuscript, appendix, milestone, or internal review use.
- The figure has a known message but needs readability, composition, export, or evidence-link QA.
- A paper-facing figure needs vector export plus preview.
- A review or rebuttal package needs durable figure provenance.

Do not use this skill when:

- The plot is disposable debug output.
- No meaningful figure question or source data exists yet.
- The task is to create a standard first-pass figure from templates; use `isomer-deepsci-paper-plot` first.
- The user asks for glossy or decorative visual treatment that conflicts with academic evidence display.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the figure surface**. Produce `DEEPSCI:FIGURE-SURFACE-CLASS` as milestone, paper main figure, appendix figure, internal review figure, or another justified surface.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-figure-polish --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Define the figure message**. Produce `DEEPSCI:FIGURE-MESSAGE` with the one comparison or claim the figure must communicate.
4. **Choose the chart form**. Select the chart form by research question, not visual taste, and remove panels that do not carry unique evidence.
5. **Apply the style contract**. Produce `DEEPSCI:FIGURE-STYLE-CONTRACT` with restrained academic styling, readable labels, muted palette, clear hierarchy, and surface-appropriate dimensions. Use the copied source style file or an Isomer alias only after checking it fits the figure.
6. **Render the first draft**. Generate an actual image output through the selected execution route and record the script, input data, and output targets semantically.
7. **Inspect and revise the render**. Inspect the rendered output and produce `DEEPSCI:FIGURE-RENDER-REVIEW`. Revise and re-export until readability, composition, label, legend, color, and claim-message checks pass.
8. **Export final formats**. Produce `DEEPSCI:FINAL-FIGURE-EXPORT` in the surface-appropriate formats, usually PNG for milestones and PDF/SVG plus PNG preview for paper-facing figures.
9. **Record durable provenance**. Produce `DEEPSCI:FIGURE-PROVENANCE-RECORD` linking the figure to source data, script, claim, paper section, review item, or downstream handoff placeholder.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-figure-polish --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

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

- Message recognition time: time needed for a reviewer to identify the main figure message from the rendered output; lower is better.
- Paper-facing export coverage: number of required paper-facing export formats produced for the selected surface; higher is better until all required formats exist.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-figure-polish.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `assets/deepscientist-academic.mplstyle` for copied upstream Matplotlib style asset available for compatibility.
- `org/src/SKILL.md` for upstream figure-polish policy preserved for audit.

## Exit Criteria

This skill can end when all applicable checks are true:

- The actual render was inspected, not only the plotting code.
- `DEEPSCI:FINAL-FIGURE-EXPORT` matches the surface class.
- `DEEPSCI:FIGURE-PROVENANCE-RECORD` links the figure to evidence and downstream use.

## Guardrails

- DO NOT treat an uninspected render as final.
- DO NOT overload one figure with unrelated claims.
- DO NOT use dashboard-like, glossy, rainbow, or decorative styling for paper figures.
- DO NOT polish debug plots without a durable use.
- DO NOT export only a raster when the paper surface needs vector output.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
