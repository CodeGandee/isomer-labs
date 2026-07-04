## Context

`isomer-admin-topic-creator` now serves as the front door for creating or preparing a Research Topic. Recent guidance made bare topic-creation requests route to `run-to finalize`, but the current `run-to` contract still excludes the named target by default. That means a default path named `run-to finalize` can stop short of the finalization step unless the user adds extra inclusive wording.

The operator skillset is validated by tests and by the `operator-admin-skills` OpenSpec capability. The change should update that contract and the skill guidance without changing lower-level Isomer CLI APIs or the main Topic Creator readiness ladder.

## Goals / Non-Goals

**Goals:**

- Make `run-to <target>` include `<target>` by default.
- Make exclusion available only when the user explicitly asks to stop before or exclude the target.
- Preserve the same main workflow order, required-input checks, mutation approval checks, and invalid-target diagnostics.
- Keep bare topic creation routed to `run-to finalize`, now with inclusive target semantics.
- Update docs, validation, and tests so agents learn the same behavior in every surface.

**Non-Goals:**

- Do not change the `fast-forward` no-stop happy path.
- Do not make `step-by-step` less interactive or remove its acknowledgement gates.
- Do not allow helper, misc, unknown, or non-main-workflow targets as executable `run-to` targets.
- Do not add new Isomer CLI commands or runtime configuration.

## Decisions

1. `run-to` target execution is inclusive by default.

   Rationale: this matches ordinary operator language. If the user says "run to finalize", the skill should run `finalize` after satisfying its predecessors. The main alternative was to keep exclusion by default and document bare topic creation as `run-to finalize inclusive`; that keeps the surprising behavior and makes default dispatch depend on hidden modifier text.

2. Exclusive execution is controlled by explicit stop-before wording.

   The skill should treat phrases such as "before <target>", "stop before <target>", "excluding <target>", and "up to but not including <target>" as requests to stop after the target's predecessors. The alternative was to add a separate subcommand or flag-like syntax, but this skill is instruction-driven and should preserve natural-language operator routing.

3. Bare topic creation keeps routing to `run-to finalize`.

   With inclusive semantics, the default request "create this topic" can finish at `finalize` when the topic slug, semantic paths, mutation approval, and readiness prerequisites are available. Explicit modes still override the default: `fast-forward`, `step-by-step`, named procedural targets, `status`, and `repair` retain their current routing.

4. The readiness ladder remains the execution boundary.

   `run-to` still follows the same main workflow order as `fast-forward`; it does not jump directly to the target. Invalid targets, helper targets, missing inputs, and blocked predecessor steps should produce diagnostics instead of partial or guessed execution.

## Risks / Trade-offs

- More work can run from the same user wording than before. Mitigation: keep mutation approval and required-input gates unchanged, and document the exclusive stop-before phrases clearly.
- Existing tests and validators may still look for exclusion-by-default wording. Mitigation: update the operator validation expectation and unit tests in the same change.
- Agents may confuse `run-to finalize` with `fast-forward`. Mitigation: keep `fast-forward` documented as the explicit no-stop happy path, while `run-to` remains target-bounded and can still stop before a target when the user explicitly asks.
