## Why

Kaoju currently treats several direction, reading-list, planning, comparison, trial-plan, and paper-review checkpoints as unconditional new human turns, even when the user's prompt explicitly delegates those reviews to the agent. Human review should remain the safe default, while explicit prompt-scoped automation should let a bounded workflow continue without redundant confirmation.

## What Changes

- Resolve a Kaoju review mode from the current prompt: `human` when the prompt is silent and `agent` only when the prompt explicitly delegates the applicable review or acceptance.
- Let explicit prompt-scoped automation cover review checkpoints for explore handoff, direction selection, reading-list acceptance, paper structure and draft acceptance, empirical-comparison intent, bounded trial plans, and local paper-build authorization.
- Require automated review to preserve the user's target, accepted evidence, resource boundary, validation rules, rationale, decision provenance, and exact resume semantics.
- Keep audit boundaries, evidence acceptance rules, invalid-state rejection, and owner-specific validation unchanged.
- Keep credentials, private or restricted data, material license decisions, destructive or irreversible actions, unexpected resource expansion, public network exposure, publication acceptance, external publication, and submission as nondelegable boundaries unless their existing owner receives the exact authorization its contract requires. Generic review automation or run-to wording does not waive them.
- Update packaged Kaoju skill guidance, project-scope installed skill projections, process documentation, and contract tests so the distinction between default human review and prompt-authorized agent review is consistent.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-research-extension`: Define prompt-resolved Kaoju review mode and distinguish automatable review checkpoints from nondelegable Gates.
- `kaoju-survey-intents`: Allow explicitly delegated agent review of Direction Sets and Reading Lists while retaining human review by default.
- `kaoju-explore-subskill`: Allow an explicit prompt to authorize automatic plan review and handoff without a second consent turn.
- `kaoju-code-execution`: Allow explicit prompt-scoped trial-plan review and execution authorization within pinned inputs, resources, and attempt bounds while preserving material-change and safety Gates.
- `kaoju-paper-production`: Allow explicit agent review of paper structure, draft, and bounded local build authorization while retaining the publication Gate and material-repair boundaries.
- `run-to-prerequisite-recovery`: Treat prompt-authorized review checkpoints as delegable within the named target closure while continuing to stop at genuinely nondelegable boundaries.

## Impact

The change affects the packaged Kaoju entrypoint, shared interaction and prerequisite-recovery references, focused explore, frame, discover, compare, trial, and write skills, their public command pages, the packaged Kaoju README, projected `.agents` skill copies, and skill-contract tests. It changes interaction policy and wording rather than artifact schemas or CLI service APIs.
