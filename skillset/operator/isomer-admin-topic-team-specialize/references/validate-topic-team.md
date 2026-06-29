# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read validation inputs:
   - Topic definition material, registration assurance evidence, specialization outputs, and topic environment setup evidence from `isomer-srv-topic-env-setup`.
   - Topic Main Development Repository predecessor evidence, projection predecessor evidence when needed, and optional delegated workspace-manager topology inspection evidence when explicitly requested.
   - Delegated `isomer-srv-agent-env-setup` evidence for Agent Workspace worktrees, agent names, branch plans, `isomer-managed/` support surfaces, cwd readiness, deferrals, blockers, and validation refs.
3. Check that `topic.intent.overview` exists, reports semantic label evidence plus resolved path metadata, and reflects the current Research Topic understanding.
4. Check registration assurance:
   - Require Project Manifest-backed `registered_research_topic_ref` and `registered_topic_workspace_ref`, or explicit registration blockers.
   - Do not validate readiness from only a provisional topic workspace seed.
5. Check copied specialization material:
   - Require `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs.
   - Accept explicit blockers when material is missing.
6. Check setup streams separately:
   - Confirm topic environment setup and Agent Workspace setup are ready, intentionally deferred, or blocked with named next actions.
   - Topic environment setup evidence should include `topic_environment_status`, `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, resolved path metadata, Topic Workspace predecessor readiness status, Topic Main Development Repository Git state, Isomer-managed namespace posture, projection metadata, resource check status for heavy setup or verification commands, setup commands, changed files, environment binding status, `per_agent_readiness_status: not checked` when reported, and blockers from `isomer-srv-topic-env-setup`.
   - Treat missing environment setup evidence as an environment-preparation blocker, not as evidence that team-profile material is missing.
7. When per-Agent Workspace cwd verification was requested, require `isomer-srv-agent-env-setup` evidence:
   - Require `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, resolved path metadata, authoritative Agent Names, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, resolved `agent.workspace` paths, branch plan, worktree status by agent, resource check status for heavy per-agent verification commands, readiness by agent, commands run, blockers, and next action.
   - Require semantic path evidence for `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support labels, and path sources.
   - Treat selected-agent evidence as partial.
   - Do not mark overall agent environment readiness as ready unless every planned Agent Name is verified.
8. Reject stale Agent Workspace setup evidence:
   - Reject legacy support roots, top-level Topic Main Development Repository collaboration directories, tmp contents as readiness evidence, or hard-coded default-only paths without semantic labels as the current standard layout.
   - Ask for `isomer-srv-agent-env-setup` verification when worktree or cwd readiness is missing, or for optional `isomer-admin-topic-workspace-mgr` inspection when the user only needs topology diagnostics.
9. Report `topic_team_validation_status` as ready, ready-with-deferrals, blocked, or not checked for static material readiness, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static-material validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- `topic.intent.overview` with resolved path metadata.
- Registration assurance from `ensure-topic-registration`, including registered Research Topic and Topic Workspace refs, Topic Workspace Pixi binding status, and any registration blockers.
- Specialized topic-team material and draft profile or packet/profile input summary from `adapt-team-template`.
- `topic_environment_status` or explicit setup blocker from `setup-topic-env`, preferably with `isomer-srv-topic-env-setup` service output evidence.
- `agent_names`, `agent_workspace_paths`, `semantic_paths`, `local_tmp_path_status`, `isomer_managed_path_status`, `branch_plan`, worktree evidence, generated-link evidence, or explicit workspace blocker from `setup-agent-workspace`.
- `agent_environment_service_output`, `topic.intent.agent_env_requirements`, and `topic.env.agent_setup_target_spec` when per-Agent Workspace cwd proof was requested, or an explicit service blocker when that setup was intentionally deferred.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run, explain that validation depends on authoritative topic refs, and tell the user to run `ensure-topic-registration` first. If environment status or Agent Workspace paths are missing, refuse to run, explain that readiness validation depends on setup outputs, and tell the user to run `setup-topic-env` and `setup-agent-workspace` first. If `topic_environment_status` claims ready without Topic Workspace predecessor evidence or a named validation ref, report the missing `isomer-srv-topic-env-setup` evidence as a blocker. If per-Agent Workspace cwd verification was requested and `agent_environment_service_output` is missing, report that missing `isomer-srv-agent-env-setup` evidence as a blocker.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from this validation. Agent environment readiness can satisfy static setup readiness only when `isomer-srv-agent-env-setup` reports all planned Agent Names ready; it does not prove runtime readiness.

Do not treat deferrals as harmless. Mark whether each deferral blocks static setup, validation, profile materialization, or later runtime operation.

Do not run materialization or live operation from validation.
