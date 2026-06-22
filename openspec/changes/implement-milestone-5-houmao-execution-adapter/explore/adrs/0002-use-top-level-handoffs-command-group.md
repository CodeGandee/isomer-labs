# Use a Top-Level Handoffs Command Group

Milestone 5 needs user-facing commands for manual handoff dispatch, observation, and Operator Agent normalization. Isomer will expose those commands under a top-level `handoffs` group because handoffs are first-class Workspace Runtime records linked to Agent Team Instances, Runs, Signal Observations, Artifacts, and Provenance Records rather than subcommands of team lifecycle only.

## Status

accepted

## Considered Options

- `team-instances handoff ...`.
- Top-level `handoffs ...`.
- Adapter-specific hidden or test-only command.

## Consequences

Milestone 5 should add command paths such as `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, and `isomer-cli handoffs normalize`, with `--agent-team-instance` used when the operation targets a launched Agent Team Instance. Public CLI tests and docs should treat handoffs as Workspace Runtime records while preserving links back to the selected Agent Team Instance.
