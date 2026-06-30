---
name: isomer-rsch-experiment-v2
description: Use when a selected hypothesis or route, accepted comparator basis, and evaluation contract are ready for one bounded implementation or measured run.
---

# Isomer Research Experiment V2

## Overview

Experiment turns one selected route into one interpretable measured result. It locks a run contract, changes only what the hypothesis needs, preserves command and metric evidence, records the result, and routes from the evidence.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- A selected hypothesis or route is ready for implementation.
- Comparator basis and evaluation contract are explicit.
- The task needs a main evidence-producing run rather than framing, baseline recovery, or follow-up analysis.
- Algorithm-first work needs a measured result for frontier review.

Do not use this skill when:

- The comparator gate is unresolved.
- The idea or route still has unresolved tradeoffs.
- The need is follow-up analysis, writing, or route decision rather than a main run.
- The work is open-ended optimization rather than one bounded measured test.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Lock the run contract**. Create <EXPERIMENT_CONTRACT> from <EXPERIMENT_CONTEXT_BRIEF>, accepted comparator basis, selected hypothesis, dataset, split, metrics, stop condition, and expected outputs.
2. **Map the minimum change**. Write <IMPLEMENTATION_CHANGE_MAP> and keep the baseline or comparator reference read-only.
3. **Run only useful smoke checks**. Create <SMOKE_CHECK_RECORD> only when command path, output schema, or evaluator wiring is still uncertain.
4. **Execute and monitor honestly**. Run the real bounded attempt through the proper Execution Adapter and preserve commands, configs, logs, outputs, and last-known-good state in <MAIN_RUN_RECORD>.
5. **Validate and record the result**. Produce <EXPERIMENT_RESULT_SUMMARY> with metric completeness, comparability, claim update, baseline relation, failure mode, and caveats.
6. **Route from evidence**. Return <EXPERIMENT_ROUTE_DECISION> or <EXPERIMENT_BLOCKER_RECORD> after the result is recorded.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/experiment-contract.md` for fix one measured run before code or compute work starts.
- `references/execution-playbook.md` for execute one bounded run while preserving evidence.
- `references/evidence-ladder.md` for choose a target proportional to the claim.
- `references/run-record-template.md` for record the measured result.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
