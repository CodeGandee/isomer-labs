## 1. JSON Manifest Models

- [x] 1.1 Confirm the implementation uses Python's standard `json` module for manifest parsing and writing without adding an extra manifest writer dependency.
- [x] 1.2 Add Houmao adapter manifest model types for `adapter-link.json`, `launch-material-manifest.json`, and `adapter-runtime-manifest.json`.
- [x] 1.3 Add schema version, manifest kind, adapter id, Isomer identity refs, Houmao adapter refs, timestamp, and Provenance ref fields to the manifest models.
- [x] 1.4 Add reconciliation state and mapping confidence enums for linked, launched by Isomer, externally detected, adopted, drifted, conflicted, stale, rejected, exact, name match, manifest match, manual, unmapped, and conflict states.
- [x] 1.5 Implement JSON parsing and rendering helpers that validate manifest kind and schema version.
- [x] 1.6 Implement canonical JSON normalization that projects parsed manifests into deterministic structures for digest calculation.
- [x] 1.7 Implement raw byte digest helpers for launch-material files referenced by JSON manifests.
- [x] 1.8 Implement redaction and secret-detection checks for manifest payloads, diagnostics, and native Houmao command output before Workspace Runtime recording.

## 2. Path Plans and Runtime Persistence

- [x] 2.1 Add Workspace Path Resolution support for durable Houmao adapter manifest paths under the selected Topic Workspace path plan.
- [x] 2.2 Add path validation for direct Houmao project overlay refs and externally detected launch-material refs.
- [x] 2.3 Add runtime store support for opaque adapter manifest refs linked to Agent Team Instance, Agent Instance, Run, handoff, Artifact, path plan, and Provenance records.
- [x] 2.4 Add runtime store support for reconciliation records with state, mapping confidence, manifest digest summary, live observation summary, diagnostics, actor ref, timestamp, and Provenance refs.
- [x] 2.5 Add validation that generic runtime inspection does not expose Houmao-specific field names as core schema fields.
- [x] 2.6 Add durable diagnostic Artifact or adapter payload ref recording for drift, conflict, stale, rejection, and adoption outcomes.
- [x] 2.7 Add restart-safe lookup that reconstructs adapter manifest refs and reconciliation summaries from Workspace Runtime.

## 3. Houmao Reconciliation Engine

- [x] 3.1 Add a read-only reconciliation planner that loads JSON manifests, Workspace Runtime records, and Houmao read-only inspection output.
- [x] 3.2 Integrate Houmao read-only commands needed for reconciliation without launching, stopping, or messaging Houmao-managed agents.
- [x] 3.3 Implement state classification for linked, launched by Isomer, externally detected, adopted, drifted, conflicted, stale, and rejected outcomes.
- [x] 3.4 Implement Agent Instance to Houmao managed-agent mapping with exact, name-match, manifest-match, manual, unmapped, and conflict confidence.
- [x] 3.5 Implement material drift detection by comparing recorded raw file digests with current referenced launch-material bytes.
- [x] 3.6 Implement manifest semantic drift detection by comparing canonical JSON digests instead of raw JSON bytes.
- [x] 3.7 Implement adoption of externally launched Houmao runtime state with explicit mapping validation and Provenance recording.
- [x] 3.8 Ensure adoption preserves user-authored Houmao launch material and does not regenerate or overwrite it.
- [x] 3.9 Ensure rejected adoption records diagnostics without mutating Agent Team Instance launch state.

## 4. Quick Launch Integration

- [ ] 4.1 Extend Houmao quick launch preflight to resolve manifest path plans before launch material is written.
- [ ] 4.2 Write or update `adapter-link.json` before Isomer invokes Houmao quick launch.
- [ ] 4.3 Write or update `launch-material-manifest.json` with generated material refs, raw file digests, source, editable policy, and Provenance refs before launch.
- [ ] 4.4 Write or update `adapter-runtime-manifest.json` after quick launch inspection records live Houmao refs and mapping confidence.
- [ ] 4.5 Link quick-launch manifest refs, launch attempt records, runtime records, and Provenance Records in Workspace Runtime.
- [ ] 4.6 Preserve existing Milestone 5 launch, inspect, stop, and handoff behavior while adding manifest refs and reconciliation summaries.

## 5. CLI and API Surface

- [x] 5.1 Add adapter link export command behavior for Houmao-backed Agent Team Instances that writes or prints `adapter-link.json` without launching Houmao agents.
- [x] 5.2 Add integrity inspection command behavior that reads manifests and live Houmao state without recording adoption or changing launch state.
- [x] 5.3 Add reconcile command behavior that validates preflight and records reconciliation outcomes when the command contract requests recording.
- [x] 5.4 Add adopt command behavior that validates mapping, paths, digests, redaction, and approval requirements before recording external Houmao runtime refs.
- [x] 5.5 Add deterministic JSON output for export, integrity inspection, reconcile, and adopt commands.
- [x] 5.6 Add text output that reports reconciliation state, mapping confidence, affected refs, and redacted diagnostics.

## 6. Tests and Validation

- [x] 6.1 Add unit tests for JSON round trip, manifest kind validation, schema version validation, and deterministic rendering.
- [x] 6.2 Add unit tests proving JSON whitespace and object field ordering changes do not change canonical manifest digests.
- [x] 6.3 Add unit tests proving referenced launch-material byte changes produce material drift.
- [x] 6.4 Add unit tests for redaction and rejection of secret-bearing manifest or Houmao payload data.
- [x] 6.5 Add unit tests for reconciliation state classification and mapping confidence decisions.
- [x] 6.6 Add unit tests for Workspace Runtime opaque manifest refs, reconciliation records, and restart-safe lookup.
- [x] 6.7 Add CLI tests for adapter link export, integrity inspection, reconcile, adopt, text output, and JSON output.
- [x] 6.8 Add tests proving direct Houmao adoption does not mark handoff or Run completion accepted without Operator Agent normalization.
- [ ] 6.9 Add live-gated or manual validation for Isomer quick launch followed by reconciliation.
- [ ] 6.10 Add live-gated or manual validation for direct `houmao-mgr` launch followed by Isomer reconcile and adopt.

## 7. Documentation and Review

- [x] 7.1 Document the two supported launch lanes: Isomer quick launch and direct Houmao operation followed by Isomer reconciliation.
- [x] 7.2 Document the JSON manifest files, their CLI-first workflow, and which fields are safe to inspect or edit manually during recovery.
- [x] 7.3 Document that Isomer does not expose the full Houmao management surface and that low-level Houmao edits remain direct `houmao-mgr` workflows.
- [x] 7.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [ ] 7.5 Run relevant live-gated or manual Houmao validation when the local Houmao checkout is available.
