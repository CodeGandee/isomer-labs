# Runtime Model

## Purpose

This file explains generated runtime assumptions and operation boundaries.

## Model

Houmao agents do not run an always-awake in-chat loop. Mail notifier support wakes an agent with a prompt when open mail is available. A generated on-event skill handles one mail event, an on-tick skill may perform one bounded scheduling or recovery pass, and the agent stops the chat turn.

## Mail

Participant handoffs use schema-typed rendered Markdown mail. The parseable `houmao-email-metadata` block identifies `schema_id`, `run_id`, `plan_revision`, `payload_id`, and handoff or route refs. The generated package defines mail semantics; maintained Houmao skills own mail send, read, reply, archive, gateway, and notifier mechanics.

## State

Loop-local state is compact bookkeeping. It stores ids, refs, statuses, control state, handoff lifecycle facts, payload refs, operator intent events, and parking packets. Workspace Runtime remains the authoritative research state for Research Tasks, Runs, Artifacts, Evidence Items, Findings, Research Claims, Gates, Decision Records, View Manifests, and Provenance Records.

## Topology

The topology mode is `tree-loop`. `deepsci-org-master` is the internal root role and only default dispatcher. Specialist results return to the master. Specialist-to-specialist dispatch requires explicit authority in the Topic Agent Team Profile.
