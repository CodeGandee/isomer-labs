# Science Task Brief Template

Use this shape when a natural-science or engineering task needs bounded startup context, handoff, or operator review.

```markdown
# Science Task Brief: <title>

## Objective
What scientific or engineering result should be produced.

## What To Compute Or Analyze
- Concrete calculations, simulations, dataset analyses, reproductions, optimizations, or validation checks.

## Setup And Constraints
- Physical parameters, package preferences, datasets, hardware, SSH or HPC expectation, privacy, units, budget, and runtime constraints.

## Success Criteria
- Quantitative convergence, correctness, reproducibility, comparison, schema, physical invariant, or validation checks.

## Deliverables
- Expected scripts, logs, outputs, figures, tables, reports, data files, Research Claims, Decision Records, or blockers.

## Evidence Recording Plan
- Expected package checks, computational Runs, dataset analyses, parameter sweeps, validation Evidence Items, Research Claims, Provenance Records, Gates, and handoff notes.
```

## Scientific Code Optimization Brief

Use this shape when the task is performance optimization of scientific code:

```markdown
# Optimization Goal

## Package
<package id or repository name>

## Language
<python|c|cpp|fortran|julia|mixed>

## Target
Specific hot path and scientific semantics that must remain unchanged.

## Editable Scope
- explicit/path/to/file.py

## Performance Metric
Primary runtime or throughput metric and aggregation rule.

## Correctness Constraints
- numeric scientific invariants and tolerances
- forbidden shortcuts or weakened solver settings

## Representative Workloads
- train-case: meaningful workload
- test-case: held-out workload

## Build
Deterministic build or install commands through approved Execution Adapter Command Requests.

## Notes
- deterministic thread, seed, MPI, launcher, and input-file constraints
```
