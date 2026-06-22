---
name: deepsci-mini-on-team-start
description: Generated on-event skill for lead mail with schema_id deepsci-mini.email.team-start.
---

# deepsci-mini On Team Start

## Trigger

Use this skill only for an incoming mail body whose `houmao-email-metadata` block has `schema_id = "deepsci-mini.email.team-start"`.

## Read First

- `../../specs/comms/templates.toml`
- `../../specs/comms/schemas/team-start.schema.json`
- `../../specs/collab/collab-overview.md`
- `../../specs/participants/participants.toml`
- `deepsci-mini-shared-template`

## Action

1. Confirm `receiver_role` is `deepsci-mini-lead`.
2. Recover `{research_topic_id}`, `{research_inquiry_id}`, and `{run_id}` from the message and Workspace Runtime context.
3. Decide whether the next bounded action is a scout handoff, a synthesis-review handoff, a Gate, closeout, or parking.
4. If required state is missing, record or report the missing refs instead of inventing them.
5. If scouting has not completed, prepare one `deepsci-mini.email.handoff-request` for `deepsci-mini-scout`.
6. If accepted scout output exists and synthesis-review has not completed, prepare one `deepsci-mini.email.handoff-request` for `deepsci-mini-synth-reviewer`.
7. If accepted synthesis-review output exists, open or reference the follow-up Research Inquiry Gate.
8. Stop after one bounded start or resume pass.
