# Act As

## Workflow

1. Parse the target kind, target name, selected Research Topic, and the following prompt that must be executed once under that identity posture.
2. Resolve the target cwd through semantic path resolution, using `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>` for a Topic Actor or `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>` for an Agent.
3. Save the previous Project Operator identity posture before running the prompt.
4. Execute only the following prompt as or on behalf of the selected Topic Actor or Agent, with shell commands and file operations defaulting to the resolved `topic.actors.workspace` or `agent.workspace`.
5. Restore the previous Project Operator identity posture immediately after the prompt's task summary, even if the task blocks or partially completes.
6. Report the target identity, resolved cwd, one-prompt restore behavior, commands run outside cwd, blockers, and provenance.

If the user's task does not map cleanly to these steps, use your native planning tool to split target selection from the one prompt, then ask for missing target or prompt content before acting.

## Operational Contract

- Treat `act-as` as temporary one-time execution, not a persistent switch.

## Guardrails

- DO NOT leave a switched posture active after the following prompt completes unless the user separately requests `switch` with persistent mode.
- DO NOT claim a launched Agent Instance, Houmao agent, independent Topic Actor process, or Execution Adapter produced the work.
