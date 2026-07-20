## Why

Project Operator Sessions can enter `isomer-op-entrypoint` from the Project root, a Topic Workspace, Topic Main, or a worker workspace. Existing Effective Context resolution can select manifest defaults that are valid command inputs but do not prove the operator's physical location, task target, or active identity posture, so an agent can silently operate on the wrong Research Topic and then improvise an invalid filesystem fallback.

## What Changes

- Add read-only CLI self-location and context-alignment queries that classify canonical cwd against registered Project, Topic Workspace, Topic Main, Topic Actor Workspace, and Agent Workspace boundaries.
- Keep Effective Topic, Topic Actor, and Agent Context as path-resolution selections while reporting ambient location, task-selected target, manifest defaults, and active acting posture as distinct concepts with source metadata.
- Require `isomer-op-entrypoint` to run context preflight for context-sensitive routes, reconcile prompt targets with ambient and default context, and pin the resolved `--topic`, `--topic-actor`, or `--agent` selectors on downstream commands.
- Strengthen identity switching so its one-task or persistent session posture is carried explicitly into downstream command planning and checked against the resolved worker cwd without creating shared persistent identity state.
- Require research preflight and production research skills to stop on target conflicts, report the conflicting sources, and avoid raw filesystem copies or alternate output locations as recovery from a failed typed operation.
- Include selected-context metadata in context-sensitive Kaoju template command results and diagnostics so wrong-topic selection is visible before an agent attempts recovery.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli-topic-context-resolution`: Distinguish ambient workspace location, effective path-resolution context, task-selected target, defaults, and acting posture, and validate their alignment.
- `isomer-cli-project-discovery`: Add progressive read-only self-location and context-check command surfaces with deterministic JSON output.
- `isomer-op-entrypoint-skill`: Make context preflight and explicit selector propagation mandatory for context-sensitive routed work.
- `operator-switch-identity-skill`: Carry session-local switched posture into downstream context checks, selectors, cwd discipline, and provenance without treating manifest defaults as active identity.
- `research-context-preflight`: Reconcile prompt-selected research targets with resolved context before durable work and retain the selected target on subsequent commands.
- `research-paradigm-skills`: Require production extension skills to consume the reconciled target and reject ad hoc filesystem fallback after typed command failure.
- `kaoju-cli-services`: Report selected Research Topic and Topic Workspace context in template operation results and failures.

## Impact

The change affects Project self-query CLI registration and payloads, cwd-to-workspace classification, Effective Context reporting, operator entrypoint and identity-switch skill guidance, shared research preflight guidance, Kaoju production skill guidance, Kaoju template service output, unit tests, packaged-skill validation, and CLI documentation. It introduces no shared current-identity file, no OS-level impersonation, and no new runtime identity authority. Implementation must coordinate with the active `add-independent-pack-welcome-skills` change because both changes touch packaged operator and extension entrypoint guidance.
