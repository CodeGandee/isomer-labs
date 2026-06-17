# Manual Mode Uses Workspace Runtime Handoff Completion Authority

Manual mode lets the Operator Agent drive delegated Agent Instances directly and observe completion through inspection, file creation, channel messages, or adapter-specific signals. Isomer Labs will treat those observations as signal sources, but a delegated task is complete only after the Operator Agent records the handoff result, produced Artifact refs, and provenance in Workspace Runtime. This keeps manual execution auditable, recoverable, and consistent with the existing SQLite control-plane plus file Artifact model.

## Status

accepted

## Considered Options

- Treat Workspace Runtime handoff completion as authoritative.
- Treat a configured channel result as authoritative.
- Treat a declared file sentinel as authoritative.
- Let Operator Agent inspection alone close the task without a normalized handoff record.

## Consequences

- Manual mode can support multiple signal sources without making any one adapter, channel, or file convention part of Isomer's core completion semantics.
- The Operator Agent must normalize observed completion into Workspace Runtime handoff state before downstream stages, Gates, Research Claims, or View Manifests depend on the result.
- Recovery and validation can query Workspace Runtime for open, completed, failed, or stale handoffs instead of replaying live messages or rescanning arbitrary files.
