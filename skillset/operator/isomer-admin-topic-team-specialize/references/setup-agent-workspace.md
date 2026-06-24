# Setup Agent Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the specialized topic-team shape, expected Agent Roles, draft profile inputs, Topic Workspace path, and Workspace Runtime posture.
2. Determine the per-agent Agent Workspace directories, ownership notes, allowed file surfaces, and boundary notes needed for the expected Agent Instances.
3. Create or report Agent Workspace directories only after the specialized team shape is clear and the target paths are safe.
4. Record workspace paths, role ownership, boundary notes, skipped actions, blockers, and validation refs.
5. Report `agent_workspace_paths`, unresolved workspace blockers, and whether `validate-topic-team` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step Agent Workspace setup plan from the specialized team shape, Topic Workspace boundary, and guardrails, then execute the plan.

## Guardrails

Use **Topic Workspace** for the topic-level work area and **Agent Workspace** for per-agent work areas.

Do not create Agent Workspaces before team specialization defines expected roles or Agent Instances.

Do not use Agent Workspace setup as a substitute for Workspace Runtime registration when runtime records are required.
