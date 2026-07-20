---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Theory Comparison Pass

## Workflow

1. **Frame the question**. Accept candidate Source Identities, comparison purpose, audience, desired source depth, and base survey refs.
2. **Derive dimensions**. Use `isomer-ext-kaoju-entrypoint->compare` to define domain-relevant dimensions, rationale, applicability, and source basis; use bounded discovery when the domain basis is unclear.
3. **Acquire and examine evidence**. Use `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine` to inspect each candidate at exact source locators.
4. **Build the theory matrix**. Record exact evidence or `not stated`, `not applicable`, `unclear`, or `disputed` in every cell.
5. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` to check identity, dimension basis, source depth, locator coverage, and unsupported inference.
6. **Synthesize**. If audit accepts the evidence, use `isomer-ext-kaoju-entrypoint->synthesize` to integrate the Theory Comparison Artifact into the survey.
7. **Stop**. Return this bounded procedure's terminal report; do not start empirical Runs internally. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route as a separate procedure Run after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a source-grounded comparison plan while preserving audit before synthesis.

## Trigger

Use when the user asks to compare named works in theory and wants the comparison to reflect meaningful dimensions in the survey domain.

## Inputs

Require candidate identities or resolvable locators, comparison question, accepted survey context, intended audience, desired source depth, and coverage constraints.

## Outputs

- Dimension definitions with rationale, applicability rules, and source bases.
- Source-grounded Theory Comparison Artifact with exact cell evidence.
- Audit Report, Claim Status Table updates, and survey comparison view.
- Explicit contradictions, missing states, and limits.

## Stop Conditions

Stop when every candidate and applicable dimension has evidence or an explicit missing state. Source-only cells remain at source-inspected depth and never receive empirical `compared` depth.

## Guardrails

- DO NOT copy a familiar comparison taxonomy without checking domain relevance.
- DO NOT fill unstated details through inference.
- DO NOT rank works whose cells are unclear, disputed, or not applicable.
