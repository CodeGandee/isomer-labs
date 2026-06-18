# Run Contract

## Purpose

This generated contract defines how a concrete `{run_id}` uses the `deepsci-org` Domain Agent Team Template after `{topic_agent_team_profile_id}` and `{agent_team_instance_id}` exist. It does not create a Run by itself.

## Required Run Inputs

- `{research_topic_id}`.
- `{research_inquiry_id}` when the task belongs to a Research Inquiry.
- `{research_task_id}`.
- `{run_id}`.
- `{topic_workspace_ref}`.
- `{workspace_runtime_ref}`.
- `{topic_agent_team_profile_id}`.
- `{agent_team_instance_id}`.
- `{coordination_policy_ref}`.
- Role-scoped Capability Binding refs and Skill Binding projection refs.
- Gate Policy refs for governed actions.
- Scheduler Policy refs when automatic mode is enabled.

## Expected Run Outputs

- Handoff records from `deepsci-org-master` to selected specialists.
- Specialist handoff results with Artifact refs, Evidence Item refs, Finding refs, Research Claim refs, caveats, blockers, and recommended next stage.
- Decision Record recommendations or final Decision Records when the master normalizes them.
- Gate recommendations or Gate outcomes when governed actions are involved.
- Parking packet or closure packet.

## Gate-Sensitive Actions

Credential use, paid or long compute, private data access, data export, external upload, destructive mutation, baseline waiver, publication-facing finality, and final completion require `{gate_policy_ref}` coverage. Automatic mode does not bypass Gates.

## Completion

`deepsci-org-master` may close the Run only after supported claims, limitations, recommendations, and final package refs are consolidated. Completion still requires explicit approval when the active Gate Policy requires it.

## Parking

Parking is valid when a blocker, stale state, contradiction, missing credential, missing policy, unresolved Gate, missing Capability Binding, missing Skill Binding projection, or missing Workspace Runtime ref prevents safe continuation. The parking packet must name last stable refs and the next safe operator action.
