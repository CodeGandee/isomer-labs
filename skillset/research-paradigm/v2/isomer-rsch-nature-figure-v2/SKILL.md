---
name: isomer-rsch-nature-figure-v2
description: Use when a Nature-family or high-impact journal figure must be created, revised, audited, or polished in Python or R with a defined evidence chain and export contract.
---

# Isomer Research Nature Figure V2

## Overview

Nature Figure starts with backend selection and figure contract before plotting. It asks for Python or R when the backend is not clear, keeps all drawing and QA in the selected backend, maps every panel to evidence, chooses a figure archetype, enforces journal export requirements, previews the actual render, and revises until scientific and visual QA pass.

Placeholder definitions live in `migrate/placeholders.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- The user asks for Nature, Nature-family, or high-impact journal figure creation or polish.
- A figure needs panel-level evidence mapping, journal export settings, editable text, statistics, or image-integrity checks.
- The user selected Python or R, or the input clearly implies one backend.
- A submission-grade figure bundle needs rendered QA evidence.

Do not use this skill when:

- The user has not chosen Python or R and no input makes the backend obvious; ask and stop.
- The task needs a quick first-pass standard ML plot; use `isomer-rsch-paper-plot-v2` unless Nature-grade composition is required.
- The requested figure would require mock data or invented statistics.
- The runtime for the selected backend is unavailable and the user has not approved setup or downscope.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check backend selection**. Produce `<NATURE_FIGURE_BACKEND_CHOICE>` as Python or R. If missing and not obvious, ask "Python or R?" and stop. Read `references/backend-selection.md` when a recommendation is requested.
2. **Define the figure contract**. Produce `<NATURE_FIGURE_CONTRACT>` with one-sentence conclusion, evidence chain, panel roles, dimensions, source data, statistics, integrity notes, and export formats. Read `references/figure-contract.md`.
3. **Check selected runtime**. Produce `<NATURE_FIGURE_RUNTIME_CHECK>` for packages, fonts, device, renderer, and export capability in the selected backend only. Do not silently switch backends.
4. **Map the evidence chain**. Produce `<NATURE_PANEL_EVIDENCE_MAP>` linking each panel to unique evidence, source data, statistics, and claim. Drop panels that do not carry unique evidence.
5. **Choose archetype and design system**. Produce `<NATURE_FIGURE_ARCHETYPE>` and read `references/nature-2026-observations.md`, `references/common-patterns.md`, `references/chart-types.md`, or `references/design-theory.md` as needed.
6. **Set journal export contract**. Produce `<NATURE_EXPORT_CONTRACT>` covering SVG/PDF/TIFF/PNG, editable text, dimensions, color, line weights, image-integrity notes, and source-data expectations.
7. **Generate with selected backend**. Use Python guidance from `references/api.md` and `references/tutorials.md`, or R guidance from `references/r-workflow.md` and `references/r-template-index.md`, to create `<NATURE_FIGURE_EXPORT_BUNDLE>`.
8. **Preview and QA**. Inspect rendered previews and produce `<NATURE_FIGURE_QA_REPORT>` using `references/qa-contract.md`. Revise with the same backend until scientific, visual, export, and integrity checks pass, or produce `<NATURE_FIGURE_BLOCKER>`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

- Prefer durable evidence and explicit placeholders over concrete source paths until storage binding is finalized.
- Prefer the smallest route that preserves downstream trust, and route missing evidence to the skill that can actually produce it.
- Prefer source-compatible `isomer-cli ext deepsci call ... --input-json '{...}'` only when the source harness behavior matters; otherwise use native Isomer topic context, provider, and execution-adapter surfaces without binding storage prematurely.
- Prefer paper-facing language that names claims, evidence, limits, and next routes without exposing operator, agent, prompt, worktree, or local runtime details.

## Cross-Step Constraints

- Every paper-facing claim must stay inside the current evidence boundary.
- Every placeholder used by runtime instructions must be listed in `migrate/placeholders.md`.
- Concrete source paths, source harness outputs, and source storage assumptions must not become final Isomer storage contracts.
- Routes to other research stages must use existing v2 skill names when an Isomer counterpart exists.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-nature-figure.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/backend-selection.md` for backend choice and mixed-workflow rules.
- `references/figure-contract.md` for figure conclusion, evidence hierarchy, panel map, and risks.
- `references/api.md` for Python helper API, palette, and validation rules.
- `references/common-patterns.md` for Python layout patterns.
- `references/chart-types.md` for chart-specific Python patterns.
- `references/tutorials.md` for end-to-end Python walkthroughs.
- `references/r-workflow.md` for R workflow.
- `references/r-template-index.md` for private/user R template adaptation.
- `references/design-theory.md` for typography, color, layout, export policy.
- `references/nature-2026-observations.md` for Nature page archetypes.
- `references/qa-contract.md` for final QA and revision contract.

## Exit Criteria

This skill can end when all applicable checks are true:

- Backend selection is explicit and all drawing/QA used that backend.
- `<NATURE_FIGURE_CONTRACT>` and `<NATURE_PANEL_EVIDENCE_MAP>` support every panel.
- `<NATURE_FIGURE_EXPORT_BUNDLE>` and `<NATURE_FIGURE_QA_REPORT>` exist, or `<NATURE_FIGURE_BLOCKER>` states the missing runtime/evidence.

## Common Mistakes

- Choosing Python or R by default when the user has not chosen.
- Cross-rendering with the unselected backend.
- Creating mock data or invented statistics.
- Hiding private local paths or internal reference filenames in figure text or user-facing prose.
- Treating template aesthetics as more important than the evidence chain.
