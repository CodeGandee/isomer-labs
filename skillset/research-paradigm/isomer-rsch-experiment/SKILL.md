---
name: isomer-rsch-experiment
description: Turn one selected route into one trustworthy measured result and route from the resulting Isomer Labs evidence.
---

# Isomer Research Experiment

## Overview

Use this skill when one selected route or promoted candidate needs a bounded implementation pass, main Run, metric validation, and durable result.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when planning, checklist control, execution, evidence quality, operational monitoring, or run recording matters.
3. **Confirm entry fit and recover inputs**. Recover the selected route, accepted comparator or waiver, metric contract, current workspace context, expected outputs, and prior incident patterns.
4. **Lock the Run contract**. Define the research question, comparator, dataset or split, metric keys, stop rule, abandonment rule, output expectations, comparability boundary, and strongest alternative hypothesis.
5. **Implement the minimum hypothesis-bound change**. Keep the comparator read-only, avoid unrelated cleanup, preserve theory fidelity, and revise the plan before changing the route.
6. **Smoke only when it answers execution uncertainty**. Use a bounded smoke or pilot to verify command path, output schema, evaluator wiring, or environment assumptions, then move to the evidence-bearing Run unless blocked.
7. **Execute, monitor, validate, and record the result**. Preserve commands, configs, logs, outputs, metrics, comparability checks, failure modes, Evidence Items, Research Claim updates, Provenance Records, and the next route Decision Record.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/plan-template.md` before substantial code edits, expensive execution, or branch-sensitive work.
- `references/checklist-template.md` when the active frontier, next step, blocked state, or closeout needs a visible control surface.
- `references/evidence-ladder.md` when deciding whether the package is minimum, solid, or maximum evidence, or whether the work is auxiliary or main.
- `references/execution-playbook.md` for run contracts, preflight checks, smoke and pilot discipline, long-running monitoring, output validation, and next-route decisions.
- `references/operational-guidance.md` for planning surfaces, resource rules, durable outputs, Evidence Item recording, and connector-facing chart notes.
- `references/run-record-template.md` when creating or reviewing a durable Run record or evaluation summary.

## Entry Signals

- A selected route or promoted candidate is ready for one bounded implementation pass or main Run.
- Comparator status, metric contract, expected outputs, and stop rules are known or can be locked before execution.
- The Research Task needs a measured result that can support, weaken, narrow, or refute a Research Claim.

## Exit Criteria

- Run contract, inputs, commands, configs, logs, outputs, metrics, and environment notes are durable.
- Metric completeness and comparator comparability have been checked.
- The result is classified as supported, refuted, inconclusive, partial, failed, or blocked.
- The handoff recommends optimize, analysis, write, decision, another experiment, reset, or blocker.

## Run Evidence Contract

For each meaningful Run, record enough of the following to make the evidence reusable:

- run id, route id, Research Inquiry Relationship, comparator reference, metric contract, dataset or split, and expected outputs
- exact execution plan through a Capability Binding and Execution Adapter, with unsettled command surfaces marked as `[[tbd-surface:api-execution-command]]`
- code or configuration deltas, keep-unchanged contract, seeds, environment notes, and resource constraints
- smoke or pilot outcomes, main-run logs, output pointers, metric rows, metric completeness, and comparability verdict
- claim-to-metric mapping, Research Claim update, evaluation summary, failure mode, caveat, and next action
- Provenance Records for source inputs, generated Artifacts, run logs, and any manual decisions

## Durable Outputs

- Run contract Artifact.
- Run logs, configs, outputs, metric records, and Evidence Items.
- Research Claim update and evaluation summary.
- Decision Record for the next route or blocker.
- Optional plan, checklist, run-record, and claim-validation Artifacts for non-trivial Runs.

## Guardrails

- Do not silently change dataset, split, metric, evaluator, comparator, or comparison recipe.
- Do not confuse smoke or pilot success with main evidence.
- Do not claim success before durable outputs exist.
- Do not rerun without a real change in code, command, environment, evidence, or route.
- Do not hide failed, partial, suspicious, non-comparable, or blocked Runs.
- Do not spend for maximum evidence before the line is at least solid.
- Use run log Artifact through Workspace Path Resolution, experiment output Artifact through Workspace Path Resolution, and the accepted Artifact and Provenance recording API for recording surfaces.
