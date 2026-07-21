# Status

## Workflow

1. Report whether a switched identity posture is active, persistent, temporary for the current task, restored after `act-as`, reset, unknown, or unavailable.
2. If active, report the complete session-local posture envelope: target kind, worker name, selected Research Topic, resolved `topic.actors.workspace` or `agent.workspace`, path and target-resolution source, persistence mode, and provenance wording.
3. If uncertain after context compaction or missing evidence, say the posture is uncertain and re-resolve before running commands as that identity.
4. State the current cwd rule: target workspace cwd when switched, normal Project Operator cwd when reset or not switched.
5. Report provenance without claiming OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution.
6. If `project self identity` reports only a manifest-default actor or agent candidate and no session envelope exists, report normal Project Operator posture; never infer that a switch is active.

If the user's task does not map cleanly to these steps, use your native planning tool to produce the shortest accurate status and mark unknown fields as uncertain rather than inventing state.

## Operational Contract

- Keep status read-only.
- Status reads only current-session memory and resolved Project evidence; it does not create or consult shared current-identity state.

## Guardrails

- DO NOT switch, reset, or run worker task commands from this command unless the user separately asks for `switch`, `act-as`, or `reset`.
