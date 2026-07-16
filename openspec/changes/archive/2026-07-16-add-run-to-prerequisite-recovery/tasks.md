## 1. Core Prerequisite-Recovery Guidance

- [x] 1.1 Add a directly linked operator reference that defines conservative prerequisite preflight, the recovery-choice prompt, inclusive target-scoped run-to authorization, and nondelegable stop boundaries without using generic troubleshooting as the primary contract.
- [x] 1.2 Update the numbered `isomer-op-entrypoint/SKILL.md` workflow to check prerequisites, pause on producible gaps, route the user's recovery choice, use the native planning tool after run-to authorization, coordinate owner routes, and resume the original target.
- [x] 1.3 Update the entrypoint routing and output references so ordinary requests retain one initial owner route while authorized run-to traversal can cross owners without transferring their mutation authority.
- [x] 1.4 Ensure entrypoint guidance classifies producible missing inputs as `paused` recovery and reserves `blocked` for unavailable external state changes.

## 2. Kaoju Run-To Integration

- [x] 2.1 Add the run-to interaction contract to `isomer-kaoju-shared`, including target-scoped authorization, routine transitive dependency handling, Gate preservation, and controller-versus-procedure boundaries.
- [x] 2.2 Revise Kaoju interaction, terminal-report, and owner-routing references so bounded procedures still return terminal reports while an authorized prompt-level controller may consume their recovery routes.
- [x] 2.3 Update the numbered `isomer-kaoju-pipeline/SKILL.md` workflow to check prerequisites, present recovery choices before prerequisite mutation, and maintain an internal dependency plan only after explicit run-to authorization.
- [x] 2.4 Audit Kaoju command pages for missing-prerequisite and unconditional-stop language; keep predecessor checks in numbered workflows, classify known producer gaps as paused recovery, and qualify macro-stop rules without weakening audit, evidence, or Gate requirements.
- [x] 2.5 Update Kaoju README or help guidance with a PDF-oriented example that distinguishes ordinary pause, run-to recovery, separate procedure Runs, and publication Gates.

## 3. DeepSci Run-To Integration

- [x] 3.1 Add the run-to controller contract to `isomer-deepsci-shared` coordination guidance while preserving latest-context preflight, worker-output policy, callbacks, placeholder bindings, and focused-skill ownership.
- [x] 3.2 Update the numbered `isomer-deepsci-pipeline/SKILL.md` workflow to check prerequisites, keep recipes single-pass, and allow the current agent to act as their external controller after explicit target-scoped run-to authorization.
- [x] 3.3 Revise DeepSci transition rules and terminal-report guidance so a known producible input yields paused recovery and an authorized controller can consume recommended routes without adding loops to a recipe or relying on generic troubleshooting.
- [x] 3.4 Audit DeepSci pass pages for external-controller and stop wording; keep predecessor checks in numbered workflows and qualify controller handoff for authorized run-to traversal while preserving separate terminal reports and nondelegable Gates.

## 4. User Documentation

- [x] 4.1 Update the human-steered research-pass tutorial with the default missing-prerequisite prompt and all four semantic choices: run to target, next prerequisite only, alternate route, and stop.
- [x] 4.2 Update the paper-writing tutorial with an end-to-end run-to example that performs audit, repair, synthesis, drafting, and local PDF construction only as required by current state.
- [x] 4.3 Update tutorial index, quickstart, and related user-facing system-skill guidance so run-to is described as prompt-scoped prerequisite recovery rather than a CLI command, global yes-to-all flag, or Run-level Control Mode.
- [x] 4.4 Verify documentation examples show run-to pausing at human Gates, material choices, destructive actions, unexpected resource boundaries, and publication or external side effects.

## 5. Validation and Tests

- [x] 5.1 Extend operator skill validation to require conservative prerequisite preflight, recovery choices, target-scoped run-to planning, owner-boundary preservation, and nondelegable stop language in the entrypoint's numbered workflow and linked reference.
- [x] 5.2 Extend research-paradigm skill validation to require consistent run-to controller semantics in the numbered Kaoju and DeepSci pipeline workflows and linked shared guidance and to reject troubleshooting-only, unqualified always-automate, or never-chain wording.
- [x] 5.3 Add positive operator validation fixtures for ordinary prerequisite pause and authorized cross-owner run-to completion.
- [x] 5.4 Add positive Kaoju and DeepSci validation fixtures for bounded terminal reports consumed by an authorized controller, plus paused-versus-blocked dependency classification.
- [x] 5.5 Add negative fixtures for troubleshooting-only prerequisite handling, implicit automation from `do <task>`, global or session-wide yes-to-all, merged prerequisite Runs, skipped Gates, and continuation after the named target.

## 6. Verification

- [x] 6.1 Run focused operator and research-paradigm validator unit tests and fix all run-to contract diagnostics.
- [x] 6.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` from the repository root.
- [x] 6.3 Run `openspec validate add-run-to-prerequisite-recovery --type change --strict --no-interactive` and confirm the change remains apply-ready.
