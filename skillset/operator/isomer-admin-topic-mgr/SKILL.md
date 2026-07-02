---
name: isomer-admin-topic-mgr
description: "Manage an initialized Isomer Research Topic after Topic Creator handoff, including topic storage, Topic Actors, topic agent team topology, environment package mutation, environment verification, boundary notes, and diagnostics."
---

# Isomer Admin Topic Mgr

Use this command-style operator skill after `isomer-admin-topic-creator` has created or resumed a Research Topic and registered a Topic Workspace. `isomer-admin-topic-mgr` manages initialized-topic storage, Topic Actors, topic agent team topology, environment mutation, environment verification, and diagnostics. It works through the Topic Workspace Manifest, Project Manifest-backed Isomer context, and semantic workspace labels such as `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.actors_root`, `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, `topic.agents_root`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, `agent.links`, `topic.records.*`, and `topic.runtime`. Additional non-main topic repositories use grouped `topic.repos.*` labels and helper-created paths under `repos/extern/...`, while user-owned nonreserved storage uses `custom.*`; register those bindings through `project paths register` or `project repos create` with explicit `storage_profile` rather than editing `topic-workspace.toml` by hand.

The canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`, and canonical per-agent worktree creation plus cwd proof belong to `isomer-srv-agent-env-setup`. This skill performs mutation only for explicitly requested actor topology, explicitly requested storage registration, explicitly requested package mutation, explicit environment verification, or manual topology operations after confirming predecessor evidence or manual acceptance. It does not derive topic ids, register new Research Topics, create Topic Workspaces from blank state, create research-paradigm v2 bootstrap outputs owned by `isomer-rsch-workspace-mgr-v2`, create Agent Instances, launch Houmao agents, run Execution Adapters, or replace topic or agent env setup services.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default subcommand**:
   - Match when this skill is invoked without a prompt and the user is not asking for help.
   - Select `status`, load [references/status.md](references/status.md), and execute the initialized-topic inspection workflow.
2. **Manual subcommand**:
   - Match when the user names one subcommand, asks for help, or asks for one bounded initialized-topic operation.
   - If the prompt asks to install or add packages for a selected Topic Workspace and does not name a subcommand, select `env-install-packages`.
   - If the prompt asks to update packages for a selected Topic Workspace and does not name a subcommand, select `env-update-packages`.
   - If the prompt asks to remove packages from a selected Topic Workspace and does not name a subcommand, select `env-remove-packages`.
   - If the prompt asks to verify topic, actor, or agent environment readiness and does not name a subcommand, select the matching `env-verify-*` subcommand.
   - Select that subcommand from the **Subcommands** tables.
   - Load only its detail page, execute that page's `## Workflow`, and report its output.
3. **Initialized-topic guard**:
   - Before mutation, require a selected Project root or Project Manifest context plus a selected Research Topic and Topic Workspace resolved through Isomer context.
   - If selected initialized topic context cannot be resolved, report a blocker and route initialization to `isomer-admin-topic-creator`; do not derive a topic id, register a topic, create a Topic Workspace, or write topic intent material from this skill.
4. **Helper subcommand**:
   - Match when the user asks for a lower-level planning, storage, actor, team, environment mutation, or environment verification stage.
   - Select the matching scoped page, load only that page, and keep the operation scoped to the selected stage.
5. Preserve the **Required Inputs**, **Output Contract**, and **Guardrails** for every subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project Manifest-backed Isomer context, selected Research Topic refs, selected Topic Workspace refs, semantic path evidence, output contract, and guardrails in this skill, then execute the plan.

## Required Inputs

- A selected Project root or Project Manifest context.
- A selected initialized Research Topic and selected Topic Workspace resolved through Isomer context, not directory scanning.
- A role binding source when planning formal Agent Names: Topic Team Instantiation Packet, Topic Agent Team Profile material, or an explicit operator-provided role-to-agent-name map.
- Topic env predecessor evidence when the operator asks this skill to inspect a prepared Topic Main Development Repository, projection roots, Topic Actor Workspaces, or existing Agent Workspace topology.
- Operator intent for mutation before any storage registration, Topic Actor registration, Topic Actor Workspace materialization, Agent Workspace topology operation, branch helper operation, package install/update/remove operation, environment verification, Workspace Boundary material writing, or packet/profile `agent_name`, `agent_branch`, or compatibility `agent_workspace_ref` edit.

## Subcommands

Load only the selected reference page before executing a subcommand.

### Status Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `status` | Report initialized-topic storage, actors, team topology, environment evidence, blockers, and next operator action | [references/status.md](references/status.md) |
| `doctor` | Diagnose stale or unsafe initialized-topic topology, storage, actor, team, environment, and retired-skill routing evidence | [references/doctor.md](references/doctor.md) |
| `help` | Print public usage, command boundaries, required inputs, outputs, and guardrails | [references/help.md](references/help.md) |

### Storage Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `storage-resolve` | Resolve Project, Research Topic, Topic Workspace, semantic paths, custom labels, and existing workspace material through Project Manifest-backed context | [references/storage-resolve.md](references/storage-resolve.md) |
| `storage-inspect-main` | Inspect or validate the resolved `topic.repos.main` path, with manual topology creation only when explicitly requested | [references/storage-inspect-main.md](references/storage-inspect-main.md) |
| `storage-validate` | Validate initialized-topic storage bindings, semantic label evidence, tmp posture, projection roots, custom surfaces, and unsafe path blockers | [references/storage-validate.md](references/storage-validate.md) |
| `storage-register-repo` | Register or inspect additional non-main `topic.repos.*` repositories through semantic storage labels and `storage_profile` | [references/storage-register-repo.md](references/storage-register-repo.md) |

### Actor Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `actors-manage` | List, show, register, update, archive, materialize, repair, and diagnose Topic Actors and Topic Actor Workspaces through `project topic-actors ...` | [references/actors-manage.md](references/actors-manage.md) |
| `actors-materialize` | Create, reuse, or repair selected Topic Actor Workspace worktrees and actor-scoped support labels | [references/actors-materialize.md](references/actors-materialize.md) |
| `actors-diagnose` | Diagnose Topic Actor bindings, actor cwd labels, branches, support labels, runtime audit refs, and repair routes | [references/actors-diagnose.md](references/actors-diagnose.md) |

### Team Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `team-plan` | Normalize Agent Names, map active role bindings, and plan worktree paths, branches, and derived compatibility refs | [references/team-plan.md](references/team-plan.md) |
| `team-materialize-workspaces` | Inspect, validate, or manually create per-agent worktrees at the resolved `agent.workspace` path for each Agent Name | [references/team-materialize-workspaces.md](references/team-materialize-workspaces.md) |
| `team-write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes for the topic repo and Agent Workspaces | [references/team-write-boundaries.md](references/team-write-boundaries.md) |
| `team-create-branch` | Create a future per-agent branch under `per-agent/<agent-name>/<branch-name>` | [references/team-create-branch.md](references/team-create-branch.md) |
| `team-validate-workspaces` | Validate Git topology, branch namespace, duplicate checkout state, `isomer-managed/` posture, and packet/profile workspace refs | [references/team-validate-workspaces.md](references/team-validate-workspaces.md) |

### Environment Mutation Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `env-install-packages` | Infer, install, and verify packages requested for the selected Topic Workspace Pixi environment from a prompt or description file | [references/env-install-packages.md](references/env-install-packages.md) |
| `env-update-packages` | Infer, update, constrain, or downgrade packages in the selected Topic Workspace Pixi environment and verify relevant checks | [references/env-update-packages.md](references/env-update-packages.md) |
| `env-remove-packages` | Infer package removal intent, remove packages from the selected Topic Workspace Pixi environment when safe, and verify relevant checks | [references/env-remove-packages.md](references/env-remove-packages.md) |

### Environment Verification Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `env-verify-topic` | Verify Topic Workspace environment readiness or route full gate-driven setup and verification to `isomer-srv-topic-env-setup` | [references/env-verify-topic.md](references/env-verify-topic.md) |
| `env-verify-actors` | Verify selected Topic Actor cwd gates, actor support labels, and per-actor blockers | [references/env-verify-actors.md](references/env-verify-actors.md) |
| `env-verify-agents` | Route formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup` and report returned evidence | [references/env-verify-agents.md](references/env-verify-agents.md) |

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Report:

- `status`: initialized-topic, storage, actor, team, environment mutation, or verification status.
- `topic`: selected `research_topic_ref` and `topic_workspace_ref`.
- `semantic_paths`: relevant semantic labels, path sources, readiness, and blockers.
- `topic_main`: `topic.repos.main` path and readiness summary when relevant.
- `topic_actors`: Topic Actor roster, actor cwd summary, actor support labels, and actor blockers when relevant.
- `agent_workspaces`: Agent Workspace path summary and unsafe topology problems when relevant.
- `environment`: package request, selected install/update/remove route, verification summary, service handoff, or blockers when relevant.
- `changed_paths`: package environment files, boundary material, generated links, or actor support material when created or changed.
- `blockers`: unsafe repo state, unsafe path, branch conflict, missing initialized-topic context, failed verification, missing input, or unapproved mutation.
- `next_action`: the next safe operator step.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity**: `research_topic_ref` and `topic_workspace_ref`.
- **Semantic paths**: full `semantic_paths` with labels, paths, sources, storage profiles, readiness, and blockers.
- **Topic main and managed paths**: `topic_main_repo_path`, `isomer_managed_path_status`, projection roots, `agent-owned/`, `links/`, and generated links.
- **Tmp posture**: `local_tmp_path_status`, ignored posture, tracked-content diagnostics, and non-durable evidence notes.
- **Topic actors**: `topic_actor_bindings`, `topic_actor_workspace_paths`, `topic_actor_branch_plan`, actor-scoped semantic labels, materialization status, runtime audit refs when available, and actor blockers.
- **Agent workspaces**: `agent_workspace_paths`, `agent_workspace_refs`, branch plan, boundary material, and validation status.
- **Environment**: `package_request_source`, `package_mutation_plan`, selected Pixi route, verification commands, verification evidence, service output, failed checks, skipped heavy checks, blockers, and next action.
- **Boundary and validation**: `boundary_material_paths`, `validation_status`, optional `agent_environment_service_output`, blockers, and `next_operator_action`.

## Guardrails

Resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context. Do not infer the selected Topic Workspace by scanning sibling directories.

Route missing or uninitialized Research Topic context to `isomer-admin-topic-creator`. Do not derive a topic id, register a topic, create a Topic Workspace, write `topic.intent.overview`, write `topic.intent.topic_env_requirements`, write `topic.intent.actor_definitions`, or create initial topic readiness from this skill.

Use Workspace Path Resolution commands for storage answers. Use `project paths get` for selected paths, `project paths explain` for source diagnostics, `project paths register` for explicit `label`/`path`/`storage_profile` bindings, `project repos create` for additional non-main grouped `topic.repos.*` repository labels that default under `repos/extern/...`, and `project topic-actors ...` for Topic Actor binding and Topic Actor Workspace operations.

Do not present this skill as the canonical creator of `topic.repos.main`, projection roots, or per-agent worktrees in the normal topic-team setup path. Route canonical Topic Main Development Repository setup and projection materialization to `isomer-srv-topic-env-setup`; route canonical Agent Workspace worktree creation and cwd verification to `isomer-srv-agent-env-setup`.

Use `env-install-packages`, `env-update-packages`, and `env-remove-packages` as the operator-owned package mutation surfaces for the selected Topic Workspace. Accept plain prompts, Markdown files, YAML, JSON, TOML, requirements-style lists, and copied blocker text as package requests; infer a concrete install, update, remove, and verification plan without requiring a fixed schema-constrained request file.

Keep the resolved `topic.repos.main` path as a normal non-bare Git repository, each resolved `topic.actors.workspace` path as a Topic Actor Workspace worktree of that repository when materialized as a worktree, and each resolved `agent.workspace` path as an Agent Workspace worktree of that repository.

Keep Topic Actor names separate from Agent Names and Agent Instance ids. The Topic Actor name owns a path and branch namespace for human-orchestrated work; it does not create Agent Team Instance membership or formal Agent Workspace identity.

Keep `agent-name` separate from Agent Instance id. The Agent Name owns a path and branch namespace; Workspace Runtime later creates globally unique Agent Instance ids.

Use `topic-owner/main` for the owner-managed checkout, `per-topic-actor/<topic-actor-name>/main` for the default Topic Actor branch, `per-topic-actor/<topic-actor-name>/<branch-name>` for future actor branches, `per-agent/<agent-name>/main` for the default per-agent branch, and `per-agent/<agent-name>/<branch-name>` for future agent branches. Reject empty segments, `..`, leading or trailing slash, `.lock` endings, cross-actor or cross-agent prefixes, and duplicate branch checkout in another worktree.

Keep worker-visible Isomer material under the resolved `topic.repos.main.isomer_managed` path, the corresponding `topic.actors.*` support labels inside each Topic Actor Workspace, or the corresponding `agent.*` support labels inside each Agent Workspace. Treat `isomer-managed/tracked/` as the Git-shared regime, `isomer-managed/topic-owned/{readonly,writable}/extern/` as external repo projection roots, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` as Topic Actor support material, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.inbox` as agent-owned material, `agent.topic_readonly` and `agent.topic_writable` as topic-owned projections, and `agent.links` as generated conveniences. Treat `topic.records.*` as owner-preserved records and `topic.runtime` as runtime support material. Treat `topic.repos.main.tmp`, `topic.actors.tmp`, and `agent.tmp` as local ignored disposable surfaces only; do not describe tmp contents as Peer Read Access, generated-link target material, handoff material, shared material, or durable readiness evidence.

Report blockers instead of silently repairing unsafe existing paths, non-Git repositories, branch conflicts, dirty or ambiguous repo state, missing base branches, packet/profile refs outside the selected Topic Workspace, failed package verification, or failed environment checks.

Do not delete, replace, pull, reset, reinitialize, or overwrite existing repositories, Topic Actor Workspace paths, or Agent Workspace paths without explicit user instruction.

Do not create local `venv`, `.venv`, or `virtualenv` environments, run ambient `pip`, use unrecorded user R libraries, mutate system package managers, run `sudo`, edit global shell profiles, install daemons, change kernel drivers, or perform machine-global package setup from environment mutation commands. Convert the request to the selected Topic Workspace Pixi environment when safe, or report a blocker.

Do not create Agent Instances, mutate Workspace Runtime records as live team truth, launch Houmao agents, run Execution Adapters, claim runtime readiness, or create v2 research placeholder binding outputs from this skill. Validated topology evidence becomes runtime truth only when later Workspace Runtime creation consumes validated actor or Agent Workspace plans.

Workspace Boundaries and Peer Read Access are advisory collaboration contracts, not filesystem-grade security isolation.
