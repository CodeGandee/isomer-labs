# Verify Agent Env Gate

Use this subcommand to verify the Topic Workspace Pixi environment from each planned Agent Workspace cwd, or to rerun verification for one authoritative Agent Name as partial evidence.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require Project, Research Topic, Topic Workspace, `manifest_path`, `pixi_environment`, semantic paths, requester, and confirmation source. |
| Topic env predecessor | Require ready or explicitly accepted Topic Workspace predecessor evidence from `require-topic-env-ready`. |
| Agent env target spec | Require resolved `topic.env.agent_setup_target_spec` from `derive-agent-env-gate`. |
| Worktree evidence | Require `create-agent-worktrees` output or read-only equivalent showing valid worktrees, support paths, and path evidence. |
| Optional selected agent | Optional. It must be one authoritative Agent Name and reports selected-agent partial readiness evidence only. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: resolved context, Topic Workspace predecessor evidence, agent env target spec, authoritative agent plan, and worktree evidence.
2. **Read the agent env target spec** and extract `## Verification Matrix`, `## Expected Results`, `## Blockers`, `## Topic Pixi Binding`, and `## Execution Log`.
3. **Check Pixi files**:
   - Confirm the resolved `manifest_path`, selected `pixi_environment`, Topic Workspace `pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
4. **Choose target agents**:
   - Default to every authoritative planned Agent Name.
   - If a selected Agent Name is provided, verify only that authoritative name and label the result as selected-agent partial readiness evidence.
5. **Confirm commands are replayable**:
   - Each verification command must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
   - Set cwd to the resolved `agent.workspace` for the target Agent Name.
6. **Verify cwd-friendly semantic path query evidence**:
   - Include or record a check that an agent-scoped semantic label can be resolved from inside each target Agent Workspace without passing Agent Name.
7. **Run verification commands** from the resolved `agent.workspace` cwd:
   - Do not rely on an activated shell, ambient Python environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script.
8. **Compare results to expected outputs** from the target spec and mark each agent command as ready, failed, or blocked.
9. **Update the target spec execution log**:
   - Include Agent Name, cwd, command, exit status, output summary, pass/fail result, partial scope when selected, blockers, and next repair action.
10. **Report readiness**:
   - Use `overall_readiness_status: ready` only when every planned agent has a ready worktree, required support paths, complete path evidence, cwd-friendly query evidence, and every required agent-env-gate command passes from that agent's cwd.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.env.agent_setup_target_spec`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all targeted commands passed from the resolved Agent Workspace cwd through recorded Pixi-scoped commands.
- `failed`: commands ran and did not satisfy expected results.
- `blocked`: predecessor artifacts, Pixi files, worktrees, support paths, path evidence, cwd query evidence, commands, or expected results are missing.
- `not checked`: verification was not requested or was intentionally deferred.

Selected-agent direct verification updates that agent's evidence but does not make `overall_readiness_status` ready unless the complete matrix has already passed.

## Guardrails

- Do not claim readiness from topic-root-only success.
- Treat Topic Workspace readiness as prerequisite evidence only; every requested Agent Workspace cwd must be verified by this subcommand before reporting per-agent readiness.
- Report `gate-cwd-incompatible` or equivalent when a topic env command cannot run from Agent Workspace cwd.
- Do not create Agent Instances, Workspace Runtime records, Houmao launch material, or Execution Adapter material.
- Do not suppress partial failures; readiness by agent and blockers must remain visible.
