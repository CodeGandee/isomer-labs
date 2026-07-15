---
name: isomer-kaoju-examine
description: Use when a Kaoju survey needs full-text or source inspection, exact locators, paper-code mapping, Source Digests, access blockers, contradictions, or Claim-Evidence Ledger updates.
---

# Kaoju Examine

## Overview

Inspect accepted materials at exact, repeatable locators and separate what the source states from what the agent infers. Source inspection raises evidence depth only to the level actually achieved.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `kaoju:source-digest`, `kaoju:source-access-blocker`, and `kaoju:claim-evidence-ledger` exactly. Return a storage blocker rather than inventing a path, profile, canonical Markdown file, or untracked JSON.

## When to Use

Use after discovery or acquisition when survey claims require direct paper, report, repository, dataset, or model inspection. Do not use this skill to infer execution success, repair code, perform a Run, or write final survey conclusions.

## Workflow

1. **Accept pinned materials**. Require Source Identities, material refs, target questions or claims, and desired verification depth.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-examine --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Inspect the authoritative source**. Read the relevant paper, report, source tree, dataset documentation, model metadata, evaluator, or configuration at exact locators. For a repository, bind every finding to Canonical External Repository ref, immutable commit, file, and line range.
4. **Map relationships**. Record paper-to-code, code-to-data, model-to-configuration, claim-to-experiment, and evaluator links only when evidence supports them.
5. **Extract evidence**. For papers, record page, section, symbol, figure, or table locators and inspect claim-driven figures and tables. Treat visual evidence as provisional until labels, caption, surrounding text, and underlying values or code support it. For code, keep observed implementation distinct from paper claims and executed behavior. Always separate the source statement from agent interpretation.
6. **Write outputs**. Produce a Source Digest or Source Access Blocker and update the Claim-Evidence Ledger with Evidence Item refs, depth, and verdict.
7. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-examine --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
8. **Return status**. Report achieved depth, unresolved claims, exact refs, blockers, and the next compare, reproduce, audit, or synthesis handoff.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Source Digest Contract

Record the Source Identity and work family, exact inspected locators, inspection method, source-stated claims, assumptions, method details, datasets and metrics, implementation mappings, contradictions, omissions, agent inferences labeled as such, achieved verification depth, evidence verdicts, and Evidence Item refs.

A Source Access Blocker records the requested identity, attempted locators and access routes, failure evidence, claims affected, partial evidence that remains usable, and bounded recovery route.

Source Digests are current-state records that the actor may inspect, refine, and approve. A revision preserves the prior digest and records its immediate source. Associated source code remains a separate verified relationship to a Canonical External Repository; it is never inferred from a matching name alone.

## Artifact Operations

Resolve `kaoju:source-digest` and `kaoju:claim-evidence-ledger` through `project artifacts describe`. Use `project artifacts put` for a new scoped digest or ledger and binding-permitted `project artifacts revise` for refinement. Let the service validate source and code locators and infer the managed structured content path.

## Reference Routing

Use `$isomer-kaoju-shared` for source identity, evidence, Artifact, lineage, and terminal contracts. Return executable questions to `$isomer-kaoju-reproduce`, comparison-ready evidence to `$isomer-kaoju-compare`, and unverified material needs to `$isomer-kaoju-acquire`.

## Foundational Principle

An exact locator makes an observation auditable; a plausible paraphrase does not. Label inference and absence instead of filling gaps.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The claim is standard in this field.” | Cite the inspected source or mark it as background inference. |
| “The code obviously implements the equation.” | Record the exact mapping and any unmatched steps. |
| “The missing detail is probably the default.” | Record `not stated` or `unclear`. |

## Red Flags

- A Source Digest has no page, section, symbol, file, line, revision, or equivalent exact locator.
- An abstract-only observation is described as full-text inspection.
- Paper and code identities are merged without relationship evidence.

## Operational Notes

- Record whether evidence supports, challenges, or leaves the claim inconclusive.
- Preserve both evidence paths and their identities.
- Record a Source Access Blocker so the audit can distinguish coverage from access.

## Guardrails

- DO NOT copy source claims into the ledger without a verdict.
- DO NOT omit contradictions.
- DO NOT treat inaccessible material as excluded.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
