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

# Prepare Code Run

## Workflow

1. Resolve the canonical repository commit, associated paper, accepted Source Digest, task-critical path, dependency hints, data posture, and existing Pixi environment candidates.
2. Use `isomer-ext-kaoju-entrypoint->trial` to record `KAOJU:ENV-PREP-PLAN` with flexible compatible constraints, risks, authorization, expected smoke outputs, and environment scope.
3. Open and synchronously dispatch a Service Request. Apply the Pixi preference order: reuse a satisfying environment; add flexible compatible constraints to an existing environment while preferring `default`; or create a dedicated environment.
4. Record exact resolved package versions and lock identity in `KAOJU:PIXI-ENV-REF`, while preserving flexible intent constraints and before-and-after Gate state in `KAOJU:ENV-GATE-REVISION`.
5. Create a durable file-backed `KAOJU:SMOKE-RUN-SCRIPT` under the Artifact owner surface. A Run-tied staged copy may execute, but neither source-tree nor Local Tmp Surface copies become canonical.
6. Execute through `smoke_run` and record `KAOJU:SMOKE-RUN-RESULT`. Environment readiness requires a successful task-critical observation, not only environment creation.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Research owner: `isomer-ext-kaoju-entrypoint->trial`; operational owner: the environment Service Request handled by the Service Team. Outputs: plan, Service Request, Gate revision, Pixi environment, smoke script, smoke result, command request, blocker, and provenance refs.

## Gates, Blockers, and Resume

Dependency mutation follows the plan authorization and Gate. Unsatisfiable constraints, lock failure, unavailable toolchain, smoke failure, or material repair pauses at plan, dispatch, resolve, smoke, or repair.
