---
name: isomer-rsch-science
description: Support scientific computation, package checks, simulation, dataset analysis, validation, and evidence-backed claims.
---

# Isomer Research Science

## Overview

Use this skill for natural-science or engineering tasks that need computational evidence: package checks, simulations, solver runs, dataset analysis, model fitting, parameter sweeps, validation, HPC work, and scientific Research Claims.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Classify the task** as package check, computation, dataset analysis, parameter sweep, validation, claim support, hypothesis, blocker, or startup brief.
3. **Route package or domain knowledge** using `references/domain-index.md` and `references/package-index-decision.md`; treat catalog knowledge as routing guidance, not runtime proof.
4. **Check the environment before computed work** using `references/package-check-playbook.md`; verify imports, executables, versions, modules, credentials, queue access, data availability, and smoke paths through approved Execution Adapters.
5. **Prepare or refine the science task brief** with `references/science-task-brief-template.md` when the task needs bounded objectives, inputs, constraints, success criteria, deliverables, or handoff context.
6. **Execute and monitor scientific work** through a Capability Binding and Execution Adapter; for SSH, scheduler, queue, or SLURM work, follow `references/hpc-execution-adapter.md`.
7. **Record evidence and claims** using `references/evidence-recording.md` and `references/claim-type-discipline.md`, then route to next Workflow Stage, Gate, Decision Record, blocker, or report.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user prompt, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, evidence boundaries, runtime boundaries, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/package-check-playbook.md` before treating a scientific package, solver, executable, dataset, license, module, or queue as usable.
- `references/claim-type-discipline.md` before recording or reporting computed, parsed, digitized, or hypothesis claims.
- `references/hpc-execution-adapter.md` for SSH, queue, scheduler, SLURM, remote log, and long-running job discipline.
- `references/science-task-brief-template.md` when organizing a scientific task, handoff, or startup brief.
- `references/evidence-recording.md` when recording package checks, runs, dataset analyses, sweeps, validation results, claims, blockers, and links.
- `references/domain-index.md` when routing by scientific domain or known package family.
- `references/package-index-decision.md` for the package-card catalog deferral and follow-up boundary.

## Entry Signals

- A scientific software, simulation, dataset, sweep, validation, or claim-support task needs computational evidence.
- Local runtime availability, queue access, data availability, units, tolerances, seeds, credentials, or licenses must be checked before execution claims.
- The result may become an Evidence Item, Research Claim, hypothesis, Decision Record, Gate, or blocker.

## Exit Criteria

- Inputs, outputs, logs, parameters, units, versions, tolerances, seeds, and caveats are durable.
- Package availability is checked or explicitly blocked before computed claims are made.
- Validation checks, controls, convergence, invariants, schemas, or domain tolerances support the interpretation.
- Claims are typed as computed, parsed, digitized, or hypothesis and linked to supporting Evidence Items.

## Durable Outputs

- Package or environment check Artifact.
- Computational Run, dataset analysis, parameter sweep, or HPC job Evidence Item.
- Validation Evidence Item with status separate from raw execution status.
- Research Claim, hypothesis, blocker, Gate, or Decision Record.
- Provenance Record linking inputs, execution, outputs, validation, and interpretation.

## Guardrails

- Do not treat package cards, domain indexes, or documentation as runtime availability.
- Do not call a result computed unless real execution produced it in the current task or the durable record explicitly links to that execution.
- Do not weaken tolerances, filters, physical models, convergence criteria, validation checks, or scientific semantics merely to pass.
- Do not submit remote or HPC jobs without a log path, job id or status plan when available, and a monitoring cadence.
- Do not record science evidence only in chat; create durable Artifacts, Evidence Items, Research Claims, Decision Records, Gates, or Provenance Records through the host surface.
- Use `[[tbd-surface:api-execution-command]]` for unsettled execution commands and run log Artifacts resolved by Workspace Path Resolution.
