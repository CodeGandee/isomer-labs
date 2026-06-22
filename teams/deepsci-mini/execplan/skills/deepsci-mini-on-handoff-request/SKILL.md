---
name: deepsci-mini-on-handoff-request
description: Generated on-event skill for specialist mail with schema_id deepsci-mini.email.handoff-request.
---

# deepsci-mini On Handoff Request

## Trigger

Use this skill only for an incoming mail body whose `houmao-email-metadata` block has `schema_id = "deepsci-mini.email.handoff-request"`.

## Read First

- `../../specs/comms/templates.toml`
- `../../specs/comms/schemas/handoff-request.schema.json`
- `../../specs/collab/topology/topology.toml`
- `../../specs/participants/participants.toml`
- `../../specs/run/run-contract.md`
- `deepsci-mini-shared-template`

## Action

1. Confirm `receiver_role` matches the current participant role.
2. Confirm `sender_role` is `deepsci-mini-lead`.
3. Treat the handoff as one bounded UC-01 Research Task or Research Task slice.
4. Use the role's Skill Binding projection and Capability Binding refs from the topic profile. Do not assume concrete tools that the topic profile did not bind.
5. Produce or update Agent Artifacts only inside the role's Agent Workspace. Promote durable dependencies through approved Isomer recording surfaces.
6. For `deepsci-mini-scout`, return source summaries, literature notes, claim candidates, Evidence Item candidates, caveats, blockers, and recommended synthesis focus.
7. For `deepsci-mini-synth-reviewer`, return factor clusters, inquiry options, weak-claim notes, review notes, accepted or rejected evidence posture, caveats, blockers, and Gate recommendations.
8. Return one `deepsci-mini.email.handoff-result` to `deepsci-mini-lead`.
9. Stop after one bounded pass. Do not sleep, poll, tail logs, or wait in chat.

## Result Rule

Normal results return to `deepsci-mini-lead`. Specialists may recommend another route, but the lead issues the next handoff unless future topic policy explicitly grants otherwise.
