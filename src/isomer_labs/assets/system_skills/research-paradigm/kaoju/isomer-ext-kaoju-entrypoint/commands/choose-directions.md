---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Choose Directions

## Workflow

1. Resolve Workspace Readiness, the Survey Contract, prior Direction Set revisions, and the active Run.
2. Ask only material boundary questions. Propose three directions by default with stable direction ids, canonical semantic `idea_id` values, titles, summaries, research questions, scope, rationale, evidence opportunity, source classes, expected outputs, risks, empirical feasibility, exact proposal paths, and one proposal-generation id.
3. Describe empirical feasibility as available, requires environment work, requires unavailable hardware or service, or unknown. Never filter a useful direction solely because the current host cannot execute it.
4. Let the actor select one or several proposals, add a custom direction, close or defer a proposal with reason, reject all, or request revision. Author one option outcome and disposition rationale per proposal. A merely unselected proposal remains open.
5. Require explicit human confirmation, invoke `isomer-op-entrypoint->research-ideas`, and persist `KAOJU:DIRECTION-SET` through the active v2 `project artifacts put` or `revise` binding. Include `research_idea_effects` with `atomic=true`, explicit facets, every exact realization, one complete generation, every Decision Record option, and each justified transition with actor, rationale, closure reason, and terminal refs.
6. Inspect returned record and canonical refs, query the Direction Set decision context, resolve proposal realizations, and run `ext research ideas validate`. Checkpoint the Run only after verification, then return selected direction ids. Do not build reading lists in this intent.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->frame`. Inputs: Workspace Readiness, Survey Contract, prior direction ref, actor choices. Output: one accepted scoped `KAOJU:DIRECTION-SET` revision.

## Gates, Blockers, and Resume

The confirmation Gate is mandatory. Material ambiguity, missing workspace readiness, binding failure, or rejected proposals pause at `propose-directions` or `confirm-directions`. Resume from the first incomplete stage with the Run and Direction Set refs.
