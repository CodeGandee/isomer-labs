## Why

Milestone 2 and 3 now have a first implementation, but they still need a completion pass before the roadmap can truthfully mark them done. The current code proves the main flow; this change turns it into a durable milestone boundary with repo fixtures, stronger negative validation, clearer profile-writing semantics, and roadmap-grade verification.

## What Changes

- Harden Domain Agent Team Template validation beyond the built-in happy path by adding custom project-local template fixtures, missing-artifact fixtures, concrete-topic/runtime leakage fixtures, and deterministic diagnostics for each failure class.
- Materialize UC-01, UC-02, UC-03, and UC-05 Topic Agent Team Profile fixtures as project files instead of only test helper strings, then validate those fixtures through the public CLI.
- Clarify and implement the design-time profile output contract: `team-profiles specialize` previews by default, `--write` writes only the profile file, and any manifest/config registration behavior must be explicit rather than implicit.
- Extend profile validation coverage for cross-topic Agent Workspace refs, duplicate profile ids regardless of status, missing required role bindings, missing fanout policy, automatic-mode policy refs, reviewer read-access policy, runtime truth, launch refs, Houmao refs, and secret-like fields.
- Update developer docs and ROADMAP milestone checkboxes once the validation suite proves Milestone 2 and 3 exit criteria.
- Preserve the boundary that Houmao launch, mailbox, gateway, managed-agent, and Agent Team Instance state remain out of scope for Milestone 2 and 3.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `domain-agent-team-template-registration`: Add completion requirements for project-local template fixtures, stronger template-boundary diagnostics, custom-template validation coverage, and roadmap-ready verification.
- `topic-agent-team-profile-specialization`: Add completion requirements for static fixture Projects, profile write/register semantics, use-case fixture validation, duplicate profile id rejection, and stronger negative validation.
- `isomer-cli-project-discovery`: Clarify command-surface behavior for `team-profiles specialize --write`, deterministic fixture validation output, and milestone completion documentation.

## Impact

- Affected code: `src/isomer_labs/team_templates.py`, `src/isomer_labs/team_profiles.py`, `src/isomer_labs/validation.py`, `src/isomer_labs/cli.py`, models and parsing helpers where needed.
- Affected tests and fixtures: add reusable fixture Projects under `tests/fixtures/`, update unit tests to load fixture files, and keep existing temporary-project tests for focused negative cases.
- Affected docs: `README.md`, `CLAUDE.md`, `ROADMAP.md`, and OpenSpec specs for the three modified capabilities.
- Affected systems: no live Houmao launch, Workspace Runtime creation, Agent Team Instance creation, mailbox, gateway, or adapter state is introduced by this change.
