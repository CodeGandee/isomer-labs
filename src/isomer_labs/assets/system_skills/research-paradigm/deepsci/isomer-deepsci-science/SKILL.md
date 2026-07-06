---
name: isomer-deepsci-science
description: Use when research work depends on scientific computation, data analysis, simulation, package checks, HPC execution, claim-type discipline, or validity evidence.
---

# Isomer Research Science

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

Science provides companion evidence discipline for scientific computation and validation. It routes tasks through package and domain context, keeps execution in Isomer command surfaces, and records claim-supporting evidence before scientific claims are trusted.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language. Package cards and `references/package-index.min.json` are passive catalog material and do not prove runtime availability.

## When to Use

Use this skill when:

- A task requires scientific package, solver, simulation, data, model, or HPC support.
- A package, executable, module, container, license, dataset, or environment needs availability and smoke checks.
- A computed, parsed, digitized, or hypothesis claim needs evidence classification.
- Experiment or analysis work needs scientific validity notes, convergence checks, unit checks, schema checks, controls, or scientific caveats.

Do not use this skill when:

- The task is ordinary software execution with no scientific validity risk.
- The needed evidence belongs to baseline, idea, experiment, or analysis without extra scientific checks.
- A package catalog card is being treated as runtime availability without an environment check.

## Workflow

When this skill is invoked, execute these steps in order.


1. **Frame the science task**. Create <SCIENCE_TASK_BRIEF> with domain, objective, inputs, expected outputs, claim type, package needs, resources, constraints, validation risks, and downstream consumer. Read `references/science-task-brief-template.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-science --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Route through package or domain context**. Search `references/package-index.min.json`, inspect `references/domain-index.md`, and open only relevant `references/packages/<package_id>.md` cards. Treat catalog material as routing context, then verify availability through <SCIENCE_PACKAGE_CHECK>. Read `references/package-check-playbook.md`.
4. **Execute through Isomer command surfaces**. Use Execution Adapter Command Requests or compatible execution bindings for code, CLI, solver, scheduler, remote shell, queue, and log work. Read `references/hpc-via-bash-exec.md` when HPC, SSH, scheduler, allocation, or remote logs are involved.
5. **Record scientific evidence**. Create or update <SCIENCE_RUN_RECORD> and <SCIENCE_VALIDATION_RESULT> for computation, parsing, digitization, dataset analysis, parameter sweep, convergence, units, schema, controls, tolerances, seeds, or invariants. Read `references/artifact-science-tool.md`.
6. **Classify claims conservatively**. Create <SCIENCE_CLAIM_RECORD> only after supporting run, analysis, sweep, package-check, or validation evidence exists. Read `references/claim-type-discipline.md`.
7. **Update the evidence graph or route**. Record <SCIENCE_EVIDENCE_GRAPH_UPDATE>, <SCIENCE_ROUTE_DECISION>, or <SCIENCE_BLOCKER_RECORD> so later skills can reconstruct what was checked, what failed, and what claims are safe. Read `references/artifact-science-tool.md`, `references/claim-type-discipline.md`, and `references/hpc-via-bash-exec.md`.
8. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-science --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

Read these preferences as defaults that apply across the whole skill. They should shape route, evidence, and handoff choices unless a step-specific page gives a stronger source-backed reason.

- Prefer package cards for routing context, not availability claims (if a solver is needed, otherwise run an environment check first).
- Prefer typed evidence records over prose-only scientific summaries (if evidence is missing, otherwise record a blocker or hypothesis).
- Prefer conservative claim types (if the computation did not run in the current workspace, otherwise do not call it computed).
- Prefer low-frequency durable monitoring for HPC and long runs (if a job is queued or running, otherwise do not infer completion).

## Cross-Step Constraints

Read these constraints as global validity boundaries for the skill. A result that violates a `must` or `must not` item is not ready to hand off until the violation is fixed, waived, or recorded as a blocker.

- Package metadata must not override task-specific evidence.
- Runtime availability must be checked before computed work when package, executable, module, container, license, or backend availability matters.
- Desired package installation after a failed availability check must route to `$isomer-op-topic-mgr env-install-packages`; this skill records package checks and blockers but does not install packages directly.
- Computed claims must link to run, analysis, sweep, package-check, validation, or evidence paths.
- Digitized or parsed evidence must not be relabeled as computed.
- Scientific tolerances, filters, physical models, convergence criteria, and validation checks must not be weakened merely to make a run pass.
- Queued or submitted jobs must not be reported as completed results.
- Blocked package checks, missing data, missing licenses, missing credentials, failed modules, and unavailable resources must be recorded when they affect the route.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Evidence-node coverage: fraction of package checks, runs, analyses, sweeps, validations, and claims that have corresponding Science Evidence Graph records when they materially affect the result; higher is better.
- Unsupported computed-claim count: number of claims labeled computed without linked run, analysis, sweep, validation, or evidence paths; lower is better.

### Checks

- Task gate: <SCIENCE_TASK_BRIEF> names domain, objective, inputs, outputs, package needs, claim type, resources, validation checks, and downstream consumer.
- Package gate: <SCIENCE_PACKAGE_CHECK> records import, executable, version, module, container, backend, license, and smoke evidence when relevant.
- Execution gate: <SCIENCE_RUN_RECORD> preserves command, input, log, output, status, environment, and package context.
- Validation gate: <SCIENCE_VALIDATION_RESULT> records convergence, units, schema, controls, tolerances, seeds, invariants, or correctness checks when they matter.
- Claim gate: <SCIENCE_CLAIM_RECORD> has claim type and linked evidence.
- Route gate: <SCIENCE_ROUTE_DECISION> or <SCIENCE_BLOCKER_RECORD> states next action or blocker plainly.

## Reference Routing

Read these pages as needed:

- `references/science-task-brief-template.md` for framing a scientific computation, validation task, or scientific code optimization brief.
- `references/package-index.min.json` and `references/domain-index.md` for package and domain routing.
- `references/packages/<package_id>.md` for package-specific routing cards.
- `references/package-check-playbook.md` for package, executable, module, container, backend, and smoke checks.
- `references/artifact-science-tool.md` for science evidence graph record shapes and required evidence rules.
- `references/hpc-via-bash-exec.md` for HPC, SSH, scheduler, queue, job id, and remote-log discipline through Isomer execution surfaces.
- `references/claim-type-discipline.md` for computed, parsed, digitized, and hypothesis claim discipline.

## Exit Criteria

This skill can end only when package availability is checked or blocked, scientific runs and validations have evidence records when applicable, claims are typed conservatively, and the next route or blocker is explicit.

## Common Mistakes

- Do not treat this skill as a solver installation or package manager.
- Do not run direct package installation from this skill; route desired Topic Workspace package setup to `$isomer-op-topic-mgr env-install-packages`.
- Do not call a result computed from a plot redraw, paper figure reading, or guess.
- Do not create science evidence only in chat.
- Do not let package-card metadata override task-specific evidence.
- Do not skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
