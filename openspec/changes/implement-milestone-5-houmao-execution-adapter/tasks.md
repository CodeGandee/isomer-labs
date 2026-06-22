## 1. Adapter Record Foundation

- [ ] 1.1 Add Houmao adapter dataclasses for adapter availability, preflight result, launch material plan, launch attempt, adapter ref mapping, inspection snapshot, stop outcome, dispatch result, Signal Observation, and normalization result.
- [ ] 1.2 Add Workspace Runtime tables or typed store helpers for opaque Execution Adapter refs, adapter payload refs, launch attempts, inspection snapshots, stop outcomes, dispatch records, Signal Observations, and adapter-linked Provenance refs.
- [ ] 1.3 Add migration or schema-version handling so Milestone 5 runtime records are rejected on unsupported Workspace Runtime schema versions before any live adapter mutation.
- [ ] 1.4 Add serialization helpers that keep Houmao-specific ids inside adapter payload JSON or adapter tables and out of generic Agent Team Instance, Agent Instance, Run, handoff, and Artifact fields.
- [ ] 1.5 Add validation helpers for adapter record ownership, missing adapter refs, stale launch state, missing launch material paths, and cross-topic adapter leakage.

## 2. Local Houmao Checkout and Preflight

- [ ] 2.1 Add Houmao checkout resolution for `extern/orphan/houmao` plus a documented local override for tests or operator runs.
- [ ] 2.2 Add preflight checks for current Workspace Runtime schema, initialized runtime, ready Topic Environment Readiness, selected Agent Team Instance, validated Topic Agent Team Profile, Agent Instance records, Agent Workspace directories, and path plans.
- [ ] 2.3 Add the read-only Houmao capability gate: resolve checkout path, verify `tmux -V`, run `pixi run houmao-mgr --version`, run `pixi run houmao-mgr --print-json system-skills list`, run `pixi run houmao-mgr --print-json project --project-dir <project> status`, and run `pixi run houmao-mgr --print-json agents global list`.
- [ ] 2.4 Add deterministic diagnostics for missing Houmao checkout, missing Houmao command/API capability, invalid launch material inputs, unresolved Gates, missing recording obligations, and unavailable environment readiness.
- [ ] 2.5 Add tests proving failed preflight does not create launch material, start Houmao agents, send handoffs, or mark launch state active.

## 3. Launch Material Generation

- [ ] 3.1 Add a launch-material builder that reads `teams/deepsci-org/execplan/agents/`, generated skills, notifier prompts, topology, communication templates, and Topic Agent Team Profile role bindings.
- [ ] 3.2 Add path-plan creation for adapter launch-material root, per-agent launch material, notifier prompt copies, mailbox metadata, gateway metadata, and adapter logs before files are written.
- [ ] 3.3 Generate per-Agent Instance launch material under the corresponding Agent Workspace or recorded Agent Workspace path plan.
- [ ] 3.4 Generate or select Houmao project-profile launch material for the public `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>` path.
- [ ] 3.5 Record launch material refs and Provenance refs in Workspace Runtime without writing to `.isomer-labs/` or the Houmao checkout, and do not classify any Milestone 5 adapter launch material as cache-like.
- [ ] 3.6 Add validation that rejects launch material paths outside the Project root or selected Topic Workspace unless a future accepted external-root contract permits them.
- [ ] 3.7 Add tests for launch-material determinism, topic scoping, missing template inputs, path-plan source detail, and absence of workspace-local `teams/` output.

## 4. Houmao Launch Inspect Stop Adapter

- [ ] 4.1 Implement a Houmao adapter facade with `preflight`, `materialize`, `launch`, `inspect`, `stop`, `dispatch_handoff`, `observe`, and `normalize` methods.
- [ ] 4.2 Implement manual-mode Agent Team Instance launch from existing Workspace Runtime records and generated launch material through the public Houmao project-profile CLI launch path.
- [ ] 4.3 Record launch attempts with status, adapter refs, Agent Instance mapping, diagnostics, timestamps, and Provenance refs.
- [ ] 4.4 Implement live inspection that returns deterministic generic runtime summaries plus bounded adapter inspection snapshots.
- [ ] 4.5 Implement stop behavior that records stopped, failed, partial, or stale outcomes and preserves launch records for audit.
- [ ] 4.6 Add partial-launch recovery behavior that exposes known Agent Instance mappings and stop diagnostics without deleting runtime records.
- [ ] 4.7 Add mocked unit tests for successful launch, failed launch, inspect snapshot recording, stop success, partial stop, stale inspection, and process-restart recovery.

## 5. Manual Handoff and Signal Observation Flow

- [ ] 5.1 Add Run creation or lookup helpers for the first manual handoff round under a launched Agent Team Instance.
- [ ] 5.2 Implement manual handoff dispatch from `deepsci-org-master` to one selected specialist Agent Instance through Houmao mail or gateway surfaces.
- [ ] 5.3 Record handoff dispatch refs, source actor ref, target actor ref, Run or Research Task ref, Completion Watcher Contract refs, expected output refs, adapter refs, and Provenance refs.
- [ ] 5.4 Implement observation ingestion for Houmao mail, gateway events, file observations, and adapter inspection output as Signal Observations.
- [ ] 5.5 Implement Operator Agent normalization that can accept a candidate handoff result and record accepted handoff state, Run updates, output Artifact refs, and Provenance Records.
- [ ] 5.6 Implement rejection or repair routing that keeps observations visible and records rejected, blocked, superseded, or Service Request refs with rationale.
- [ ] 5.7 Add tests proving adapter observations alone do not mark handoffs or Runs complete.

## 6. CLI and API Surface

- [ ] 6.1 Add `isomer-cli team-instances launch` with Project selectors, topic selectors, Agent Team Instance selector, adapter selector, text output, deterministic JSON, and explicit mutation reporting.
- [ ] 6.2 Add `isomer-cli team-instances inspect-live` for bounded Houmao adapter inspection without creating Agent Team Instances or launching additional agents.
- [ ] 6.3 Add `isomer-cli team-instances stop` with deterministic stop outcome output and cleanup diagnostics.
- [ ] 6.4 Add a top-level `isomer-cli handoffs dispatch` command with Project selectors, topic selectors, Agent Team Instance selector, Run or Research Task refs, text output, deterministic JSON, and explicit mutation reporting.
- [ ] 6.5 Add `isomer-cli handoffs observe` and `isomer-cli handoffs normalize` command paths that record Signal Observations and accepted or rejected normalization results.
- [ ] 6.6 Update root help, command-surface text, JSON output shapes, and read-only command tests for all Milestone 5 commands.
- [ ] 6.7 Add CLI tests for launch preflight failure, mocked launch success, inspect-live, stop, handoff dispatch, observation, normalization, and no-Houmao-field leakage in generic output.

## 7. Runtime Validation and Recovery

- [ ] 7.1 Extend runtime validation to report missing adapter refs, missing durable launch material files, stale adapter snapshots, partial stop outcomes, unresolved launch Gates, and cross-topic adapter leakage.
- [ ] 7.2 Validate that launched Agent Team Instances retain generic lifecycle refs and opaque adapter refs after process restart.
- [ ] 7.3 Validate that inspection snapshots with large logs, transcripts, mailbox content, or command output store file-backed refs rather than inline rich content.
- [ ] 7.4 Validate that adapter records do not treat specialist claims, measurements, or summaries as Evidence Item support until normalized into accepted recording objects.
- [ ] 7.5 Add negative tests for missing Houmao checkout, invalid launch material path, missing Agent Workspace, missing readiness, unsupported runtime schema, unresolved Gate, stale handoff, and broken adapter mapping.

## 8. Houmao Repository Boundary and Live Tests

- [ ] 8.1 Add a live-test capability check that reports Houmao checkout path, read-only capability-gate results, and skipped status when unavailable.
- [ ] 8.2 Add a live-gated integration or manual test that launches one manual-mode `deepsci-org` Agent Team Instance through the local Houmao checkout using the public project-profile CLI launch path.
- [ ] 8.3 Extend the live-gated test to dispatch one handoff, observe a Houmao mail or gateway result, normalize it into Workspace Runtime, and stop the Agent Team Instance.
- [ ] 8.4 Document the read-only Houmao capability-gate commands, optional live/manual validation commands, and the rule that Houmao defects are fixed in the Houmao repository before Isomer depends on them.
- [ ] 8.5 Add safeguards so Isomer tests do not write into or commit `extern/orphan/houmao` except through explicit separate Houmao work.

## 9. Documentation and Roadmap

- [ ] 9.1 Update README command examples and narrative for Milestone 5 launch, inspect-live, stop, handoff observation, normalization, and live-test availability.
- [ ] 9.2 Update ROADMAP.md Milestone 5 checklist only after implementation and validation are complete.
- [ ] 9.3 Add developer notes for adapter record boundaries, opaque Houmao refs, local Houmao build expectations, and no-Houmao-term generic schema policy.
- [ ] 9.4 Add troubleshooting notes for failed preflight, missing readiness, missing Houmao checkout, partial launch, partial stop, and rejected handoff result.

## 10. Verification

- [ ] 10.1 Run `openspec validate --all` after implementation and after any spec edits.
- [ ] 10.2 Run `pixi run lint`.
- [ ] 10.3 Run `pixi run typecheck`.
- [ ] 10.4 Run `pixi run test`.
- [ ] 10.5 Run `pixi run validate-research-skills`.
- [ ] 10.6 Run the live-gated Houmao integration or manual test when the local Houmao checkout passes its own validation, and record skipped status otherwise.
