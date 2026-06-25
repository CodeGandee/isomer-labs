# Topic Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Run the `resolve-workspace` workflow to select Project, Research Topic, Topic Workspace, and relevant packet/profile material through Project Manifest-backed context.
2. Run the `ensure-main-repo` workflow for `<topic-workspace-dir>/repos/topic-main`, creating it only when the operator requested creation and the target path is safe.
3. Run the `plan-agents` workflow to normalize agent keys, map active role bindings, plan `<topic-workspace-dir>/agents/<agent-key>`, plan `per-agent/<agent-key>/main`, and propose or validate `agent_workspace_ref` values.
4. Run the `create-worktrees` workflow for safe planned entries and stop individual entries on blockers instead of overwriting existing paths.
5. Run the `write-boundaries` workflow for topic-level and per-agent advisory Workspace Boundary and Peer Read Access notes.
6. Run the `validate-worktrees` workflow to check Git topology, branch namespace, duplicate checkout state, and packet/profile refs.
7. Run the `summarize` workflow and report the output contract with blockers and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to split the request into the closest subcommands, run read-only stages first, and ask for explicit mutation only when needed.

## Full Flow Boundary

The full flow prepares static Git-backed Agent Workspace paths. It does not create Agent Instances, mutate Workspace Runtime records, launch Houmao agents, or run Execution Adapters.

Runtime Agent Team Instance creation later consumes validated `agent_workspace_ref` values and records Agent Workspace path plans. Without approved refs, runtime keeps the generated default path under `<topic-workspace>/agents/<agent-instance-id>`.
