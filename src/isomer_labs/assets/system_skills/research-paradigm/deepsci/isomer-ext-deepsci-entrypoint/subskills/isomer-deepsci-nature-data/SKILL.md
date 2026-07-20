---
name: isomer-deepsci-nature-data
description: Use when a manuscript needs a Nature-ready Data Availability statement, repository plan, dataset citation plan, FAIR metadata check, or author-facing data-sharing audit.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Research Nature Data

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-ext-deepsci-entrypoint->shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-ext-deepsci-entrypoint->shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-ext-deepsci-entrypoint->shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Nature Data maps every result-supporting dataset to an availability route before drafting prose. It inventories generated, processed, reused, restricted, source-data, software-output, model, table, image, and statistical-analysis materials, chooses repository and identifier strategy, drafts explicit statement text, and records missing fields without inventing accession details.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step references and copied source support files preserve the source skill's operative guidance while using native Isomer Research Topic, Research Inquiry, Research Task, Topic Workspace, and runtime-neutral handoff language.

## When to Use

Use this skill when:

- A Nature-family or high-impact journal manuscript needs a data availability statement.
- Datasets, source data, figure data, derived files, models, or statistical-analysis files need repository and identifier planning.
- The author needs FAIR metadata, license, provenance, embargo, or citation checks.
- Chinese author-facing data-availability notes need bilingual alignment.

Do not use this skill when:

- The task is general manuscript rewriting or statistics.
- No dataset inventory can be produced from available evidence.
- The requested statement would require inventing repositories, DOIs, access committees, licenses, approvals, or embargoes.
- The target journal policy has changed and has not been checked when the exact policy matters.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify journal and article type**. Produce `DEEPSCI:DATA-AVAILABILITY-CONTEXT` with target journal, article type, policy source, and author constraints. Read `references/policy-principles.md` and `references/source-basis.md` when exact rules matter.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-data --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Inventory datasets**. Produce `DEEPSCI:DATASET-INVENTORY` covering every dataset or source file supporting results, including raw, processed, figure source, secondary, restricted, model, table, image, and statistical-analysis data.
4. **Classify access routes**. Produce `DEEPSCI:DATA-ACCESS-CLASSIFICATION` for each dataset: public repository, controlled access, paper/supplement, reused public source, third-party restricted, request-based, or not applicable.
5. **Choose repository strategy**. Produce `DEEPSCI:REPOSITORY-STRATEGY` before drafting text, including repository candidates, identifiers, versioning, embargo, license, accession, and dataset citation needs. Read `references/repository-and-identifiers.md`.
6. **Draft data availability text**. Produce `DEEPSCI:DATA-AVAILABILITY-STATEMENT` using `references/statement-patterns.md`, mapping every dataset class to a concrete location, restriction, or action.
7. **Add dataset citation actions**. Produce `DEEPSCI:DATASET-CITATION-ACTIONS` for public and reused datasets, including formal dataset citations and missing identifier work.
8. **Run FAIR metadata audit**. Produce `DEEPSCI:FAIR-METADATA-AUDIT` using `references/fair-metadata-checklist.md`, covering metadata, README, file organization, license, provenance, and reuse clarity.
9. **Return ready text or blocker**. If fields are confirmed, return ready-to-paste text and actions. Otherwise produce `DEEPSCI:DATA-AVAILABILITY-BLOCKER` with author confirmations, missing identifiers, risk flags, and Chinese author-facing questions when useful via `references/chinese-author-alignment.md`.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-nature-data --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
11. **Close the operation set**. After end callbacks, invoke `isomer-ext-deepsci-entrypoint->shared`, follow its Operation Set Closeout reference, and invoke `isomer-op-entrypoint->operation-sets`. When material operation-set files exist, accept and verify every disposition, require a `complete` receipt, and return the receipt id with durable record refs; treat a path, rendered file, Git commit, or terminal prose as unavailable for handoff. When no operation set was opened and only durable records were used, return `closeout: not_applicable` with those refs. If closeout is partial, stale, or invalid, return `paused` with accepted refs, the partial receipt when present, diagnostics, and the exact resume command.

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
- Blocked states must name the missing evidence, author input, runtime capability, or route decision rather than hiding the blocker behind polished prose.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Dataset route coverage: fraction of result-supporting datasets with a public, controlled, reused-source, request-based, supplementary, or explicit blocked availability route; higher is better.
- FAIR metadata coverage: fraction of required findability, accessibility, interoperability, reusability, license, provenance, README, and DataCite-style fields completed or explicitly blocked; higher is better.

### Checks

- Evidence check: all claims, figures, tables, responses, or statements are traceable to source evidence or explicitly marked as missing.
- Route check: the next skill route is named when this skill cannot responsibly finish the task itself.
- Placeholder check: all handoff objects in the workflow appear in `migrate/placeholders.md`.
- Source-preservation check: source logic remains auditable in `org/src/` and `org/analysis/analysis-of-nature-data.md`.
- Paper-hygiene check: manuscript-facing output excludes route-control wording, local runtime details, and unsupported certainty.

## Reference Routing

Read these pages as needed:

- `references/policy-principles.md` for Nature/Springer Nature data-sharing principles and edge cases.
- `references/source-basis.md` for which official source supports which rule.
- `references/repository-and-identifiers.md` for repository, accession, DOI, embargo, version, and citation guidance.
- `references/statement-patterns.md` for ready-to-adapt statement patterns.
- `references/fair-metadata-checklist.md` for FAIR metadata, README, license, provenance, and DataCite checks.
- `references/chinese-author-alignment.md` for Chinese terminology and author-facing intake questions.

## Exit Criteria

This skill can end when all applicable checks are true:

- Every result-supporting dataset has an availability route or explicit blocker.
- `DEEPSCI:DATA-AVAILABILITY-STATEMENT` does not invent repositories, identifiers, licenses, or approvals.
- `DEEPSCI:FAIR-METADATA-AUDIT` and `DEEPSCI:DATASET-CITATION-ACTIONS` record remaining actions.

## Guardrails

- DO NOT use available on request as a default instead of a justified exception.
- DO NOT invent accession numbers, DOIs, embargoes, licenses, or ethics approvals.
- DO NOT write polished prose before repository strategy is clear.
- DO NOT ignore target journal instructions when exact policy matters.
- DO NOT let data availability become a general manuscript rewrite task.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
