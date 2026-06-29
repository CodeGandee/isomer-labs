# Help

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Help intent | Use this page when the prompt names `help`, asks for usage, or invokes the skill without a concrete setup task. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-srv-agent-env-setup` prepares service-safe Agent Workspace cwd readiness from Topic Workspace predecessor evidence and is the owner of `agent-env-gate.md`, `isomer-agent-env-gate.md`, selected-agent partial evidence, and overall Agent Workspace readiness.
2. Explain that concrete setup defaults to `setup-agent-env`, while direct subcommands are available for manual setup, inspection, or partial repair.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs: Project Manifest context, registered Research Topic, Topic Workspace, ready topic env predecessor, `user-intent/src/agent-env-gate.md`, authoritative Topic Team Instantiation Packet or derived Topic Agent Team Profile Agent Names, semantic path evidence, and mutation confirmation.
5. State the output contract: semantic paths with labels and sources, requester, confirmation source, optional Service Request or Provenance refs, Topic Main Repository, agent workspace paths, branch plan, worktree status by agent, readiness by agent, overall readiness, commands run, blockers, and next action.
6. State the key guardrails: no per-agent Pixi environments, no dependency mutation by default, no directory-scan agent selection, no silent Git repair, no Agent Instance creation, no Workspace Runtime mutation, no Houmao launch, no Execution Adapter operation, and no research decision authority.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-agent-env-context` | Resolve Project, Research Topic, Topic Workspace, Pixi binding, semantic paths, and invocation posture. | `semantic_paths`, requester, confirmation source, optional refs, and blockers. |
| `require-topic-env-ready` | Require Topic Workspace Pixi predecessor readiness. | `topic_environment_status`, predecessor gate path, and repair route. |
| `read-agent-env-gate` | Read the source Agent Workspace cwd gate. | Source gate summary, commands, expected results, cwd assumptions, and blockers. |
| `plan-agent-workspaces` | Plan Agent Workspaces from authoritative topic-team material. | Agent Names, branches, semantic paths, path sources, and blockers. |
| `derive-agent-env-gate` | Write the derived operational gate. | `agent_env_gate_path` and verification matrix. |
| `ensure-topic-main-repository` | Prepare the Topic Main Repository. | `topic_main_repository`, owner branch, changed files, commands run, blockers. |
| `create-agent-worktrees` | Prepare per-agent worktrees and support paths. | `worktree_status_by_agent`, support labels, boundary material posture, blockers. |
| `verify-agent-env-gate` | Verify cwd commands from Agent Workspace paths. | `readiness_by_agent`, selected-agent partial evidence, commands run, blockers. |
| `setup-agent-env` | Run the full all-agent flow. | Combined setup report and `overall_readiness_status`. |
| `help` | Print usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Examples

- `$isomer-srv-agent-env-setup setup-agent-env <topic-id>`
- `$isomer-srv-agent-env-setup verify-agent-env-gate <topic-id> --agent analyst`
- `$isomer-srv-agent-env-setup require-topic-env-ready for <topic-id>`

## Boundary Notes

This service complements `isomer-srv-topic-env-setup`, which produces Topic Workspace predecessor evidence, and `isomer-admin-topic-workspace-mgr`, which owns Git-only static topology flows. It is the env-gate-aware service for per-agent Agent Workspace cwd verification.
