# Status

## Workflow

1. Report whether a switched identity posture is active, persistent, temporary for the current task, restored after `act-as`, reset, unknown, or unavailable.
2. If active, report target kind, target name, selected Research Topic, resolved `topic.actors.workspace` or `agent.workspace`, path source, and persistence mode.
3. If uncertain after context compaction or missing evidence, say the posture is uncertain and re-resolve before running commands as that identity.
4. State the current cwd rule: target workspace cwd when switched, normal Project Operator cwd when reset or not switched.
5. Report provenance without claiming OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution.

If the user's task does not map cleanly to these steps, use your native planning tool to produce the shortest accurate status and mark unknown fields as uncertain rather than inventing state.

## Guardrails

Status is read-only. Do not switch, reset, or run worker task commands from this command unless the user separately asks for `switch`, `act-as`, or `reset`.
