---
name: isomer-admin-topic-workspace-mgr
description: "Prepare, validate, and summarize a Git-backed Topic Workspace layout with a shared topic repository and per-agent Agent Workspace worktrees."
---

# Isomer Admin Topic Workspace Mgr

Use this command-style operator skill when a Project Operator Session needs to prepare one Topic Workspace for topic-local collaboration through `<topic-workspace-dir>/repos/topic-main`, its `isomer-managed/` worker-facing namespace, and per-agent Git worktrees under `<topic-workspace-dir>/agents/<agent-name>`. It prepares static filesystem and Git topology, plans topic-local `agent_name` values, derives compatibility `agent_workspace_ref` values when older material needs them, writes advisory Workspace Boundary notes, and reports blockers; it does not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or replace `isomer-srv-topic-env-setup`.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default subcommand**: If this skill is invoked without a prompt and the user is not asking for help, select `topic-workspace`, load [references/topic-workspace.md](references/topic-workspace.md), and execute the full preparation workflow.
2. **Manual subcommand**: If the user names one subcommand, asks for help, or asks for one bounded operation, select that subcommand from the **Subcommands** tables, load only its detail page, execute that page's `## Workflow`, and report its output.
3. **Helper subcommand**: If the user asks for a lower-level planning or validation stage, select the matching helper page, load only that page, and keep the operation scoped to the selected stage.
4. Preserve the **Required Inputs**, **Output Contract**, and **Guardrails** for every subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project Manifest-backed Isomer context, Git worktree topology, output contract, and guardrails in this skill, then execute the plan.

## Required Inputs

- A selected Project root or Project Manifest context.
- A selected Research Topic and selected Topic Workspace resolved through Isomer context, not directory scanning.
- A role binding source when planning agents: Topic Team Instantiation Packet, Topic Agent Team Profile material, or an explicit operator-provided role-to-agent-name map.
- Operator intent for mutation before creating `repos/topic-main`, adding worktrees, writing Workspace Boundary material, or editing packet/profile `agent_name`, `agent_branch`, or compatibility `agent_workspace_ref` fields.

## Subcommands

Load only the selected reference page before executing a subcommand.

### Procedural Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, Topic Workspace, and existing workspace material through Project Manifest-backed context | [references/resolve-workspace.md](references/resolve-workspace.md) |
| `ensure-main-repo` | Create or validate `<topic-workspace-dir>/repos/topic-main` as the shared non-bare topic repository | [references/ensure-main-repo.md](references/ensure-main-repo.md) |
| `plan-agents` | Normalize agent names, map active role bindings, and plan worktree paths, branches, and derived compatibility refs | [references/plan-agents.md](references/plan-agents.md) |
| `create-worktrees` | Create or validate per-agent worktrees under `<topic-workspace-dir>/agents/<agent-name>` | [references/create-worktrees.md](references/create-worktrees.md) |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes for the topic repo and Agent Workspaces | [references/write-boundaries.md](references/write-boundaries.md) |
| `create-agent-branch` | Create a future per-agent branch under `per-agent/<agent-name>/<branch-name>` | [references/create-agent-branch.md](references/create-agent-branch.md) |
| `validate-worktrees` | Validate Git topology, branch namespace, duplicate checkout state, and packet/profile workspace refs | [references/validate-worktrees.md](references/validate-worktrees.md) |
| `summarize` | Report prepared layout, refs, validation status, blockers, and next operator action | [references/summarize.md](references/summarize.md) |

### Helper Subcommands

Helper subcommands are callable when the operator wants one implementation stage: `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, and `validate-worktrees`.

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print public usage, command boundaries, required inputs, outputs, and guardrails | [references/help.md](references/help.md) |
| `topic-workspace` | Run the normal full flow: resolve, ensure repo, plan, create worktrees, write boundaries, validate, summarize | [references/topic-workspace.md](references/topic-workspace.md) |

## Output Contract

When reporting results, include these fields in structured prose or JSON, depending on the caller's print mode:

- `research_topic_ref`: selected Research Topic id or explicit blocker.
- `topic_workspace_ref`: selected Topic Workspace id and path.
- `topic_main_repo_path`: `<topic-workspace-dir>/repos/topic-main`.
- `isomer_managed_path_status`: readiness for `isomer-managed/.gitignore`, `tracked/`, `agent-owned/`, `topic-owned/`, and `links/`.
- `agent_workspace_paths`: role id, agent name, planned Agent Workspace path, and readiness for each active role binding.
- `agent_workspace_refs`: derived compatibility packet or profile `agent_workspace_ref` values that were validated, proposed, or changed when older material needs them.
- `branch_plan`: default `per-agent/<agent-name>/main` branch, owner branch `topic-owner/main`, and future branch namespace for each agent name.
- `boundary_material_paths`: topic-level and per-agent Workspace Boundary docs written or validated.
- `validation_status`: ready, ready-with-deferrals, blocked, or not checked.
- `blockers`: unsafe repo state, unsafe path, normalized key collision, duplicate branch checkout, cross-topic ref, missing input, or unapproved mutation.
- `next_operator_action`: usually rerun a specific subcommand, update packet/profile material, run `isomer-admin-topic-team-specialize validate-topic-team`, create an Agent Team Instance through runtime workflow, or stop on blockers.

## Guardrails

Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context. Do not infer the selected Topic Workspace by scanning sibling directories.

Keep `<topic-workspace-dir>/repos/topic-main` as a normal non-bare Git repository and `<topic-workspace-dir>/agents/<agent-name>` as an Agent Workspace worktree of that repository.

Keep `agent-name` separate from Agent Instance id. The agent name owns a path and branch namespace; Workspace Runtime later creates globally unique Agent Instance ids.

Use `topic-owner/main` for the owner-managed checkout, `per-agent/<agent-name>/main` for the default per-agent branch, and `per-agent/<agent-name>/<branch-name>` for future branches. Reject empty segments, `..`, leading or trailing slash, `.lock` endings, cross-agent prefixes, and duplicate branch checkout in another worktree.

Keep worker-visible Isomer material under `repos/topic-main/isomer-managed/` or the same namespace inside each agent worktree. Treat `isomer-managed/tracked/` as the Git-shared regime, `isomer-managed/agent-owned/` as ignored material owned by the current worktree, `isomer-managed/topic-owned/` as ignored topic-owned projections, and `isomer-managed/links/` as ignored generated conveniences. Treat root `records/*` as owner-preserved records and root `runtime/*` as runtime support material.

Report blockers instead of silently repairing unsafe existing paths, non-Git repositories, branch conflicts, dirty or ambiguous repo state, missing base branches, or packet/profile refs outside the selected Topic Workspace.

Do not delete, replace, pull, reset, reinitialize, or overwrite existing repositories or Agent Workspace paths without explicit user instruction.

Do not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or claim runtime readiness from this skill. Static worktree setup becomes runtime truth only when later Workspace Runtime creation consumes validated `agent_name`, branch, and Agent Workspace path plans.

Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
