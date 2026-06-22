## 1. Existing Adapter Foundation Audit

- [x] 1.1 Audit current `team-instances launch`, `launch-material prepare`, `inspect-live`, `stop`, `reconcile`, and `adopt` behavior against the current main specs before adding handoff behavior.
- [x] 1.2 Record only real gaps from the audit as implementation subtasks; do not rebuild already-passing launch material, quick launch, inspect-live, stop, manifest reconciliation, or adoption behavior.
- [x] 1.3 Confirm new work uses current modules under `src/isomer_labs/cli/commands/`, `src/isomer_labs/houmao/`, and `src/isomer_labs/runtime/` and does not restore removed compatibility shims.
- [x] 1.4 Confirm all new JSON output uses root-level `isomer-cli --print-json ...` through existing CLI output helpers and does not add command-local JSON flags.

## 2. Runtime Handoff and Observation Records

- [x] 2.1 Add or extend runtime models, schema, rows, and store helpers for handoff dispatch records, Signal Observations, normalization outcomes, adapter payload refs, adapter command refs, and adapter-linked Provenance refs.
- [x] 2.2 Add Run creation or lookup helpers for the first manual handoff round under a launched or adopted Agent Team Instance.
- [x] 2.3 Add serialization helpers that keep Houmao mailbox ids, gateway event ids, message ids, managed-agent ids, session refs, and command payload refs inside adapter payload JSON or adapter tables.
- [x] 2.4 Add schema-version handling so unsupported Workspace Runtime schema versions are rejected before handoff dispatch, observation ingestion, or normalization mutation.
- [x] 2.5 Extend runtime validation for missing adapter refs, stale handoffs, missing durable handoff payload files, broken Signal Observation refs, unresolved Gates, and cross-topic adapter leakage.

## 3. Houmao Handoff Adapter

- [x] 3.1 Extend `src/isomer_labs/houmao/adapter.py` or focused Houmao package modules with `dispatch_handoff`, `observe_handoff`, and `normalize_handoff` operations.
- [x] 3.2 Implement handoff dispatch from `deepsci-org-master` to one selected specialist Agent Instance through Houmao mail or gateway surfaces.
- [x] 3.3 Implement observation ingestion for Houmao mail replies, gateway events, file observations, command payloads, and bounded inspection output as Signal Observations.
- [x] 3.4 Implement Operator Agent normalization that can accept a candidate handoff result and record accepted handoff state, Run updates, output Artifact refs, rationale, and Provenance refs.
- [x] 3.5 Implement rejection, blocked, superseded, repair, and follow-up routing that keeps observations visible and records rationale plus corrective Service Request or handoff refs when present.
- [x] 3.6 Add preflight diagnostics for missing Houmao checkout, unavailable mail or gateway capability, invalid Agent Instance mapping, unresolved Gate, missing recording obligations, and unavailable runtime readiness.

## 4. Handoffs CLI Surface

- [x] 4.1 Add a top-level `isomer-cli handoffs` command group in the modular CLI command package and register it from the CLI app.
- [x] 4.2 Add `isomer-cli handoffs dispatch` with Project selectors, topic selectors, Agent Team Instance selector, source and target Agent Instance selectors, Run or Research Task refs, expected output refs, structured text output, deterministic `--print-json` output, and explicit mutation reporting.
- [x] 4.3 Add `isomer-cli handoffs observe` with selectors for handoff, Run, Agent Team Instance, observation source, adapter payload refs, structured text output, deterministic `--print-json` output, and non-authoritative observation reporting.
- [x] 4.4 Add `isomer-cli handoffs normalize` with accepted, rejected, blocked, superseded, repair, and follow-up outcomes, rationale capture, output Artifact refs, structured text output, deterministic `--print-json` output, and explicit mutation reporting.
- [x] 4.5 Update root help, handoff command help, and command-surface tests so `handoffs` is discoverable and the commands do not advertise `--json`, `--format json`, or `--format=json`.

## 5. Tests

- [x] 5.1 Add mocked unit tests for dispatch preflight failure with no Houmao mail, gateway mutation, accepted handoff state, or Run completion.
- [x] 5.2 Add mocked unit tests for successful dispatch, persisted handoff refs, adapter payload refs, command refs, Run linkage, and Provenance refs.
- [x] 5.3 Add mocked unit tests for observation ingestion from mail, gateway, file, and inspection-like payloads as Signal Observations.
- [x] 5.4 Add mocked unit tests proving adapter observations alone do not mark handoffs or Runs complete and do not promote returned claims into Evidence Items.
- [x] 5.5 Add mocked unit tests for accepted normalization, rejected normalization, repair routing, stale handoff validation, restart recovery, and no-Houmao-field leakage in generic output.
- [x] 5.6 Add CLI tests for structured text output and root-level `--print-json` output for `handoffs dispatch`, `handoffs observe`, and `handoffs normalize`.

## 6. Houmao Repository Boundary and Live Validation

- [x] 6.1 Add or update a live-test capability check that reports Houmao checkout path, read-only capability-gate results, and skipped or unavailable status before mutation.
- [x] 6.2 Add a live-gated integration or manual test that uses the existing launch foundation, dispatches one handoff, observes a Houmao mail or gateway result, normalizes it into Workspace Runtime, and stops or reports cleanup state.
- [x] 6.3 Document the read-only Houmao capability-gate commands, optional live/manual validation commands, and the rule that Houmao defects are fixed in the Houmao repository before Isomer depends on them.
- [x] 6.4 Add safeguards so Isomer tests do not write into or commit `extern/orphan/houmao` except through explicit separate Houmao work.

## 7. Documentation and Roadmap

- [x] 7.1 Update README command examples and narrative for `handoffs dispatch`, `handoffs observe`, `handoffs normalize`, root-level `--print-json`, and live-test availability.
- [x] 7.2 Update developer notes for adapter record boundaries, opaque Houmao refs, local Houmao build expectations, Signal Observation authority, and no-Houmao-term generic schema policy.
- [x] 7.3 Update troubleshooting notes for failed handoff preflight, missing readiness, missing Houmao checkout, missing mail or gateway capability, stale handoff, rejected result, and repair routing.
- [x] 7.4 Update ROADMAP.md Milestone 5 checklist only after implementation and validation are complete.

## 8. Verification

- [x] 8.1 Run `openspec validate implement-milestone-5-houmao-execution-adapter --strict` after spec edits.
- [x] 8.2 Run `openspec validate --all` after implementation.
- [x] 8.3 Run `pixi run lint`.
- [x] 8.4 Run `pixi run typecheck`.
- [x] 8.5 Run `pixi run test`.
- [x] 8.6 Run `pixi run validate-research-skills`.
- [x] 8.7 Run the live-gated Houmao integration or manual test when the local Houmao checkout passes its own validation, and record skipped status otherwise. Skipped live mode because `ISOMER_MANUAL_LIVE_HOUMAO=1` was not set; fake manual mode passed.
