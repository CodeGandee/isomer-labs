# Env Verify Agents

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, role binding source, authoritative Agent Names, `topic.repos.main`, `agent.workspace`, and required `agent.*` support labels.
2. Inspect topic env predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, and `topic.env.agent_setup_target_spec` or explicit agent target spec.
3. Route formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup` with selected Research Topic, Topic Workspace, Agent Names, semantic path expectations, and requested verification scope.
4. Consume returned service evidence for worktree status, cwd verification status, commands run, selected-agent partial status, blockers, and next action.
5. Report formal Agent Workspace readiness without claiming Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter readiness, or runtime launch readiness.

If the user's task does not map cleanly to these steps, route the smallest safe verification request to `isomer-srv-agent-env-setup` and report any missing predecessor evidence as a blocker.

## Output

Report the Agent environment verification outcome and selected Research Topic, then summarize Agent Names and workspace paths, semantic paths, service and command evidence, blockers, and the next action.

## Operational Notes

- The env-gate-aware service owner is `isomer-srv-agent-env-setup`.

## Guardrails

- DO NOT hand-roll formal Agent Workspace cwd proof in this skill.
