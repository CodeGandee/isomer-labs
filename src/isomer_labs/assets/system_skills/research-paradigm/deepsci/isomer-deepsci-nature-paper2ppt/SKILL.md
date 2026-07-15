---
name: isomer-deepsci-nature-paper2ppt
description: Use when a complete Chinese PPTX presentation must be built from a scientific paper, preprint, PDF, article text, abstract, figure legends, or reading notes.
---

# Isomer Research Nature Paper2PPT

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Nature Paper2PPT is deck-first. It extracts source material in two passes, classifies the paper type, chooses presentation logic, builds a Chinese slide plan, selects evidence figures, prepares assets, writes slide content and speaker notes, creates an editable `.pptx`, then verifies package structure and rendered previews when possible.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- The user asks for a Chinese journal-club, group-meeting, seminar, thesis, or academic PPTX from a paper.
- A paper PDF, text, abstract, figure legends, notes, or extracted paper material is available.
- The desired output is an actual editable `.pptx`, not only an outline.
- Figures must be selected as evidence rather than decoration.

Do not use this skill when:

- Only a generic outline is requested and no deck is needed.
- The source material is too thin to identify claims, methods, results, or figures.
- The task would require inventing numbers, mechanisms, datasets, or figure details.
- Full OCR, full supplement extraction, or all-slide rendered QA would be wasteful and not requested.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Extract source material**. Produce `<PAPER_PRESENTATION_SOURCE_PACKET>` with metadata, abstract, headings, figure legends, table captions, claims, methods, results, and limitations from available source material.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-paper2ppt --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Classify the paper type**. Produce `<PAPER_TYPE_CLASSIFICATION>` before slide planning: discovery, mechanism, method, resource, clinical, materials/engineering, review, or another justified type.
4. **Choose presentation logic**. Select claim-first, question-to-evidence, problem-to-solution, workflow-to-validation, evidence-map, or another suited logic.
5. **Build the Chinese plan**. Produce `<CHINESE_PRESENTATION_PLAN>` with 10-16 slide sequence, story spine, section flow, and audience-facing emphasis.
6. **Select evidence figures**. Produce `<PRESENTATION_FIGURE_SELECTION>` with only figures and panels that carry the argument. Prefer fewer readable key panels over many cramped graphics.
7. **Extract and prepare assets**. Produce `<PRESENTATION_ASSET_MANIFEST>` for figure crops, rendered pages, provenance, captions, and local asset quality.
8. **Write slide content**. Produce `<CHINESE_SLIDE_CONTENT>` with Chinese titles, bullets, captions, takeaways, and speaker notes, preserving evidence limits and citation/attribution needs.
9. **Build and verify the PPTX**. Create `<PPTX_DECK>`, reopen or inspect package structure, render previews when a renderer is available, revise defects, and produce `<PPTX_QA_REPORT>` plus `<PPTX_REVISION_LOG>` when revisions occur.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-paper2ppt --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

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
- Missing Python packages for PPTX construction or verification must be routed to `$isomer-op-topic-mgr env-install-packages`; do not perform package setup inside this research skill.
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Slide count fit: number of slides in a quick or unspecified deck; closer to the 10-14 slide target is better, and staying at or below 16 is better unless the user asked for a detailed seminar.
- Embedded media count: number of embedded figures or media items that remain readable at presentation scale; higher is better until every evidence-critical visual is represented.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-nature-paper2ppt.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `org/src/SKILL.md` for upstream deck construction policy, paper-type guidance, output file contract, and QA rules.

## Exit Criteria

This skill can end when all applicable checks are true:

- `<PPTX_DECK>` exists as an editable deck, not only an outline or script.
- `<PRESENTATION_ASSET_MANIFEST>` records figure provenance.
- `<PPTX_QA_REPORT>` records package checks and any render limitations.

## Guardrails

- DO NOT stop at an outline instead of building the PPTX.
- DO NOT invent missing numbers, mechanisms, datasets, or figure details.
- DO NOT use figures as decoration instead of evidence.
- DO NOT cram too many panels into unreadable slides.
- DO NOT run full OCR or full supplement extraction without a reason.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
