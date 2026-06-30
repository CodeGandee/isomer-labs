## Context

Topic env and agent env setup now derive operational gate files with a `## Gate Checklist` section. The checklist makes the gate easier to read, but the current service and operator wording still needs to state that readiness is computed from checklist state. The affected reader is an agent executing Isomer skills: it must know that unchecked required items block readiness, and that a weak smoke test cannot complete a checklist item whose purpose is to prove a heavier critical path.

## Goals / Non-Goals

**Goals:**

- Define `## Gate Checklist` as the required readiness contract for derived topic env and agent env target specs.
- Make `ready` depend on every required checklist item being checked with evidence.
- Preserve bounded real-path verification as valid when it still exercises the critical path named by the checklist item.
- Require blocked, failed, partial, and not-checked states to name the exact checklist item and reason.
- Make topic-team specialization reject delegated readiness evidence that leaves required checklist items incomplete.

**Non-Goals:**

- Do not introduce a new gate file format beyond Markdown checkboxes.
- Do not require full-scale heavy runs when a bounded real-path command proves the same critical path.
- Do not remove user override paths, but require overrides to be explicit evidence.
- Do not change Isomer runtime APIs, storage labels, or workspace layout.

## Decisions

1. `## Gate Checklist` is required work, not a progress decoration.

   The generated gate can still contain supporting sections such as `## Verification Commands`, `## Expected Results`, and `## Execution Log`, but the checklist is the readable index of required readiness items. Optional diagnostics should live outside the gate checklist so an unchecked optional item does not make readiness ambiguous.

2. Readiness is computed by checklist state plus evidence.

   A checked item counts only when the execution log, command output summary, resource probe, path evidence, dependency mutation, or expected-result comparison proves that item. An unchecked item makes the result not ready. The verifier then classifies it as blocked, failed, or not checked based on what happened.

3. Bounded real-path checks remain valid; unrelated smoke tests do not.

   A reduced check is valid when it exercises the critical code path, such as compiling one required CUDA target with reduced parallelism or running a tiny benchmark through the real kernel. A smoke test is insufficient when it proves only generic imports, device visibility, or repository presence while the checklist item requires a build, inference, dataset, or benchmark path.

4. User downgrades are explicit overrides.

   If the user instructs the agent to accept a weaker check, the agent must record the overridden checklist item, the weaker evidence, and the user instruction. That evidence can explain the result, but it must not be silently presented as full proof of the original critical path.

5. Operator validation consumes the service result conservatively.

   `isomer-admin-topic-team-specialize` should trust `ready` only when the service output shows complete required checklist evidence. Missing or incomplete checklist evidence becomes a static setup blocker or partial status, not a deferred success.

## Risks / Trade-offs

- [Risk] More gates will stop as blocked instead of ready when generated checklist items are vague. Mitigation: improve derivation guidance so every checklist item has a pass condition, evidence source, and blocker condition.
- [Risk] Agents may over-test heavy paths to avoid blockers. Mitigation: keep bounded real-path language prominent and require lightweight resource probes before heavy commands.
- [Risk] Existing text that mentions deferral can conflict with the checklist rule. Mitigation: revise readiness wording so deferral is allowed only when the workflow explicitly did not request verification, not when a required checklist item failed to run.
