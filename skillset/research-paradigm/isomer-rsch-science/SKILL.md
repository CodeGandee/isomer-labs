---
name: isomer-rsch-science
description: Support scientific computation, package checks, simulation, dataset analysis, validation, and evidence-backed claims.
---

Use this skill for scientific software, simulations, package routing, dataset
analysis, parameter sweeps, validation, and scientific claims that require
explicit computational evidence.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/science.md`

## Entry Signals

- A scientific software, simulation, package, dataset, sweep, validation, or
  claim-support task needs computational evidence.
- Local runtime availability, data availability, units, tolerances, or
  credentials must be checked before execution claims.
- The result may become an Evidence Item, Research Claim, hypothesis, or
  blocker.

## Exit Criteria

- Inputs, outputs, logs, parameters, units, versions, tolerances, and caveats
  are durable.
- Validation checks, controls, convergence, invariants, or domain tolerances
  support the interpretation.
- The result is recorded as a supported claim, hypothesis, or blocker.

## Procedure

1. Classify the task: package check, computation, analysis, sweep, validation,
   claim support, hypothesis, or blocker.
2. Use package or domain cards only as routing knowledge; verify local
   availability separately.
3. Check modules, executables, versions, credentials, queue access, or data
   availability before claiming execution is possible.
4. Run computation only through the host execution capability.
5. Record inputs, outputs, logs, parameters, units, versions, tolerances, and
   caveats.
6. Validate results through schema checks, controls, convergence, invariants,
   units, or domain tolerances.
7. Record supported claims only after validation; otherwise record hypothesis
   or blocker.

## Durable Outputs

- Package or environment check Artifact.
- Computational run, dataset analysis, or sweep Artifact.
- Validation Evidence Item.
- Research Claim, hypothesis, or blocker.

## Guardrails

- Do not treat package cards as runtime availability.
- Do not call a result computed unless real execution produced it.
- Do not weaken tolerances to pass validation.
- Use `[[tbd-surface:api-execution-command]]` for unsettled execution commands.
