# Switch

## Workflow

1. Parse the requested target kind, target name, selected Research Topic, and persistence mode; if any target field is ambiguous, ask for the missing value before switching.
2. Resolve the target cwd through semantic path resolution, using `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>` for a Topic Actor or `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>` for an Agent.
3. Check that the resolved cwd is safe and ready for the requested task; route Topic Actor readiness gaps to `isomer-op-topic-mgr actors-diagnose` or `project topic-actors diagnose`, and route Agent Workspace gaps to `isomer-op-topic-mgr team-validate-workspaces` or available Agent Workspace setup evidence.
4. Apply one-task mode by default and restore the previous Project Operator identity posture after the bounded task; apply persistent mode only when the user explicitly asks to persist for the current operator session.
5. Run task commands from the resolved `topic.actors.workspace` or `agent.workspace`; state why before any command uses another resolved semantic path.
6. Report status, target identity, cwd, persistence mode, blockers, changed paths, and provenance.

If the user's task does not map cleanly to these steps, use your native planning tool to isolate the switch target, choose one-task mode unless persistence is explicit, and ask only for unresolved target identity information.

## Guardrails

- DO NOT infer the target by scanning workspace directories. Do not use Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd. Do not claim OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution.
