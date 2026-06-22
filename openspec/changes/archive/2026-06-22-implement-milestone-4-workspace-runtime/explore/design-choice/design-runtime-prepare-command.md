# Runtime Prepare Command

## Context

Milestone 4 needs a mutating command that prepares and records selected Research Topic Pixi environment readiness before Milestone 5 Houmao launch work depends on it. `doctor` remains read-only, and `runtime init` only creates or reopens Workspace Runtime storage.

## Decision

Use `isomer-cli runtime prepare` as the explicit mutating readiness command.

## Rationale

`runtime prepare` sits with `runtime init`, `runtime inspect`, and `runtime validate`, so it keeps readiness mutation inside the Workspace Runtime command group. It also avoids blurring Project Manifest workspace discovery (`workspaces list`) with runtime mutation and keeps environment readiness at Topic Workspace scope rather than tying it to one Agent Team Instance too early.

## Implications

- `runtime prepare` records selected topic Pixi environment use, readiness status, readiness diagnostics, checked or prepared timestamp, actor ref when known, and Provenance refs.
- Readiness records use final-state statuses only in Milestone 4: `ready`, `failed`, `blocked`, `stale`, and `superseded`. Missing readiness is represented by no readiness record.
- `runtime prepare` requires an initialized current-schema Workspace Runtime.
- `runtime prepare` does not launch Houmao agents, create mailboxes or gateways, or materialize adapter launch dossiers.
- User-visible environment repair that goes beyond bounded readiness preparation remains Service Request work.
