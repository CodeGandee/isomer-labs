---
name: isomer-kaoju-paper-search
description: Use when a Kaoju task needs bounded paper identity resolution, topic search, citation retrieval, citation-neighborhood traversal, or adjacent-paper retrieval through a resolved Literature Provider Binding.
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

# Kaoju Paper Search

## Overview

Own bounded paper retrieval while keeping survey strategy, selection, material access, source inspection, and evidence acceptance with their existing Kaoju owners. Resolve one provider-neutral action, execute it through an agent-available external tool under the selected Literature Provider Binding, normalize the result, and record one normalized provider-output observation as one Artifact for the logical action.

Read `isomer-ext-kaoju-entrypoint->shared` for family-wide evidence, Gate, Artifact, provenance, and terminal rules. Read only the selected command page plus `references/provider-selection.md`, `references/result-contract.md`, `references/execution-and-errors.md`, and the chosen bundle-local approach.

## When to Use

Use for a direct bounded paper-search task or when `discover`, `acquire`, or another declared caller needs paper lookup, target resolution, forward or backward citation retrieval, bounded citation-neighborhood traversal, or adjacent-paper retrieval. Do not use this skill for discovery strategy, inclusion judgment, Reading List composition, material acquisition, full-text examination, or claim-bearing evidence acceptance.

## Workflow

1. **Accept one logical action**. Require the research purpose, evidence-use intent, query, target, or seeds, direction, date range, normalized fields, bounds, stop conditions, and downstream owner.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-paper-search --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Load shared contracts**. Use `isomer-ext-kaoju-entrypoint->shared` for evidence, Gate, provenance, and terminal posture. Provider output remains orientation or scouting material until an existing owner accepts it.
4. **Load the action page**. Read exactly one page from the Actions table and resolve relative dates into an explicit inclusive date or year range before provider execution.
5. **Resolve provider selection**. Apply `references/provider-selection.md`. Honor the Literature Provider Binding, an explicit compatible approach request, credential and Gate policy, and a reduced or blocked posture when no external approach is available.
6. **Resolve bounds and execution policy**. Apply `references/execution-and-errors.md`. Default graph depth to one hop, declare every result, page, node, per-node, depth, retry, and resource bound, and prevent cycles by resolved provider identity.
7. **Execute outside Isomer data services**. Use an available external provider-native or general-purpose CLI, or a bounded direct-HTTPS tool when policy permits. Do not ask `isomer-cli` to search, resolve, recommend, fetch citations, fetch references, or normalize provider responses.
8. **Normalize the provider output**. Apply `references/result-contract.md`. Preserve target and candidate identity, parent seed, citation direction, filters, pagination, filtering location, completeness, missing fields, null or unresolved records, successful partial pages, limitations, and provider provenance without inventing metadata.
9. **Record one observation**. Consolidate the complete or partial logical action into one `isomer-literature-provider-observation.v1` payload and run `isomer-cli --print-json ext research literature record --payload-file OBSERVATION.json --topic <topic>`. Raw responses are optional redacted file-backed attachments and are never required for validation or indexing.
10. **Hand off without promotion**. Give normalized observation refs to `discover` for strategy and disposition, to `acquire` for selected material access, and to `examine` for exact source inspection. Do not write their durable outputs.
11. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-paper-search --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
12. **Return terminal status**. Report `complete`, `paused`, or `blocked`; action and provider; requested and applied bounds; observation ref; complete, truncated, or partial posture; limitations; Gate or credential posture; downstream owner; and exact continuation point.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use your native planning tool to build a bounded step-by-step plan from the action contract, supplied context, and requested output, then execute it.

## Subcommands

| Action | Required Input | Result Posture | Internal Designator | Detail |
| --- | --- | --- | --- | --- |
| `resolve-paper` | Stable identifier, publication URL, title, or distinguishing metadata | One resolved target, explicit ambiguity, or unresolved posture | `isomer-ext-kaoju-entrypoint->paper-search->resolve-paper()` | `commands/resolve-paper.md` |
| `search-papers` | Topic or metadata query plus filters and result bounds | Bounded candidate set with query provenance | `isomer-ext-kaoju-entrypoint->paper-search->search-papers()` | `commands/search-papers.md` |
| `find-citing-papers` | Resolved target plus forward-search bounds | Provider-reported edges from citing papers to the target | `isomer-ext-kaoju-entrypoint->paper-search->find-citing-papers()` | `commands/find-citing-papers.md` |
| `explore-cited-papers` | Resolved target plus backward-search bounds | Provider-reported edges from the target to cited papers | `isomer-ext-kaoju-entrypoint->paper-search->explore-cited-papers()` | `commands/explore-cited-papers.md` |
| `trace-citation-neighborhood` | Resolved seeds, direction, depth, node, per-node, and page bounds | Cycle-safe bounded graph frontier | `isomer-ext-kaoju-entrypoint->paper-search->trace-citation-neighborhood()` | `commands/trace-citation-neighborhood.md` |
| `find-related-papers` | Positive seeds, optional negative seeds, filters, and result bound | Non-citation adjacent-paper candidates tied to their seeds | `isomer-ext-kaoju-entrypoint->paper-search->find-related-papers()` | `commands/find-related-papers.md` |

## Evidence Boundary

A normalized literature observation proves only what the selected provider reported at the recorded time and bounds. Citation edges remain provider-reported. Paper metadata, citation contexts, recommendation rank, and influence labels do not establish a Research Claim, full-text relationship, quality judgment, or reproducibility result.

`isomer-kaoju-discover` remains the sole producer of the Discovery Ledger, Reading List, Related-Work Catalog Delta, and Curated Source Intake Delta. `isomer-kaoju-acquire` owns material access and immutable identity. `isomer-kaoju-examine` owns exact source inspection, Source Digests, Findings, and accepted Evidence Item links.

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for family-wide evidence, Gate, Artifact, provenance, callback, and terminal contracts. Read `references/provider-selection.md`, `references/result-contract.md`, and `references/execution-and-errors.md` for every action, then load exactly one compatible page under `references/approaches/`. Return normalized observation refs to the requesting owner without assuming that owner’s selection, acquisition, examination, or durable-output authority.

## Guardrails

- DO NOT present provider operations as the public paper-search action model.
- DO NOT silently substitute a provider when the actor requested a specific unavailable approach.
- DO NOT traverse an ambiguous target or an unbounded graph.
- DO NOT describe a bounded, truncated, partial, or locally filtered result as exhaustive.
- DO NOT put credentials, authorization headers, secret query values, or unredacted provider responses in chat, commands shown to users, logs, Artifacts, or Provenance Records.
- DO NOT create a Reading List, Discovery Ledger, Source Digest, Finding, or Evidence Item for a direct bounded search.
- DO NOT invoke or normalize a provider response through `isomer-cli`; use `ext research literature` only for normalized local data.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome and state the action, scope, observation ref, completeness, limitations, and handoff. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
