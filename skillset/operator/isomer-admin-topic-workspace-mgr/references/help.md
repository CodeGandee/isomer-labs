# Help

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Print a concise description:
   - `isomer-admin-topic-workspace-mgr` provides Topic Actor CRUD, Topic Actor Workspace materialization or repair, actor-scoped path diagnostics, optional topology inspection, branch helpers, Workspace Boundary summaries, manual compatibility operations, and legacy diagnostics through semantic labels such as `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, and `agent.links`.
2. Explain that invoking the skill without a prompt defaults to `topic-workspace`, while explicit help prints this usage surface.
3. Print the available public subcommands as a three-column table with `Subcommand`, `Purpose`, and `Produces` columns.
4. Name the required inputs: Project Manifest context, Research Topic, Topic Workspace, optional Topic Actor names, optional packet/profile material, and any requested agent-name mapping.
5. State the output contract:
   - Include semantic paths with labels and sources, topic repo path, `isomer-managed/` regime status, projection roots, local tmp posture, records root, runtime root, Topic Actor bindings, Topic Actor Workspace paths, actor branch plan, agent workspace paths, branch plan, derived compatibility refs, boundary docs, and generated links.
   - Include optional `isomer-srv-agent-env-setup` evidence when already available, validation status, blockers, and next operator action.
6. State the key guardrails:
   - No directory-scanning selection, no silent Git repair, and no cross-topic refs.
   - No canonical Topic Main Development Repository setup or normal per-agent worktree ownership; route those to topic and agent env setup services.
   - No Agent Instance creation, Houmao launch, or Execution Adapter operation. Topic Actor registration and materialization may write runtime audit/provenance records when runtime is available, but those records do not replace the Topic Workspace Manifest as topology authority.

If the user's task does not map cleanly to these steps, use your native planning tool to decide which usage details to print, then execute the plan.

## Public Subcommands

| Subcommand | Purpose | Produces |
| --- | --- | --- |
| `resolve-workspace` | Resolve Project, Research Topic, Topic Workspace, and semantic paths through Project Manifest-backed context. | Topic Workspace path, semantic paths, candidate packet/profile material, blockers. |
| `ensure-main-repo` | Inspect or validate the resolved `topic.repos.main` path, `topic.repos.main.tmp`, and tracked Isomer namespace, with creation only as an explicit manual topology operation. | `topic_main_repo_path`, `local_tmp_path_status`, `isomer_managed_path_status`, base branch, repo readiness, blockers. |
| `manage-actors` | List, show, register, update, archive, materialize, repair, or diagnose Topic Actors and Topic Actor Workspaces. | Topic Actor bindings, `topic.actors.workspace` paths, `per-topic-actor/<topic-actor-name>/main` branch plan, audit refs, blockers. |
| `plan-agents` | Normalize agent names and map active role bindings to resolved `agent.workspace` paths and branches. | Agent name map, semantic paths, derived compatibility refs, `per-agent/<agent-name>/main` branch plan. |
| `create-worktrees` | Inspect, validate, or manually create per-agent Git worktrees, `agent.tmp`, and ignored `agent.*` support paths. | Ready or created Agent Workspace worktrees, local tmp posture, `isomer-managed/` regime status, skipped entries, blockers. |
| `write-boundaries` | Write advisory Workspace Boundary and Peer Read Access notes. | Boundary material paths, ownership notes, branch rules, generated-link notes. |
| `create-agent-branch` | Create a future per-agent branch under the owning agent prefix. | `per-agent/<agent-name>/<branch-name>` branch result, base ref, blockers. |
| `validate-worktrees` | Validate Git topology, local tmp posture, `isomer-managed/` layout, generated links, and packet/profile workspace refs. | `validation_status`, ready entries, tmp, cross-topic, layout, or Git blockers. |
| `summarize` | Summarize prepared layout and next operator action. | Consumer-neutral report with paths, branches, local tmp posture, `isomer-managed/` regimes, generated links, refs, blockers, and next action. |
| `topic-workspace` | Run the full optional support flow. | Topic-main inspection, projection roots, optional manual worktree results, `isomer-managed/` material, boundary material, validation result, summary. |
| `help` | Print this usage information. | Public subcommand table, required inputs, outputs, guardrails. |

## Boundary Notes

This skill complements `isomer-admin-topic-prepare`, `isomer-admin-manual-research-session`, and `isomer-admin-topic-team-specialize`: common preparation resolves reusable topic state, manual sessions choose research actors and write start packs, specialization defines topic-team material and static setup evidence, while this skill owns Topic Actor topology operations plus optional topology inspection, branch helpers, boundary summaries, manual compatibility operations, and legacy diagnostics.

This skill also stays separate from `isomer-srv-topic-env-setup`, which owns gate-driven topic environment setup, Topic Main Development Repository setup, canonical external repository acquisition, and external repo projection materialization.

This skill stays separate from `isomer-srv-agent-env-setup`, which owns `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, prepared Topic Main Development Repository predecessor checks, per-Agent Workspace worktree creation, cwd verification, readiness by Agent Name, and partial selected-agent repair evidence. Name or call that service for per-agent environment readiness only when the caller requested it and topic env predecessor evidence exists.
