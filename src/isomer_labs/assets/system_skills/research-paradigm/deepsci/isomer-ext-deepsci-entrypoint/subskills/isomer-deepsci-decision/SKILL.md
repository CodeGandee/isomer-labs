---
name: isomer-deepsci-decision
description: Use when research work needs an explicit evidence-backed route choice, stop, branch, baseline reuse, writing, finalization, reset, or user-sensitive decision before continuing.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Research Decision

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-ext-deepsci-entrypoint->shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-ext-deepsci-entrypoint->shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-ext-deepsci-entrypoint->shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: when a decision selects, defers, closes, reopens, supersedes, collapses, or branches ideas, invoke `isomer-op-entrypoint->research-ideas`. Record the complete considered option set and authored outcomes, then correlate explicit facet transitions, closure reasons, exact realizations, generation membership, terminal refs, and justified lineage with the Decision Record. Use the exact structured source object, never rendered Markdown, as the realization source; do not compress the decision into status or infer rejected alternatives from prose.

Decision makes one route judgment from durable evidence, records the verdict and smallest valid action, then gets the Research Topic moving again. It does not substitute for state reconciliation when the active line is still unclear.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

## When to Use

Use this skill when:

- The next route is not obvious.
- Evidence is mixed or contradictory.
- A blocker needs an explicit route.
- A user preference, scope, cost, or publishability choice cannot be inferred safely.
- A line may need to stop, branch, reset, write, review, finalize, or reuse a comparator.

Do not use this skill when:

- The active state is too ambiguous and first needs intake or scout-style reconciliation.
- The next action is already obvious from durable evidence.
- The real task is baseline recovery, ideation, execution, or analysis rather than a route judgment.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check decision readiness**. Build DEEPSCI:DECISION-CONTEXT-BRIEF and confirm the current line, latest decisive result, and stale-route state are clear enough to judge. Read `references/operational-guidance.md` before judging readiness.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-decision --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **State the route question**. Record DEEPSCI:ROUTE-QUESTION with the real choice, strongest support, strongest contradiction, main risk, main cost, new evidence, and canonical parents from the result, blocker, or route state being judged. Read `references/research-route-criteria.md` and `isomer-ext-deepsci-entrypoint->shared` before evidence compression.
4. **Choose the smallest canonical action**. Use DEEPSCI:DECISION-EVIDENCE-PACKET to select one action from the canonical action set without hiding alternatives. When the action changes an idea, prepare the complete Decision Record option set, expected facet transitions, reason and rationale, terminal refs, exact realization refs, generation membership, and justified lineage before recording the verdict. Read `references/canonical-actions.md`, `references/research-route-criteria.md`, `isomer-op-entrypoint->research-ideas`, and `isomer-ext-deepsci-entrypoint->shared`.
5. **Record the verdict atomically**. Create DEEPSCI:ROUTE-DECISION-RECORD with verdict, action, reason, evidence, every considered option, next route, and record lineage. Commit the corresponding Research Idea decision options and justified selection, deferral, closure, reopening, branch, collapse, or `subsumes` effects in the same acceptance operation, then verify decision context and transitions. Read `references/strategic-decision-template.md`.
6. **Preserve the resume point**. Write DEEPSCI:DECISION-CHECKPOINT-MEMORY when the decision changes the active route, or create DEEPSCI:USER-DECISION-REQUEST or DEEPSCI:DECISION-BLOCKER-RECORD when local evidence cannot decide safely; use `revision_of` through the revise command for content-changing checkpoint updates. Read `references/checkpoint-memory-template.md` and `references/operational-guidance.md`.
7. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-decision --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
8. **Close the operation set**. After end callbacks, invoke `isomer-ext-deepsci-entrypoint->shared`, follow its Operation Set Closeout reference, and invoke `isomer-op-entrypoint->operation-sets`. When material operation-set files exist, accept and verify every disposition, require a `complete` receipt, and return the receipt id with durable record refs; treat a path, rendered file, Git commit, or terminal prose as unavailable for handoff. When no operation set was opened and only durable records were used, return `closeout: not_applicable` with those refs. If closeout is partial, stale, or invalid, return `paused` with accepted refs, the partial receipt when present, diagnostics, and the exact resume command.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/operational-guidance.md` for tactical route judgment, baseline reuse, user-input, blocker, and checkpoint rules.
- `references/canonical-actions.md` for use a stable action vocabulary so downstream stages know what changed.
- `references/research-route-criteria.md` for judge routes from evidence rather than optimism.
- `references/strategic-decision-template.md` for record a consequential route decision durably.
- `references/checkpoint-memory-template.md` for preserve a resume point after a route-changing decision.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Route-blocking unknown count: number of unresolved state, evidence, preference, scope, or cost unknowns that would change the chosen canonical action; lower is better.
- Rejected-alternative coverage: fraction of serious rejected alternatives or blockers in DEEPSCI:ROUTE-DECISION-RECORD with a decisive reason and evidence basis; higher is better.

### Checks

- Readiness check: DEEPSCI:DECISION-CONTEXT-BRIEF makes the current line, latest decisive result, and stale-route state clear enough to judge or routes to a reconciliation skill.
- Question check: DEEPSCI:ROUTE-QUESTION names the real decision, strongest support, strongest contradiction, main risk, main cost, and genuinely new evidence.
- Action check: the chosen canonical action is the smallest action that resolves the current state and does not hide a blocker behind vague continuation.
- Record check: DEEPSCI:ROUTE-DECISION-RECORD includes verdict, action, reason, evidence, rejected alternatives, and next route.
- User-decision check: DEEPSCI:USER-DECISION-REQUEST appears only when local evidence cannot safely resolve a real preference, scope, or cost choice.
- Continuity check: DEEPSCI:DECISION-CHECKPOINT-MEMORY or the next route record is explicit enough that later production DeepSci skills do not need to guess what changed.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later production DeepSci skills do not need to guess what changed or why.

## Guardrails

- DO NOT continue after the route, gate, or blocker is already clear.
- DO NOT replace evidence requirements with optimistic prose.
- DO NOT bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
