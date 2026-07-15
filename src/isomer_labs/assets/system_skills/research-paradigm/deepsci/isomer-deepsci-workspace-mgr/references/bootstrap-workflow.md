# Bootstrap Workflow

## Workflow

1. Resolve the selected Research Topic and Topic Workspace through Isomer context, not sibling directory scanning.
2. Check base Topic Workspace readiness first from Topic Creator summaries, Topic Manager evidence, registration evidence, or final topic-team summary: registered topic and workspace refs, Workspace Runtime readiness, topic overview, topic environment readiness, ready `topic.repos.main`, materialized research record labels, selected production DeepSci skill placeholder bindings, and a topic-level placeholder binding index or readiness report.
3. Check selected Topic Actor readiness when the workflow is human-orchestrated: Topic Actor bindings, `topic.actors.workspace`, actor support labels, actor cwd instructions, actor metadata for production DeepSci records, actor onboarding evidence, and actor blockers.
4. Check formal team readiness only when the selected topology includes a formal team layer. In that case, read `<topic-workspace>/isomer-topic-summary.md` as the primary Topic Team Specialization completion signal and verify topic-team validation status, profile material, Agent Workspace access, and storage-boundary evidence.
5. Confirm Workspace Runtime readiness with fresh inspection or validation output before trusting old state.
6. Confirm the minimal semantic labels needed for production DeepSci research bootstrap through Workspace Path Resolution.
7. Identify the bootstrap actor. Prefer Topic Service Master when it is running; otherwise use Project Operator Session or Operator Agent as the fallback actor.
8. Build DEEPSCI:RSCH-WORKSPACE-CONTEXT with topic refs, Topic Creator summary refs or Topic Manager evidence, selected production DeepSci skill set, selected Topic Actors, actor workspace readiness, optional topic-team summary path, optional topic-team validation status, runtime readiness, topic-team profile material signal when selected, formal Agent Workspace context when selected, actor identity, selected reset checkpoint id when available, and any setup blockers.
9. Decide whether production DeepSci bootstrap outputs should survive Topic Workspace reset. If they should, plan a checkpoint update with `isomer-cli project topic-reset update-checkpoint --topic <research-topic-id> <checkpoint-id>` after bootstrap records, managed payload files, or explicit exports exist; if not, record that those outputs are redo-after-reset behavior.
10. Continue to semantic-surface planning only when the context is concrete enough for later production DeepSci skills to avoid guessing.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded bootstrap plan from the selected Topic Workspace, available runtime output, and the user's request.

## Entry Checks

- Registered Research Topic and Topic Workspace refs exist, not only a provisional seed.
- Topic Creator summary, Topic Manager evidence, or topic operation summary reports Workspace Runtime readiness, topic environment readiness, `topic.repos.main` readiness, record-label readiness, and topic setup blockers.
- Selected Topic Actor bindings and Topic Actor Workspaces are ready when the workflow includes human-orchestrated actors.
- `isomer-topic-summary.md` exists and is current enough only when the selected topology includes formal team material.
- Formal team summaries report `topic_team_validation_status` as ready or ready-with-deferrals. Treat blocked, not-checked, stale, absent, or ambiguous status as a blocker only for the formal team layer.
- The summary or topic setup evidence has no blocker that affects production DeepSci research bootstrap, Workspace Runtime readiness, selected Topic Actor readiness, topic-team profile material when selected, or Agent Workspace access when selected.
- Fresh runtime inspection or validation output exists for the selected topic and does not contradict the summary.
- The minimal semantic labels needed for bootstrap resolve or produce explicit blockers: `topic.workspace`, `topic.runtime`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, `topic.records.logs`, selected `topic.actors.workspace` labels when actors are selected, optional `topic.team_profile_bundle` when formal team material is selected, and optional `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links` when formal agents will write pre-promotion material.
- Topic Actor Workspace context exists for selected Topic Actors, or formal Agent Workspace context exists for formal agents that will write pre-promotion material.
- The actor performing bootstrap is named in the result.
- Reset-survival intent is explicit: selected production DeepSci bootstrap outputs either update the reset checkpoint after creation or are documented as redo-after-reset behavior.

## Minimal Readiness Signals

Use these signals because they are stable products of Topic Team Specialization and the platform, not because every generated file must be checked:

- Base topic signal: Topic Creator output, Topic Manager evidence, topic operation summary, or Isomer context names registered refs and does not describe the workspace as provisional.
- Setup signal: Topic Creator summary, topic operation summary, or topic-team summary carries topic environment status, topic-main readiness, record-label readiness, and no setup blocker that affects production DeepSci bootstrap.
- Runtime signal: fresh runtime inspection or validation output exists for the selected topic.
- Topic Actor signal: the Topic Workspace Manifest and path resolution identify selected Topic Actors plus each actor's `topic.actors.workspace`, support labels, runtime kind, role kind, and blockers.
- Profile-material signal: when formal team material is selected, the summary or `topic.team_profile_bundle` label identifies the selected topic-team profile material. Do not require `materialize-profile` output unless the selected workflow explicitly needs an approved launch-facing profile.
- Agent-access signal: when formal agents are selected, the summary and path resolution identify Agent Names plus each planned agent's `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links` surfaces.

## Boundary

This skill does not create the Topic Main Development Repository, create Topic Actor or Agent worktrees, repair Pixi environments, or run domain research stages. It verifies the post-preparation research contract and reports blockers for setup services, Topic Manager actor management, or the operator when the contract is not ready.
