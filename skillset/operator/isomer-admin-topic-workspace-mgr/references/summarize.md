# Summarize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the latest resolve, repo, agent plan, worktree, boundary, branch, and validation results available in the operator context.
2. Summarize the resolved `topic.repos.main` path, source, readiness, and blockers before showing any default path.
3. Summarize each agent name, role id, resolved `agent.workspace` path, path source, current branch, expected branch namespace, required `agent.*` support label status, `agent.tmp` local ignored disposable posture, and derived compatibility `agent_workspace_ref` when present.
4. Summarize `topic.repos.main.tmp` and `agent.tmp` separately from shared material, including ignore policy and tracked-content diagnostics.
5. Summarize boundary material paths and whether Workspace Boundary, Peer Read Access, owner/reader split, and generated-link notes are present and advisory.
6. When `isomer-srv-agent-env-setup` evidence is available, summarize `source_agent_env_gate_path`, `agent_env_gate_path`, readiness by agent, overall readiness, command evidence, blockers, and next action under a separate agent environment readiness heading.
7. Summarize validation status, blockers, skipped actions, generated links, profile or packet edits, and refs that remain to be updated.
8. Name the next operator action, such as rerun one subcommand, call `isomer-srv-agent-env-setup setup-agent-env`, call `isomer-admin-topic-team-specialize validate-topic-team`, create an Agent Team Instance through runtime workflow, or stop on blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a consumer-neutral summary from whatever validated evidence exists.

## Output

Report `research_topic_ref`, `topic_workspace_ref`, `semantic_paths`, `topic_main_repo_path`, `isomer_managed_path_status`, `local_tmp_path_status`, `records_root`, `runtime_root`, `agent_workspace_paths`, derived `agent_workspace_refs`, `branch_plan`, `generated_links`, `boundary_material_paths`, optional `agent_environment_service_output`, `validation_status`, `blockers`, and `next_operator_action`.

Include cwd-friendly guidance for prepared agents: from inside their own Agent Workspace, they can query labels such as `agent.private_artifacts`, `agent.scratch`, `agent.public_share`, and `agent.tmp` without passing Agent Name. Cross-agent queries still require explicit Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share context. State that `agent.tmp` is local, ignored, disposable, not shared, and not durable evidence.

Do not claim live team readiness, Workspace Runtime readiness, or per-agent environment readiness from static workspace preparation. Agent environment readiness must come from `isomer-srv-agent-env-setup` evidence, and selected-agent evidence from that service remains partial until every planned Agent Name is verified.
