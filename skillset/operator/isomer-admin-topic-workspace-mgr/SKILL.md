---
name: isomer-admin-topic-workspace-mgr
description: "Inspect, validate, and summarize optional Git-backed Topic Workspace topology, branch helpers, boundary notes, and legacy compatibility diagnostics."
---

# Isomer Admin Topic Workspace Mgr

Use this command-style operator skill when a Project Operator Session needs optional topology inspection, branch helper operations, advisory Workspace Boundary summaries, manual compatibility operations, or legacy diagnostics for a Topic Workspace. It works through semantic workspace labels such as `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.agents_root`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`. Additional non-main topic repositories use grouped `topic.repos.*` labels and helper-created paths under `repos/extern/...`, while user-owned nonreserved storage uses `custom.*`; register those bindings through `project paths register` or `project repos create` with explicit `storage_profile` rather than editing `topic-workspace.toml` by hand. The `isomer-default.v1` layout binds collaboration labels to paths such as `<topic-workspace-dir>/repos/topic-main`, `<resolved topic.repos.main>/tmp/`, `<resolved topic.repos.main>/isomer-managed/topic-owned/readonly/extern/`, `<resolved topic.repos.main>/isomer-managed/topic-owned/writable/extern/`, `<topic-workspace-dir>/agents/<agent-name>`, and `<resolved agent.workspace>/tmp/`, but safe Topic Workspace Manifest bindings may differ. This skill inspects and summarizes static filesystem and Git topology, plans topic-local `agent_name` values, derives compatibility `agent_workspace_ref` values when older material needs them, writes advisory Workspace Boundary notes, and reports blockers. The canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`, and canonical per-agent worktree creation plus cwd proof belong to `isomer-srv-agent-env-setup`. This skill performs mutation only for explicitly requested manual topology or compatibility operations after confirming predecessor evidence or manual acceptance. It does not treat non-main topic repositories as Agent Workspace worktree sources, claim per-Agent Workspace environment readiness, own `topic.intent.agent_env_requirements` or `topic.env.agent_setup_target_spec`, or verify per-agent cwd commands. It does not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or replace topic or agent env setup services.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default subcommand**:
   - Match when this skill is invoked without a prompt and the user is not asking for help.
   - Select `topic-workspace`, load [references/topic-workspace.md](references/topic-workspace.md), and execute the full inspection and optional support workflow.
2. **Manual subcommand**:
   - Match when the user names one subcommand, asks for help, or asks for one bounded operation.
   - Select that subcommand from the **Subcommands** tables.
   - Load only its detail page, execute that page's `## Workflow`, and report its output.
3. **Helper subcommand**:
   - Match when the user asks for a lower-level planning or validation stage.
   - Select the matching helper page, load only that page, and keep the operation scoped to the selected stage.
4. Preserve the **Required Inputs**, **Output Contract**, and **Guardrails** for every subcommand.

    If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project Manifest-backed Isomer context, Git worktree topology, output contract, and guardrails in this skill, then execute the plan.

## Required Inputs

- A selected Project root or Project Manifest context.
- A selected Research Topic and selected Topic Workspace resolved through Isomer context, not directory scanning.
- A role binding source when planning agents: Topic Team Instantiation Packet, Topic Agent Team Profile material, or an explicit operator-provided role-to-agent-name map.
- Topic env predecessor evidence when the operator asks this skill to inspect a prepared Topic Main Development Repository, projection roots, or existing Agent Workspace topology.
- Operator intent for mutation before any manual topology operation, including registering Topic Workspace Manifest bindings with `label`/`path`/`storage_profile`, creating or repairing topology outside the normal service path, adding worktrees, writing Workspace Boundary material, or editing packet/profile `agent_name`, `agent_branch`, or compatibility `agent_workspace_ref` fields.

## Subcommands

Load only the selected reference page before executing a subcommand.

### Procedural Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, Topic Workspace, and existing workspace material through Project Manifest-backed context | [references/resolve-workspace.md](references/resolve-workspace.md) |
| `ensure-main-repo` | Inspect or validate the resolved `topic.repos.main` path, with manual topology creation only when explicitly requested | [references/ensure-main-repo.md](references/ensure-main-repo.md) |
| `plan-agents` | Normalize agent names, map active role bindings, and plan worktree paths, branches, and derived compatibility refs | [references/plan-agents.md](references/plan-agents.md) |
| `create-worktrees` | Inspect, validate, or manually create per-agent worktrees at the resolved `agent.workspace` path for each Agent Name | [references/create-worktrees.md](references/create-worktrees.md) |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes for the topic repo and Agent Workspaces | [references/write-boundaries.md](references/write-boundaries.md) |
| `create-agent-branch` | Create a future per-agent branch under `per-agent/<agent-name>/<branch-name>` | [references/create-agent-branch.md](references/create-agent-branch.md) |
| `validate-worktrees` | Validate Git topology, branch namespace, duplicate checkout state, and packet/profile workspace refs | [references/validate-worktrees.md](references/validate-worktrees.md) |
| `summarize` | Report inspected layout, refs, validation status, blockers, and next operator action | [references/summarize.md](references/summarize.md) |

### Helper Subcommands

Helper subcommands are callable when the operator wants one implementation stage: `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, and `validate-worktrees`.

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print public usage, command boundaries, required inputs, outputs, and guardrails | [references/help.md](references/help.md) |
| `topic-workspace` | Run the full support flow: resolve, inspect topic-main, plan agents, optionally create worktrees when explicitly requested, write boundaries, validate, summarize | [references/topic-workspace.md](references/topic-workspace.md) |

## Output Contract

When reporting results, include these fields in structured prose or JSON, depending on the caller's print mode:

- `research_topic_ref`: selected Research Topic id or explicit blocker.
- `topic_workspace_ref`: selected Topic Workspace id and path.
- `semantic_paths`: resolved labels, paths, sources, readiness, and blockers for `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.agents_root`, `topic.records`, `topic.runtime`, `agent.workspace`, `agent.tmp`, and required agent support labels.
- `topic_main_repo_path`: resolved `topic.repos.main` path.
- `isomer_managed_path_status`: readiness for `isomer-managed/.gitignore`, `tracked/`, `agent-owned/`, `topic-owned/`, projection roots, and `links/`.
- `local_tmp_path_status`: readiness for `topic.repos.main.tmp` and `agent.tmp`, including resolved paths, ignored posture, tracked-content diagnostics, and confirmation that tmp material is not shared or durable evidence.
- `agent_workspace_paths`: role id, agent name, resolved `agent.workspace` path, source, and readiness for each active role binding.
- `agent_workspace_refs`: derived compatibility packet or profile `agent_workspace_ref` values that were validated, proposed, or changed when older material needs them.
- `branch_plan`: default `per-agent/<agent-name>/main` branch, owner branch `topic-owner/main`, and future branch namespace for each agent name.
- `boundary_material_paths`: topic-level and per-agent Workspace Boundary docs written or validated.
- `validation_status`: ready, ready-with-deferrals, blocked, or not checked.
- `agent_environment_service_output`: optional summarized `isomer-srv-agent-env-setup` evidence when a caller already requested per-Agent Workspace cwd verification, including `source_agent_env_gate_path`, `agent_env_gate_path`, readiness by agent, overall readiness, commands run, blockers, and next action.
- `blockers`: unsafe repo state, unsafe path, normalized key collision, duplicate branch checkout, cross-topic ref, missing input, or unapproved mutation.
- `next_operator_action`: usually rerun a specific subcommand, update packet/profile material, make a caller-requested `isomer-srv-agent-env-setup` call after topic env predecessor evidence exists, run `isomer-admin-topic-team-specialize validate-topic-team`, create an Agent Team Instance through runtime workflow, or stop on blockers.

## Guardrails

Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context. Do not infer the selected Topic Workspace by scanning sibling directories.

Use Workspace Path Resolution commands for storage answers. Use `project paths get` for selected paths, `project paths explain` for source diagnostics, `project paths register` for explicit `label`/`path`/`storage_profile` bindings, and `project repos create` for additional non-main grouped `topic.repos.*` repository labels that default under `repos/extern/...`.

Do not present this skill as the canonical creator of `topic.repos.main`, projection roots, or per-agent worktrees in the normal topic-team setup path. Route canonical Topic Main Development Repository setup and projection materialization to `isomer-srv-topic-env-setup`; route canonical Agent Workspace worktree creation and cwd verification to `isomer-srv-agent-env-setup`.

Keep the resolved `topic.repos.main` path as a normal non-bare Git repository and each resolved `agent.workspace` path as an Agent Workspace worktree of that repository.

Keep `agent-name` separate from Agent Instance id. The agent name owns a path and branch namespace; Workspace Runtime later creates globally unique Agent Instance ids.

Use `topic-owner/main` for the owner-managed checkout, `per-agent/<agent-name>/main` for the default per-agent branch, and `per-agent/<agent-name>/<branch-name>` for future branches. Reject empty segments, `..`, leading or trailing slash, `.lock` endings, cross-agent prefixes, and duplicate branch checkout in another worktree.

Keep worker-visible Isomer material under the resolved `topic.repos.main.isomer_managed` path or the corresponding `agent.*` support labels inside each Agent Workspace. Treat `isomer-managed/tracked/` as the Git-shared regime, `isomer-managed/topic-owned/{readonly,writable}/extern/` as external repo projection roots, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.inbox` as agent-owned material, `agent.topic_readonly` and `agent.topic_writable` as topic-owned projections, and `agent.links` as generated conveniences. Treat `topic.records.*` as owner-preserved records and `topic.runtime` as runtime support material. Treat `topic.repos.main.tmp` and `agent.tmp` as local ignored disposable surfaces only; do not describe tmp contents as Peer Read Access, generated-link target material, handoff material, shared material, or durable readiness evidence.

Report blockers instead of silently repairing unsafe existing paths, non-Git repositories, branch conflicts, dirty or ambiguous repo state, missing base branches, or packet/profile refs outside the selected Topic Workspace.

Do not delete, replace, pull, reset, reinitialize, or overwrite existing repositories or Agent Workspace paths without explicit user instruction.

Do not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or claim runtime readiness from this skill. Validated topology evidence becomes runtime truth only when later Workspace Runtime creation consumes validated `agent_name`, branch, and Agent Workspace path plans.

Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
