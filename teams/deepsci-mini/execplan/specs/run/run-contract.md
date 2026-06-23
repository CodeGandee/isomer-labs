# Run Contract

## Purpose

This generated run contract defines the expected shape of a bounded `deepsci-mini` UC-01 run. It does not launch agents or mutate Workspace Runtime by itself.

## Required Inputs

- `{research_topic_id}`.
- `{research_inquiry_id}`.
- `{research_task_id}`.
- `{run_id}`.
- `{topic_agent_team_profile_bundle_ref}`.
- `{topic_agent_team_profile_id}` when emitted as derived runtime metadata.
- `{agent_team_instance_id}`.
- `{workspace_runtime_ref}`.
- `{gate_policy_ref}`.

## Handoff Sequence

1. `deepsci-mini-lead` receives a team-start request or Operator Agent prompt.
2. `deepsci-mini-lead` sends one scout handoff to `deepsci-mini-scout`.
3. `deepsci-mini-scout` returns one handoff result.
4. `deepsci-mini-lead` normalizes accepted scout output.
5. `deepsci-mini-lead` sends one synthesis-review handoff to `deepsci-mini-synth-reviewer`.
6. `deepsci-mini-synth-reviewer` returns one handoff result.
7. `deepsci-mini-lead` normalizes accepted synthesis-review output.
8. `deepsci-mini-lead` opens or references the follow-up Research Inquiry Gate.
9. The Operator Agent records the selected inquiry and rationale as a Decision Record.

## Expected Outputs

- Source summary Artifact refs.
- Literature note Artifact refs.
- Claim candidate refs.
- Evidence Item refs or candidates.
- Synthesis note refs.
- Review note refs.
- View Manifest refs for literature matrix, claim graph, and inquiry comparison.
- Follow-up Research Inquiry Gate ref.
- Decision Record ref.
- Provenance Record refs.

## Stop Conditions

- Stop at any Gate that requires human selection.
- Stop when required source, evidence, or synthesis refs are missing.
- Stop when a handoff result is blocked, failed, stale, or outside scope.
- Stop when candidate claims would be strengthened without accepted Evidence Item refs.
- Stop when live Houmao readiness is absent and the run was requested in live mode.

## Recovery

Recovery reads existing Workspace Runtime refs and loop-local handoff state. It must not replay raw mail as authoritative research state without lead normalization.
