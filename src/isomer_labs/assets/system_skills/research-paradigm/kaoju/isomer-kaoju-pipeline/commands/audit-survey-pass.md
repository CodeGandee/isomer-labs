# Audit Survey Pass

## Workflow

1. **Freeze closeout inputs**. Accept the Survey Contract, survey Artifact refs, Evidence Items, Runs, Findings, Decisions, Provenance Records, and intended conclusions.
2. **Audit without repair**. Use `$isomer-kaoju-audit` to check coverage, identity, exact locators, provenance, depth, verdict, source drift, patches, failures, metrics, fairness, and lineage.
3. **Route defects**. If evidence is not ready, report bounded repair routes and return `paused` or `blocked`; do not repair inside the audit pass.
4. **Accept narrowed claims when explicit**. A `ready-with-narrowed-claims` decision must state the narrowed conclusions and excluded evidence.
5. **Synthesize accepted evidence**. Use `$isomer-kaoju-synthesize` only from an accepted Audit Report to write the Claim Status Table and Kaoju Dossier.
6. **Stop**. Return the pipeline terminal report with audit and synthesis refs, limitations, unresolved questions, and resume point.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded closeout plan while preserving non-mutating audit and accepted-evidence-only synthesis.

## Trigger

Use when the user asks to audit, close out, consolidate, or refresh the conclusions of an existing survey evidence set.

## Inputs

Require the active Survey Contract, exact target Artifact versions, accepted evidence refs, intended conclusion set, comparison contracts when applicable, and audit boundary.

## Outputs

- Audit Report with defects, severity, affected claims, accepted partial evidence, repair routes, and readiness decision.
- Claim Status Table and Kaoju Dossier only when the Audit Report is accepted.
- Terminal resource, Gate, blocker, and resume information.

## Stop Conditions

Stop at `not-ready` without synthesis, or after synthesis from `ready` or `ready-with-narrowed-claims`. This pass does not invent evidence, silently relabel it, or choose a repair procedure.

## Common Mistakes

- Fixing a source locator while auditing and forgetting the new lineage step.
- Treating polished prose as evidence readiness.
- Omitting failed Runs or contradictory Evidence Items from closeout.
