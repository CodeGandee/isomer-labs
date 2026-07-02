# Summarize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the latest resolve, repo, Topic Actor, agent plan, worktree, package installation, boundary, branch, and validation results available in the operator context.
2. Summarize the resolved `topic.repos.main` path, source, readiness, and blockers before showing any default path.
3. Summarize each Topic Actor:
   - Include topic actor name, actor kind, runtime kind, role kind, controller kind or ref, resolved `topic.actors.workspace` path, path source, current branch, expected `per-topic-actor/<topic-actor-name>/` branch namespace, required `topic.actors.*` support label status, `topic.actors.tmp` local ignored disposable posture, materialization status, runtime audit refs when available, and blockers.
   - Include the canonical repair route through `project topic-actors ...` when actor topology is missing or stale.
4. Summarize each agent:
   - Include agent name, role id, resolved `agent.workspace` path, path source, current branch, expected branch namespace, required `agent.*` support label status, and `agent.tmp` local ignored disposable posture.
   - Include derived compatibility `agent_workspace_ref` when present.
5. Summarize `topic.repos.main.tmp`, `topic.actors.tmp`, and `agent.tmp` separately from shared material, including ignore policy and tracked-content diagnostics.
6. Summarize boundary material paths and whether Workspace Boundary, Peer Read Access, owner/reader split, and generated-link notes are present and advisory.
7. When `isomer-srv-agent-env-setup` evidence is available, summarize it under a separate agent environment readiness heading:
   - Include `source_agent_env_gate_path`, `agent_env_gate_path`, readiness by agent, overall readiness, command evidence, blockers, and next action.
8. When package installation evidence is available, summarize package request source, selected Pixi target, install routes, verification status, already-present packages, changed files, package blockers, and the requester skill or next rerun target when known.
9. Summarize validation status, blockers, skipped actions, generated links, profile or packet edits, and refs that remain to be updated.
10. Name the next operator action:
   - Examples include rerun one subcommand, make a caller-requested `isomer-srv-agent-env-setup setup-agent-env` call after topic env predecessor evidence exists, call `isomer-admin-topic-team-specialize validate-topic-team`, create an Agent Team Instance through runtime workflow, or stop on blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a consumer-neutral summary from whatever validated evidence exists.

## Output

Report `research_topic_ref`, `topic_workspace_ref`, `semantic_paths`, `topic_main_repo_path`, projection roots, `isomer_managed_path_status`, `local_tmp_path_status`, `records_root`, `runtime_root`, `topic_actor_bindings`, `topic_actor_workspace_paths`, `topic_actor_branch_plan`, `topic_actor_runtime_audit_refs`, `agent_workspace_paths`, derived `agent_workspace_refs`, `branch_plan`, `package_install_plan`, `package_verification`, `package_blockers`, `generated_links`, `boundary_material_paths`, optional `agent_environment_service_output`, `validation_status`, `blockers`, and `next_operator_action`.

Include cwd-friendly guidance for prepared Topic Actors and agents: from inside their own Topic Actor Workspace, an actor can query labels such as `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, and `topic.actors.tmp` without passing Topic Actor name when cwd inference is unambiguous; from inside their own Agent Workspace, agents can query labels such as `agent.private_artifacts`, `agent.scratch`, `agent.public_share`, and `agent.tmp` without passing Agent Name. Cross-actor and cross-agent queries still require explicit Topic Actor name, Agent Name, Agent Instance, handoff, Artifact, or boundary-approved share context. State that `topic.actors.tmp` and `agent.tmp` are local, ignored, disposable, not shared, and not durable evidence.

Do not claim live team readiness, Workspace Runtime readiness, or per-agent environment readiness from static topology inspection. Agent environment readiness must come from `isomer-srv-agent-env-setup` evidence, and selected-agent evidence from that service remains partial until every planned Agent Name is verified.
