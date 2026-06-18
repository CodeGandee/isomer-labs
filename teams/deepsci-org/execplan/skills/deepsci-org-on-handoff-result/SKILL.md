---
name: deepsci-org-on-handoff-result
description: Generated on-event skill for master mail with schema_id deepsci-org.email.handoff-result.
---

# deepsci-org On Handoff Result

## Trigger

Use this skill only for an incoming mail body whose `houmao-email-metadata` block has `schema_id = "deepsci-org.email.handoff-result"`.

## Read First

- `../../specs/comms/templates.toml`
- `../../specs/comms/schemas/handoff-result.schema.json`
- `../../specs/collab/collab-overview.md`
- `../../specs/state/state-overview.md`
- `../../specs/state/invariants.toml`
- `deepsci-org-shared-template`

## Action

1. Confirm `receiver_role` is `deepsci-org-master`.
2. Validate that `handoff_id`, `sender_role`, `status`, `summary`, and `recommended_next_stage` are present.
3. Normalize the result into loop-local bookkeeping when the harness is available, then into `{workspace_runtime_ref}` through the approved Isomer recording surface.
4. Preserve Artifact refs, Evidence Item refs, Finding refs, Research Claim refs, Decision Record recommendations, Gate recommendations, caveats, and blockers.
5. If status is `needs_gate`, open or reference the required Gate through the Operator Agent path.
6. If status is `blocked`, `failed`, or `partial`, record a blocker or parking packet unless a safe next handoff is obvious and policy-covered.
7. If status is `completed`, call `deepsci-org-on-tick` for one bounded scheduling pass when no Gate blocks progress.
8. Stop after normalization and at most one follow-up tick.

## Boundary

Do not let a specialist result become authoritative research state until `deepsci-org-master` normalizes it into Workspace Runtime.
