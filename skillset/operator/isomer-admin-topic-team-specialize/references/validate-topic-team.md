# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read topic definition material, registration assurance evidence, specialization outputs, topic environment setup evidence from `isomer-srv-topic-env-setup`, Agent Workspace paths, agent names, branch plans, `isomer-managed/` regime status, generated-link evidence, delegated Git-backed workspace manager evidence, deferrals, blockers, and validation refs.
3. Check that `topic-overview.md` exists and reflects the current Research Topic understanding.
4. Check that registration assurance names Project Manifest-backed `registered_research_topic_ref` and `registered_topic_workspace_ref`, or records explicit registration blockers. Do not validate readiness from only a provisional topic workspace seed.
5. Check that copied specialization material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs exist or have explicit blockers.
6. Check that topic environment setup and Agent Workspace setup are ready as durable preparation, intentionally deferred, or blocked with named next actions. Environment setup evidence should include `topic_environment_status`, `env_gate_path`, `derived_gate_path` when available, service readiness status, setup commands, changed files, environment binding status, and blockers from `isomer-srv-topic-env-setup`. Treat missing environment setup evidence as an environment-preparation blocker, not as evidence that team-profile material is missing. When Git-backed worktrees were requested, require `isomer-admin-topic-workspace-mgr` validation evidence for `topic.main_repo`, `agent.workspace`, required `agent.*` support labels, generated links, boundary material, path sources, and blockers, or report missing delegated setup as a blocker.
7. Reject stale Agent Workspace setup evidence that treats legacy support roots, top-level Topic Main Repository collaboration directories, or hard-coded default-only paths without semantic labels as the current standard layout; ask for `isomer-admin-topic-workspace-mgr` validation of semantic labels and `isomer-managed/`.
8. Report `topic_team_validation_status` as ready, ready-with-deferrals, blocked, or not checked for static material readiness, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static-material validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- `<topic-dir>/topic-def/topic-overview.md`.
- Registration assurance from `ensure-topic-registration`, including registered Research Topic and Topic Workspace refs, Topic Workspace Pixi binding status, and any registration blockers.
- Specialized topic-team material and draft profile or packet/profile input summary from `specialize-team`.
- `topic_environment_status` or explicit setup blocker from `setup-topic-env`, preferably with `isomer-srv-topic-env-setup` service output evidence.
- `agent_names`, `agent_workspace_paths`, `semantic_paths`, `isomer_managed_path_status`, `branch_plan`, generated-link evidence, or explicit workspace blocker from `setup-agent-workspace`.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run, explain that validation depends on authoritative topic refs, and tell the user to run `ensure-topic-registration` first. If environment status or Agent Workspace paths are missing, refuse to run, explain that readiness validation depends on setup outputs, and tell the user to run `setup-topic-env` and `setup-agent-workspace` first. If `topic_environment_status` claims ready without service readiness evidence or a named validation ref, report the missing `isomer-srv-topic-env-setup` evidence as a blocker. If the requested Agent Workspace layout is Git-backed and delegated workspace manager evidence is missing, report that missing delegated setup as a blocker.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from this validation.

Do not treat deferrals as harmless. Mark whether each deferral blocks static setup, validation, profile materialization, or later runtime operation.

Do not run materialization or live operation from validation.
