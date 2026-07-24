---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Landscape Pass

## Workflow

1. **Frame**. Use `isomer-ext-kaoju-entrypoint->workspace` and `isomer-ext-kaoju-entrypoint->frame` to accept a Survey Contract with field boundary, five source classes, coverage date, depth, outputs, resources, and stop conditions.
2. **Discover**. Use `isomer-ext-kaoju-entrypoint->discover` for strategy, version families, query provenance, inclusion decisions, and type-aware links across papers, technical reports, source repositories, datasets, and models. Discover invokes `isomer-ext-kaoju-entrypoint->paper-search` for bounded paper lookup and citation retrieval and retains durable discovery ownership.
3. **Acquire selectively**. Use `isomer-ext-kaoju-entrypoint->acquire` only for materials needed to reach the accepted inspection depth.
4. **Examine**. Use `isomer-ext-kaoju-entrypoint->examine` to create Source Digests and Claim-Evidence Ledger entries at exact locators.
5. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` to check coverage, identity, provenance, depth, and claim traceability.
6. **Synthesize**. If the Audit Report is accepted, use `isomer-ext-kaoju-entrypoint->synthesize` to produce the Related-Work Catalog, Field Summary, Claim Status Table, and remaining frontier.
7. **Stop**. Return this bounded procedure's terminal report without selecting another procedure internally. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded stage plan from these skills while preserving audit before synthesis.

## Trigger

Use when the user wants a broad understanding of a field, problem, technique, or representative work, including a list of related works and a summary.

## Inputs

Require the survey question or seed, boundary or clarification mode, desired audience and depth, coverage date, resource envelope, and accepted prior refs. Papers and technical reports are primary related works; repositories, datasets, and models remain typed implementation or evidence links.

## Outputs

- Survey Contract and Discovery Ledger refs.
- Version-aware Related-Work Catalog with inclusion and exclusion evidence.
- Source Digests and Claim-Evidence Ledger refs for representative works.
- Accepted Audit Report, Field Summary, Claim Status Table, and Kaoju Dossier or bounded subset.
- `searched_through`, coverage limits, unresolved access blockers, and remaining frontier.

## Stop Conditions

Stop when the accepted coverage and representative-depth conditions are met, or return `paused` or `blocked` when access, resources, Gates, or material ambiguity prevents them. Never call the survey exhaustive unless the Survey Contract defines a finite, verifiable universe.

## Guardrails

- DO NOT let code search replace literature search.
- DO NOT read every candidate deeply before triage.
- DO NOT hide excluded candidates or query provenance.
