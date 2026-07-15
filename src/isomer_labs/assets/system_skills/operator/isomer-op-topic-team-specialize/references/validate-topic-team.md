# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Read validation inputs:
   - Prepared-topic evidence when present, including reused common preparation refs, Workspace Runtime readiness, topic-main readiness, storage bootstrap refs, current Topic Actor roster, and Topic Actor Workspace refs.
   - Topic definition material, registration assurance evidence, specialization outputs, and topic environment setup evidence from `isomer-srv-topic-env-setup`.
   - Topic Main Development Repository predecessor evidence, projection predecessor evidence when needed, and optional delegated workspace-manager topology inspection evidence when explicitly requested.
   - Delegated `isomer-srv-agent-env-setup` evidence for Agent Workspace worktrees, agent names, branch plans, `isomer-managed/` support surfaces, cwd readiness, blockers, and validation refs.
3. Check that `topic.intent.overview` exists, reports semantic label evidence plus resolved path metadata, and reflects the current Research Topic understanding.
4. Check registration assurance:
   - Require Project Manifest-backed `registered_research_topic_ref` and `registered_topic_workspace_ref`, or explicit registration blockers.
   - Do not validate readiness from only a provisional topic workspace seed.
5. Check copied specialization material:
   - Require `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs.
   - Accept explicit blockers when material is missing.
6. Check Topic Actor coexistence:
   - Preserve active Topic Actor bindings and Topic Actor Workspace refs as predecessor context.
   - Do not require Topic Actor bindings for formal team readiness, and do not treat Topic Actor readiness as Agent Workspace readiness.
   - If actor topology is stale or blocked, report it separately and route repair to `isomer-op-topic-mgr` without deleting or converting actor bindings.
7. Check setup streams separately:
   - Confirm topic environment setup and Agent Workspace setup are ready, not requested, or blocked with named next actions. If an env gate exists and names runnable targets, missing bounded real-path verification is a blocker, not a deferral.
   - Topic environment setup evidence should include `topic_environment_status`, `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, its `## Gate Checklist`, resolved path metadata, Topic Workspace predecessor readiness status, Topic Main Development Repository Git state, Isomer-managed namespace posture, projection metadata, operation classification evidence from bounded-run tips, resource check status for commands classified as `heavy` or `unknown-risk`, setup commands, changed files, environment binding status, `per_agent_readiness_status: not checked` when reported, and blockers from `isomer-srv-topic-env-setup`.
   - Accept topic environment setup as ready only when every required topic gate checklist item is checked with supporting execution, path, dependency, resource, or expected-result evidence. If any required checklist item is unchecked, failed, blocked, missing, or completed only by a weaker smoke test that does not prove the named critical path, report static setup readiness as blocked, failed, or not checked with the exact checklist item and next action.
   - Treat missing environment setup evidence as an environment-preparation blocker, not as evidence that team-profile material is missing.
8. When per-Agent Workspace cwd verification was requested, require `isomer-srv-agent-env-setup` evidence:
   - Require `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, its `## Gate Checklist`, resolved path metadata, authoritative Agent Names, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, resolved `agent.workspace` paths, branch plan, worktree status by agent, operation classification evidence from bounded-run tips, resource check status for commands classified as `heavy` or `unknown-risk`, readiness by agent, commands run, blockers, and next action.
   - Require semantic path evidence for `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support labels, and path sources.
   - Treat selected-agent evidence as partial.
   - Do not mark overall agent environment readiness as ready unless every planned Agent Name is verified and every required per-agent checklist item is checked with supporting cwd evidence.
   - If delegated agent env evidence contains an unchecked, failed, blocked, partial, or not-checked checklist item, report the exact Agent Name, checklist item, reason, and next action.
9. Reject stale Agent Workspace setup evidence:
   - Reject legacy support roots, top-level Topic Main Development Repository collaboration directories, tmp contents as readiness evidence, or hard-coded default-only paths without semantic labels as the current standard layout.
   - Ask for `isomer-srv-agent-env-setup` verification when worktree or cwd readiness is missing, or for optional `isomer-op-topic-mgr` inspection when the user only needs topology diagnostics.
10. State naturally whether static Topic Team material is ready, ready with deferrals, blocked, or not checked, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static-material validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- `topic.intent.overview` with resolved path metadata.
- Registration assurance from `ensure-topic-registration`, including registered Research Topic and Topic Workspace refs, Topic Workspace Pixi binding status, and any registration blockers.
- Specialized topic-team material and draft profile or packet/profile input summary from `adapt-team-template`.
- Prepared-topic evidence and current Topic Actor roster when present; missing Topic Actor evidence is not a formal team blocker unless the selected team flow explicitly depends on it.
- `topic_environment_status` or explicit setup blocker from `setup-topic-env`, preferably with `isomer-srv-topic-env-setup` service output evidence.
- `agent_names`, `agent_workspace_paths`, `semantic_paths`, `local_tmp_path_status`, `isomer_managed_path_status`, `branch_plan`, worktree evidence, generated-link evidence, or explicit workspace blocker from `setup-agent-workspace`.
- `agent_environment_service_output`, `topic.intent.agent_env_requirements`, and `topic.env.agent_setup_target_spec` when per-Agent Workspace cwd proof was requested, or an explicit not-requested note when per-Agent Workspace cwd proof is out of scope.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run directly, explain that validation depends on authoritative topic refs, and offer targeted fast-forward recovery through `ensure-topic-registration` to `validate-topic-team`.

If specialization, environment status, or Agent Workspace paths are missing, refuse to run directly, explain that readiness validation depends on setup outputs, and offer targeted fast-forward recovery to `validate-topic-team`. Use `python scripts/query_step_dependencies.py path --target validate-topic-team --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target validate-topic-team --exclude-target` for the exclusive path.

If `topic_environment_status` claims ready without Topic Workspace predecessor evidence, required `## Gate Checklist` completion evidence, or a named validation ref, report the missing `isomer-srv-topic-env-setup` evidence as a blocker. If per-Agent Workspace cwd verification was requested and `agent_environment_service_output` is missing, report that missing `isomer-srv-agent-env-setup` evidence as a blocker.

## Guardrails

- DO NOT claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from this validation. Agent environment readiness can satisfy static setup readiness only when `isomer-srv-agent-env-setup` reports all planned Agent Names ready; it does not prove runtime readiness.

- DO NOT describe a weaker smoke-test downgrade as proof that the original critical path passed. Preserve the user downgrade, weaker evidence, affected checklist item, and limitation in validation blockers or deferrals.

- DO NOT treat deferrals as harmless. Mark whether each deferral blocks static setup, validation, profile materialization, or later runtime operation.

- DO NOT run materialization or live operation from validation.
