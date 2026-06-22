## Context

Milestone 5 established the Houmao Execution Adapter foundation: Isomer can prepare launch material, quick-launch or adopt a Houmao-backed Agent Team Instance, inspect and stop it, dispatch manual handoffs, ingest Signal Observations, and normalize a handoff result into Workspace Runtime. Milestone 6 is the first research-facing vertical slice on top of that foundation. Its target is UC-01, Explore a New Research Direction, run headlessly with deterministic tests and optional live Houmao validation against the pinned Flash Attention 4 on GB10 topic.

The current runtime already has generic lifecycle records for Research Inquiry, Research Task, Run, Artifact, Gate, Evidence Item, Decision Record, Provenance Record, and related kinds, but the code only uses a subset of them. The current research-recording specs define the concepts, while implementation still needs focused storage helpers, validation, CLI output, and a repeatable workflow that writes real records. Milestone 6 should use those generic record kinds first and add specialized tables only if the lifecycle record shape cannot preserve required links, status, or file-backed content.

The audience for this change is the operator and future automation: a user should be able to run one command or manual script, inspect deterministic JSON, and see a coherent Topic Workspace with the UC-01 research path recorded. A future GUI or richer Operator Agent can consume the same records later.

## Goals / Non-Goals

**Goals:**

- Provide a repeatable UC-01 fixture and headless runner that works in deterministic adapter-simulated mode and can be live-gated for real Houmao.
- Pin the fixture to Research Topic `flash-attention-gb10-peak-performance-optimization`, seed Research Inquiry `gb10-flash-attention-4-direction-selection`, Research Task `map-gb10-flash-attention-optimization-directions`, and the `deepsci-mini` Domain Agent Team Template.
- Record a minimal but coherent Research Inquiry graph, Research Tasks, Runs, handoffs, Artifacts, Evidence Items, Findings or claim candidates, a follow-up Gate, a selected follow-up Research Inquiry, a Decision Record, View Manifest records, and Provenance Records.
- Keep all UC-01 records topic-scoped and restart-safe through Workspace Runtime.
- Use the existing Houmao adapter and handoff normalization boundary; adapter observations remain non-authoritative until Operator Agent normalization.
- Expose structured human-readable output and root-level `--print-json` output for the UC-01 path.
- Keep Houmao native terms out of generic lifecycle, recording, and view records.
- End with a follow-up Decision Record that classifies the next path as UC-07-style measured optimization, more scouting, or a different Flash Attention 4 investigation.

**Non-Goals:**

- Do not implement a GUI renderer or AG-UI runtime for Milestone 6.
- Do not implement automatic Control Mode, automatic Completion Watcher execution, or task-level fanout beyond the bounded UC-01 flow.
- Do not implement full literature provider integrations; fixture-backed or file-backed seed-source and literature-note Artifacts are enough for the first vertical slice.
- Do not run GB10 measurements, baseline benchmarks, candidate optimization experiments, automatic replay, or compute-budget Gates; those belong to Milestone 7 / UC-07.
- Do not promote claim candidates to supported Research Claims unless valid Evidence Item links exist.
- Do not make the UC-01 runner the general workflow engine for all use cases.

## Decisions

### Decision: Treat UC-01 as a fixture-backed workflow package

The implementation should add a fixture Project and a runner/manual test that drives the public CLI and runtime APIs. The fixture should include Research Topic `flash-attention-gb10-peak-performance-optimization`, Topic Workspace, seed Research Inquiry `gb10-flash-attention-4-direction-selection`, Research Task `map-gb10-flash-attention-optimization-directions`, one `deepsci-mini` Topic Agent Team Profile, explicit Pixi readiness binding, expected output refs, and a follow-up-inquiry Gate policy ref. The runner should avoid hidden setup beyond explicit runtime init, runtime prepare, team creation, adapter launch or simulation, handoff rounds, and recording calls.

Alternative considered: encode UC-01 directly as a permanent built-in command with hardcoded data. That would prove less about normal Projects and more about one special command path, so the fixture should stay Project-shaped and the runner should operate through standard Project discovery.

### Decision: Use generic lifecycle records first for research-state identity

Research Inquiry, Research Task, Run, Artifact, Gate, Evidence Item, Decision Record, Provenance Record, and View Manifest identity should be represented with accepted generic record kinds and typed helper APIs. Rich content should live as files under the Topic Workspace and be referenced by lifecycle or recording metadata. If a record needs fields that do not fit `RuntimeLifecycleRecord`, add small typed helper records or metadata payloads behind the runtime store, but do not invent provider-specific core fields.

Alternative considered: create dedicated tables for every UC-01 record type immediately. That would give stronger SQL shape, but it risks schema churn before the recording model settles. A hybrid approach is better: generic lifecycle identity plus focused helper payloads only where tests need durable lookup or validation.

### Decision: Use `deepsci-mini` as the UC-01 seed team

Milestone 6 should use `deepsci-mini`, a three-role Domain Agent Team Template under `teams/deepsci-mini`, instead of the heavier seven-role `deepsci-org` template. `deepsci-mini` has `deepsci-mini-lead`, `deepsci-mini-scout`, and `deepsci-mini-synth-reviewer`. This keeps UC-01 focused on the acceptance slice: seed-source collection, Flash Attention implementation notes, GB10 or Blackwell feature notes, evidence synthesis, weak-claim review, follow-up inquiry options, Gate resolution, and Decision Record creation. `deepsci-org` remains the larger template for later milestones that need baseline reproduction, implementation, analysis fanout, writing, publication surfaces, or independent full review loops.

Alternative considered: use a reduced `deepsci-org` Topic Agent Team Profile. That would still inherit the larger template's conceptual surface and required role vocabulary, so a separate mini template is cleaner for the first vertical slice.

### Decision: Model UC-01 as two bounded specialist handoffs plus lead closeout

The headless flow should create bounded Research Tasks and Runs for scouting and synthesis-review, then dispatch manual handoffs to selected `deepsci-mini` Agent Instances. The top-level fixture Research Task remains `map-gb10-flash-attention-optimization-directions`, with subordinate handoff work scoped to literature, feature, factor, and synthesis-review outputs. Each handoff result should remain a Signal Observation until the Operator Agent path normalizes it. Accepted normalized results should create or update Artifacts, Evidence Items, Finding or claim-candidate records, View Manifests, and Provenance Records.

Alternative considered: bypass handoffs and write all fixture Artifacts directly. Direct fixture writes would be easier, but it would fail to prove that Milestone 5 handoff mechanics can support research-state recording.

### Decision: Record follow-up inquiry selection through a Gate and Decision Record

The UC-01 closeout should present inquiry options as durable Artifacts or View Manifest inputs, open a follow-up Research Inquiry Gate, and resolve it through a Decision Record that names the selected follow-up inquiry and rejected alternatives when present. The selected follow-up Research Inquiry should be recorded and linked to the originating Research Topic or parent Research Inquiry, and the Decision Record should classify the selected route as UC-07-style measured optimization, more scouting, or a different Flash Attention 4 investigation.

Alternative considered: start a baseline measurement as soon as the selected inquiry points to optimization. That would collapse UC-01 into UC-07 and make the first research-direction slice depend on GB10 measurement availability, so Milestone 6 should stop at the classified follow-up decision.

Alternative considered: record the selected inquiry as a plain Artifact. That would leave the most important route choice outside the lifecycle and decision graph, so it should become a Gate plus Decision Record.

### Decision: Store minimal View Manifests as durable view records, not renderer output

Milestone 6 should create View Manifest records for the literature matrix, claim graph, and inquiry comparison. Each View Manifest should reference the underlying Artifacts, Evidence Items, Findings or claim candidates, inquiries, and Decision Record. It should not require a GUI renderer, GUI Component Instances, or AG-UI event transport.

Alternative considered: delay View Manifests until GUI work. The roadmap asks for CLI-readable view records now, and storing the semantic view input gives Milestone 8 and UC-04 a stable target later.

### Decision: Keep simulated and live Houmao paths behind the same acceptance contract

The deterministic acceptance path should use an adapter-simulated or fake Houmao mode. The live path should be gated by an explicit environment variable and read-only capability checks before mutation, mirroring Milestone 5 manual validation. Both paths should leave the same generic UC-01 records, with only adapter payloads differing.

Alternative considered: require live Houmao for Milestone 6 completion. That would make the primary regression suite fragile and host-dependent. Live validation should be optional and recorded as skipped when the live gate is absent.

## Risks / Trade-offs

- Runtime record shape is too generic for query needs -> Add small typed helper APIs and tests around the required UC-01 queries before adding large new tables.
- Fixture output becomes canned and does not exercise the adapter path -> Require at least one dispatch, observation, normalization, and runtime reopen in the deterministic runner.
- Claim candidates are mistaken for supported Research Claims -> Keep claim-candidate or Finding records separate from supported Research Claims unless Evidence Item links pass validation.
- Gate resolution becomes a hidden flag -> Require an explicit Gate record, Decision Record, selected inquiry ref, actor ref, and Provenance Record for closeout.
- Live Houmao behavior drifts from fake mode -> Keep a live-gated manual test that reports capability checks, skip state, and cleanup state, but make deterministic fake mode the default CI-style validation.
- View Manifest scope expands into GUI rendering -> Store semantic manifest records only and defer GUI Component Instances and rendering to later milestones.
- Mini team hides too much specialist separation -> Keep `deepsci-mini` limited to UC-01 and preserve `deepsci-org` for later milestones that need separate experiment, writing, and independent review contexts.

## Migration Plan

Milestone 6 can be implemented as an additive runtime schema extension. Opening an existing current-schema Workspace Runtime for mutation should create missing additive tables or metadata surfaces as needed, while unsupported schema versions must still fail before mutation. Fixture Projects should be new test material and should not require migration of existing fixtures.

Rollback is straightforward for source changes because UC-01 records are additive. A runtime created with Milestone 6 additions should still be inspectable for existing Milestone 5 records through existing summaries; commands that depend on new UC-01 record helpers may report missing tables or unsupported schema if run by older code.

## Open Questions

- Should Finding records be represented as a first-class runtime table in Milestone 6, or as lifecycle records with file-backed metadata until Milestone 8 expands the recording API?
- What exact public command spelling should the UC-01 runner use, and should the `tests/manual` validation script call the same implementation helper?
- How much of the literature matrix, GB10 feature notes, and claim graph should be deterministic fixture content versus adapter-produced content from the simulated handoff replies?
