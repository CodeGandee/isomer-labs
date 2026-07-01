# Bootstrap Workflow

## Workflow

1. Resolve the selected Research Topic and Topic Workspace through Isomer context, not sibling directory scanning.
2. Read `<topic-workspace>/isomer-topic-summary.md` as the primary Topic Team Specialization completion signal. If it is absent, stop with <RSCH_WORKSPACE_BLOCKER_RECORD> and route back to `isomer-admin-topic-team-specialize finalize-topic-team`.
3. Check the summary for the minimal readiness signals in this page. Do not inventory every file produced by Topic Team Specialization.
4. Confirm Workspace Runtime readiness with fresh inspection or validation output before trusting old state.
5. Confirm the minimal semantic labels needed for v2 research bootstrap through Workspace Path Resolution.
6. Identify the bootstrap actor. Prefer Topic Service Master when it is running; otherwise use Project Operator Session or Operator Agent as the fallback actor.
7. Build <RSCH_WORKSPACE_CONTEXT> with topic refs, the summary path, topic-team validation status, runtime readiness, topic-team profile material signal, Agent Workspace context, actor identity, and any setup blockers.
8. Continue to semantic-surface planning only when the context is concrete enough for later v2 skills to avoid guessing.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded bootstrap plan from the selected Topic Workspace, available runtime output, and the user's request.

## Entry Checks

- `isomer-topic-summary.md` exists in the selected registered Topic Workspace root and is current enough for the requested bootstrap.
- The summary reports registered Research Topic and Topic Workspace refs, not only a provisional seed.
- The summary reports `topic_team_validation_status` as ready or ready-with-deferrals. Treat blocked, not-checked, stale, absent, or ambiguous status as a blocker.
- The summary's `## Blockers and Deferrals` section has no blocker that affects v2 research bootstrap, Workspace Runtime readiness, topic-team profile material, or Agent Workspace access.
- Fresh runtime inspection or validation output exists for the selected topic and does not contradict the summary.
- The minimal semantic labels needed for bootstrap resolve or produce explicit blockers: `topic.workspace`, `topic.runtime`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, `topic.records.logs`, `topic.team_profile_bundle`, `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links`.
- Agent Workspace context exists for the agents that will write pre-promotion material.
- The actor performing bootstrap is named in the result.

## Minimal Readiness Signals

Use these signals because they are stable products of Topic Team Specialization and the platform, not because every generated file must be checked:

- Final summary signal: `<topic-workspace>/isomer-topic-summary.md` exists and names the registered topic, registered workspace, validation status, blockers, and next operator action.
- Registration signal: the summary or Isomer context names registered refs and does not describe the workspace as provisional.
- Setup signal: the summary carries topic environment status, agent environment status when checked, and no setup blocker that affects v2 bootstrap.
- Runtime signal: fresh runtime inspection or validation output exists for the selected topic.
- Profile-material signal: the summary or `topic.team_profile_bundle` label identifies the selected topic-team profile material. Do not require `materialize-profile` output unless the selected workflow explicitly needs an approved launch-facing profile.
- Agent-access signal: the summary and path resolution identify Agent Names plus each planned agent's `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links` surfaces.

## Boundary

This skill does not create the Topic Main Development Repository, create per-agent worktrees, repair Pixi environments, or run domain research stages. It verifies the post-specialization research contract and reports blockers for setup services or the operator when the contract is not ready.
