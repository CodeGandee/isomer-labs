# Validation and Blockers

## Workflow

1. Validate <RSCH_WORKSPACE_CONTEXT> for selected topic refs, Topic Creator or Topic Workspace Manager evidence, selected v2 skill set, final topic summary signal when formal team material is selected, topic-team validation status, topic-team profile material signal, runtime readiness, Agent Workspace context, and actor identity.
2. Validate <RSCH_STORAGE_LABEL_PLAN> for available labels, planned labels, optional `custom.*` needs, and blocked support.
3. Validate <RSCH_PLACEHOLDER_BINDING_REGISTRY> for kind coverage, producer and consumer clarity, and missing binding status.
4. Validate <RSCH_AGENT_ACCESS_PLAN> for pre-promotion surfaces, generated conveniences, and promotion boundaries.
5. Produce <RSCH_BOOTSTRAP_VALIDATION_REPORT> when the v2 research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> when a missing input or platform surface would force later skills to guess.

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
- missing-selected-v2-skill-set
- missing-agent-workspace-context
- missing-semantic-label
- planned-label-not-implemented
- unsafe-path-source
- promotion-support-missing
- placeholder-binding-incomplete
- actor-not-recorded

## Validation Report

The validation report should include:

- status: ready, ready-with-deferrals, blocked, or stale
- checked topic and actor
- selected v2 skill set
- final topic summary path and topic-team validation status
- semantic label summary
- placeholder binding summary
- Agent Workspace access summary
- blockers and next action

Do not mark the bootstrap ready when a later v2 skill would need to invent a location, infer producer ownership, or cite an unpromoted scratch path as durable evidence.

## Readiness Decision Rules

- Missing `isomer-topic-summary.md` means Topic Team Specialization has not reached the final summary boundary; route back to `isomer-admin-topic-team-specialize finalize-topic-team`.
- A summary that reports provisional registration, blocked validation, not-checked validation, stale setup evidence, or relevant blockers means bootstrap is blocked.
- A ready-with-deferrals summary can pass only when each deferral is unrelated to v2 research bootstrap, Workspace Runtime readiness, topic-team profile material, and Agent Workspace access.
- Fresh runtime inspection or validation output must agree with the summary. If it contradicts the summary, treat the summary as stale.
- Do not mark bootstrap ready from directory existence alone; require the final summary signal plus fresh semantic resolution or explicit blockers.
