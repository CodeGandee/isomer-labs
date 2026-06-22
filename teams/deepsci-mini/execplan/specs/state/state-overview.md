# State Overview

## Purpose

This generated state contract defines loop-local bookkeeping for `deepsci-mini`. It does not replace Isomer Workspace Runtime; it stores compact control facts that help generated skills and harness commands validate handoff, mail, and control posture.

## Authority

Workspace Runtime is authoritative for Research Topics, Research Inquiries, Research Tasks, Runs, Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, and Provenance Records. Loop-local state is adapter-side bookkeeping for generated mail payloads, control mode, participant identity, handoff ids, and recovery posture.

## Entity Families

- `participants`: generated role ids, role kind, and active posture.
- `handoffs`: request/result lifecycle keyed by handoff id.
- `payloads`: rendered or structured mail payload refs.
- `decisions`: compact loop-local Decision Record refs and Gate refs.
- `operator_intents`: requested pause, resume, manual step, stop, repair, or override events.

## Boundaries

State stores compact ids, refs, statuses, timestamps, and scalar decisions. Mail bodies, source summaries, literature notes, synthesis prose, and review notes belong in rendered mail or Isomer Artifacts.

## Invariants

- The root role is `deepsci-mini-lead`.
- Specialist handoff results return to `deepsci-mini-lead`.
- `manual` execution mode is not `paused`.
- A follow-up inquiry closeout requires a Gate ref and Decision Record ref.
- Candidate claims are not supported Research Claims without accepted Evidence Item refs.
