# Switch

## Workflow

1. Parse the requested target kind, target name, selected Research Topic, and persistence mode; if any target field is ambiguous, ask for the missing value before switching.
2. Resolve the target cwd through semantic path resolution, using `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>` for a Topic Actor or `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>` for an Agent.
3. From the resolved `topic.actors.workspace` or `agent.workspace`, run `project self location` and the matching `project self check --scope topic-actor|agent` with explicit `--topic` and worker selector. Stop before mutation unless the selected worker resolves to that cwd with a nonblocking verdict.
4. Check that the resolved cwd is safe and ready for the requested task; route Topic Actor readiness gaps to `isomer-op-topic-mgr actors-diagnose` or `project topic-actors diagnose`, and route Agent Workspace gaps to `isomer-op-topic-mgr team-validate-workspaces` or available Agent Workspace setup evidence.
5. Create the session-local posture envelope with target kind, Research Topic, worker name, resolved workspace cwd, persistence mode, and provenance source and wording. Apply one-task mode by default and restore the previous Project Operator identity posture after the bounded task; apply persistent mode only when the user explicitly asks to persist for the current operator session.
6. Run task commands from the resolved `topic.actors.workspace` or `agent.workspace` with explicit `--topic` plus `--topic-actor` or `--agent` selectors whenever supported. State why before any command uses another resolved semantic path and retain the same selectors there.
7. Report status, complete posture envelope, blockers, changed paths, and provenance.

If the user's task does not map cleanly to these steps, use your native planning tool to isolate the switch target, choose one-task mode unless persistence is explicit, and ask only for unresolved target identity information.

## Operational Notes

- Do not use Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd.
- Do not claim OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution.
- Do not write persistent posture into Project Manifest, local context, Topic Workspace Manifest, Workspace Runtime, or any cross-session current-identity file.
- A manifest default or sole manifest actor does not activate a switch.

## Guardrails

- DO NOT infer the target by scanning workspace directories.
