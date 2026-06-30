---
name: isomer-rsch-science-v2
description: Use when research work depends on scientific computation, data analysis, simulation, package checks, HPC execution, claim-type discipline, or validity evidence.
---

# Isomer Research Science V2

## Overview

Science provides companion evidence discipline for scientific computation and validation. It routes tasks through package and domain context, keeps execution in Isomer command surfaces, and records claim-supporting evidence nodes before scientific claims are trusted.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- A task requires scientific package, solver, simulation, data, model, or HPC support.
- A package, executable, module, container, or environment needs availability and smoke checks.
- A computed, parsed, digitized, or hypothesis claim needs evidence classification.
- Experiment or analysis work needs scientific validity notes.

Do not use this skill when:

- The task is ordinary software execution with no scientific validity risk.
- The needed evidence belongs to baseline, idea, experiment, or analysis without extra scientific checks.
- A package catalog card is being treated as runtime availability without an environment check.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Frame the science task**. Create <SCIENCE_TASK_BRIEF> with domain, objective, inputs, expected outputs, claim type, package needs, and validation risks.
2. **Route through package or domain context**. Use package and domain knowledge only as routing context, then verify availability through <SCIENCE_PACKAGE_CHECK> before computed work.
3. **Execute through Isomer command surfaces**. Use Execution Adapter Command Requests or compatible harness calls for code, CLI, solver, scheduler, and HPC work.
4. **Record scientific evidence**. Create <SCIENCE_RUN_RECORD> and <SCIENCE_VALIDATION_RESULT> for computation, parsing, digitization, dataset analysis, parameter sweep, convergence, units, schema, or controls.
5. **Classify claims conservatively**. Create <SCIENCE_CLAIM_RECORD> only after supporting run, analysis, sweep, or validation evidence exists.
6. **Update the evidence graph or route**. Record <SCIENCE_EVIDENCE_GRAPH_UPDATE>, <SCIENCE_ROUTE_DECISION>, or <SCIENCE_BLOCKER_RECORD>.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/science-task-brief.md` for frame a scientific computation or validation task before execution.
- `references/evidence-recording.md` for record scientific evidence as typed nodes before claims.
- `references/package-routing.md` for use package knowledge as routing context, not availability proof.
- `references/hpc-execution-adapter.md` for handle ssh, scheduler, queue, and log evidence through isomer command surfaces.
- `references/claim-discipline.md` for calibrate scientific claims to evidence type.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
