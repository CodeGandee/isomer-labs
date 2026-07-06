---
name: isomer-deepsci-experiment
description: Use when a selected hypothesis or route, accepted comparator basis, and evaluation contract are ready for one bounded implementation or measured run.
---

# Isomer Research Experiment

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Experiment turns one selected route into one interpretable measured result. It locks a run contract, changes only what the hypothesis needs, preserves command and metric evidence, records the result, and routes from the evidence.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

## When to Use

Use this skill when:

- A selected hypothesis or route is ready for implementation.
- Comparator basis and evaluation contract are explicit.
- The task needs a main evidence-producing run rather than framing, baseline recovery, route selection, or follow-up analysis.
- Algorithm-first work needs a measured result for frontier review.

Do not use this skill when:

- The comparator gate is unresolved.
- The idea or route still has unresolved tradeoffs.
- The need is writing, follow-up analysis, or explicit route choice rather than a main run.
- The work is open-ended optimization rather than one bounded measured test.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Lock the run contract**. Recover <EXPERIMENT_CONTEXT_BRIEF>, accepted comparator basis, selected hypothesis, dataset, split, metric keys, stop condition, abandonment condition, budget, expected outputs, and route linkage, then create <EXPERIMENT_CONTRACT> with `follow_up_to` or `derived_from` lineage from the selected hypothesis and route decision. Read `references/experiment-contract.md`, `references/main-experiment-plan-template.md`, `references/evidence-ladder.md`, and `isomer-deepsci-shared/references/artifact-lineage-recording.md` before code or compute work starts.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-experiment --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Prepare the control surface**. Create or refresh <EXPERIMENT_PLAN> and <EXPERIMENT_CHECKLIST> when the run is non-trivial, expensive, branch-sensitive, or long-running. Read `references/main-experiment-plan-template.md`, `references/main-experiment-checklist-template.md`, and `references/operational-guidance.md` for the required fields and update cadence.
4. **Map and implement the minimum change**. Write <IMPLEMENTATION_CHANGE_MAP>, keep the comparator reference read-only, and change only what the hypothesis needs. Read `references/execution-playbook.md` for preflight, workspace, implementation, retry, and diagnosis rules.
5. **Run only useful smoke checks**. Create <SMOKE_CHECK_RECORD> only when command path, output schema, evaluator wiring, or implementation risk is still uncertain. Read `references/execution-playbook.md` and update <EXPERIMENT_CHECKLIST> before launching the main run.
6. **Execute and monitor honestly**. Run the real bounded attempt through the proper Execution Adapter, preserve commands, configs, logs, outputs, seeds, environment facts, and last-known-good state in <MAIN_RUN_RECORD>, and link the run to <EXPERIMENT_CONTRACT> with `derived_from` lineage. Read `references/execution-playbook.md` and `references/operational-guidance.md`.
7. **Validate and record the result**. Produce <EXPERIMENT_RESULT_SUMMARY>, <CLAIM_VALIDATION_RECORD>, and <EXPERIMENT_ARTIFACT_MANIFEST> with metric completeness, finite values, comparability, claim update, baseline relation, failure mode, caveats, exact evidence pointers, and canonical lineage from the main run. Read `references/run-record-template.md`, `references/evidence-ladder.md`, and `references/operational-guidance.md`.
8. **Route from evidence**. Return <EXPERIMENT_ROUTE_DECISION> or <EXPERIMENT_BLOCKER_RECORD> after the result or blocker is recorded, using `follow_up_to` lineage from the result, claim validation, or blocker. Use the measured result, not intent, to choose analysis, writing, optimization/frontier review, another experiment, reset, stop, or an explicit decision route. Read `references/run-record-template.md`, `references/evidence-ladder.md`, and `references/execution-playbook.md`.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-experiment --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer one clean implementation pass and one real run over repeated half-runs (if the route is already concrete, otherwise resolve the missing route first).
- Prefer the smallest valid experiment package that answers the research question (if the claim needs stronger evidence, climb the evidence ladder deliberately).
- Prefer existing verified comparator evidence over full reproduction when equivalence and comparability are preserved (if an efficiency change affects comparability, treat it as an experiment change).
- Prefer direct local evidence before routine user questions (if durable evidence is missing after inspection, record the missing precondition).

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- The comparator reference must remain read-only unless the run is explicitly a comparator-repair route.
- Dataset, split, metric definition, evaluator logic, or comparison recipe must not change silently.
- Extra metrics may be recorded as supplementary output, but required metric keys must not be omitted.
- Smoke or pilot success must not be reported as main evidence.
- Metrics, logs, claims, and improvement narratives must not be fabricated.
- A run must be recorded as partial or blocked when evidence, metrics, comparability, or environment facts are insufficient.
- After a main result is recorded, the next route must be chosen from the measured result before launching another large run.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Evidence target level: achieved evidence level relative to the planned minimum, solid, or maximum target; higher is better only after comparability is preserved.
- Required metric completeness: fraction of required metric keys that are finite, traceable to outputs, and comparable with the accepted comparator; higher is better.

### Checks

- Contract readiness: <EXPERIMENT_CONTRACT> names the question, hypothesis, comparator, dataset, split, metric keys, stop and abandonment conditions, expected outputs, and route linkage.
- Scope control: <IMPLEMENTATION_CHANGE_MAP> covers the intended mechanism and excludes unrelated cleanup.
- Evidence completeness: <MAIN_RUN_RECORD> includes commands, configs, logs, outputs, seeds, environment facts, and last-known-good state.
- Metric validity: required metric keys are present, finite, traceable to outputs, and comparable with the accepted comparator contract or the deviation is explicit.
- Interpretation quality: <EXPERIMENT_RESULT_SUMMARY> classifies the claim as supported, refuted, inconclusive, partial, or blocked with caveats.
- Route quality: <EXPERIMENT_ROUTE_DECISION> or <EXPERIMENT_BLOCKER_RECORD> gives the single best next action and why.

## Reference Routing

Read these pages as needed:

- `references/experiment-contract.md` for the distilled contract gate from the source entrypoint.
- `references/main-experiment-plan-template.md` for the native plan structure and run-contract fields.
- `references/main-experiment-checklist-template.md` for the live control checklist during implementation, smoke, main run, validation, and closeout.
- `references/execution-playbook.md` for preflight, workspace, minimum-change implementation, smoke, long-run monitoring, diagnosis, validation, and routing.
- `references/operational-guidance.md` for planning surfaces, workspace boundaries, resources, durable outputs, memory, evidence records, and connector-facing charts.
- `references/evidence-ladder.md` for choosing `minimum`, `solid`, or `maximum` evidence targets and separating auxiliary evidence from main evidence.
- `references/run-record-template.md` for the result record distilled from source recording and evaluation-summary rules.

## Exit Criteria

This skill can end only when one of the following is durably true:

- A main run is completed, recorded, and routed.
- The run failed and <EXPERIMENT_BLOCKER_RECORD> records what was attempted, where it failed, whether the failure was methodological or infrastructural, and the best next action.
- The next route is clearly analysis, writing, optimization/frontier review, another experiment, reset, stop, or explicit decision.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
- Do not skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
