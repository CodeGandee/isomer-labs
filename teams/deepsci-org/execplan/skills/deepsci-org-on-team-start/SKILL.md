---
name: deepsci-org-on-team-start
description: Generated on-event skill for mail with schema_id deepsci-org.email.team-start; wakes deepsci-org-master for one bounded start or resume pass.
---

# deepsci-org On Team Start

## Trigger

Use this skill only for an incoming mail body whose `houmao-email-metadata` block has `schema_id = "deepsci-org.email.team-start"`.

## Read First

- `../../specs/comms/templates.toml`
- `../../specs/comms/schemas/team-start.schema.json`
- `../../specs/collab/collab-overview.md`
- `../../specs/state/state-overview.md`
- `../../harness/commands.toml`

## Action

1. Confirm the metadata `schema_id`, `run_id`, `plan_revision`, `payload_id`, `{topic_agent_team_profile_id}`, and `{agent_team_instance_id}`.
2. Confirm this is a specialized topic profile context, not the raw Domain Agent Team Template being launched directly.
3. Check the generated control context with `../../harness/bin/deepsci-org control status --run-id <run-id>` when the harness is available.
4. Record or reference the Run start through the approved Workspace Runtime surface when that integration is available.
5. If no Gate or missing policy blocks progress, call `deepsci-org-on-tick` for one bounded scheduling pass.
6. Stop after the start or one follow-up tick. Do not wait in chat for later mail.

## Boundaries

Mailbox reading, archiving, replies, gateway posture, notifier posture, and agent prompting are maintained Houmao platform operations. This skill owns only loop-local event semantics.
