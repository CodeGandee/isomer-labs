---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Comparative Pass

## Workflow

1. **Draft comparison intent**. Use `isomer-ext-kaoju-entrypoint->frame` and `isomer-ext-kaoju-entrypoint->compare` to record candidate identities, desired conclusions, prior-evidence reuse, data, environment, reproduction or reimplementation routes, metrics, fairness, resources, Gates, and unresolved decisions.
2. **Present the checkpoint**. Show the Comparison Intent Document and ask: “Do you want to clarify for more detail, or proceed?” Wait for the Proceed Decision.
3. **Check readiness after approval**. Use `isomer-ext-kaoju-entrypoint->workspace`; query registered datasets first, validate reusable Runs, and identify candidate blockers.
4. **Acquire, examine, and prepare**. Use `isomer-ext-kaoju-entrypoint->acquire`, `isomer-ext-kaoju-entrypoint->examine`, and `isomer-ext-kaoju-entrypoint->reproduce` only as required by the accepted intent.
5. **Run the comparison**. Use `isomer-ext-kaoju-entrypoint->compare` under the frozen Comparison Contract and retain raw outputs, adaptations, quality checks, and uncertainty evidence.
6. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` to check metric traceability, candidate eligibility, fairness, variability, failures, and `not-comparable` decisions.
7. **Synthesize**. If audit accepts the evidence, use `isomer-ext-kaoju-entrypoint->synthesize` to produce the Comparison Matrix and survey delta.
8. **Stop**. Return this bounded procedure's terminal report without expanding the candidate set autonomously. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a controlled comparison plan while preserving the Proceed Decision and audit before synthesis.

## Trigger

Use when the user wants to compare methods A, B, C, or more through actual Runs rather than reported theory or source claims alone.

## Inputs

Require candidate identities, user comparison intent, target task and data, metrics and evaluator semantics, fairness priorities, resource envelope, desired uncertainty, prior survey and Run refs, and clarification posture.

## Outputs

- Reviewed Comparison Intent Document and Proceed Decision.
- Comparison Contract, candidate-readiness records, and governed preparation refs.
- Candidate Run, raw-output, environment, input, evaluator, adaptation, and quality-check refs.
- Audited Comparison Matrix with variability, uncertainty, failures, and `not-comparable` outcomes.
- Claim Status Table and survey delta refs.

## Stop Conditions

No candidate preparation or research Run starts before the Proceed Decision. Stop when the accepted candidates have eligible results or explicit blockers under the resource boundary; do not hide missing candidates or normalize away task semantics.

## Guardrails

- DO NOT treat the plan as internal scratch work instead of a user-reviewed survey Artifact.
- DO NOT reuse old Runs without contract compatibility checks.
- DO NOT report only successful candidates.
