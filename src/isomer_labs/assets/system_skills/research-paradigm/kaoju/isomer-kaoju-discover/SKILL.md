---
name: isomer-kaoju-discover
description: Use when a Kaoju survey needs broad field discovery, curated reference resolution, seed-direction expansion, version families, query provenance, or bounded selection decisions.
---

# Kaoju Discover

## Overview

Find relevant work through recorded routes and preserve the difference between a conceptual work, its versions, and linked implementation materials. Search rank, date, and citation count inform discovery but never decide inclusion alone.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `kaoju:discovery-ledger`, `kaoju:related-work-delta`, and `kaoju:curated-intake-delta` exactly. Return a storage blocker instead of inventing a path, profile, direct Markdown state, or untracked JSON.

## Workflow

1. **Accept the contract**. Require a Survey Contract, seeds or curated items, desired source classes, coverage bounds, and output purpose.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-discover --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Plan bounded routes**. Choose landscape queries, curated identity resolution, or backward, neighboring, forward, and post-seed expansion routes.
4. **Search five source classes**. Search papers, technical reports, source repositories, datasets, and models while treating papers and reports as primary related works.
5. **Normalize identities**. Group supported version families, record immutable material identities when available, and retain ambiguous relationships.
6. **Decide inclusion**. Record query or parent seed, route, relevance rationale, decision, reason, `latest_after`, `searched_through`, and achieved depth for every candidate.
7. **Write discovery outputs**. Produce a Discovery Ledger and candidate Related-Work Catalog or delta with unresolved identities and frontier limits.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-discover --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Report accepted output refs, blockers, and the acquire or examine handoff.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use for broad landscape discovery, priority handling of user-nominated sources, or expansion from named seed works. Do not use this skill to claim full-text inspection, execute code, download large materials, or synthesize final conclusions.

## Discovery Modes

| Mode | Required behavior |
| --- | --- |
| Landscape | Use multiple bounded queries, source classes, terminology variants, and representative routes. |
| Curated intake | Give every nominated item a stable intake id and a resolved identity attempt, but no automatic authority or inclusion. |
| Direction expansion | Trace backward, neighboring, forward, and post-seed work; record parent seed and route for each candidate. |

Each curated item ends as included, excluded, duplicate, or blocked. Each blocked item carries its attempted Source Identity and next resolution route.

## Reference Routing

Use `$isomer-kaoju-shared` for source identity, evidence, lineage, and terminal contracts. Send selected materials to `$isomer-kaoju-acquire` when access or checkout is required, and to `$isomer-kaoju-examine` for claim-bearing inspection.

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

## Common Mistakes

- Deduplicating different versions before deciding their relationship. Build the work family first.
- Omitting excluded items. Retain their reasons so later passes can audit coverage.
- Mixing linked repositories, datasets, and models into the primary paper list without type-aware relationships.
