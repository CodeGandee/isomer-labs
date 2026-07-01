---
name: isomer-rsch-nature-polishing-v2
description: Use when academic prose needs Nature-leaning polishing, restructuring, or translation without hiding weak evidence or inventing claims.
---

# Isomer Research Nature Polishing V2

## Overview

Nature Polishing edits argument before wording. It identifies paper type, diagnoses the failure mode, checks claim boundaries, exposes unsupported claims, rebuilds section logic, applies section-specific moves, polishes sentences, and returns revised text plus cautions when evidence is insufficient.

Placeholder definitions live in `migrate/placeholders.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A manuscript section, abstract, title, paragraph, conclusion, or Chinese draft needs Nature-leaning English polish.
- The task requires restructuring argument flow before sentence-level editing.
- The draft may overclaim, mix Results and Discussion, bury the gap, or lack claim boundaries.
- The user wants polished text plus evidence-scope warnings.

Do not use this skill when:

- The user asks for new scientific claims from scratch.
- Evidence is missing for the requested claim and the user wants it hidden by prose.
- The task is full paper drafting from evidence; use `isomer-rsch-write-v2`.
- The task is reviewer-response routing; use `isomer-rsch-rebuttal-v2`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify paper type**. Produce `<PAPER_TYPE_DIAGNOSIS>` for the manuscript logic: research, method, hypothesis-driven, algorithmic, device, resource, review, or another justified type.
2. **Diagnose failure mode**. Produce `<PROSE_FAILURE_DIAGNOSIS>`: wrong paper-type logic, missing gap, unsupported claim, evidence without interpretation, missing boundary, Results/Discussion mixing, weak title or abstract, or sentence clutter.
3. **Check claim boundary**. Produce `<CLAIM_BOUNDARY_CHECK>` from available evidence, citations, and user-provided context before polishing. If the claim is unsupported, produce `<POLISHING_EVIDENCE_BLOCKER>` instead of smoothing it over.
4. **Rebuild section logic**. Produce `<SECTION_LOGIC_REBUILD>` using `references/writing-strategy.md` and `references/section-moves.md`, fixing gap, claim, order, reader flow, and section-specific responsibilities.
5. **Apply section moves and phrase support**. Use `references/phrasebank-playbook.md` for hedging, transitions, evidence language, limitations, and future-work phrasing when needed.
6. **Polish sentences and paragraphs**. Produce `<POLISHED_MANUSCRIPT_TEXT>` with concise, calibrated, citation-aware prose while preserving the author meaning and evidence boundary.
7. **Run style guardrails**. Produce `<POLISHING_STYLE_QA>` using `references/style-guardrails.md`, checking register, mechanics, paragraph flow, article use, punctuation, AI/provenance hygiene, and claim calibration.
8. **Return revised text or caution**. Return the polished text with a compact diagnosis and any `<POLISHING_EVIDENCE_BLOCKER>` or claim-scope warning that must accompany the revision.

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

## Cross-Step Quality Gates

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
