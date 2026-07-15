# Finalize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, Workspace Runtime, and `topic.workspace.summary` through Workspace Path Resolution. The default summary path is `<topic-workspace>/isomer-status-summary.md`.
2. Validate required readiness signals: Project readiness, Research Topic registration, Topic Workspace registration, Workspace Runtime initialization, `topic.intent.overview`, topic environment readiness evidence, ready `topic.repos.main`, actor readiness when in scope, and semantic path resolution evidence.
3. Resolve actor scope. If actor setup was requested, or the default `operator` Topic Actor was not explicitly opted out, require `topic.intent.actor_definitions`, selected Topic Actor bindings, selected Topic Actor Workspace readiness, `topic.env.actor_env_gates`, and actor cwd verification evidence. If no actors were requested and the default `operator` Topic Actor was explicitly opted out, record actor readiness as skipped with the opt-out reason.
4. Include Topic Service Master preparation state when setup-actors reached Houmao-backed work: `ready`, `skipped`, `blocked`, or `not_configured`, plus suggested names, recorded binding status or skip reason, Topic Workspace Manifest binding evidence when present, and the Project Manifest Houmao integration evidence used for that state.
5. Build the Topic Workspace readiness summary with identity, generated-at timestamp, overall status, ready surfaces, verified checks, blocked signals, skipped optional work, installed or materialized surfaces, semantic labels and resolved paths, delegated owner evidence, command evidence when available, and durable-versus-editable distinctions.
6. If the Topic Workspace and `topic.workspace.summary` resolve, write or refresh the summary even when readiness is blocked. If the summary path cannot resolve, report the resolver diagnostic and do not guess a root-level file path.
7. When Workspace Runtime and the selected Topic Workspace resolve, create or refresh the first structured reset checkpoint with `isomer-cli project topic-reset checkpoint --topic <research-topic-id>`, using `topic.workspace.summary`, operator-level readiness evidence, semantic path evidence, preserved setup record ids, selected Topic Actor refs, and blockers as checkpoint input. If readiness is blocked, create a blocked checkpoint or report the deterministic blocker diagnostics from the command.
8. Print a compact final report with `ready`, `verified`, `skipped`, and `blocked` groups plus the resolved summary path and reset checkpoint id when available.

If the user's task does not map cleanly to these steps, report which readiness signals can be validated and which selector, semantic label, or predecessor evidence blocks finalization.

## Summary Shape

Write `topic.workspace.summary` as Markdown with these sections when information is available:

- **Identity**: Project root, Research Topic ref, Topic Workspace ref, Topic Workspace path, generated time, and overall status.
- **Ready**: Usable workspace surfaces, including `topic.repos.main`, Workspace Runtime, selected Topic Actor Workspaces, and actor onboarding surfaces.
- **Verified**: Checks performed with evidence refs, command output refs, delegated owner outputs, or semantic path diagnostics.
- **Blocked**: Missing or failed required signals with exact semantic label, actor name, or artifact name.
- **Skipped**: Optional work intentionally out of scope, including actor readiness when the default `operator` actor was explicitly opted out and no other actors were requested.
- **Topic Service Master**: Preparation state, suggested specialist name, launch profile name, managed agent name, binding status, skip reason or blocker, Topic Workspace Manifest binding evidence when available, Project Manifest Houmao integration evidence, returned skill route when enabled, and explicit note that launch remains a later lifecycle operation.
- **Installed or Materialized**: Topic env, repositories, runtime, actor workspaces, actor onboarding surfaces, and other prepared surfaces.
- **Semantic Paths**: Labels, resolved paths, source, storage profile, and diagnostics.
- **Evidence**: Command evidence, service outputs, runtime refs, and validation refs.
- **Reset Checkpoint**: Checkpoint id, managed payload file path, explicit Markdown export path when present, checkpoint status, source readiness evidence, and blockers.

## Guardrails

- MUST limit `finalize` to Topic Workspace preparation; it does not finalize research findings or replace `isomer-deepsci-finalize`.

- DO NOT recommend a next research step, research-stage skill, Houmao launch, formal team specialization, or manual session route. Name blockers and evidence, but do not prescribe what to run next.

- DO NOT create research handoff records. Topic Creator readiness is represented by `topic.workspace.summary`, ready/verified/blocked state, actor onboarding context, and durable evidence refs.

- DO NOT inspect, require, name, or route through research-paradigm skills when creating the first reset checkpoint. The first checkpoint is an operator-owned initialization boundary derived from Workspace Runtime, Workspace Path Resolution, `topic.workspace.summary`, and operator-level readiness evidence.

- DO NOT use Git stash, branch reset, commit creation, tags, refs, or project-root tracking as reset checkpoint material. The reset checkpoint is a structured Workspace Runtime and research-record artifact.
