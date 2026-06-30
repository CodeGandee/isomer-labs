---
name: isomer-rsch-science-v2
description: Use when research needs scientific computation, package checks, simulation, dataset analysis, model fitting, parameter sweeps, or validity judgment.
---

# Isomer Research Science V2

## Overview

Science supports the research loop when scientific computation or data validity affects trust. It does not replace experiment or analysis; it clarifies whether the scientific evidence is usable.

## When to Use

Use this skill when a package, simulation, dataset, solver, model fit, parameter sweep, unit convention, tolerance, or scientific assumption can change the trustworthiness of a frame, experiment, analysis, or decision. Do not use it for ordinary command execution that carries no scientific validity question.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Classify the scientific task**. Name whether the issue is package readiness, computation, simulation, dataset analysis, model fitting, sweep, validation, or scientific claim support.
2. **State assumptions and inputs**. Make units, parameters, tolerances, versions, seeds, and data boundaries explicit when they affect trust.
3. **Run or inspect the smallest valid check**. Prefer the check that changes the research decision most directly.
4. **Validate the result**. Compare against theory, benchmark behavior, sanity checks, or expected invariants.
5. **Produce [[rsch-object:science-validity-note]]**. When the check itself is a bounded test, also produce [[rsch-object:experiment-contract]] or [[rsch-object:experiment-result]] as appropriate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 shared loop, the placeholder registry, and the user's request, then execute the plan.

## Semantic Inputs

- Optional [[rsch-object:research-frame]]
- Optional [[rsch-object:experiment-contract]]
- Optional [[rsch-object:experiment-result]]
- Optional [[rsch-object:analysis-finding]]

## Semantic Outputs

- [[rsch-object:science-validity-note]]
- Optional [[rsch-object:experiment-contract]]
- Optional [[rsch-object:experiment-result]]
- Optional [[rsch-object:analysis-finding]]

## Reference Routing

- Read `isomer-rsch-shared-v2` for the core loop and placeholder rule.

## Guardrails

- Do not treat documentation or package availability as scientific validity.
- Do not make computed claims without checking assumptions, units, and tolerances.
- Do not hide numerical instability, data mismatch, or failed reproduction.

## Source Lineage

Distilled from the DeepScientist science process analysis: classify scientific work, check runtime and package readiness, run computation, validate results, and state evidence-backed scientific claims with limits.
