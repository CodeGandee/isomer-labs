## Why

Core env setup and team specialization skills still embed a fixed definition of "heavy operation" even though that definition is application-specific and should be user-tunable. Moving this classification to `isomer-misc-bounded-run-tips` keeps orchestration skills focused on contracts while letting users adapt resource-risk rules for their hardware, workload, and research domain.

## What Changes

- Add an explicit operation-classification contract to `isomer-misc-bounded-run-tips`.
- Require topic env gate derivation to ask bounded-run tips to classify setup and verification operations before deciding whether a resource check and bounded plan are needed.
- Require agent env gate derivation to ask bounded-run tips to classify per-agent cwd verification operations before deciding whether selected-agent partial coverage or bounded execution is needed.
- Require team specialization and service verification wording to stop owning fixed normative lists of heavy operations; they may use examples, but classification evidence must come from bounded-run tips.
- Require generated gates and service output to record classification source, classification result, reason, resource dimensions, and follow-up bounded guidance when needed.

## Capabilities

### New Capabilities

- `isomer-bounded-run-tips-skill`: Defines the user-tunable misc skill contract for classifying operations and planning bounded real-path execution.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Topic env gate generation must delegate operation classification to bounded-run tips.
- `isomer-agent-env-setup-service-skill`: Agent env gate generation must delegate per-agent cwd operation classification to bounded-run tips.
- `isomer-service-env-setup-enclosure`: Shared env setup enclosure policy must treat operation classification as delegated user-tunable guidance.
- `topic-team-specialization-module-skill`: Operator specialization must require delegated service outputs to include classification evidence without defining heavy-operation categories itself.

## Impact

- Affects `skillset/misc/isomer-misc-bounded-run-tips` by adding classification guidance and report fields.
- Affects topic env setup and agent env setup reference pages that derive gates, verify gates, and report resource checks.
- Affects topic team specialization guardrails and delegated service-output expectations.
- Affects OpenSpec specs and validation tests that currently look for hard-coded heavy-operation examples in core skills.
