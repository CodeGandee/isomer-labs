# Fast Forward

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Determine whether the user supplied enough topic substance:
   - Accept a concrete Research Topic, an explicit registered topic ref with concrete topic material, or enough source material to seed a topic.
   - If no topic substance is supplied, ask for the actual research topic and stop before running `init-topic`.
2. Run `init-topic` when the topic workspace directory is missing or provisional setup is requested.
3. Run `resolve-topic-intent` to resolve `topic.intent.overview` and write topic understanding before any setup or specialization step.
4. Run `clarify-topic` only when missing or unclear topic details block registration, setup, or specialization.
5. Run `ensure-topic-registration`:
   - Verify or create Project Manifest-backed Research Topic and Topic Workspace refs.
   - Verify the Topic Workspace Pixi binding needed by `isomer-srv-topic-env-setup`.
   - Stop on registration or binding blockers.
6. Run `resolve-topic-env-gate` to resolve `topic.intent.topic_env_requirements` when the topic needs environment setup or the user supplied a clear runnable target.
7. Run `setup-topic-env` when setup source exists:
   - Continue when `topic.intent.topic_env_requirements` is usable or an explicit topic env target spec is supplied.
   - Create or validate `topic.env.topic_setup_target_spec`, then delegate Topic Workspace, Topic Main Development Repository, canonical external repo, projection, dependency, and verification materialization to `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> auto`.
8. Run `specialize-team` to select or confirm one Domain Agent Team Template and execute the helper specialization path through draft profile output.
9. Run `clarify-topic-team` only when specialization outputs contain open questions that block setup or validation.
10. Run or rerun `resolve-topic-env-gate` and `setup-topic-env` when specialization adds or changes runnable environment requirements.
11. Run `resolve-agent-env-gate` after Topic Workspace predecessor evidence and specialization evidence exist when per-Agent Workspace cwd readiness is requested.
12. Run `setup-agent-workspace` after required inputs exist:
   - Require `topic.intent.agent_env_requirements`, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor evidence when needed, specialization evidence, and authoritative Agent Names.
   - Create or validate `topic.env.agent_setup_target_spec`, then delegate per-agent worktree creation and cwd readiness proof to `$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>`.
   - Use `isomer-admin-topic-workspace-mgr` only for explicitly requested topology inspection, branch helper, boundary summary, or legacy compatibility diagnostics.
13. Run `validate-topic-team`, then run `finalize-topic-team` to create `isomer-topic-summary.md`.
14. Stop at final topic-team summary output:
   - Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary.
   - Require the needed validation or approval inputs before crossing that boundary.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute the plan.

## Output Contract

Report semantic labels and resolved paths for topic overview, topic env source intent, topic env target spec, agent env source intent, and agent env target spec when present; also report registration status, registered topic and workspace refs, environment binding status, selected Domain Agent Team Template, copied material paths, topic environment status, Topic Main Development Repository and projection predecessor evidence, Agent Workspace paths, topic-team validation status, `isomer-topic-summary.md` path, blockers, deferrals, and next operator action.
