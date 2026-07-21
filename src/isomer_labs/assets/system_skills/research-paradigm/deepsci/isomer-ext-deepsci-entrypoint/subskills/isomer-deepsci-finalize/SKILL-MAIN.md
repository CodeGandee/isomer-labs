---
name: isomer-deepsci-finalize
description: Use when a Research Topic or Research Inquiry is ready to close, pause, archive, publish, or hand off with final claims, limitations, recommendations, and a clean resume path.
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

# Isomer Research Finalize

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-ext-deepsci-entrypoint->shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-ext-deepsci-entrypoint->shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-ext-deepsci-entrypoint->shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Idea-recording reminder: invoke `isomer-op-entrypoint->research-ideas` when finalization supports, refutes, defers, closes, reopens, supersedes, or follows up a durable concept. Commit explicit evidence and decision facet transitions with terminal refs, closure reasons, a durable decision ref when applicable, and exact object-valued realizations. Preserve the concept for resume-state changes; introduce another idea and justified lineage only for a distinct follow-up direction. Final summaries, claim ledgers, resume packets, and rendered Markdown are not idea realizations.

Finalize closes or pauses work responsibly. It consolidates accepted evidence, records claim status and limitations, chooses stop, park, publish, or continue-later routing, and refuses closure when evidence or writing gates still block it.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

## When to Use

Use this skill when:

- The evidence base is stable enough for a final recommendation.
- The user asks for final summary, closure, archive, or handoff.
- A paper, report, or long-running route needs final claim and limitation status.
- A topic should pause with a clean resume packet.

Do not use this skill when:

- Major evidence gaps remain unresolved.
- The current line obviously needs another experiment, analysis, baseline, or idea pass.
- The paper or bundle gates are not submission-ready but finalization is being used to avoid repair.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Gather closure context**. Build DEEPSCI:FINALIZE-CONTEXT-BRIEF from accepted comparator state, runs, analysis, writing state, decisions, blockers, package or paper manifests, and the canonical parents for any closure records. Read `references/closure-gate.md`, `references/finalization-checklist.md`, and `isomer-ext-deepsci-entrypoint->shared` for the inventory gates.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-finalize --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Check closure legitimacy**. If required evidence, writing, review, proofing, or submission gates fail, create DEEPSCI:FINALIZE-BLOCKER-RECORD or route to decision instead of forcing closure. Read `references/closure-gate.md`.
4. **Build the claim ledger**. Classify every important claim in DEEPSCI:CLAIM-LEDGER as supported, partially supported, unsupported, or deferred with evidence and caveats. Read `references/claim-ledger-template.md`.
5. **State limitations and failures**. Create DEEPSCI:FINAL-LIMITATIONS-REPORT including data, metric, implementation, resource, literature, and unsupported-claim limits. Read `references/final-summary-template.md` and `references/finalization-checklist.md`.
6. **Write final state**. Produce DEEPSCI:FINAL-SUMMARY and DEEPSCI:RESUME-PACKET when continuation is plausible, using `derived_from` lineage from claim ledger, limitations, and package state. Read `references/final-summary-template.md` and `references/resume-packet-template.md`.
7. **Choose closure route**. Record DEEPSCI:CLOSURE-DECISION and preserve DEEPSCI:FINALIZE-CONTINUITY-UPDATE for stop, park-and-continue-later, publish-and-continue, archive, or route-back decisions, linking them with `follow_up_to` lineage from final summary or blocker records. Read `references/resume-packet-template.md` and `references/checkpoint-memory-template.md`.
8. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-finalize --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
9. **Close the operation set**. After end callbacks, invoke `isomer-ext-deepsci-entrypoint->shared`, follow its Operation Set Closeout reference, and invoke `isomer-op-entrypoint->operation-sets`. When material operation-set files exist, accept and verify every disposition, require a `complete` receipt, and return the receipt id with durable record refs; treat a path, rendered file, Git commit, or terminal prose as unavailable for handoff. When no operation set was opened and only durable records were used, return `closeout: not_applicable` with those refs. If closeout is partial, stale, or invalid, return `paused` with accepted refs, the partial receipt when present, diagnostics, and the exact resume command.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/closure-gate.md` for prevent premature finalization.
- `references/claim-ledger-template.md` for classify final claim status.
- `references/final-summary-template.md` for write the responsible end-state summary.
- `references/resume-packet-template.md` for leave a clean continuation path.
- `references/finalization-checklist.md` for closure checklist, package inventory, and anti-pattern gates.
- `references/checkpoint-memory-template.md` for pause-ready or continue-later checkpoint continuity notes.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Closure blocker count: number of unresolved evidence, writing, review, proofing, submission, package, or route blockers that still prevent honest closure; lower is better.
- Claim-ledger coverage: fraction of important outcomes classified as supported, partially supported, unsupported, or deferred with evidence paths and caveats; higher is better.

### Checks

- Context check: DEEPSCI:FINALIZE-CONTEXT-BRIEF inventories accepted comparator state, runs, analysis, writing state, decisions, blockers, and package or paper manifests before closure judgment.
- Legitimacy check: DEEPSCI:FINALIZE-BLOCKER-RECORD or route-back decision exists whenever required evidence, writing, review, proofing, or submission gates fail.
- Claim check: DEEPSCI:CLAIM-LEDGER preserves important claims, caveats, evidence, and downgrade history instead of silently deleting weakened beliefs.
- Limitation check: DEEPSCI:FINAL-LIMITATIONS-REPORT records data, metric, implementation, resource, literature, reproducibility, and unsupported-claim limits.
- Recommendation check: DEEPSCI:CLOSURE-DECISION states stop, park-and-continue-later, publish-and-continue, archive, or route-back with the evidence and reopen condition.
- Resume check: DEEPSCI:RESUME-PACKET or DEEPSCI:FINALIZE-CONTINUITY-UPDATE tells a later agent what to read first, what not to repeat, and which route remains open.

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
