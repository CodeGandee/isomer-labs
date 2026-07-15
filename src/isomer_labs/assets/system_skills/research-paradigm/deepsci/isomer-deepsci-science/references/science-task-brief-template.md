# Science Task Brief Template

Use this reference to frame a scientific computation, validation task, startup handoff, or scientific code optimization before execution. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State objective and domain**. Name the scientific or engineering result, domain, task type, and downstream consumer.
2. **State what to compute or analyze**. List calculations, simulations, dataset analyses, reproductions, parameter sweeps, validations, or code optimizations.
3. **State setup and constraints**. Record physical parameters, units, package preferences, datasets, hardware, remote/HPC expectations, privacy, budget, runtime, and resource limits.
4. **State success criteria**. Define convergence, correctness, reproducibility, comparison, schema, units, tolerance, or validation checks.
5. **State deliverables and evidence plan**. Name expected scripts, logs, outputs, figures, tables, reports, data files, DEEPSCI:SCIENCE-PACKAGE-CHECK, DEEPSCI:SCIENCE-RUN-RECORD, DEEPSCI:SCIENCE-VALIDATION-RESULT, and DEEPSCI:SCIENCE-CLAIM-RECORD.
6. **Use optimization brief shape when needed**. For scientific code optimization, add package, language, target hot path, editable scope, performance metric, correctness constraints, representative workloads, build commands, and deterministic runtime constraints.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer bounded Copilot-style task framing for one package check, local calculation, dataset inspection, or result explanation.
- Prefer autonomous framing only when compute, data, privacy, network, resources, and success criteria are clear enough.
- Prefer explicit correctness constraints for performance optimization (if performance is optimized, otherwise forbid scientific shortcuts).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:SCIENCE-TASK-BRIEF must not require a fixed source filename or `goal.md` shape.
- Scientific code optimization must preserve scientific semantics, numeric invariants, tolerances, and forbidden shortcuts.
- Success criteria must be inspectable from outputs, logs, validation records, or evidence paths.
- Expected package checks and evidence node types must be explicit when computation is planned.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Brief-field coverage: fraction of domain, objective, inputs, outputs, package needs, claim type, privacy, units, budget, runtime constraints, validation checks, and evidence-recording fields completed; higher is better.
- Missing-validation count: number of task outputs or claims without a planned validation, invariant, tolerance, schema, unit, or correctness check; lower is better.

### Checks

- Objective gate: domain, task type, objective, and downstream consumer are clear.
- Setup gate: inputs, parameters, units, packages, resources, and constraints are explicit.
- Success gate: validation checks and deliverables are concrete.
- Evidence gate: planned science evidence records are named.
- Optimization gate: target, editable scope, performance metric, correctness constraints, representative workloads, and build route are specified when optimizing scientific code.

## Template

### Objective

- scientific or engineering result:
- domain:
- task type:
- downstream consumer:

### What To Compute or Analyze

- calculations, simulations, analyses, reproductions, sweeps, or validations:

### Setup and Constraints

- parameters and units:
- package or solver preferences:
- datasets:
- hardware or HPC expectations:
- privacy or network constraints:
- budget and runtime constraints:

### Success Criteria

- convergence:
- correctness:
- reproducibility:
- comparison:
- schema or units:
- tolerance:

### Deliverables

- scripts:
- logs:
- outputs:
- figures or tables:
- reports or data files:

### Evidence Recording Plan

- package check:
- run or analysis record:
- validation result:
- claim record:
