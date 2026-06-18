# Validation

## Purpose

This file records validation instructions and known validation posture.

## Commands

Run the generated harness validation:

```bash
teams/deepsci-org/execplan/harness/bin/deepsci-org validate
```

Useful read-only checks:

```bash
teams/deepsci-org/execplan/harness/bin/deepsci-org query participants
teams/deepsci-org/execplan/harness/bin/deepsci-org query topology
teams/deepsci-org/execplan/harness/bin/deepsci-org query templates
teams/deepsci-org/execplan/harness/bin/deepsci-org control get-mode
teams/deepsci-org/execplan/harness/bin/deepsci-org instantiation placeholders
```

## Expected Posture

`validate-execplan` checks generated package shape and contracts only. It does not require concrete mailboxes, gateway posture, prepared Agent Profiles, live Agent Instances, workspace readiness, or launchability, because those are later `prepare-agents`, `prepare-workspace`, `validate-loop`, `launch-agents`, and `start` concerns.

## Known Omission

`execplan/adrs/` is omitted because this was a non-interactive fast-forward generation with no execplan-local accepted decisions.
