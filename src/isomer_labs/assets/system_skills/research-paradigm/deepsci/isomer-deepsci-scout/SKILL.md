---
name: isomer-deepsci-scout
description: Use when a Research Topic or Research Inquiry lacks enough framing, metric clarity, literature orientation, benchmark context, or comparator direction to route into baseline, idea, experiment, decision, or closure work.
---

# Isomer Research Scout

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Scout makes an unclear research situation concrete enough to choose the next route. It resolves only the framing unknowns that can change downstream work, records the result as semantic handoff material, and stops once baseline, idea, Decision Record, Gate, or blocker routing is clear.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

## When to Use

Use this skill when:

- The Research Topic, Research Inquiry, or Research Task is still ambiguous.
- The dataset, split, benchmark, primary metric, or fair-comparison rule is unclear.
- No trustworthy comparator direction has been identified.
- The paper, repository, or benchmark neighborhood is too thin to route with confidence.
- A paused topic needs framing reconstruction before deeper work resumes.
- The next route is blocked by ambiguity rather than implementation, execution, or verification.

Do not use this skill when:

- The task frame, comparator, dataset, metric contract, and scope are already fixed.
- A validated comparator exists and the work is ready for `isomer-deepsci-idea`, `isomer-deepsci-experiment`, or `isomer-deepsci-analysis`.
- The real blocker is command execution, environment repair, implementation, or verification rather than framing.
- The user asks for exhaustive literature review after the next route is already clear.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Check entry fit**. Use **Entry Signals**, **Pre-Scout Gate**, and `references/operational-guidance.md` to decide whether scout should run or route directly to another production DeepSci skill.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-scout --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Reconstruct the current frame**. Build `<SCOUT_CONTEXT_BRIEF>` from user constraints, Workspace Runtime records, Artifacts, Evidence Items, Findings, Decision Records, and local repository context. Read `references/operational-guidance.md` for the context quality gate.
4. **Reuse prior knowledge first**. Build `<SCOUT_MEMORY_REUSE_NOTE>` from available Workspace Runtime or source-compatible prior-knowledge retrieval before broad discovery. Read `references/operational-guidance.md` and `references/paper-triage-playbook.md` before opening external discovery.
5. **Name the minimum unknowns**. Produce `<SCOUT_MINIMUM_UNKNOWNS>` with only questions that can change baseline, idea, Decision Record, Gate, or blocker routing. Read `references/operational-guidance.md` for unknown classification constraints.
6. **Search the unresolved neighborhood**. Use **Discovery Discipline**, `references/paper-triage-playbook.md`, and `references/literature-scout-template.md` to produce `<SCOUT_DISCOVERY_LEDGER>` only when local evidence cannot settle route-changing unknowns.
7. **Clarify route-facing outputs**. Produce or revise `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<LITERATURE_SCOUTING_REPORT>` when those objects are needed by the next route. Read `references/eval-contract-template.md` and `references/baseline-shortlist-template.md`.
8. **Record the next route or blocker**. Return `<NEXT_ROUTE_DECISION>` when routing is clear, or `<SCOUT_BLOCKER_RECORD>` when missing input, conflicting contracts, or weak comparator candidates prevent a responsible route. Read `references/operational-guidance.md` for blocker and stop rules.
9. **Preserve continuity**. Create `<SCOUT_CONTINUITY_UPDATE>` for any reusable conclusion, changed route, literature lesson, metric caveat, or blocker before leaving scout. Read `references/operational-guidance.md` and `references/literature-scout-template.md` for durable-output requirements.
10. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-scout --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/operational-guidance.md` when the scout pass needs the full tactical workflow, continuity rules, blocked-state handling, or harness guidance.
- `references/paper-triage-playbook.md` when paper, repository, benchmark, or provenance discovery affects the route.
- `references/literature-scout-template.md` when external discovery materially changes the frame and must become `<LITERATURE_SCOUTING_REPORT>`.
- `references/eval-contract-template.md` when dataset, split, metric, fairness, useful-improvement threshold, evidence, or ambiguity must become `<EVALUATION_CONTRACT>`.
- `references/baseline-shortlist-template.md` when serious comparator candidates must become `<BASELINE_SHORTLIST>`.

## Entry Signals

Run scout only when at least one route-changing unknown remains after quick local context review:

- Task definition is too vague for a bounded Research Task.
- Dataset, benchmark, split, metric, or fair-comparison rule is unsettled.
- Candidate comparators exist but provenance, implementation availability, or metric compatibility is uncertain.
- Local Artifacts and Findings disagree with the user's apparent framing.
- Literature or repository context could change whether the next route is `isomer-deepsci-baseline`, `isomer-deepsci-idea`, `isomer-deepsci-decision`, a Gate, or a blocker.

Exit quickly when the frame is already explicit and the next route is obvious.

## Pre-Scout Gate

Before broad discovery, inspect available durable context in this order:

1. User-provided task description and explicit constraints.
2. Workspace Runtime records for the current Research Topic, Research Inquiry, Research Task, Runs, Gates, Decision Records, and Provenance Records.
3. Artifacts, Evidence Items, Findings, comparator records, and literature notes.
4. Topic Main Development Repository docs and benchmark or evaluation docs.
5. Prior memory or compatibility memory results.

If this context already yields a stable `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<NEXT_ROUTE_DECISION>`, record the decision and stop instead of searching.

## Discovery Discipline

Use discovery only for unresolved questions that can change the next route. Prefer primary papers, official repositories, benchmark documentation, and provider-bound literature results over recollection or broad web summaries.

When current literature, repository state, or benchmark details may have changed, use available search or Literature Provider Binding surfaces. For source-compatible harness behavior, route legacy state, evidence, and shell-tool calls through `isomer-cli ext deepsci call ... --input-json <json-object>` or the corresponding Execution Adapter Command Request, then status durable meaning with the placeholders in `migrate/placeholders.md`.

Search for disconfirming evidence as well as supportive evidence. Stop when the next route is clear, not when every adjacent paper has been collected.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Route-changing unknown count: number of unresolved framing unknowns that can still change baseline, idea, Decision Record, Gate, or blocker routing; lower is better.
- Evaluation-contract coverage: fraction of task, dataset, split, primary metric, metric direction, fair-comparison rule, useful-improvement threshold, evidence, and ambiguity fields that are explicit when relevant; higher is better.

### Checks

- Entry check: scout runs only when at least one route-changing unknown remains after quick local durable context review.
- Context check: <SCOUT_CONTEXT_BRIEF> makes the task frame, current comparator status, evidence state, and blockers explicit before discovery.
- Reuse check: <SCOUT_MEMORY_REUSE_NOTE> or an equivalent context note explains what prior knowledge was reused before broad search.
- Discovery check: <SCOUT_DISCOVERY_LEDGER> keeps only discoveries that affect task framing, evaluation contract, comparator direction, route choice, or blocker status.
- Handoff check: <EVALUATION_CONTRACT>, <BASELINE_SHORTLIST>, and <NEXT_ROUTE_DECISION> are explicit enough for the next production DeepSci skill, or <SCOUT_BLOCKER_RECORD> states what is missing and why it matters.
- Continuity check: <SCOUT_CONTINUITY_UPDATE> preserves reusable literature lessons, metric caveats, route changes, or blockers before leaving scout.

## Exit Criteria

Scout can end when all applicable checks are true:

- `<SCOUT_CONTEXT_BRIEF>` states the task frame clearly enough for the next route.
- `<EVALUATION_CONTRACT>` states task, dataset, split, metric direction, fair-comparison rule, and known ambiguities.
- `<BASELINE_SHORTLIST>` identifies at least one justified comparator route, or explains why idea work can proceed without more comparator scouting.
- `<NEXT_ROUTE_DECISION>` names `isomer-deepsci-baseline`, `isomer-deepsci-idea`, `isomer-deepsci-decision`, a Gate, a blocker, or another justified production DeepSci route.
- `<LITERATURE_SCOUTING_REPORT>` exists when external discovery materially changed the route.
- `<SCOUT_BLOCKER_RECORD>` exists when the frame cannot responsibly be completed.

## Guardrails

- DO NOT turn scout into an exhaustive survey instead of a route-setting stage.
- DO NOT ask the user routine technical questions before checking local durable evidence.
- DO NOT guess the metric, split, or comparator identity when local evidence is ambiguous.
- DO NOT repeat wide discovery when prior Artifacts, Findings, Decision Records, or memory already narrow the space.
- DO NOT write long paper summaries that do not change `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, or `<NEXT_ROUTE_DECISION>`.
- DO NOT inflate novelty when the apparent gap is already closed by standard engineering, straightforward scaling, or a strong recent result.
- DO NOT route to idea work before comparator trust is durable enough.
- DO NOT hide a blocked scout state behind generic literature commentary.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
