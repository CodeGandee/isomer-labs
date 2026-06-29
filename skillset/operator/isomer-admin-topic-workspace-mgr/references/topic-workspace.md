# Topic Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Run the `resolve-workspace` workflow to select Project, Research Topic, Topic Workspace, and relevant packet/profile material through Project Manifest-backed context.
2. Run the `ensure-main-repo` workflow:
   - Cover the resolved `topic.repos.main` path, `topic.repos.main.tmp` local ignored disposable posture, and `topic.repos.main.isomer_managed` namespace.
   - Create the repository only when the operator requested creation and the target path is safe.
3. Run the `plan-agents` workflow:
   - Normalize agent names, map active role bindings, resolve `agent.workspace` for each Agent Name, and plan `per-agent/<agent-name>/main`.
   - Propose or validate derived compatibility `agent_workspace_ref` values when older material needs them.
4. Run the `create-worktrees` workflow:
   - Prepare safe planned entries, including `agent.tmp` local ignored disposable posture.
   - Stop individual entries on blockers instead of overwriting existing paths.
5. Run the `write-boundaries` workflow for topic-level and per-agent advisory Workspace Boundary, Peer Read Access, owner/reader split, and generated-link notes.
6. Run the `validate-worktrees` workflow to check Git topology, branch namespace, duplicate checkout state, local tmp posture, `isomer-managed/` layout, generated links, and packet/profile refs.
7. Handle per-Agent Workspace environment readiness only when requested:
   - If the user explicitly asked for readiness, call or name `isomer-srv-agent-env-setup setup-agent-env` only after the Git topology is validated.
   - Otherwise report that agent environment verification is not checked.
8. Run the `summarize` workflow and report the output contract with blockers and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to split the request into the closest subcommands, run read-only stages first, and ask for explicit mutation only when needed.

When the operator asks to add another non-main topic repository, register it through `project repos create <repo-label>` or `project paths register topic.repos.<group...>.<repo-name> --storage-profile topic_repo`. Helper-created repositories default under `repos/extern/<repo-label-path>` and are supporting topic-local repositories, not Agent Workspace worktree sources. The Topic Workspace Manifest binding must keep the compact `label`/`path`/`storage_profile` shape. Report the resulting semantic label and path source before using the repository.

## Full Flow Boundary

The full flow prepares static Git-backed Agent Workspace paths. It does not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or prove that every Agent Workspace cwd can run a gate command.

Per-Agent Workspace cwd readiness belongs to `isomer-srv-agent-env-setup`. That service consumes this skill's validated `topic.repos.main`, `topic.repos.main.tmp`, `agent.workspace`, `agent.tmp`, branch plan, support-path evidence, `topic.env.topic_setup_target_spec` predecessor evidence, and `topic.intent.agent_env_requirements` or an explicit agent env target spec, then verifies `topic.env.agent_setup_target_spec` from every authoritative Agent Workspace cwd. A selected-agent rerun from that service is partial evidence only and does not make the whole topic team ready.

Runtime Agent Team Instance creation later consumes validated `agent_name`, branch, `agent.workspace` path plans, and `agent.*` support path plans. Missing semantic label evidence is a launch-facing blocker; runtime must not silently fall back to `<topic-workspace>/agents/<agent-instance-id>`.
