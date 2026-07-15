# Choose Directions

## Workflow

1. Resolve Workspace Readiness, the Survey Contract, prior Direction Set revisions, and the active Run.
2. Ask only material boundary questions. Propose three directions by default with stable ids, titles, research questions, scope, rationale, evidence opportunity, source classes, expected outputs, risks, and empirical feasibility.
3. Describe empirical feasibility as available, requires environment work, requires unavailable hardware or service, or unknown. Never filter a useful direction solely because the current host cannot execute it.
4. Let the actor select one or several proposals, add a custom direction, reject all, or request revision. Preserve rejected and revised proposals in history.
5. Require explicit human confirmation, then persist `KAOJU:DIRECTION-SET` through `project artifacts put` or `revise` with the survey scope.
6. Checkpoint the Run and return the selected direction ids. Do not build reading lists in this intent.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-frame`. Inputs: Workspace Readiness, Survey Contract, prior direction ref, actor choices. Output: one accepted scoped `KAOJU:DIRECTION-SET` revision.

## Gates, Blockers, and Resume

The confirmation Gate is mandatory. Material ambiguity, missing workspace readiness, binding failure, or rejected proposals pause at `propose-directions` or `confirm-directions`. Resume from the first incomplete stage with the Run and Direction Set refs.
