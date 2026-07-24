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

# Build Reading List

## Workflow

1. Resolve one accepted direction and its independent direction scope. Never merge several selected directions into one implicit list.
2. Resolve the target request before discovery. With no count, target three priority and three secondary works. For category counts, use each supplied non-negative integer and default an omitted category to three. For one positive total `N`, target `(N + 1) // 2` priority and `N // 2` secondary works. Ask for clarification before discovery when the request mixes total and category modes, uses invalid counts, or produces an empty target.
3. Use `isomer-ext-kaoju-entrypoint->discover` to plan search strategy across papers, technical reports, repositories, datasets, and models while treating papers and reports as primary works. For paper identity, query, citation, or adjacent-paper retrieval, discover invokes `isomer-ext-kaoju-entrypoint->paper-search` with purpose, evidence-use intent, normalized fields, direction, filters, and bounds, then records query or seed, provider or access method, route, searched-through date, identity resolution, version family, disposition, and coverage limits in the Discovery Ledger.
4. Reach the effective priority and secondary targets. Preserve inaccessible or unresolved targets as blockers; use bounded backfill without hiding shortages.
5. Deduplicate versions by work family while retaining exact version identities and relationships.
6. Present the list for inspection and refinement. Report the effective and achieved category counts. A short list may be approved with a non-blocking shortage warning against the effective target.
7. Persist `KAOJU:READING-LIST` as a scoped current-state Artifact with `target_counts` and `achieved_counts`, then checkpoint the Run. Record the target basis as `default`, `user-total`, or `user-categories`, and record `requested_total` for `user-total`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->discover`. Inputs: accepted `KAOJU:DIRECTION-SET`, direction id, Survey Contract, provider bindings, and optional target-count request. Outputs: scoped Reading List and Discovery Ledger refs.

## Gates, Blockers, and Resume

Human approval is required. Provider failure, source-access limits, unresolved identity, or binding failure records blockers. Resume at discovery, backfill, refine, or approve without discarding prior query provenance.
