# Run To

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Parse the requested target procedural subcommand. Valid targets are `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, and `finalize`.
2. If `run-to` was selected by the default bare topic-creation dispatch and the user did not name a target, use target `finalize` with the `finalize` target included by default.
3. Reject missing, unknown, helper, misc, or non-main-workflow targets. Report that `run-to` only accepts procedural main workflow targets and list the valid targets.
4. Detect explicit exclusion wording such as `before <target>`, `stop before <target>`, `excluding <target>`, or `up to but not including <target>`. Without explicit exclusion wording, include the target by default.
5. Use the same readiness ladder and reuse rules as `fast-forward`: `ensure-project`, `resolve-topic-input`, `register-topic`, `create-research-intent`, `init-runtime`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, and `finalize`.
6. In default inclusive mode, run or validate predecessor stages and then run the target when its prerequisites and required inputs are available.
7. In explicit exclusion mode, run or validate only the predecessor stages needed to stop before the target. Report that the target was excluded because the user asked to stop before it.
8. Stop at missing user input, missing selected context, unresolved semantic paths, or blocked predecessor conditions. Do not skip a blocked step to reach a later target.
9. If default inclusive mode reaches a blocked target, report the missing input or dependency and do not treat the target as completed.
10. If `run-to finalize` succeeds in default inclusive mode, write `topic.workspace.summary` and stop after the ready/verified/blocked report. If explicit exclusion is used with `run-to finalize`, stop before `finalize` and do not write or refresh the summary.

If the user's task does not map cleanly to these steps, report the valid target list and ask for one procedural target.

## Guardrails

`run-to` is automatic like `fast-forward`, not interactive like `step-by-step`. It still must stop before mutation that lacks required inputs, selected context, semantic path resolution, or operator approval.

Do not accept helper commands such as `ensure-project`, `resolve-topic-input`, `register-topic`, or `init-runtime` as `run-to` targets. They are internal ladder stages used to reach procedural targets.

Do not stop before the target by default. Exclude the target only when the user explicitly asks to stop before it.
