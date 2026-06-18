# Baseline Gate Checklist

Use this compact checklist before closing a baseline Gate. It is optional; the hard requirement is a durable accepted, blocked, Baseline-Waiver Policy-backed waived, replaced, or route-changed state.

## Identity

- baseline id:
- route:
- acceptance target:
- primary comparator:
- source identity:

## Current Frontier

- [ ] next execution, verification, acceptance, blocker, waiver, or route-switch step is explicit
- [ ] active uncertainty is written as a concrete question
- [ ] next Workflow Stage Cursor is known if this Gate clears or blocks

## Core Gate

- [ ] comparator identity and provenance are explicit
- [ ] dataset, split, evaluation path or Capability Binding, required metrics, and metric directions are explicit enough to judge comparability
- [ ] trusted outputs or metrics are traceable to Evidence Items, Artifacts, Run records, source documents, reusable package records, or evaluation observations
- [ ] smoke was used, skipped, or replaced by direct verification for an explicit reason when that choice matters
- [ ] expected result files, trusted-output pointers, or package records have been checked
- [ ] metric-contract Artifact exists or will be produced before acceptance
- [ ] baseline Gate is accepted, blocked, Baseline-Waiver Policy-backed waived, replaced, or route-changed with a durable Decision Record

## Blocked Boundary

- [ ] if blocked, the failure class is explicit
- [ ] if blocked, tried steps and evidence pointers are recorded
- [ ] if blocked, next best move is attach, import, retry, repair, reset, waive under Baseline-Waiver Policy, open a Gate through Gate Policy preflight, or route through decision

## Closeout

- [ ] concise baseline summary written
- [ ] caveats carried forward
- [ ] next Workflow Stage Cursor named explicitly
