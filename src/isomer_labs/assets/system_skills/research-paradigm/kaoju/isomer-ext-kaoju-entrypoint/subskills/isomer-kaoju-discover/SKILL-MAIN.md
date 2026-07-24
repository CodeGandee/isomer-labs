---
name: isomer-kaoju-discover
description: Use when a Kaoju survey needs broad field discovery, curated reference resolution, seed-direction expansion, version families, query provenance, or bounded selection decisions.
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

# Kaoju Discover

## Overview

Find relevant work through recorded routes and preserve the difference between a conceptual work, its versions, and linked implementation materials. Search rank, date, and citation count inform discovery but never decide inclusion alone.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:DISCOVERY-LEDGER`, `KAOJU:RELATED-WORK-DELTA`, and `KAOJU:CURATED-INTAKE-DELTA` exactly. Return a storage blocker instead of inventing a path, profile, direct Markdown state, or untracked JSON.

Portfolio reminder: papers, reports, repositories, datasets, models, search routes, reading-list entries, and related-work candidates are survey material, not Research Ideas. Invoke `isomer-op-entrypoint->research-ideas` only when an actor explicitly promotes a distinct durable direction or when starting focused work justifies an `exploring` transition on an existing Direction Set idea with an exact Research Task ref.

## When to Use

Use for broad landscape discovery, priority handling of user-nominated sources, or expansion from named seed works. Do not use this skill to claim full-text inspection, execute code, download large materials, or synthesize final conclusions.

## Workflow

1. **Accept the contract**. Require a Survey Contract, seeds or curated items, desired source classes, coverage bounds, output purpose, and any actor-supplied Reading List count request.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-discover --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Plan bounded routes**. Own landscape strategy, terminology variants, source-class coverage, seed selection, and backward, neighboring, forward, and post-seed expansion plans. Route paper identity lookup, paper queries, citation retrieval, citation-neighborhood traversal, and adjacent-paper retrieval through `isomer-ext-kaoju-entrypoint->paper-search` with purpose, evidence-use intent, expected normalized fields, direction, filters, and bounds.
4. **Resolve a Reading List target when requested**. With no count, use three priority and three secondary works. For category counts, accept non-negative integers and default an omitted category to three. For one positive total `N`, use `(N + 1) // 2` priority and `N // 2` secondary. Ask for clarification before discovery when total and category modes are mixed, a count is invalid, or the effective target is empty.
5. **Search five source classes**. Search papers, technical reports, source repositories, datasets, and models while treating papers and reports as primary related works. Invoke `paper-search` for paper-specific retrieval and consume its normalized provider-output observation; retain non-paper retrieval with the applicable owner.
6. **Normalize identities**. Group supported version families, record immutable material identities when available, and retain ambiguous relationships.
7. **Decide inclusion**. Record query or parent seed, route, relevance rationale, decision, reason, `latest_after`, `searched_through`, and achieved depth for every candidate.
8. **Compose a direction reading list when requested**. Keep exactly one direction scope per list. Reach the effective priority and secondary targets across five source classes, anchored by papers or technical reports. Include stable links, source type, one-line relevance, summary, planned depth, query provenance, version family, disposition, priority, and blocker recovery. Record `target_counts` with its `default`, `user-total`, or `user-categories` basis and record `achieved_counts`; a `user-total` target also records `requested_total`. A shortage against the effective target is a preserved warning, not a blocker.
9. **Write discovery outputs**. Produce a Discovery Ledger and candidate Related-Work Catalog, delta, curated intake delta, or Reading List with unresolved identities and frontier limits. Human nominations use the normal identity and disposition path.
10. **Support inspection and refinement**. Render the current scoped Reading List from the state DB, present effective and achieved category counts, accept additions, removals, thread expansion, target revision, or shorter-list approval, and revise the same scoped object with actor approval and lineage.
11. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-discover --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
12. **Return status**. Report accepted output refs, effective and achieved counts, shortage warnings, blockers, approval posture, and the acquire or examine handoff.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Discovery Modes

| Mode | Required behavior |
| --- | --- |
| Landscape | Use multiple bounded queries, source classes, terminology variants, and representative routes. |
| Curated intake | Give every nominated item a stable intake id and a resolved identity attempt, but no automatic authority or inclusion. |
| Direction expansion | Trace backward, neighboring, forward, and post-seed work; record parent seed and route for each candidate. |

Each curated item ends as included, excluded, duplicate, or blocked. Each blocked item carries its attempted Source Identity and next resolution route.

Every Discovery Ledger entry records the query text or seed, provider or access method, route, search time and `searched_through` date, resolved identity, version family, disposition and reason, achieved depth, and coverage limits. Search convergence is a bounded observation, not proof of completeness.

## Artifact Operations

Resolve each produced semantic id with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Use `project artifacts put` for append-only deltas and new scoped objects and `project artifacts revise` for a current Reading List or catalog update; never repeat or override inferred record kind, profile, label, scope, or locator fields.

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for source identity, evidence, lineage, and terminal contracts. Use `isomer-ext-kaoju-entrypoint->paper-search` for bounded paper retrieval while this skill retains strategy, cross-source coverage, candidate disposition, version families, Reading List composition, and sole ownership of Discovery Ledger and existing discovery deltas. Send selected materials to `isomer-ext-kaoju-entrypoint->acquire` when access or checkout is required, and to `isomer-ext-kaoju-entrypoint->examine` for claim-bearing inspection.

## Foundational Principle

Discovery proves that a candidate was found under a recorded route. It does not prove the candidate's claims, quality, relationship, or reproducibility.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The first results define the field.” | Expand terminology and routes within the Survey Contract. |
| “The newest work is most relevant.” | Record relevance against the survey question and evidence, not date alone. |
| “The repository title matches the paper.” | Preserve the relationship as unresolved until source evidence supports it. |

## Red Flags

- A candidate has no query or parent-seed provenance.
- “Exhaustive” or “all works” appears without a defensible bounded universe.
- A mutable release label is treated as immutable identity.

## Operational Notes

- Build the work family first.
- Retain their reasons so later passes can audit coverage.

## Guardrails

- DO NOT deduplicate different versions before deciding their relationship.
- DO NOT omit excluded items.
- DO NOT mix linked repositories, datasets, and models into the primary paper list without type-aware relationships.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
