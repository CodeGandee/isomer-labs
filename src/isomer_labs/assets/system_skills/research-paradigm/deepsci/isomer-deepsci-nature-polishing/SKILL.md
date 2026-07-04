---
name: isomer-deepsci-nature-polishing
description: Use when academic prose needs Nature-leaning polishing, restructuring, or translation without hiding weak evidence or inventing claims.
---

# Isomer Research Nature Polishing

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`, and request `--render markdown` only for the generated review view.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Nature Polishing edits argument before wording. It identifies paper type, diagnoses the failure mode, checks claim boundaries, exposes unsupported claims, rebuilds section logic, applies section-specific moves, polishes sentences, and returns revised text plus cautions when evidence is insufficient.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A manuscript section, abstract, title, paragraph, conclusion, or Chinese draft needs Nature-leaning English polish.
- The task requires restructuring argument flow before sentence-level editing.
- The draft may overclaim, mix Results and Discussion, bury the gap, or lack claim boundaries.
- The user wants polished text plus evidence-scope warnings.

Do not use this skill when:

- The user asks for new scientific claims from scratch.
- Evidence is missing for the requested claim and the user wants it hidden by prose.
- The task is full paper drafting from evidence; use `isomer-deepsci-write`.
- The task is reviewer-response routing; use `isomer-deepsci-rebuttal`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify paper type**. Produce `<PAPER_TYPE_DIAGNOSIS>` for the manuscript logic: research, method, hypothesis-driven, algorithmic, device, resource, review, or another justified type.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-polishing --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Diagnose failure mode**. Produce `<PROSE_FAILURE_DIAGNOSIS>`: wrong paper-type logic, missing gap, unsupported claim, evidence without interpretation, missing boundary, Results/Discussion mixing, weak title or abstract, or sentence clutter.
4. **Check claim boundary**. Produce `<CLAIM_BOUNDARY_CHECK>` from available evidence, citations, and user-provided context before polishing. If the claim is unsupported, produce `<POLISHING_EVIDENCE_BLOCKER>` instead of smoothing it over.
5. **Rebuild section logic**. Produce `<SECTION_LOGIC_REBUILD>` using `references/writing-strategy.md` and `references/section-moves.md`, fixing gap, claim, order, reader flow, and section-specific responsibilities.
6. **Apply section moves and phrase support**. Use `references/phrasebank-playbook.md` for hedging, transitions, evidence language, limitations, and future-work phrasing when needed.
7. **Polish sentences and paragraphs**. Produce `<POLISHED_MANUSCRIPT_TEXT>` with concise, calibrated, citation-aware prose while preserving the author meaning and evidence boundary.
8. **Run style guardrails**. Produce `<POLISHING_STYLE_QA>` using `references/style-guardrails.md`, checking register, mechanics, paragraph flow, article use, punctuation, AI/provenance hygiene, and claim calibration.
9. **Return revised text or caution**. Return the polished text with a compact diagnosis and any `<POLISHING_EVIDENCE_BLOCKER>` or claim-scope warning that must accompany the revision.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-polishing --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

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

- Long-sentence count: number of polished sentences longer than 30 words; lower is better.
- Claim-boundary violation count: number of polished claims whose strength exceeds the source evidence, author meaning, or known limitation boundary; lower is better.

### Checks

- Claim-boundary check: <CLAIM_BOUNDARY_CHECK> exists before polished claims are returned and marks any missing support, overclaim risk, or needed downgrade.
- Argument-order check: the rewrite addresses paper type, section job, paragraph logic, and claim/evidence/boundary fit before sentence-level polish.
- Source-fidelity check: <POLISHED_MANUSCRIPT_TEXT> preserves author meaning and does not invent data, references, mechanisms, methods, novelty, or conclusions.
- Style-QA check: <POLISHING_STYLE_QA> records sentence length, paragraph controlling idea, Results versus Discussion drift, citation hygiene, and AI-boundary risks when relevant.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, prompt state, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/writing-strategy.md` for paper architecture and argument strategy.
- `references/section-moves.md` for section-specific move orders and phrase patterns.
- `references/phrasebank-playbook.md` for hedging, transition, evidence, limitation, and future-work phrase families.
- `references/style-guardrails.md` for style, mechanics, paragraph, citation, and AI-boundary checks.

## Exit Criteria

This skill can end when all applicable checks are true:

- `<CLAIM_BOUNDARY_CHECK>` exists before polished claims are returned.
- `<POLISHED_MANUSCRIPT_TEXT>` preserves evidence limits and author meaning.
- `<POLISHING_STYLE_QA>` or `<POLISHING_EVIDENCE_BLOCKER>` records residual risks.

## Common Mistakes

- Inventing data, mechanisms, novelty, references, or claims.
- Using polished language to hide missing support.
- Letting AI author the core scientific argument from scratch.
- Skipping paper-type diagnosis before restructuring.
- Polishing Chinese or rough drafts sentence-by-sentence before rebuilding logic.
