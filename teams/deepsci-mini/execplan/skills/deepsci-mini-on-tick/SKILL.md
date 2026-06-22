---
name: deepsci-mini-on-tick
description: Generated bounded tick skill for deepsci-mini scheduling, recovery, completion, and manual-step decisions.
---

# deepsci-mini On Tick

## Trigger

Use this skill only after a team-start event, accepted handoff result, or operator prompt asks for one bounded `deepsci-mini` scheduling pass.

## Read First

- `../../specs/collab/collab-overview.md`
- `../../specs/collab/topology/topology.toml`
- `../../specs/state/state-overview.md`
- `../../specs/state/invariants.toml`
- `../../harness/commands.toml`
- `deepsci-mini-shared-template`

## Action

1. Query or reconstruct current run state, execution mode, open handoffs, accepted scout refs, accepted synthesis-review refs, and Gate state.
2. If execution mode is manual, choose at most one safe next action and stop after that action is described or dispatched.
3. If a handoff is open, do not dispatch another dependent handoff.
4. If scout output is missing, route one handoff to `deepsci-mini-scout`.
5. If scout output is accepted and synthesis-review output is missing, route one handoff to `deepsci-mini-synth-reviewer`.
6. If synthesis-review output is accepted and no closeout Gate exists, open or request the follow-up Research Inquiry Gate.
7. If the Gate is resolved, record or verify the selected follow-up Research Inquiry and Decision Record.
8. If state is inconsistent, stale, blocked, or unsupported, park the run with a recovery note instead of advancing.
9. Stop after one bounded pass.
