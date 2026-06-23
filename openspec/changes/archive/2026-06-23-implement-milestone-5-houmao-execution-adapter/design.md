## Context

The recent adapter and CLI refactors changed the starting point for Milestone 5. Isomer now has modular CLI command packages, a CLI-backed Houmao adapter layer, launch material preparation, quick launch, live inspection, stop, JSON manifest reconciliation, and adoption. The remaining roadmap slice is not the first launch adapter; it is the manual handoff/control layer that sits above the existing Houmao lifecycle adapter.

The canonical language still keeps Houmao as an Execution Adapter implementation detail. Core Isomer records should keep provider-neutral names such as Execution Adapter ref, Agent Team Instance, Agent Instance, Run, handoff, Signal Observation, Artifact, and Provenance Record. Houmao-specific ids, project-profile paths, mailbox ids, gateway urls, notifier refs, managed-agent ids, session refs, and command payloads belong in opaque adapter payload refs or adapter-specific records, not in generic Project Manifest, Research Topic Config, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Run, handoff, or Artifact fields.

The local Houmao source checkout lives at `extern/orphan/houmao`. Isomer may use that checkout for live-gated validation, but defects discovered in Houmao should be fixed in the Houmao repository and validated with Houmao's own commands before the Isomer adapter relies on the fix.

## Goals / Non-Goals

**Goals:**

- Reuse the current modular implementation under `src/isomer_labs/cli/commands/`, `src/isomer_labs/houmao/`, and `src/isomer_labs/runtime/` without restoring removed compatibility shims.
- Add a top-level `handoffs` CLI group for manual dispatch, observation, and normalization of one Houmao-backed `deepsci-org` handoff round.
- Add provider-neutral runtime records or typed helpers for handoff dispatch, Signal Observations, normalization outcomes, adapter payload refs, Run linkage, Artifact refs, and Provenance refs.
- Extend the Houmao adapter facade with handoff dispatch, observation ingestion, and normalization helpers that use Houmao mail, gateway, file, or bounded inspection signals as adapter-scoped evidence.
- Keep existing `team-instances launch`, `launch-material prepare`, `inspect-live`, `stop`, `reconcile`, and `adopt` behavior as the launch foundation, and audit those surfaces only for gaps against current main specs.
- Add unit tests that mock Houmao and live-gated integration or manual tests that run only when the local Houmao build is available.

**Non-Goals:**

- Do not rebuild the already-implemented launch material, quick launch, inspect-live, stop, reconciliation, or adoption foundation unless an audit finds a gap.
- Do not implement automatic-mode scheduling, multi-team concurrent launch, task-level fanout launch, GUI rendering, service-team launch, or full UC-01 research completion.
- Do not make Houmao terms first-class Isomer domain fields, schema names, or generic CLI labels.
- Do not copy or vendor Houmao source into Isomer, and do not commit `extern/orphan/houmao` state.
- Do not hide environment repair inside launch or handoff dispatch; failed preflight should direct setup work through Service Requests or explicit Houmao checkout fixes.

## Decisions

### Decision 1: Current package boundaries are authoritative

Implement this slice inside the current package structure. CLI behavior belongs in modular command files under `src/isomer_labs/cli/commands/`, Houmao-specific behavior belongs under `src/isomer_labs/houmao/`, runtime models and stores belong under `src/isomer_labs/runtime/`, and shared JSON/text output must flow through the existing CLI output helpers. New code must not recreate removed flat modules such as `houmao_cli_adapter.py`, `houmao_manifests.py`, `runtime_store.py`, `runtime_validation.py`, or a monolithic `cli.py`.

Alternative considered: keep the original design's flat-module names as illustrative examples. That would preserve stale guidance and increase the chance that implementation reintroduces compatibility shims removed by the recent cleanup.

### Decision 2: Existing lifecycle adapter is a dependency, not new scope

The existing Houmao CLI-backed adapter layer remains responsible for materialization, quick launch, inspect-live, stop, manifest reconciliation, and adoption. This change should add missing handoff/control behavior and include an audit task for current lifecycle commands rather than duplicating implementation tasks that are already done.

Alternative considered: leave launch, inspect, stop, and manifest tasks in this change as unchecked work. That would overstate the remaining scope and make the implementation pass spend time retreading archived changes.

### Decision 3: Opaque adapter refs and provider-neutral handoff records

Store Houmao-specific mailbox refs, gateway refs, managed-agent refs, message ids, session refs, command outputs, and payload paths in adapter-specific records or opaque payload refs. Generic records may link to `execution-adapter:houmao` and adapter payload refs, but they must not add generic fields such as `houmao_managed_agent_id`, `mailbox_id`, `gateway_url`, or `houmao_message_id`.

Alternative considered: add Houmao fields directly to handoff, Run, Agent Team Instance, or Agent Instance records. That would simplify the first backend but would leak implementation language into the core Isomer schema.

### Decision 4: Manual handoff normalization is the authority

The adapter may observe candidate completion through Houmao mail, gateway events, files, command output, or inspection snapshots, but only Operator Agent normalization can mark a handoff accepted and attach produced Artifact, Run, Finding, Evidence Item, Decision Record, or Provenance refs. Signal Observations remain durable evidence of possible completion, not completion authority.

Alternative considered: mark a handoff accepted as soon as a Houmao reply arrives. That would bypass the manual-mode control model and could incorrectly promote unreviewed text into accepted research state.

### Decision 5: Top-level handoffs CLI group

Expose manual handoff dispatch, observation, and normalization under a top-level `handoffs` command group: `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, and `isomer-cli handoffs normalize`. These commands should accept `--agent-team-instance` when the operation targets a launched or adopted Agent Team Instance, while the handoff record remains a first-class Workspace Runtime record linked to Run, Signal Observation, Artifact, and Provenance refs.

Alternative considered: expose handoff behavior under `team-instances handoff ...`. That would frame handoffs as only team lifecycle actions, even though handoffs are durable runtime records that can span Runs, Artifacts, observations, and normalization.

### Decision 6: Root-level print-json governs all commands

Handoff commands should use structured human-readable output by default and deterministic JSON only through the existing root switch: `isomer-cli --print-json handoffs ...`. Do not add command-local `--json` or `--format json` flags.

Alternative considered: add handoff-specific JSON flags for convenience. That would conflict with the recently established CLI shape and make output tests inconsistent across commands.

### Decision 7: Live Houmao tests are capability-gated

Unit tests should mock the Houmao adapter boundary and prove records, command output, validation, side effects, and failure behavior. Live integration or manual tests should report skipped or unavailable status unless `extern/orphan/houmao` exists and the required read-only Houmao capability checks pass.

Alternative considered: require a live Houmao launch and handoff round in the default test suite. That would make local development brittle and blur the repository boundary when Houmao is absent or mid-change.

## Risks / Trade-offs

- [Risk] Handoff logic could duplicate lifecycle launch code. Mitigation: route handoff commands through the existing adapter facade and existing runtime store helpers wherever possible.
- [Risk] Adapter observation content can be mistaken for accepted research output. Mitigation: store observations as Signal Observations and require explicit normalization before changing handoff or Run terminal state.
- [Risk] Runtime records can drift into a second adapter database. Mitigation: store only the adapter refs, payload refs, observations, command summaries, and normalization links needed to map Houmao state back to generic Workspace Runtime records.
- [Risk] Houmao mail or gateway surfaces may drift. Mitigation: keep adapter parsing thin, gate live tests by capability checks, and document exact Houmao commands used by live validation.
- [Risk] Fixes needed in Houmao could be accidentally committed through Isomer. Mitigation: keep Houmao under `extern/orphan/`, document separate validation, and make Isomer tests report the Houmao checkout path and validation status rather than vendoring changes.

## Migration Plan

1. Audit existing launch, launch-material, inspect-live, stop, reconcile, and adopt commands against current main specs and record only real gaps as implementation work.
2. Add or extend runtime models, schema, store helpers, and validation for handoff dispatch records, Signal Observations, normalization outcomes, adapter payload refs, and adapter-linked Provenance refs.
3. Extend `src/isomer_labs/houmao/adapter.py` and related Houmao package modules with dispatch, observe, and normalize operations that preserve provider-neutral outputs.
4. Add `src/isomer_labs/cli/commands/handoffs.py` and register the top-level `handoffs` command group through the modular CLI app.
5. Add mocked unit tests for text output, `--print-json` output, failed preflight, dispatch, observation ingestion, accepted normalization, rejected normalization, and no Houmao-field leakage in generic records.
6. Add a live-gated integration or manual test that uses the existing launch foundation, dispatches one handoff, observes a Houmao mail or gateway result, normalizes it, and stops or reports cleanup state.
7. Update README and ROADMAP notes after implementation and validation pass.

Rollback is data-preserving: failed dispatches, rejected observations, normalization records, and stopped or stale adapter records remain visible in Workspace Runtime. If a migration changes schema shape, mutating commands must reject unsupported runtime schema versions before dispatching handoffs or changing normalization state.

## Open Questions

None.
