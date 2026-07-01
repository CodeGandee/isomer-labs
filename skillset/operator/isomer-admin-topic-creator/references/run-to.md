# Run To

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Parse the requested target procedural subcommand. Valid targets are `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, and `finalize`.
2. Reject missing, unknown, helper, misc, or non-main-workflow targets. Report that `run-to` only accepts procedural main workflow targets and list the valid targets.
3. Detect explicit inclusive wording such as `through <target>`, `include <target>`, or `<target> inclusive`. Without explicit inclusive wording, exclude the target by default.
4. Use the same readiness ladder and reuse rules as `fast-forward`: `ensure-project`, `resolve-topic-input`, `register-topic`, `create-research-intent`, `init-runtime`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, `bootstrap-research`, and `finalize`.
5. In default mode, run or validate only the predecessor stages needed to stop before the target. Report that the target was excluded by default.
6. In inclusive mode, run or validate predecessor stages and then run the target when its prerequisites and required inputs are available.
7. Stop at missing user input, missing selected context, unresolved semantic paths, or blocked predecessor conditions. Do not skip a blocked step to reach a later target.
8. If inclusive mode reaches a blocked target, report the missing input or dependency and do not treat the target as completed.
9. If inclusive `run-to finalize` succeeds, write `topic.workspace.summary` and stop after the ready/verified/blocked report. If default `run-to finalize` is used, stop before `finalize` and do not write or refresh the summary.

If the user's task does not map cleanly to these steps, report the valid target list and ask for one procedural target.

## Guardrails

`run-to` is automatic like `fast-forward`, not interactive like `step-by-step`. It still must stop before mutation that lacks required inputs, selected context, semantic path resolution, or operator approval.

Do not accept helper commands such as `ensure-project`, `resolve-topic-input`, `register-topic`, `init-runtime`, or `bootstrap-research` as `run-to` targets. They are internal ladder stages used to reach procedural targets.

Do not run the target by default. Include it only when the user explicitly asks for inclusive execution.
