# Topic Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Run the `resolve-workspace` workflow to select Project, Research Topic, Topic Workspace, and relevant packet/profile material through Project Manifest-backed context.
2. Run the `ensure-main-repo` workflow in inspection mode:
   - Cover the resolved `topic.repos.main` path, `topic.repos.main.tmp` local ignored disposable posture, `topic.repos.main.isomer_managed`, projection roots, and `topic.repos.main.projections.manifest`.
   - Do not create topic-main in the normal support flow. If the repository is missing, route canonical repair to `isomer-srv-topic-env-setup`.
   - Create or repair topology only when the operator explicitly requests a manual topology operation, the risk is named, and predecessor evidence or explicit manual acceptance exists.
3. Run the `plan-agents` workflow:
   - Normalize agent names, map active role bindings, resolve `agent.workspace` for each Agent Name, and plan `per-agent/<agent-name>/main`.
   - Propose or validate derived compatibility `agent_workspace_ref` values when older material needs them.
4. Run the `create-worktrees` workflow only when explicit manual worktree support was requested:
   - Require prepared Topic Main Development Repository predecessor evidence or an explicit manual topology operation.
   - Prepare safe planned entries, including `agent.tmp` local ignored disposable posture.
   - Stop individual entries on blockers instead of overwriting existing paths.
   - If no manual worktree support was requested, skip creation and report that canonical per-agent worktree creation belongs to `isomer-srv-agent-env-setup`.
5. Run the `write-boundaries` workflow for topic-level and per-agent advisory Workspace Boundary, Peer Read Access, owner/reader split, and generated-link notes.
6. Run the `validate-worktrees` workflow to check Git topology, branch namespace, duplicate checkout state, local tmp posture, `isomer-managed/` layout, generated links, and packet/profile refs.
7. Handle per-Agent Workspace environment readiness only when requested:
   - If the user explicitly asked for readiness, name `isomer-srv-agent-env-setup setup-agent-env` as the normal owner of worktree creation and cwd proof after topic env predecessor evidence exists.
   - Otherwise report that agent environment verification is not checked.
8. Run the `summarize` workflow and report the output contract with blockers and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to split the request into the closest subcommands, run read-only stages first, and ask for explicit mutation only when needed.

When the operator asks to add another non-main topic repository, register it through `project repos create <repo-label>` or `project paths register topic.repos.<group...>.<repo-name> --storage-profile topic_repo`. Helper-created repositories default under `repos/extern/<repo-label-path>` and are supporting topic-local repositories, not Agent Workspace worktree sources. The Topic Workspace Manifest binding must keep the compact `label`/`path`/`storage_profile` shape. Report the resulting semantic label and path source before using the repository.

## Full Flow Boundary

The full flow provides optional topology inspection and support. It does not create topic-main in the normal flow, create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, run Execution Adapters, or prove that every Agent Workspace cwd can run a gate command.

Per-Agent Workspace cwd readiness belongs to `isomer-srv-agent-env-setup`. That service consumes Topic Workspace predecessor evidence, prepared Topic Main Development Repository evidence, projection predecessor evidence, authoritative Agent Names, `topic.intent.agent_env_requirements` or an explicit agent env target spec, and resolved path evidence, then creates or validates worktrees and verifies `topic.env.agent_setup_target_spec` from every authoritative Agent Workspace cwd. A selected-agent rerun from that service is partial evidence only and does not make the whole topic team ready.

Runtime Agent Team Instance creation later consumes validated `agent_name`, branch, `agent.workspace` path plans, and `agent.*` support path plans. Missing semantic label evidence is a launch-facing blocker; runtime must not silently fall back to `<topic-workspace>/agents/<agent-instance-id>`.
