# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description: `isomer-admin-topic-workspace-mgr` prepares a Git-backed Topic Workspace layout with `repos/topic-main` and per-agent Agent Workspace worktrees.
2. Explain that invoking the skill without a prompt defaults to `topic-workspace`, while explicit help prints this usage surface.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs: Project Manifest context, Research Topic, Topic Workspace, optional packet/profile material, and any requested agent-name mapping.
5. State the output contract: topic repo path, records root, runtime root, agent workspace paths, branch plan, derived compatibility `agent_workspace_ref` values, boundary docs, validation status, blockers, and next operator action.
6. State the key guardrails: no directory-scanning selection, no silent Git repair, no cross-topic refs, no Agent Instance creation, no Workspace Runtime mutation, no Houmao launch, and no Execution Adapter operation.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed context. | Topic Workspace path, `repos/topic-main` path, candidate packet/profile material, blockers. |
| `ensure-main-repo` | Create or validate the shared non-bare topic repository. | `topic_main_repo_path`, base branch, repo readiness, blockers. |
| `plan-agents` | Normalize agent names and map active role bindings to worktree paths and branches. | Agent name map, derived compatibility refs, `per-agent/<agent-name>/main` branch plan. |
| `create-worktrees` | Create or validate per-agent Git worktrees. | Ready or created Agent Workspace worktrees, skipped entries, blockers. |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes. | Boundary material paths, ownership notes, branch rules. |
| `create-agent-branch` | Create a future per-agent branch under the owning agent prefix. | `per-agent/<agent-name>/<branch-name>` branch result, base ref, blockers. |
| `validate-worktrees` | Validate Git topology and packet/profile workspace refs. | `validation_status`, ready entries, cross-topic or Git blockers. |
| `summarize` | Summarize prepared layout and next operator action. | Consumer-neutral report with paths, branches, refs, blockers, and next action. |
| `topic-workspace` | Run the full normal preparation flow. | Shared repo, per-agent worktrees, boundary material, validation result, summary. |
| `help` | Print this usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Boundary Notes

This skill complements `isomer-admin-topic-team-specialize`: specialization defines topic-team material and static setup evidence, while this skill prepares the Git-backed Topic Workspace worktree layout used by `setup-agent-workspace` when requested.

This skill also stays separate from `isomer-srv-topic-env-setup`, which owns gate-driven topic environment setup and independent repository acquisition for environment checks.
