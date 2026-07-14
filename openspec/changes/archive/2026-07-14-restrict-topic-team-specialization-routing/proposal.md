## Why

Operator and research-workspace routing can infer Topic Team Specialization from generic topic preparation, launch-facing readiness, or a missing summary even when the user did not request an Agent Team. This sends ordinary topic preparation into Domain Agent Team Template discovery and violates the established separation between Topic Creator, Topic Manager, and formal team specialization.

## What Changes

- Require either an explicit `isomer-op-topic-team-specialize` invocation or Agent Team intent established by the prompt or authoritative formal-team context before any skill routes to Topic Team Specialization.
- Define positive Agent Team signals and explicitly reject generic topic preparation, workspace readiness, launch-facing work, missing summaries, or missing Agent Workspaces as sufficient routing evidence.
- Align EntryPoint, Welcome, DeepSci workspace bootstrap, and Team Specialization handoff guidance with the same routing invariant.
- Add focused validation coverage for allowed Agent Team routes and denied false-positive routes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-op-entrypoint-skill`: Restrict Team Specialization selection and readiness recovery to explicit or contextually established Agent Team intent.
- `isomer-admin-welcome-skill`: Qualify launch-facing recommendations so generic launch or preparation language cannot imply a formal Agent Team.
- `research-paradigm-skills`: Make formal-team bootstrap and missing-summary recovery conditional on a selected formal Agent Team layer.

## Impact

The change affects packaged operator and DeepSci skill instructions, their mirrored `skillset/` surfaces, skill validation rules and fixtures, and the three modified main-spec capabilities. It changes routing guidance only; no CLI schema, durable record format, or runtime API changes.
