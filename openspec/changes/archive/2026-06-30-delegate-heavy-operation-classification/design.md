## Context

The previous bounded-run change made `isomer-misc-bounded-run-tips` the first routing surface for resource-safe execution plans. The remaining leak is that core env setup and topic-team specialization skills still define what counts as heavy by listing operation categories such as compilation, model inference, large downloads, broad test suites, and GPU jobs.

That list is not truly platform-neutral. A project may treat `ncu`, a single CUDA compile, a benchmark script, a package install, a small inference run, or a dataset transform differently depending on hardware, project conventions, and user policy. The misc skill layer is intended to be easy for users to edit on demand, so the operation classification rule belongs there.

## Goals / Non-Goals

**Goals:**

- Move normative operation classification from core service/operator skills into `isomer-misc-bounded-run-tips`.
- Make classification output explicit enough for generated gates and service outputs to audit.
- Let topic env setup, agent env setup, and team specialization consume classification evidence instead of carrying hard-coded heavy-operation category lists.
- Preserve readiness behavior: operations classified as heavy or unknown-risk still need bounded real-path evidence or blockers.

**Non-Goals:**

- Do not remove examples of commonly heavy operations from docs when they are clearly non-normative.
- Do not make bounded-run tips responsible for package source choice, Pixi enclosure, repo materialization, or team orchestration.
- Do not relax the rule that smoke tests cannot replace required source-intent paths.
- Do not add runtime automation; this remains skill-document guidance and validation.

## Decisions

1. Add classification as a bounded-run tips responsibility.

   `isomer-misc-bounded-run-tips` should expose an operation-classification contract. Given a natural-language task, command, cwd, expected result, and available context, it classifies the operation as `light`, `heavy`, `unknown-risk`, or `not-applicable`. It also records the reason, resource dimensions, and whether bounded execution guidance is required.

   Alternative considered: keep classification examples in each service skill and only delegate execution planning. That keeps the same duplication problem and makes user customization harder.

2. Core skills ask for classification before deciding resource handling.

   Topic env and agent env derivation should extract candidate operations, then consult bounded-run tips for classification. If the classification is `heavy` or `unknown-risk`, the gate must include a resource check plan and bounded real-path command or blocker. If classification is `light`, the gate may record that no resource check is needed. If classification is `not-applicable`, the operation should be handled by the relevant non-runtime policy.

   Alternative considered: classify only after an operation looks risky to the service skill. That still makes the service skill own the first risk filter.

3. Team specialization consumes service evidence.

   `isomer-admin-topic-team-specialize` should require delegated service output to include operation classification evidence and bounded-plan evidence when needed. It should not define the heavy-operation category list directly.

   Alternative considered: have the operator skill call bounded-run tips directly. That would duplicate service responsibility and blur the service boundary.

4. Examples remain examples.

   The codebase can still say "for example, CUDA compile or benchmark execution" as reader aid. Normative language should avoid fixed lists like "treat X, Y, and Z as heavy" unless the text clearly says the list is an example and the classification source is bounded-run tips.

5. Skill writing stays concise and structured.

   Skill changes should use concise language, Markdown lists for steps, branches, and multiple key points, and short structured sections instead of long prose paragraphs. This matters more here because classification, routing, and readiness rules can otherwise blur together and become hard for an agent to execute reliably.

## Risks / Trade-offs

- [Risk] Agents may forget to classify simple operations and produce noisy gates. → Mitigation: classification can return `light` or `not-applicable`, and the gate only needs full resource plans for `heavy` or `unknown-risk`.
- [Risk] Moving the definition to a misc skill makes behavior user-editable and less uniform across projects. → Mitigation: generated gates must record classification source, result, reason, and resource dimensions so differences are visible.
- [Risk] Verification may inherit stale classification from a bad generated gate. → Mitigation: install and verify steps block when classification evidence is missing or inconsistent with the required operation.
- [Risk] Existing validators may overfit to hard-coded examples. → Mitigation: update validators to require delegation wording and classification evidence instead of fixed heavy-operation lists.
- [Risk] Skill docs may become long prose while explaining the new delegation boundary. → Mitigation: use concise wording, Markdown lists, and structured step/branch sections when editing skills.
