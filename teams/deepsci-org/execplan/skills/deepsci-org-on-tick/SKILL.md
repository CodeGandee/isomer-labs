---
name: deepsci-org-on-tick
description: Generated bounded tick skill for deepsci-org scheduling, recovery, completion, and manual-step decisions.
---

# deepsci-org On Tick

## Trigger

Use this skill after processing a generated mail event, or when the Project-facing Operator Agent asks `deepsci-org-master` to perform one bounded manual step.

## Read First

- `../../specs/collab/collab-overview.md`
- `../../specs/collab/topology/topology.toml`
- `../../specs/participants/participants.toml`
- `../../specs/state/state-overview.md`
- `../../specs/run/run-contract.md`
- `../../harness/commands.toml`

## Action

1. Query control status, current Run refs, open handoffs, open Gates, and parking posture from the harness or Workspace Runtime.
2. If run state is `paused`, `stopped`, `completed`, or blocked by an unresolved Gate, record the reason and stop.
3. If recovery is needed, perform one bounded recovery action: identify the last stable refs, current open mail or handoff, missing readiness fact, or inconsistent state.
4. If a safe next handoff exists, render one `deepsci-org.email.handoff-request` for the selected specialist.
5. If no safe next handoff exists, record a parking packet with blocker reason and next safe operator action.
6. If closure criteria are satisfied, record a closure packet with supported claims, limitations, recommendations, final package refs, and final Gate posture.
7. Stop after one scheduling, recovery, parking, or closure pass.

## Mode Rule

Manual mode means the Operator Agent wakes one bounded participant turn. Automatic mode means notifier prompts may wake participants according to topic policy. Neither mode permits in-chat waiting.
