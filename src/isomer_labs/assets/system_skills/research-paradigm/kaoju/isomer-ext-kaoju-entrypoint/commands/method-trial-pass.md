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

# Method Trial Pass

## Workflow

1. **Frame the route**. Accept one paper method, target capability or claim, intended-data or generated-data route, desired numbers, resources, Gates, and stop conditions.
2. **Check readiness**. Use `isomer-ext-kaoju-entrypoint->workspace` and query the Topic Dataset Manifest before asking for data or proposing a download.
3. **Resolve and inspect materials**. Use `isomer-ext-kaoju-entrypoint->discover`, `isomer-ext-kaoju-entrypoint->acquire`, and `isomer-ext-kaoju-entrypoint->examine` to pin paper, code, dataset or generation plan, model, evaluator, and method-to-code mapping.
4. **Freeze execution**. Use `isomer-ext-kaoju-entrypoint->frame` to accept the execution contract and user decisions for material substitutions or expensive work.
5. **Run the trial**. Use `isomer-ext-kaoju-entrypoint->trial` to preserve upstream-faithful, adapted, repaired, failed, blocked, and probe Runs separately. Invoke `isomer-ext-kaoju-entrypoint->reproduce` only when the accepted conclusion is genuine reproduction and its stronger fidelity contract can be met.
6. **Audit**. Use `isomer-ext-kaoju-entrypoint->audit` to check identity, execution fidelity, input basis, evaluator, raw outputs, patches, and claim calibration.
7. **Synthesize**. If audit accepts the evidence, use `isomer-ext-kaoju-entrypoint->synthesize` to add the Method Trial Artifact and Findings to the survey.
8. **Stop**. Return first-hand numbers, limitations, and this bounded procedure's terminal report. An explicitly authorized prompt-level run-to controller may consume an in-closure recovery route after the report is recorded.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute one bounded method-trial plan while preserving audit before synthesis.

## Trigger

Use when the user asks to get one paper's source code and dataset, run it, and report numbers, or asks for a generated-data rough idea because the intended dataset is too large, restricted, costly, or unnecessary for initial understanding.

## Inputs

Require the paper or method identity, desired route, target claim or behavior, metric and evaluator intent, resource boundary, accepted substitutions, Gate posture, and prior evidence refs.

## Outputs

- Pinned paper, code, data or Generated Dataset Artifact, model, evaluator, environment, and execution refs.
- Separate Runs for faithful, adapted, repaired, failed, blocked, and generated-input attempts.
- Method Trial Artifact with numbers, quality checks, raw-output refs, evidence verdicts, and limitations.
- Accepted Audit Report and survey delta when synthesis is ready.

## Stop Conditions

Stop after the accepted trial contract succeeds, fails, or reaches its resource bound. Generated-data results use `run_purpose: capability-probe`, no stronger than `executed` depth, and are never labeled paper reproduction or benchmark evidence.

## Guardrails

- DO NOT repair before preserving the faithful failure.
- DO NOT report a generated-input number beside paper results without a route label.
- DO NOT let environment setup consume an unbounded resource budget.
