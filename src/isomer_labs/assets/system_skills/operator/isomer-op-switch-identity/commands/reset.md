# Reset

## Workflow

1. Confirm whether a persistent switched identity posture is known in the current operator session.
2. Clear the active switched posture and restore normal Project Operator identity for future plans, shell commands, and file operations.
3. Report the previously selected target kind, target name, selected Research Topic, cwd, and persistence mode when known.
4. State that future commands no longer default to the previous `topic.actors.workspace` or `agent.workspace`.
5. Preserve provenance by saying the Project Operator reset its switched posture, not that a Topic Actor process, launched Agent Instance, Houmao agent, or Execution Adapter stopped.

If the user's task does not map cleanly to these steps, use your native planning tool to clear any known persistent posture and report unknown fields as unknown.

## Guardrails

Reset does not delete workspace files, change branches, stop runtime agents, mutate Workspace Runtime records, or undo task edits. It only clears the Project Operator's remembered identity posture.
