# State Overview

## Purpose

This generated state contract defines loop-local bookkeeping for a Houmao-backed `deepsci-org` execution package. It is not the Isomer Workspace Runtime. The Workspace Runtime at `{workspace_runtime_ref}` remains the durable research state authority for Research Inquiries, Research Tasks, Runs, Artifacts, Evidence Items, Findings, Research Claims, Gates, Decision Records, View Manifests, and Provenance Records.

## Backend

The selected backend is SQLite because the loop has stable entities, participant roles, handoffs, operator intent events, and control transitions. The schema lives in `schema.sql`, deterministic seed data lives in `seed.toml`, and validation checks live in `invariants.toml`.

## Entity Families

- `plan_metadata`: generated revision, source posture, template layer, and topology mode.
- `run_control`: run state, execution mode, selected topic profile, and active Gate or parking refs.
- `participants`: role templates and binding placeholders.
- `handoffs`: master-to-specialist handoff lifecycle facts.
- `mail_payloads`: payload ids, schema ids, mail refs, and processing status.
- `operator_intent_events`: pause, resume, stop, mode switch, redirect, Gate outcome, and recovery requests.
- `parking_packets`: compact blockers and resume instructions.

## Boundaries

This state stores compact refs, ids, statuses, timestamps, route facts, and audit facts. It does not store rich paper text, raw command output, credentials, provider payloads, external data, full mail bodies, or Workspace Runtime state.

## Scheduling Queries

- Which Run is active?
- Is the Run paused, stopped, completed, parked, or recovering?
- Which handoff is open for each role?
- Which handoff has a result that the master has not normalized?
- Which Gate or policy gap blocks progress?
- Which role can receive the next bounded handoff?

## Transition Rules

- `not_started -> running`: requires a valid `deepsci-org.email.team-start` payload.
- `running -> paused`: requires operator intent.
- `paused -> running`: requires operator intent and no blocking Gate.
- `running -> recovering`: requires inconsistency, stale state, or interrupted launch posture.
- `running -> parked`: requires a blocker, missing policy, stale state, contradiction, missing credential, missing capability, or unresolved Gate.
- `running -> completed`: requires closure packet refs and final Gate satisfaction when the active Gate Policy requires it.
- Any state -> `stopped`: requires operator intent and does not imply scientific completion.

## Active Ownership

The active Task Handler is queryable by `handoffs.receiver_role` and the Agent Instance refs supplied by the Topic Agent Team Profile or Agent Team Instance. The template records role ownership, but concrete Agent Instances remain topic-level runtime facts.
