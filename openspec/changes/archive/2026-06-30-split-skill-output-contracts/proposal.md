## Why

Current skill output contracts often read like internal state dumps. They mix user-facing status, operator handoff fields, and audit/debug bookkeeping, so default chat output loses focus on what the user needs to understand: what happened, what is ready, what changed, what is blocked, and what to do next.

## What Changes

- Add a shared skill output contract convention that splits reportable fields into **Essential Output** and **Complete Output**.
- Make **Essential Output** the default chat output for skills outside `skillset/research-paradigm/`.
- Allow users to request **Complete Output** with explicit wording such as complete, verbose, audit, debug, full handoff, JSON, or full output.
- Revise large service and operator skill contracts so user-facing essentials stay focused, while semantic path diagnostics, storage profiles, provenance refs, full command logs, matrices, and detailed evidence move to complete output.
- Keep subcommand reference pages compatible by having them report through the parent essential/complete output mode unless they already define a small local output contract.

## Capabilities

### New Capabilities
- `skill-output-contracts`: Shared requirements for user-friendly skill reporting with essential-by-default and complete-on-request output contracts.

### Modified Capabilities
- `isomer-service-env-setup-skill`: Topic env setup output contract must split essential user output from complete handoff/audit fields.
- `isomer-agent-env-setup-service-skill`: Agent env setup output contract must split essential user output from complete per-agent handoff/audit fields.
- `topic-team-specialization-module-skill`: Topic team specialization output contract must split essential user output from complete specialization, environment, and workspace evidence.
- `topic-workspace-manager-skill`: Topic workspace manager output contract must split essential topology output from complete semantic path and worktree evidence.
- `isomer-admin-project-manager-skill`: Project manager output contract must split essential lifecycle output from complete Project, cleanup, relocation, and runtime bookkeeping.

## Impact

- Affects `skillset/operator/*`, `skillset/service/*`, `skillset/misc/*`, and `skillset/skill-creator`, excluding `skillset/research-paradigm/*`.
- Affects validator expectations in `scripts/validate_skillsets.py` and related unit fixtures in `tests/unit/test_validate_skillsets.py`.
- Affects OpenSpec specs for the listed skill capabilities.
- No runtime dependency changes are expected.
