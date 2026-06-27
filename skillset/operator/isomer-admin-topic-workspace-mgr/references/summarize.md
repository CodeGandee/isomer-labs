# Summarize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the latest resolve, repo, agent plan, worktree, boundary, branch, and validation results available in the operator context.
2. Summarize the shared topic repository `<topic-workspace-dir>/repos/topic-main`.
3. Summarize each agent name, role id, Agent Workspace path, current branch, expected branch namespace, `isomer-managed/` path status, and derived compatibility `agent_workspace_ref` when present.
4. Summarize boundary material paths and whether Workspace Boundary, Peer Read Access, owner/reader split, and generated-link notes are present and advisory.
5. Summarize validation status, blockers, skipped actions, generated links, profile or packet edits, and refs that remain to be updated.
6. Name the next operator action, such as rerun one subcommand, call `isomer-admin-topic-team-specialize validate-topic-team`, create an Agent Team Instance through runtime workflow, or stop on blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a consumer-neutral summary from whatever validated evidence exists.

## Output

Report `research_topic_ref`, `topic_workspace_ref`, `topic_main_repo_path`, `isomer_managed_path_status`, `records_root`, `runtime_root`, `agent_workspace_paths`, derived `agent_workspace_refs`, `branch_plan`, `generated_links`, `boundary_material_paths`, `validation_status`, `blockers`, and `next_operator_action`.

Do not claim live team readiness or Workspace Runtime readiness from static workspace preparation.
