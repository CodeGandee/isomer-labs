# Validation and Blockers

## Workflow

1. Validate <RSCH_WORKSPACE_CONTEXT> for selected topic refs, Topic Creator or Topic Manager evidence, selected production DeepSci skill set, final topic summary signal when formal team material is selected, topic-team validation status, topic-team profile material signal, runtime readiness, Agent Workspace context, and actor identity.
2. Validate <RSCH_STORAGE_LABEL_PLAN> for available labels, planned labels, optional `custom.*` needs, and blocked support.
3. Validate <RSCH_PLACEHOLDER_BINDING_REGISTRY> for kind coverage, producer and consumer clarity, and missing binding status.
4. Validate <RSCH_AGENT_ACCESS_PLAN> for pre-promotion surfaces, generated conveniences, and promotion boundaries.
5. Validate reset-survival intent: if bootstrap setup should survive Topic Workspace reset, require a selected reset checkpoint and a planned or completed `isomer-cli project topic-reset update-checkpoint` call that names preserved records, structured payloads, on-demand views, semantic labels, support paths, source label, actor refs, and provenance refs.
6. Produce <RSCH_BOOTSTRAP_VALIDATION_REPORT> when the production DeepSci research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> when a missing input or platform surface would force later skills to guess.

If the user's task does not map cleanly to these steps, use your native planning tool to list the unchecked validation areas and stop with a blocker when durable outputs would otherwise be ambiguous.

## Blocker Classes

- missing-topic-context
- missing-topic-summary
- provisional-topic-summary
- stale-topic-summary
- blocked-topic-team-validation
- setup-blocker-in-summary
- missing-profile-bundle
- missing-runtime-readiness
- missing-topic-creator-summary
- missing-topic-actor-readiness
- missing-selected-production DeepSci-skill-set
- missing-agent-workspace-context
- missing-semantic-label
- planned-label-not-implemented
- unsafe-path-source
- promotion-support-missing
- placeholder-binding-incomplete
- actor-not-recorded
- reset-checkpoint-not-selected
- reset-survival-update-missing

## Validation Report

The validation report should include:

- status: ready, ready-with-deferrals, blocked, or stale
- checked topic and actor
- selected production DeepSci skill set
- final topic summary path and topic-team validation status
- semantic label summary
- placeholder binding summary
- Agent Workspace access summary
- reset-survival decision and checkpoint update refs when applicable
- blockers and next action

Do not mark the bootstrap ready when a later production DeepSci skill would need to invent a location, infer producer ownership, or cite an unpromoted scratch path as durable evidence.

Do not imply production DeepSci bootstrap setup will survive Topic Workspace reset unless the selected reset checkpoint has been updated. Unrecorded production DeepSci preparation is valid only as redo-after-reset behavior.

## Readiness Decision Rules

- Missing `isomer-topic-summary.md` means Topic Team Specialization has not reached the final summary boundary; route back to `isomer-op-topic-team-specialize finalize-topic-team`.
- A summary that reports provisional registration, blocked validation, not-checked validation, stale setup evidence, or relevant blockers means bootstrap is blocked.
- A ready-with-deferrals summary can pass only when each deferral is unrelated to production DeepSci research bootstrap, Workspace Runtime readiness, topic-team profile material, and Agent Workspace access.
- Fresh runtime inspection or validation output must agree with the summary. If it contradicts the summary, treat the summary as stale.
- Do not mark bootstrap ready from directory existence alone; require the final summary signal plus fresh semantic resolution or explicit blockers.
