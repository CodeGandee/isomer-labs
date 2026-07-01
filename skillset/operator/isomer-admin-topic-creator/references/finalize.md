# Finalize

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, Workspace Runtime, and `topic.workspace.summary` through Workspace Path Resolution. The default summary path is `<topic-workspace>/isomer-topic-workspace-summary.md`.
2. Validate required readiness signals: Project readiness, Research Topic registration, Topic Workspace registration, Workspace Runtime initialization, `topic.intent.overview`, topic environment readiness evidence, ready `topic.repos.main`, v2 research bootstrap outputs, materialized placeholder-binding entrypoints, and semantic path resolution evidence.
3. Resolve actor scope. If actor setup was requested, or the default `operator` Topic Actor was not explicitly opted out, require `topic.intent.actor_definitions`, selected Topic Actor bindings, selected Topic Actor Workspace readiness, `topic.env.actor_env_gates`, and actor cwd verification evidence. If no actors were requested and the default `operator` Topic Actor was explicitly opted out, record actor readiness as skipped with the opt-out reason.
4. Build the Topic Workspace readiness summary with identity, generated-at timestamp, overall status, ready surfaces, verified checks, blocked signals, skipped optional work, installed or materialized surfaces, semantic labels and resolved paths, delegated owner evidence, command evidence when available, and durable-versus-editable distinctions.
5. If the Topic Workspace and `topic.workspace.summary` resolve, write or refresh the summary even when readiness is blocked. If the summary path cannot resolve, report the resolver diagnostic and do not guess a root-level file path.
6. Print a compact final report with `ready`, `verified`, and `blocked` groups plus the resolved summary path when available.

If the user's task does not map cleanly to these steps, report which readiness signals can be validated and which selector, semantic label, or predecessor evidence blocks finalization.

## Summary Shape

Write `topic.workspace.summary` as Markdown with these sections when information is available:

- **Identity**: Project root, Research Topic ref, Topic Workspace ref, Topic Workspace path, generated time, and overall status.
- **Ready**: Usable workspace surfaces, including `topic.repos.main`, Workspace Runtime, selected Topic Actor Workspaces, and bootstrap surfaces.
- **Verified**: Checks performed with evidence refs, command output refs, delegated owner outputs, or semantic path diagnostics.
- **Blocked**: Missing or failed required signals with exact semantic label, actor name, or artifact name.
- **Skipped**: Optional work intentionally out of scope, including actor readiness when the default `operator` actor was explicitly opted out and no other actors were requested.
- **Installed or Materialized**: Topic env, repositories, runtime, actor workspaces, placeholder-binding entrypoints, and other prepared surfaces.
- **Semantic Paths**: Labels, resolved paths, source, storage profile, and diagnostics.
- **Evidence**: Command evidence, service outputs, runtime refs, and validation refs.

## Guardrails

`finalize` finalizes Topic Workspace preparation only. It does not finalize research findings and does not replace `isomer-rsch-finalize-v2`.

Do not recommend a next research step, v2 skill, Houmao launch, formal team specialization, or manual session route. Name blockers and evidence, but do not prescribe what to run next.

Do not create start packs. Topic Creator readiness is represented by `topic.workspace.summary`, ready/verified/blocked state, and durable evidence refs.
