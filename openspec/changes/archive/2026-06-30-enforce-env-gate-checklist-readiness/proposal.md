## Why

Derived topic and agent environment gates now use Markdown checklists, but the skills still need a precise rule that checklist completion is the source of environment readiness. Without that rule, an agent can mark an environment ready after a weaker smoke test, leaving a critical build, inference, dataset, or benchmark path unproven.

## What Changes

- Treat every item in a generated gate's `## Gate Checklist` as required readiness work unless it is explicitly moved to a non-readiness diagnostic section.
- Require `ready` only when every required checklist item is checked and backed by evidence from the relevant command, path check, resource probe, expected-result comparison, or recorded setup step.
- Require unchecked checklist items to remain visible and be classified as blocked, failed, or not checked with a concrete reason and next action.
- Forbid marking a checklist item done with a reduced smoke test that does not prove the item's critical code path, unless the user explicitly instructs the agent to downgrade the item and that override is recorded.
- Align topic env setup, agent env setup, and topic-team specialization validation so delegated readiness reports are rejected when required checklist items are incomplete.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Topic environment gate derivation and verification must compute readiness from required checklist completion and evidence.
- `isomer-agent-env-setup-service-skill`: Agent environment gate derivation and verification must compute per-agent and overall readiness from required checklist completion, preserving selected-agent partial evidence as partial.
- `topic-team-specialization-module-skill`: Operator setup and validation must accept service readiness only when required checklist items are complete, or report explicit blockers for incomplete items.

## Impact

This affects Markdown skill instructions under `skillset/service/isomer-srv-topic-env-setup`, `skillset/service/isomer-srv-agent-env-setup`, and `skillset/operator/isomer-admin-topic-team-specialize`, plus repository validation rules or tests that assert the gate checklist semantics. No runtime API, dependency, or schema migration is required.
