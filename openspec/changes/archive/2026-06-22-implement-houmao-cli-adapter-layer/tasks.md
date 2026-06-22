## 1. Adapter Boundary and Command Runner
- [x] 1.1 Confirm and encode the command catalog seeded by exploration: version, system-skills list, project status, project specialist/profile creation, project agents launch/list/get/stop, and global agents list through `houmao-mgr --print-json`.
- [x] 1.2 Add a Houmao CLI runner that resolves the configured command or local checkout, runs subprocesses with bounded cwd/env, captures stdout/stderr/exit status, parses JSON, redacts diagnostics, and never imports Houmao modules.
- [x] 1.3 Add adapter availability and preflight result models with stable diagnostics for missing checkout, missing command, missing `--print-json` support, invalid Workspace Runtime schema, missing topic readiness, and missing Agent Team Instance records.
- [x] 1.4 Add unit tests proving the adapter modules import without `houmao` installed and mocked command runs produce deterministic success, invalid JSON, timeout, and nonzero-exit diagnostics.

## 2. Path Plans and Runtime Records
- [x] 2.1 Add path-plan helpers for a Houmao adapter root, launch material root, per-Agent Instance material, command payloads, launch logs, inspection snapshots, stop outcomes, and generated Houmao project/profile files.
- [x] 2.2 Add validation that generated adapter paths stay under the selected Topic Workspace or Agent Workspace path plans and do not write into `.isomer-labs/`, the Houmao checkout, another Topic Workspace, or untracked workspace-local team directories.
- [x] 2.3 Add Workspace Runtime tables or typed store helpers for CLI command runs, adapter payload refs, materialization outcomes, launch attempts, per-agent launch command refs, inspection snapshots, stop outcomes, and manifest links.
- [x] 2.4 Add restart-safe lookup and validation for missing payload files, missing manifests, partial launch mappings, stale inspection snapshots, and cross-topic adapter refs.

## 3. Shared Materialization and Prepare-only Flow
- [x] 3.1 Implement a launch-material builder that consumes the selected Agent Team Instance, Agent Instance records, Agent Workspaces, Topic Agent Team Profile, and adapter configuration.
- [x] 3.2 Generate deterministic Houmao project/profile/specialist material and per-Agent Instance launch inputs under recorded adapter paths.
- [x] 3.3 Write or update `adapter-link.json` and `launch-material-manifest.json` during materialization, including raw byte digests, editable policy, mapping hints, source refs, and Provenance refs.
- [x] 3.4 Add `isomer-cli team-instances launch-material prepare <agent-team-instance-id> --adapter houmao` with text and JSON output that reports material refs and manual `houmao-mgr` guidance without launching agents.
- [x] 3.5 Add tests for deterministic materialization, no cache classification, no live Houmao mutation in prepare-only mode, manifest digests, path validation, and direct-edit drift detection integration with reconciliation.

## 4. Quick Launch
- [x] 4.1 Add a Houmao adapter facade method for quick launch that runs preflight, materializes files, creates a launch attempt record, launches one Houmao managed agent per Agent Instance, and records per-agent command results.
- [x] 4.2 Write or update `adapter-runtime-manifest.json` after launch inspection records live Houmao refs, Agent Instance mappings, lifecycle observations, mapping confidence, diagnostics, and Provenance refs.
- [x] 4.3 Link quick-launch manifest refs, command refs, adapter payload refs, launch attempts, and reconciliation summaries in Workspace Runtime.
- [x] 4.4 Preserve partial launch state when one agent starts and a later launch fails, including known mappings and stop/inspect recovery diagnostics.
- [x] 4.5 Add `isomer-cli team-instances launch <agent-team-instance-id> --adapter houmao` with deterministic JSON, explicit mutation reporting, and clear failed-preflight behavior.
- [x] 4.6 Add mocked unit and CLI tests for successful launch, failed preflight, invalid command output, partial launch, process restart recovery, and no Houmao internals in generic output fields.

## 5. Inspect-live, Stop, and Reconciliation Hooks
- [x] 5.1 Add live inspect facade behavior that reads Workspace Runtime, manifests, and Houmao CLI state, then returns bounded generic summaries plus adapter inspection snapshots.
- [x] 5.2 Add stop facade behavior that targets known mapped Houmao managed agents, records stopped, failed, partial, or stale outcomes, and preserves launch records for audit.
- [x] 5.3 Wire `isomer-cli team-instances inspect-live <agent-team-instance-id> --adapter houmao` to read-only adapter inspection without launching or stopping agents.
- [x] 5.4 Wire `isomer-cli team-instances stop <agent-team-instance-id> --adapter houmao` to explicit live mutation with deterministic text and JSON output.
- [x] 5.5 Connect quick-launch and prepare-only records to the existing manifest reconciliation planner so `launched_by_isomer`, external detection, adoption, drift, conflict, stale, and rejected states can be computed from the new adapter records.
- [x] 5.6 Add tests for inspect-live read-only behavior, stop success, partial stop, stale refs, reconciliation after quick launch, and reconciliation after direct `houmao-mgr` launch from prepared material.

## 6. Validation and Documentation
- [x] 6.1 Extend runtime validation to report missing adapter payload files, missing launch material, stale command records, partial launch state, unresolved stop outcomes, and invalid cross-topic adapter mappings.
- [x] 6.2 Add developer documentation for the two launch paths: Isomer quick launch and prepare-only/manual Houmao operation followed by reconciliation or adoption.
- [x] 6.3 Add troubleshooting notes for missing Houmao checkout, failed preflight, invalid CLI JSON, missing readiness, direct edit drift, partial launch, and partial stop.
- [x] 6.4 Add a live-gated or manual validation script that uses the local Houmao checkout to prepare material, quick-launch at least one small Agent Team Instance, inspect it, stop it, and reconcile the manifest state.
- [x] 6.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
