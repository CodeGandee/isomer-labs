# Fulfill an Environment Service Request

## Required Inputs

Require one canonical Service Request ref in `dispatched` state, a supported Topic Workspace environment scope, a linked environment-preparation plan or target spec, explicit authorization, expected output semantic ids, and the parent Research Task and Run refs when present.

## Workflow

1. Load the request through `project service-requests status` and validate supported scope, task, authorization, dispatch mode, expected outputs, and links. Reject no-wait operation and provider-specific payload fields.
2. Resolve the Topic Workspace, Pixi manifest, candidate environments, source repository, dependency intent, task-critical path, resource posture, and current gate state. Report ambiguity without mutation.
3. Apply the ordered strategy: reuse an existing satisfying environment; add flexible compatible constraints to an existing environment while preferring `default`; otherwise create a dedicated environment. Preserve flexible intent in the plan and exact resolved versions plus lock identity in the resulting environment ref.
4. Record before-and-after gate state in `kaoju:env-gate-revision` and the selected environment in `kaoju:pixi-env-ref` through typed Artifact operations.
5. Create `kaoju:smoke-run-script` as a durable ordinary-file Artifact under the service-owned record surface. Execute only a Run-tied staged copy through an Execution Adapter Command Request whose command starts with `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`. Never use the ambient shell environment, and never make a source-tree or Local Tmp Surface copy canonical.
6. Record `kaoju:smoke-run-result` with command request, environment lock, task-critical observation, warnings, logs, exit status, timing, and provenance. Environment readiness requires a successful task-critical observation, not installation success alone.
7. On bounded repair, preserve the failed smoke Run and Gate revision. A material dependency, source, script-semantics, resource, or interpretation change requires a revised plan and human Gate.
8. Complete the Service Request with environment, Gate revision, smoke script, smoke result, support Artifact, command request, Run, blocker, and Provenance Record refs. On timeout or interruption, return the stable request ref and first incomplete stage.

If the user's task does not map cleanly to these steps, use your native planning tool to restate the authorized Service Request as a staged environment-preparation plan, then execute only the supported service-safe portion.

## Output Boundary

The Service Request is operational coordination, not a Research Task or Workflow Stage. The Service Team observes and returns support state; the Kaoju trial owner retains research interpretation and trial-plan authority. Houmao, gateway, mailbox, and provider payloads remain adapter details outside canonical records.
