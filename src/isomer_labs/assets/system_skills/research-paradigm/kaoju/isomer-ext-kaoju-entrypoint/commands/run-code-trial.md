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

# Run Code Trial

## Workflow

1. Resolve the accepted source, environment, smoke result, data, and prior attempt refs by state-DB query. Reject ambient-environment execution.
2. Use `isomer-ext-kaoju-entrypoint->trial` to record `KAOJU:METHOD-TRIAL-PLAN`, including a durable minimal wrapper, compatible upstream command or smallest necessary adaptation, evaluator, metrics, resources, attempt bound, fidelity, expected outputs, and limitations.
3. Present the exact plan at the human Gate. Rejection records a terminal Run without execution.
4. Begin a distinct Run and execute the approved wrapper through `code_trial`.
5. Record immutable `KAOJU:METHOD-TRIAL-RUN` and `KAOJU:METHOD-TRIAL-RESULT` Artifacts with source, environment, data, logs, outputs, timing, resources, adaptations, checks, verdict, verification depth, and limitations.
6. Classify failures. Retry an identical transient request only within the attempt bound. Any material dependency, source, data, wrapper, evaluator, metric, resource, fidelity, or interpretation change requires a revised plan and another Gate.
7. For random-data trials, reuse `KAOJU:GENERATED-DATASET`, set `purpose: capability-probe`, and claim no stronger than executed verification depth.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->trial`. Outputs: plan, Gate, wrapper, Run, result, generated dataset when applicable, log, blocker, and provenance refs.

## Gates, Blockers, and Resume

The execution Gate is mandatory. Failed Runs remain visible. Resume at prerequisites, plan, Gate, execute, evaluate, classify-retry, or revise-plan without overwriting any attempt.
