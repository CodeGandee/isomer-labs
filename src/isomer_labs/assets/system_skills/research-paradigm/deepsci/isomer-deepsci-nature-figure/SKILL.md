---
name: isomer-deepsci-nature-figure
description: Use when a Nature-family or high-impact journal figure must be created, revised, audited, or polished in Python or R with a defined evidence chain and export contract.
---

# Isomer Research Nature Figure

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Nature Figure starts with backend selection and figure contract before plotting. It asks for Python or R when the backend is not clear, keeps all drawing and QA in the selected backend, maps every panel to evidence, chooses a figure archetype, enforces journal export requirements, previews the actual render, and revises until scientific and visual QA pass.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- The user asks for Nature, Nature-family, or high-impact journal figure creation or polish.
- A figure needs panel-level evidence mapping, journal export settings, editable text, statistics, or image-integrity checks.
- The user selected Python or R, or the input clearly implies one backend.
- A submission-grade figure bundle needs rendered QA evidence.

Do not use this skill when:

- The user has not chosen Python or R and no input makes the backend obvious; ask and stop.
- The task needs a quick first-pass standard ML plot; use `isomer-deepsci-paper-plot` unless Nature-grade composition is required.
- The requested figure would require mock data or invented statistics.
- The runtime for the selected backend is unavailable and the user has not routed setup through `$isomer-op-topic-mgr env-install-packages` or downscoped the task.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check backend selection**. Produce `DEEPSCI:NATURE-FIGURE-BACKEND-CHOICE` as Python or R. If missing and not obvious, ask "Python or R?" and stop. Read `references/backend-selection.md` when a recommendation is requested.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-figure --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Define the figure contract**. Produce `DEEPSCI:NATURE-FIGURE-CONTRACT` with one-sentence conclusion, evidence chain, panel roles, dimensions, source data, statistics, integrity notes, and export formats. Read `references/figure-contract.md`.
4. **Check selected runtime**. Produce `DEEPSCI:NATURE-FIGURE-RUNTIME-CHECK` for packages, fonts, device, renderer, and export capability in the selected backend only. If selected-backend packages are missing, stop before rendering and route a natural-language package request to `$isomer-op-topic-mgr env-install-packages`; do not silently switch backends.
5. **Map the evidence chain**. Produce `DEEPSCI:NATURE-PANEL-EVIDENCE-MAP` linking each panel to unique evidence, source data, statistics, and claim. Drop panels that do not carry unique evidence.
6. **Choose archetype and design system**. Produce `DEEPSCI:NATURE-FIGURE-ARCHETYPE` and read `references/nature-2026-observations.md`, `references/common-patterns.md`, `references/chart-types.md`, or `references/design-theory.md` as needed.
7. **Set journal export contract**. Produce `DEEPSCI:NATURE-EXPORT-CONTRACT` covering SVG/PDF/TIFF/PNG, editable text, dimensions, color, line weights, image-integrity notes, and source-data expectations.
8. **Generate with selected backend**. Use Python guidance from `references/api.md` and `references/tutorials.md`, or R guidance from `references/r-workflow.md` and `references/r-template-index.md`, to create `DEEPSCI:NATURE-FIGURE-EXPORT-BUNDLE`.
9. **Preview and QA**. Inspect rendered previews and produce `DEEPSCI:NATURE-FIGURE-QA-REPORT` using `references/qa-contract.md`. Revise with the same backend until scientific, visual, export, and integrity checks pass, or produce `DEEPSCI:NATURE-FIGURE-BLOCKER`.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-figure --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

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
- Missing backend packages must be routed to `$isomer-op-topic-mgr env-install-packages`; do not perform package setup inside this research skill.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Final text size fit: final-size label text stays within the selected journal-readable point-size range; closer to the accepted range is better.
- Panel evidence coverage: fraction of panels with explicit source data, statistic, claim, and integrity notes; higher is better.

### Checks

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
- `DEEPSCI:NATURE-FIGURE-CONTRACT` and `DEEPSCI:NATURE-PANEL-EVIDENCE-MAP` support every panel.
- `DEEPSCI:NATURE-FIGURE-EXPORT-BUNDLE` and `DEEPSCI:NATURE-FIGURE-QA-REPORT` exist, or `DEEPSCI:NATURE-FIGURE-BLOCKER` states the missing runtime/evidence.

## Guardrails

- DO NOT choose Python or R by default when the user has not chosen.
- DO NOT cross-render with the unselected backend.
- DO NOT create mock data or invented statistics.
- DO NOT hide private local paths or internal reference filenames in figure text or user-facing prose.
- DO NOT treat template aesthetics as more important than the evidence chain.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
