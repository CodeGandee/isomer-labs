---
name: isomer-admin-topic-workspace-mgr
description: "Inspect, validate, and summarize Topic Workspace topology, including Topic Actor CRUD, Topic Actor Workspace materialization or repair, actor-scoped path diagnostics, optional Git-backed topology inspection, branch helpers, package installation into the selected Topic Workspace Pixi environment, boundary notes, and topology diagnostics."
---

# Isomer Admin Topic Workspace Mgr

Use this command-style operator skill when a Project Operator Session needs Topic Actor CRUD, Topic Actor Workspace materialization or repair, actor-scoped path diagnostics, optional topology inspection, branch helper operations, package installation into the selected Topic Workspace Pixi environment, advisory Workspace Boundary summaries, manual topology operations, or diagnostics for a Topic Workspace. It works through semantic workspace labels such as `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.actors_root`, `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, `topic.agents_root`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`. Additional non-main topic repositories use grouped `topic.repos.*` labels and helper-created paths under `repos/extern/...`, while user-owned nonreserved storage uses `custom.*`; register those bindings through `project paths register` or `project repos create` with explicit `storage_profile` rather than editing `topic-workspace.toml` by hand. The `isomer-default.v1` layout binds collaboration labels to paths such as `<topic-workspace-dir>/repos/topic-main`, `<resolved topic.repos.main>/tmp/`, `<resolved topic.repos.main>/isomer-managed/topic-owned/readonly/extern/`, `<resolved topic.repos.main>/isomer-managed/topic-owned/writable/extern/`, `<topic-workspace-dir>/actors/<topic-actor-name>`, `<resolved topic.actors.workspace>/tmp/`, `<topic-workspace-dir>/agents/<agent-name>`, and `<resolved agent.workspace>/tmp/`, but safe Topic Workspace Manifest bindings may differ. This skill inspects and summarizes static filesystem and Git topology, manages Topic Actor bindings as Topic Workspace Manifest topology authority, plans topic-local `agent_name` values, derives compatibility `agent_workspace_ref` values when older material needs them, installs requested packages through the selected Topic Workspace Pixi environment, writes advisory Workspace Boundary notes, and reports blockers. The canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`, and canonical per-agent worktree creation plus cwd proof belong to `isomer-srv-agent-env-setup`. This skill performs mutation only for explicitly requested actor topology, explicitly requested package installation, or manual topology operations after confirming predecessor evidence or manual acceptance. Topic Actor registration and materialization may write Workspace Runtime mutation or provenance audit records when runtime is available, but the Topic Workspace Manifest remains the topology and path-resolution authority. It does not treat non-main topic repositories as Topic Actor Workspace or Agent Workspace worktree sources, claim per-Agent Workspace environment readiness, own `topic.intent.agent_env_requirements` or `topic.env.agent_setup_target_spec`, or verify per-agent cwd commands. It does not create Agent Instances, launch Houmao agents, run Execution Adapters, or replace topic or agent env setup services.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default subcommand**:
   - Match when this skill is invoked without a prompt and the user is not asking for help.
   - Select `topic-workspace`, load [references/topic-workspace.md](references/topic-workspace.md), and execute the full inspection and optional support workflow.
2. **Manual subcommand**:
   - Match when the user names one subcommand, asks for help, or asks for one bounded operation.
   - If the prompt asks to install, add, repair, or verify packages for a Topic Workspace and does not name a subcommand, select `install-packages`.
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
- Operator intent for mutation before any manual topology operation or package installation, including registering Topic Workspace Manifest bindings with `label`/`path`/`storage_profile`, creating or repairing topology outside the normal service path, adding worktrees, adding packages to the selected Topic Workspace Pixi environment, writing Workspace Boundary material, or editing packet/profile `agent_name`, `agent_branch`, or compatibility `agent_workspace_ref` fields.

## Subcommands

Load only the selected reference page before executing a subcommand.

### Procedural Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, Topic Workspace, and existing workspace material through Project Manifest-backed context | [references/resolve-workspace.md](references/resolve-workspace.md) |
| `ensure-main-repo` | Inspect or validate the resolved `topic.repos.main` path, with manual topology creation only when explicitly requested | [references/ensure-main-repo.md](references/ensure-main-repo.md) |
| `manage-actors` | List, show, register, update, archive, materialize, repair, and diagnose Topic Actors and Topic Actor Workspaces through `project topic-actors ...` | [references/manage-actors.md](references/manage-actors.md) |
| `plan-agents` | Normalize agent names, map active role bindings, and plan worktree paths, branches, and derived compatibility refs | [references/plan-agents.md](references/plan-agents.md) |
| `create-worktrees` | Inspect, validate, or manually create per-agent worktrees at the resolved `agent.workspace` path for each Agent Name | [references/create-worktrees.md](references/create-worktrees.md) |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes for the topic repo and Agent Workspaces | [references/write-boundaries.md](references/write-boundaries.md) |
| `create-agent-branch` | Create a future per-agent branch under `per-agent/<agent-name>/<branch-name>` | [references/create-agent-branch.md](references/create-agent-branch.md) |
| `validate-worktrees` | Validate Git topology, branch namespace, duplicate checkout state, and packet/profile workspace refs | [references/validate-worktrees.md](references/validate-worktrees.md) |
| `install-packages` | Infer, install, and verify packages requested for the selected Topic Workspace Pixi environment from a prompt or description file | [references/install-packages.md](references/install-packages.md) |
| `summarize` | Report inspected layout, refs, validation status, blockers, and next operator action | [references/summarize.md](references/summarize.md) |

### Helper Subcommands

Helper subcommands are callable when the operator wants one implementation stage: `resolve-workspace`, `ensure-main-repo`, `manage-actors`, `plan-agents`, `create-worktrees`, `install-packages`, and `validate-worktrees`.

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print public usage, command boundaries, required inputs, outputs, and guardrails | [references/help.md](references/help.md) |
| `topic-workspace` | Run the full support flow: resolve, inspect topic-main, plan agents, optionally create worktrees when explicitly requested, write boundaries, validate, summarize | [references/topic-workspace.md](references/topic-workspace.md) |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Report:

- `status`: topology, worktree, or validation status.
- `topic`: selected `research_topic_ref` and `topic_workspace_ref`.
- `topic_main`: `topic.repos.main` path and readiness summary.
- `agent_workspaces`: Agent Workspace path summary and any unsafe topology problem.
- `packages`: package installation request, selected install route, verification summary, or package blockers when `install-packages` runs.
- `tmp_posture`: local tmp readiness summary for `topic.repos.main.tmp` and `agent.tmp`.
- `changed_paths`: boundary material or generated links when created or changed.
- `blockers`: unsafe repo state, unsafe path, branch conflict, missing input, or unapproved mutation.
- `next_action`: the next safe operator step.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity**: `research_topic_ref` and `topic_workspace_ref`.
- **Semantic paths**: full `semantic_paths` with labels, paths, sources, readiness, and blockers.
- **Topic main and managed paths**: `topic_main_repo_path`, `isomer_managed_path_status`, projection roots, `agent-owned/`, `links/`, and generated links.
- **Tmp posture**: `local_tmp_path_status`, ignored posture, tracked-content diagnostics, and non-durable evidence notes.
- **Topic actors**: `topic_actor_bindings`, `topic_actor_workspace_paths`, `topic_actor_branch_plan`, actor-scoped semantic labels, materialization status, runtime audit refs when available, and actor blockers.
- **Agent workspaces**: `agent_workspace_paths`, `agent_workspace_refs`, and `branch_plan`.
- **Packages**: `package_request_source`, `package_install_plan`, `package_install_routes`, `package_verification`, `already_present_packages`, `package_blockers`, and `package_execution_log` when package installation is requested.
- **Boundary and validation**: `boundary_material_paths`, `validation_status`, optional `agent_environment_service_output`, blockers, and `next_operator_action`.

## Guardrails

Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context. Do not infer the selected Topic Workspace by scanning sibling directories.

Use Workspace Path Resolution commands for storage answers. Use `project paths get` for selected paths, `project paths explain` for source diagnostics, `project paths register` for explicit `label`/`path`/`storage_profile` bindings, `project repos create` for additional non-main grouped `topic.repos.*` repository labels that default under `repos/extern/...`, and `project topic-actors ...` for Topic Actor binding and Topic Actor Workspace operations.

Do not present this skill as the canonical creator of `topic.repos.main`, projection roots, or per-agent worktrees in the normal topic-team setup path. Route canonical Topic Main Development Repository setup and projection materialization to `isomer-srv-topic-env-setup`; route canonical Agent Workspace worktree creation and cwd verification to `isomer-srv-agent-env-setup`.

Use `install-packages` as the operator-owned package-add surface for the selected Topic Workspace. Accept plain prompts, Markdown files, YAML, JSON, requirements-style lists, and copied blocker text as package requests; infer a concrete install plan without requiring a fixed schema-constrained request file.

Keep the resolved `topic.repos.main` path as a normal non-bare Git repository, each resolved `topic.actors.workspace` path as a Topic Actor Workspace worktree of that repository when materialized as a worktree, and each resolved `agent.workspace` path as an Agent Workspace worktree of that repository.

Keep Topic Actor names separate from Agent Names and Agent Instance ids. The Topic Actor name owns a path and branch namespace for human-orchestrated work; it does not create Agent Team Instance membership or formal Agent Workspace identity.

Keep `agent-name` separate from Agent Instance id. The agent name owns a path and branch namespace; Workspace Runtime later creates globally unique Agent Instance ids.

Use `topic-owner/main` for the owner-managed checkout, `per-topic-actor/<topic-actor-name>/main` for the default Topic Actor branch, `per-topic-actor/<topic-actor-name>/<branch-name>` for future actor branches, `per-agent/<agent-name>/main` for the default per-agent branch, and `per-agent/<agent-name>/<branch-name>` for future agent branches. Reject empty segments, `..`, leading or trailing slash, `.lock` endings, cross-actor or cross-agent prefixes, and duplicate branch checkout in another worktree.

Keep worker-visible Isomer material under the resolved `topic.repos.main.isomer_managed` path, the corresponding `topic.actors.*` support labels inside each Topic Actor Workspace, or the corresponding `agent.*` support labels inside each Agent Workspace. Treat `isomer-managed/tracked/` as the Git-shared regime, `isomer-managed/topic-owned/{readonly,writable}/extern/` as external repo projection roots, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` as Topic Actor support material, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.inbox` as agent-owned material, `agent.topic_readonly` and `agent.topic_writable` as topic-owned projections, and `agent.links` as generated conveniences. Treat `topic.records.*` as owner-preserved records and `topic.runtime` as runtime support material. Treat `topic.repos.main.tmp`, `topic.actors.tmp`, and `agent.tmp` as local ignored disposable surfaces only; do not describe tmp contents as Peer Read Access, generated-link target material, handoff material, shared material, or durable readiness evidence.

Report blockers instead of silently repairing unsafe existing paths, non-Git repositories, branch conflicts, dirty or ambiguous repo state, missing base branches, or packet/profile refs outside the selected Topic Workspace.

Do not delete, replace, pull, reset, reinitialize, or overwrite existing repositories or Agent Workspace paths without explicit user instruction.

Do not create local `venv`, `.venv`, or `virtualenv` environments, run ambient `pip`, use unrecorded user R libraries, mutate system package managers, run `sudo`, edit global shell profiles, install daemons, change kernel drivers, or perform machine-global package setup from `install-packages`. Convert the request to the selected Topic Workspace Pixi environment when safe, or report a blocker.

Do not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or claim runtime readiness from this skill. Validated topology evidence becomes runtime truth only when later Workspace Runtime creation consumes validated `agent_name`, branch, and Agent Workspace path plans.

Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
