---
name: isomer-rsch-baseline-v2
description: Use when research work needs a trustworthy comparator, metric contract, accepted waiver, or blocker before hypotheses, experiments, analysis, or claims can proceed.
---

# Isomer Research Baseline V2

## Overview

Baseline secures one trustworthy comparator and comparison contract, then gets out of the way. It chooses the lightest route that can support downstream comparison, verifies evidence before acceptance, and closes the gate through confirmation, waiver, or blocker.

Placeholder definitions live in `migrate/placeholders.md`. Step support pages under `references/` preserve the source skill's guidance, preferences, constraints, and quality gates in native Isomer language.

## When to Use

Use this skill when:

- No credible comparator exists.
- The active comparator is stale, unverified, incomparable, or unclear after resume.
- A provided baseline package, local service, trusted output, source repository, or registry package must be attached, imported, verified, reproduced, repaired, or published.
- A failed reproduction needs bounded repair before downstream work can compare fairly.

Do not use this skill when:

- A verified active comparator and metric contract already exist and the next route is clearly idea, experiment, writing, or finalization.
- The baseline gate was explicitly waived for this route.
- The real task is ideation, main execution, analysis, or writing rather than comparator trust.

## Workflow

When this skill is invoked, execute these steps in order.

1. **Choose the acceptance target**. Use <BASELINE_CONTEXT_BRIEF> to decide whether the current target is comparison-ready, paper-repro-ready, registry-publishable, waived, or blocked. Read `references/route-selection.md` and `references/boundary-cases.md`.
2. **Select the lightest trustworthy route**. Record <COMPARATOR_ROUTE_RECORD> and, when ambiguity or cost warrants it, <BASELINE_ROUTE_PLAN> for attach, import, verify-local-existing, reproduce, repair, publish, waive, or block. Read `references/route-selection.md`, `references/artifact-flow-examples.md`, `references/baseline-plan-template.md`, and `references/baseline-checklist-template.md`.
3. **Make comparability explicit**. Produce <COMPARABILITY_CONTRACT> for task, dataset, split, evaluation path, required metric ids, metric directions, source identity, expected outputs, known deviations, variants, and caveats. Read `references/comparability-contract.md` and `references/artifact-payload-examples.md`.
4. **Audit only what the route needs**. Create <CODEBASE_AUDIT_RECORD> only when attach, import, or verify-local-existing cannot establish trust and reproduce or repair needs source understanding. Read `references/codebase-audit-checklist.md` and `references/operational-guidance.md`.
5. **Collect and verify necessary evidence**. Gather <BASELINE_VERIFICATION_EVIDENCE> sufficient for the selected acceptance target, then verify real outputs, metrics, service responses, package records, source identity, environment facts, and deviations before acceptance. Read `references/verification-record-template.md`, `references/comparability-contract.md`, and `references/operational-guidance.md`.
6. **Close the baseline gate**. Record <ACCEPTED_BASELINE_RECORD>, <BASELINE_WAIVER_RECORD>, or <BASELINE_BLOCKER_RECORD>, including <BASELINE_PAYLOAD_RECORD> fields when acceptance, waiver, or blocking status matters. Read `references/artifact-payload-examples.md`, `references/artifact-flow-examples.md`, and `references/baseline-checklist-template.md`.
7. **Route and stop**. Return <BASELINE_ROUTE_DECISION> once the baseline is accepted, waived, blocked, or route-changed. Do not keep doing comparator work after the current acceptance target is satisfied unless one explicit unresolved comparison risk remains. Read `references/artifact-payload-examples.md`, `references/artifact-flow-examples.md`, and `references/operational-guidance.md`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Cross-Step Preferences

- Prefer attach, import, or verify-local-existing before full reproduction (if those routes can establish trust, otherwise escalate to reproduce or repair).
- Prefer the route with highest trust per unit time and compute (if a heavier route does not remove a named comparison risk, otherwise stop at the lighter accepted comparator).
- Prefer direct verification over smoke work when command path, environment viability, evaluator wiring, and output schema are already concrete (if uncertainty remains, otherwise use a bounded smoke check).
- Prefer a compact route record for fast paths (if the route is ambiguous, code-touching, expensive, broken, long-running, or intended for reuse, otherwise use the full route plan and checklist).
- Prefer asking the user only for real scope, cost, permission, data-access, or scientific-preference decisions (if local evidence can answer the question, otherwise inspect it first).

## Cross-Step Constraints

- Attach, import, or publish alone must not open the downstream baseline gate.
- Verification must precede acceptance.
- Metrics must trace to real outputs, logs, service responses, source artifacts, registry records, or package records.
- Dataset, split, metric definition, metric direction, evaluation path, source identity, variants, and known deviations must not be silently normalized away.
- Later stages must not need to guess the active comparator, trusted metrics, metric directions, provenance, or caveats.
- Repeated failure without new evidence, code change, environment change, or route change must stop and route to repair, decision, blocker, waiver, or bounded clarification.
- Baseline identifiers and variant names should stay stable enough for later stages to cite without guesswork.

## Cross-Step Quality Gates

- Target gate: <BASELINE_CONTEXT_BRIEF> names the trust state, acceptance target, candidate comparator, and active uncertainty.
- Route gate: <COMPARATOR_ROUTE_RECORD> chooses one dominant route and explains why lighter routes are or are not trustworthy.
- Contract gate: <COMPARABILITY_CONTRACT> records task, dataset, split, evaluation path, required metric ids, metric directions, source identity, known deviations, and caveats.
- Evidence gate: <BASELINE_VERIFICATION_EVIDENCE> traces trusted metrics or outputs to real evidence.
- Acceptance gate: <ACCEPTED_BASELINE_RECORD>, <BASELINE_WAIVER_RECORD>, or <BASELINE_BLOCKER_RECORD> states confirmation, waiver, or blocker status and next route.
- Handoff gate: <BASELINE_ROUTE_DECISION> leaves one trusted comparator, one explicit blocker, one explicit waiver, or one explicit route change.

## Reference Routing

Read these pages as needed:

- `references/route-selection.md` for trust-per-cost route choice among attach, import, verify-local-existing, reproduce, repair, publish, waive, and block.
- `references/boundary-cases.md` for comparison-ready versus paper-repro-ready, trusted-with-caveats, weak provenance, unclear local comparator, heavier-but-not-more-trustworthy routes, and repeated failure.
- `references/baseline-plan-template.md` for durable route records when the route is ambiguous, code-touching, expensive, broken, long-running, or reuse-facing.
- `references/baseline-checklist-template.md` for acceptance-boundary checklist fields.
- `references/comparability-contract.md` for the comparison basis that later work must not guess.
- `references/codebase-audit-checklist.md` for reproduce or repair routes that need a source audit.
- `references/verification-record-template.md` for baseline evidence before acceptance.
- `references/artifact-flow-examples.md` for native evidence-flow sequences for attach, import, verify-local-existing, publish, and waiver.
- `references/artifact-payload-examples.md` for accepted, waived, blocked, and route-decision payload fields.
- `references/operational-guidance.md` for durable route records, execution tactics, environment choices, reuse, and continuity notes.

## Exit Criteria

This skill can end only when one of these states is durable:

- A baseline is attached, imported, locally verified, reproduced, repaired, or published and accepted.
- A waiver decision explicitly leaves the baseline gate with a reason.
- A broken route is blocked and the next decision is recorded.
- A route change is recorded because the previous route is no longer the best trust-per-cost path.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
- Do not skip the support pages referenced by workflow steps; they contain the source skill's operative guidance and gates.
