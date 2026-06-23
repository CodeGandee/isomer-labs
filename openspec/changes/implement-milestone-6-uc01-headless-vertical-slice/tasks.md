## 1. Foundation and Scope Check

- [x] 1.1 Confirm the Milestone 5 Houmao launch, handoff dispatch, Signal Observation, normalization, fake manual validation, and root `--print-json` behavior are present before starting Milestone 6 implementation.
- [x] 1.2 Re-read ROADMAP Milestone 6, the pinned UC-01 use-case source, the UC-07 boundary, and the canonical domain language before naming new records, CLI labels, or fixture fields.
- [x] 1.3 Decide the public UC-01 command spelling and whether the manual validation script calls the same implementation helper.
- [x] 1.4 Audit existing runtime lifecycle record kinds and validation helpers to choose which UC-01 records can use `RuntimeLifecycleRecord` directly and which need focused helper payloads.
- [x] 1.5 Confirm M6 stops at follow-up inquiry selection and does not implement GB10 measurement, baseline benchmark, candidate optimization, automatic replay, or compute-budget Gate behavior reserved for UC-07.

## 2. UC-01 Fixture Project

- [x] 2.1 Add a UC-01 fixture Project with Research Topic `flash-attention-gb10-peak-performance-optimization`, one Topic Workspace, seed Research Inquiry `gb10-flash-attention-4-direction-selection`, Research Task `map-gb10-flash-attention-optimization-directions`, one `deepsci-mini` Topic Agent Team Profile, explicit topic Pixi readiness binding, and follow-up-inquiry Gate policy ref.
- [x] 2.2 Add deterministic fixture source material for seed-source summaries, Flash Attention implementation notes, GB10 or Blackwell feature notes, attention-kernel bottleneck notes, shape-family constraints, correctness constraints, claim candidates, review notes, and follow-up inquiry options.
- [x] 2.3 Add expected Artifact refs or Artifact kinds to the UC-01 profile or Research Topic Config without embedding runtime truth.
- [x] 2.4 Add fixture validation tests proving the Project validates before Workspace Runtime creation and rejects runtime-truth leakage.

## 3. Runtime Research Recording Foundations

- [x] 3.1 Add or extend runtime models, row mappers, schema, and store helpers for UC-01 Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, and Provenance Records.
- [x] 3.2 Add transactional helper APIs for recording an accepted UC-01 handoff output as file-backed content plus linked runtime records.
- [x] 3.3 Add helper APIs for opening and resolving the follow-up-inquiry Gate and recording the selected follow-up Research Inquiry, route classification, and Decision Record.
- [x] 3.4 Add helper APIs for writing literature matrix, claim graph, and inquiry comparison View Manifest records.
- [x] 3.5 Preserve generic schema boundaries by keeping Houmao-native refs in adapter payloads, manifests, or adapter tables rather than generic UC-01 records.
- [x] 3.6 Add schema-version handling so unsupported Workspace Runtime versions reject UC-01 mutations before creating runtime records or files.

## 4. UC-01 Workflow Runner Core

- [x] 4.1 Implement a reusable UC-01 runner module outside the CLI app monolith that accepts Effective Topic Context, adapter mode, actor ref, follow-up selection, and optional Agent Team Instance id.
- [x] 4.2 Implement explicit runtime bootstrap steps: `runtime init`, `runtime prepare`, Agent Team Instance create or reuse, and adapter launch or simulation readiness.
- [x] 4.3 Implement bounded scouting and synthesis-review task creation with Research Inquiry `gb10-flash-attention-4-direction-selection`, Research Task `map-gb10-flash-attention-optimization-directions`, Run, Agent Team Instance, Agent Instance, handoff, and expected output refs.
- [x] 4.4 Dispatch each UC-01 task through the existing handoff adapter path or simulated adapter path, observe candidate completion, and normalize accepted results before writing research records.
- [x] 4.5 Record seed-source summaries, Flash Attention implementation notes, GB10 or Blackwell feature notes, attention-kernel bottleneck notes, shape-family constraints, correctness constraints, claim candidates or Findings, Evidence Items, review notes, inquiry options, and Provenance Records from accepted normalized results.
- [x] 4.6 Open the follow-up-inquiry Gate, resolve the deterministic or user-selected option, record the Decision Record with route classification, and create the selected follow-up Research Inquiry and relationship.
- [x] 4.7 Write minimal View Manifest records for literature matrix, claim graph, and inquiry comparison.
- [x] 4.8 Make the runner restart-safe by reading existing records when rerun and refusing duplicate destructive mutation unless an explicit resume or replace policy is implemented.
- [x] 4.9 Ensure the runner exits after the follow-up Decision Record and does not start UC-07 measurement, baseline, candidate optimization, automatic replay, or correctness-check execution.

## 5. CLI and Output Surface

- [x] 5.1 Add the chosen modular CLI command group and register it from the CLI app without expanding the root app monolith.
- [x] 5.2 Add UC-01 run options for Project selectors, topic selectors, Agent Team Instance selector, adapter mode, live-gate controls, actor ref, and follow-up inquiry selection.
- [x] 5.3 Emit deterministic root-level `--print-json` output with Project refs, topic refs, Agent Team Instance ref, Research Inquiry refs, Research Task refs, Run refs, handoff refs, Artifact refs, Evidence Item refs, Gate ref, Decision Record ref, route classification, View Manifest refs, Provenance refs, diagnostics, and live or simulated mode.
- [x] 5.4 Emit structured human-readable text output for major UC-01 stages without raw JSON by default.
- [x] 5.5 Add a read-only UC-01 validation or inspect path that reports current UC-01 graph state and diagnostics without creating missing records, launching agents, dispatching handoffs, or resolving Gates.
- [x] 5.6 Update command-surface tests so the UC-01 command is discoverable and does not advertise command-local `--json`, `--format json`, or `--format=json`.

## 6. Adapter-Simulated and Live Houmao Modes

- [x] 6.1 Add deterministic adapter-simulated responses for Flash Attention 4 on GB10 scouting and synthesis-review handoffs that exercise dispatch, observation, normalization, payload refs, and research-record writing.
- [x] 6.2 Add live-gated UC-01 capability checks that report Houmao command resolution, checkout path candidates, read-only probes, and skipped status before mutation.
- [x] 6.3 Add live cleanup handling that stops or reports cleanup state for launched Houmao Agent Team Instances and preserves partial state for recovery.
- [x] 6.4 Confirm simulated and live modes leave the same generic UC-01 record graph, with differences limited to adapter payload refs and diagnostics.

## 7. Runtime Validation and Inspection

- [x] 7.1 Extend runtime validation to report missing UC-01 Artifacts, Evidence Items, Gate, Decision Record, View Manifest, and Provenance refs without deleting partial records.
- [x] 7.2 Validate that candidate claims are not treated as supported Research Claims without accepted Evidence Item links.
- [x] 7.3 Validate that an open follow-up-inquiry Gate blocks UC-01 closeout while unrelated inspection remains allowed.
- [x] 7.4 Validate topic scoping for UC-01 records, including Agent Team Instance, Agent Instance, Run, Artifact, Gate, Decision Record, View Manifest, and path refs.
- [x] 7.5 Include UC-01 record counts or summaries in runtime inspect, runtime validate, Agent Team Instance show, or the dedicated UC-01 inspect output.
- [x] 7.6 Validate that route classification can point to UC-07-style measured optimization, more scouting, or a different Flash Attention 4 investigation without creating measured optimization records in M6.

## 8. Tests and Manual Validation

- [x] 8.1 Add unit tests for pinned UC-01 fixture validation, no runtime-truth leakage, explicit topic readiness binding, and exact Research Topic, seed Research Inquiry, Research Task, and `deepsci-mini` role refs.
- [x] 8.2 Add unit tests for runtime store helpers that write and reload UC-01 Artifacts, Evidence Items, Findings or claim candidates, Gates, Decision Records, View Manifests, and Provenance Records.
- [x] 8.3 Add CLI tests for simulated UC-01 run JSON output, structured text output, command help, and read-only validation.
- [x] 8.4 Add restart-recovery tests that run UC-01, reopen Workspace Runtime, and inspect all required lifecycle and recording refs.
- [x] 8.5 Add negative tests for unsupported schema, open follow-up Gate, missing Evidence Item refs, missing Artifact files, missing Provenance refs, and cross-topic leakage.
- [x] 8.6 Add or update a manual live-gated test that runs the UC-01 path with real Houmao when `ISOMER_MANUAL_LIVE_HOUMAO=1` is set and records skipped status otherwise.
- [x] 8.7 Ensure tests do not write into or commit `extern/orphan/houmao` except through explicit separate Houmao work.
- [x] 8.8 Add negative tests proving UC-01 does not create baseline measurement, candidate optimization, speedup, utilization, correctness-result, automatic replay, or compute-budget Gate records.

## 9. Documentation and Roadmap

- [x] 9.1 Update README or workflow docs with the UC-01 headless command, simulated mode, live-gated mode, and expected output refs.
- [x] 9.2 Update troubleshooting docs for missing UC-01 fixture state, failed adapter mode, open follow-up Gate, unsupported claim support, missing Artifact files, and incomplete Provenance refs.
- [x] 9.3 Update runtime and Houmao adapter docs to describe UC-01 record boundaries, route classification, no-measurement scope, and live-gated validation.
- [x] 9.4 Keep ROADMAP.md Milestone 6 aligned after implementation and validation are complete, including the UC-01 to UC-07 handoff boundary.

## 10. Verification

- [x] 10.1 Run `openspec validate implement-milestone-6-uc01-headless-vertical-slice --strict` after spec edits.
- [x] 10.2 Run `openspec validate --all` after implementation.
- [x] 10.3 Run `pixi run lint`.
- [x] 10.4 Run `pixi run typecheck`.
- [x] 10.5 Run `pixi run test`.
- [x] 10.6 Run `pixi run validate-research-skills`.
- [x] 10.7 Run the UC-01 simulated headless validation command or manual test and record the output summary, including selected route classification.
- [x] 10.8 Run the live-gated UC-01 validation when local Houmao passes its own validation, or record skipped status when the live gate is absent.
