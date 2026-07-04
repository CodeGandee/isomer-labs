# Help

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Help intent | Use this page when the prompt names `help`, asks for usage, or invokes the skill without a concrete setup task. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description:
   - `isomer-srv-agent-env-setup` prepares service-safe Agent Workspace cwd readiness from Topic Workspace and Topic Main Development Repository predecessor evidence.
   - It owns selected-agent partial evidence, Agent Workspace worktrees, and overall Agent Workspace readiness; in the normal operator flow, `isomer-op-topic-team-specialize` owns the derived target specs.
2. Explain that concrete setup defaults to `setup-agent-env`, while direct subcommands are available for manual setup, inspection, or partial repair.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs:
   - Include Project Manifest context, registered Research Topic, Topic Workspace, ready `topic.env.topic_setup_target_spec` predecessor evidence, ready Topic Main Development Repository and projection predecessor evidence, `topic.intent.agent_env_requirements` or an explicit manual target spec, authoritative Topic Team Instantiation Packet or derived Topic Agent Team Profile Agent Names, semantic path evidence, and mutation confirmation.
5. State the output contract:
   - Include semantic paths with labels and sources, requester, confirmation source, optional Service Request or Provenance refs, Topic Main Development Repository predecessor evidence, projection predecessor evidence, agent workspace paths, branch plan, worktree status by agent, readiness by agent, overall readiness, commands run, blockers, and next action.
6. State the key guardrails:
   - No per-agent Pixi environments, dependency mutation by default, directory-scan agent selection, topic-main/projection repair, or silent Git repair.
   - No Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter operation, or research decision authority.
   - Literal guardrails: no per-agent Pixi environments, no dependency mutation by default, no Workspace Runtime mutation, and no Execution Adapter operation.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project, Research Topic, Topic Workspace, Pixi binding, semantic paths, and invocation posture. | `semantic_paths`, requester, confirmation source, optional refs, and blockers. |
| `require-topic-env-ready` | Require Topic Workspace Pixi predecessor readiness. | `topic_environment_status`, predecessor target spec path, and repair route. |
| `require-topic-main-ready` | Require prepared topic-main and projection predecessor evidence. | `topic_main_repository`, projection predecessor status, and repair route. |
| `read-agent-env-gate` | Read the source Agent Workspace cwd intent. | Source intent metadata, commands, expected results, cwd assumptions, and blockers. |
| `plan-agent-workspaces` | Plan Agent Workspaces from authoritative topic-team material. | Agent Names, branches, semantic paths, path sources, and blockers. |
| `derive-agent-env-gate` | Write or validate the per-agent operational target spec. | `agent_env_target_spec_path`, target spec source, and verification matrix. |
| `create-agent-worktrees` | Prepare per-agent worktrees and support paths. | `worktree_status_by_agent`, support labels, boundary material posture, blockers. |
| `verify-agent-env-gate` | Verify cwd commands from Agent Workspace paths. | `readiness_by_agent`, selected-agent partial evidence, commands run, blockers. |
| `setup-agent-env` | Run the full all-agent flow. | Combined setup report and `overall_readiness_status`. |
| `help` | Print usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Examples

- `$isomer-srv-agent-env-setup setup-agent-env <topic-id>`
- `$isomer-srv-agent-env-setup verify-agent-env-gate <topic-id> --agent analyst`
- `$isomer-srv-agent-env-setup require-topic-env-ready for <topic-id>`
- `$isomer-srv-agent-env-setup require-topic-main-ready for <topic-id>`

## Boundary Notes

This service complements `isomer-srv-topic-env-setup`, which produces Topic Workspace, topic-main, and projection predecessor evidence, and `isomer-op-topic-mgr`, which handles optional topology inspection, branch-helper support, boundary summaries, and `env-verify-agents` routing. It is the env-gate-aware service for per-agent Agent Workspace cwd verification.
