# Runtime Model

## Purpose

This generated support document summarizes runtime boundaries for the `deepsci-mini` execplan.

## Contents

## Runtime Authority

Isomer Workspace Runtime is authoritative for Research Inquiries, Research Tasks, Runs, Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, and Provenance Records. Generated loop-local state is only compact adapter-side bookkeeping for handoff, payload, control, and recovery posture.

## Mail Runtime

Participant communication is mail-driven by default. Generated mail renderers include a `houmao-email-metadata` block, and generated on-event skills choose behavior by `schema_id`. Agents process one bounded event or tick and stop.

## Control Mode

`deepsci-mini` defaults to manual mode. Manual mode means the operator wakes participants for bounded passes; it is not paused. A future automatic mode requires topic policy, Gate policy, Scheduler Policy, and completion watcher refs.

## Recovery

Recovery starts by reading Workspace Runtime and loop-local handoff state. Raw mail and files are completion candidates until the lead normalizes them.
