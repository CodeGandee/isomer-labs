# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-admin-topic-workspace-mgr` prepares Git-backed Topic Workspace surfaces through semantic labels such as `topic.main_repo`, `topic.main_repo.isomer_managed`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`.
2. Explain that invoking the skill without a prompt defaults to `topic-workspace`, while explicit help prints this usage surface.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs: Project Manifest context, Research Topic, Topic Workspace, optional packet/profile material, and any requested agent-name mapping.
5. State the output contract: semantic paths with labels and sources, topic repo path, `isomer-managed/` regime status, records root, runtime root, agent workspace paths, branch plan, derived compatibility `agent_workspace_ref` values, boundary docs, generated links, optional `isomer-srv-agent-env-setup` evidence when already available, validation status, blockers, and next operator action.
6. State the key guardrails: no directory-scanning selection, no silent Git repair, no cross-topic refs, no Agent Instance creation, no Workspace Runtime mutation, no Houmao launch, and no Execution Adapter operation.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, Topic Workspace, and semantic paths through Project Manifest-backed context. | Topic Workspace path, semantic paths, candidate packet/profile material, blockers. |
| `ensure-main-repo` | Create or validate the resolved `topic.main_repo` path and tracked Isomer namespace. | `topic_main_repo_path`, `isomer_managed_path_status`, base branch, repo readiness, blockers. |
| `plan-agents` | Normalize agent names and map active role bindings to resolved `agent.workspace` paths and branches. | Agent name map, semantic paths, derived compatibility refs, `per-agent/<agent-name>/main` branch plan. |
| `create-worktrees` | Create or validate per-agent Git worktrees and ignored `agent.*` support paths. | Ready or created Agent Workspace worktrees, `isomer-managed/` regime status, skipped entries, blockers. |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes. | Boundary material paths, ownership notes, branch rules, generated-link notes. |
| `create-agent-branch` | Create a future per-agent branch under the owning agent prefix. | `per-agent/<agent-name>/<branch-name>` branch result, base ref, blockers. |
| `validate-worktrees` | Validate Git topology, `isomer-managed/` layout, generated links, and packet/profile workspace refs. | `validation_status`, ready entries, cross-topic, layout, or Git blockers. |
| `summarize` | Summarize prepared layout and next operator action. | Consumer-neutral report with paths, branches, `isomer-managed/` regimes, generated links, refs, blockers, and next action. |
| `topic-workspace` | Run the full normal preparation flow. | Shared repo, per-agent worktrees, `isomer-managed/` material, boundary material, validation result, summary. |
| `help` | Print this usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Boundary Notes

This skill complements `isomer-admin-topic-team-specialize`: specialization defines topic-team material and static setup evidence, while this skill prepares the Git-backed Topic Workspace worktree layout used by `setup-agent-workspace` when requested.

This skill also stays separate from `isomer-srv-topic-env-setup`, which owns gate-driven topic environment setup and independent repository acquisition for environment checks.

This skill stays separate from `isomer-srv-agent-env-setup`, which owns `user-intent/src/agent-env-gate.md`, `user-intent/derived/isomer-agent-env-gate.md`, Topic Main Repository environment configuration, per-Agent Workspace cwd verification, readiness by Agent Name, and partial selected-agent repair evidence. Route requests for per-agent environment readiness to that service after Git topology evidence exists.
