## Context

Milestone 5 introduces the Houmao Execution Adapter as the first live adapter slice for launching, inspecting, stopping, and handoff observation. The current Milestone 5 artifacts already keep Houmao ids behind opaque adapter refs, launch through Houmao's public project-profile surface, and retain launch material as durable evidence rather than cache-like files.

The missing behavior is operator interoperability. A user may use Isomer's quick launch path, or they may directly use `houmao-mgr` to edit Houmao project-profile launch material, launch agents, inspect sessions, stop agents, or repair Houmao-side state. Isomer needs a manifest contract that lets it observe and reconcile those direct operations without adopting every low-level Houmao feature as core Isomer language.

## Goals / Non-Goals

**Goals:**

- Define durable JSON adapter manifests that link Isomer Agent Team Instance refs to Houmao project-profile and runtime refs.
- Support both Isomer quick launch and direct `houmao-mgr` operation through the same reconciliation contract.
- Detect and classify runtime and launch-material integrity states such as linked, launched by Isomer, externally detected, adopted, drifted, conflicted, stale, and rejected.
- Keep Houmao fields adapter-scoped through JSON manifests, adapter payload refs, diagnostic Artifacts, and Provenance Records.
- Use deterministic JSON for durable manifests and CLI/API consumers, while keeping persisted manifest documents distinct from command output payloads.
- Add implementation tasks that can be tested without launching Houmao, plus live-gated checks for direct Houmao reconciliation.

**Non-Goals:**

- Do not expose the full Houmao management surface through Isomer.
- Do not add Houmao-specific fields to generic Project Manifest, Research Topic Config, Agent Team Instance, Agent Instance, Run, handoff, or Artifact schemas.
- Do not make background file watching, passive-server polling, or automatic adoption required for Milestone 5.
- Do not treat direct Houmao state as authoritative Isomer state until an explicit reconcile or adopt operation records that decision.
- Do not rewrite user-edited Houmao launch material unless the user runs an explicit Isomer repair or regeneration command.

## Decisions

### Decision 1: JSON manifest family

Use three adapter-scoped JSON manifest files as the bridge contract: `adapter-link.json`, `launch-material-manifest.json`, and `adapter-runtime-manifest.json`. The path resolver records their durable paths under the selected Topic Workspace or Agent Workspace path plans, typically below an adapter-owned runtime directory for one Agent Team Instance.

`adapter-link.json` records stable correlation: Isomer Agent Team Instance ref, Topic Workspace ref, Topic Agent Team Profile ref, Execution Adapter ref, Houmao project directory ref, expected Houmao profile names, expected managed-agent names, and manifest provenance.

`launch-material-manifest.json` records file inventory: generated or adopted launch material refs, raw file digests, semantic role mapping, owning source, editable policy, and last observed state.

`adapter-runtime-manifest.json` records observed runtime state: Houmao native manifest refs, session refs, gateway/mailbox refs, lifecycle state, mapped Isomer Agent Instance refs, mapping confidence, integrity state, diagnostics, and observation provenance.

Alternative considered: use a configuration-oriented manifest format because it is friendlier for hand-inspected operator files. The expected path is CLI-managed manifests rather than direct hand editing, so JSON better matches Houmao `--print-json`, Isomer `--json`, deterministic validation, and standard-library implementation.

### Decision 2: One reconciliation contract for two launch lanes

The Isomer quick lane writes `adapter-link.json` and `launch-material-manifest.json` before launch, invokes `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>`, and writes `adapter-runtime-manifest.json` after inspecting the launch result.

The direct Houmao lane starts from an exported or user-provided `adapter-link.json`, lets the user edit and launch through `houmao-mgr`, and then requires an explicit Isomer reconcile or adopt command. Reconcile reads the JSON manifests, Workspace Runtime records, Houmao project status, and Houmao managed-agent registry output, then reports or records the observed mapping.

Alternative considered: make Isomer continuously detect arbitrary Houmao launches. That would require watchers or polling and would still be ambiguous without correlation material, so Milestone 5 should use explicit reconciliation instead.

### Decision 3: Explicit reconciliation states

Reconciliation produces a state summary with one of these primary states: `linked`, `launched_by_isomer`, `external_detected`, `adopted`, `drifted`, `conflicted`, `stale`, or `rejected`. The state is stored as adapter-scoped runtime data and surfaced through generic lifecycle summaries without making those labels generic lifecycle enum values unless a future core lifecycle change accepts them.

The reconciliation result also records mapping confidence per Agent Instance: `exact`, `name_match`, `manifest_match`, `manual`, `unmapped`, or `conflict`.

Alternative considered: collapse reconciliation into pass/fail validation. That would hide recoverable cases such as user-edited launch material or an externally launched but adoptable team.

### Decision 4: Canonical JSON digests and raw material digests

Integrity uses two digest layers. JSON manifests are parsed, normalized into a deterministic canonical JSON structure, and digested so whitespace and object field ordering do not create false drift. Referenced launch-material files use raw byte digests because their exact bytes are the material Houmao consumes.

Implementation should use Python's standard `json` module for parsing and writing manifest files. Manifest writers should emit stable indentation, sorted object keys where appropriate, and explicit schema versions so CLI-managed files remain diffable and deterministic.

Alternative considered: hash raw JSON bytes. That would make harmless whitespace or object-order changes look like runtime drift, which is unnecessary when JSON can be parsed and canonicalized before hashing.

### Decision 5: CLI mutation boundaries

Add explicit command behavior for link export, reconciliation, adoption, and integrity inspection. The exact command names can be finalized during implementation, but the intended shape is `isomer-cli team-instances adapter-link export`, `isomer-cli team-instances reconcile`, `isomer-cli team-instances adopt`, and `isomer-cli team-instances inspect-live --integrity`.

Read-only commands can report discovered Houmao state and integrity diagnostics, but only explicit reconcile or adopt commands may update Workspace Runtime or write a new adapter-runtime manifest. CLI `--json` output remains deterministic JSON and uses the same schema discipline as durable manifests, while preserving separate document kinds.

Alternative considered: fold reconcile into ordinary inspect. That would surprise users because inspect currently implies observation, while reconciliation mutates Isomer records.

### Decision 6: Opaque persistence and provenance

Workspace Runtime stores opaque adapter manifest refs, reconciliation record refs, digest summaries, and adoption outcome refs. Generic runtime records continue to name Agent Team Instance, Agent Instance, Run, handoff, Artifact, Signal Observation, and Provenance Record refs using Isomer domain language.

Each manifest creation, launch, external detection, adoption, drift decision, conflict result, and rejection creates or links Provenance Records. Large native Houmao payloads, command outputs, logs, and snapshots remain file-backed Artifacts or adapter payload refs rather than inline schema fields.

Alternative considered: store Houmao project, profile, mailbox, gateway, and managed-agent fields directly in generic runtime tables. That would simplify first-pass queries but would violate the Execution Adapter boundary.

## Risks / Trade-offs

- [Risk] Direct Houmao launches may be impossible to map confidently without a link manifest. -> Mitigation: support post-hoc adopt with explicit user confirmation and mapping confidence, but prefer exported link manifests before direct launch.
- [Risk] JSON files can drift from Workspace Runtime state. -> Mitigation: make reconciliation compare both sides and record drift instead of silently choosing one source.
- [Risk] JSON is less pleasant for manual editing than configuration-oriented formats. -> Mitigation: make CLI commands the primary edit/export/reconcile surface and treat direct JSON edits as advanced recovery behavior.
- [Risk] Users may expect Isomer to support every Houmao operation once direct reconciliation exists. -> Mitigation: document that Isomer adopts and observes Houmao-backed Agent Team Instance state, while low-level Houmao editing remains a direct `houmao-mgr` workflow.
- [Risk] Adoption could record secret-bearing Houmao payloads. -> Mitigation: enforce manifest redaction, store secret-bearing native data only as disallowed diagnostics, and fail reconciliation when credentials or tokens appear in adapter payloads.

## Migration Plan

1. Add JSON manifest models, parser/writer helpers, canonicalization, and digest helpers.
2. Add path-plan support for adapter manifest files and referenced launch material.
3. Extend Houmao quick launch to create link and material manifests before launch and runtime manifest after inspection.
4. Add read-only reconciliation planning that classifies live Houmao state without mutating Workspace Runtime.
5. Add explicit reconcile and adopt operations that persist adapter refs, runtime manifests, reconciliation records, and Provenance Records.
6. Add CLI commands and deterministic JSON output for export, inspect integrity, reconcile, and adopt.
7. Add unit tests for JSON round trip, canonical digest stability, raw file digest drift, direct adoption, conflict handling, and no-Houmao availability.
8. Add live-gated or manual validation comparing Isomer quick launch with direct `houmao-mgr` launch followed by Isomer reconciliation.

Rollback is data-preserving. Existing Workspace Runtime records remain valid; new JSON manifest refs and reconciliation records can be ignored by older code, and failed reconciliation records remain visible as diagnostics rather than deleting launch or adoption evidence.

## Open Questions

None.
